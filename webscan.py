# pylint: disable=C0116
# pylint: disable=C0114
import os
import re
import time
import csv
import requests
from dotenv import load_dotenv
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

load_dotenv()

API_KEY = os.getenv("API_KEY")
CX = os.getenv("CX")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}


def scrape_jobs(query):
    # Use the Google API to get search results
    search_results = google_api_search(query)

    job_positions = []

    for result in search_results:
        url = result.get("link")

        try:
            # Use requests to get the HTML content of the page
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            if response.status_code == 200:
                # use BeautifulSoup to parse the HTML
                soup = BeautifulSoup(response.content, "html.parser")

                # Extract job position data from anchor tags
                job_links = soup.find_all("a", href=True)

                for link in job_links:
                    job_title = link.get_text().strip()
                    job_url = link["href"]

                    # Filter out irrelevant links using regular expression
                    if re.search(
                        r"(apply|jobs?|careers?|positions?|opportunities?)",
                        job_url,
                        re.I,
                    ):
                        # Add "https://" to relative URL
                        if job_url.startswith("/"):
                            job_url = "https://" + job_url[2:]

                        job_positions.append({"job_title": job_title, "url": job_url})
                time.sleep(2)

        except requests.exceptions.RequestException as e:  # pylint: disable=C0103
            if (
                isinstance(e, requests.exceptions.HTTPError)
                and e.response.status_code == 403
            ):
                print(f"Access to {url} is forbidden. Skipping...")
            else:
                print(f"Error while scraping {url}: {e}")

    return job_positions


def google_api_search(query):
    # Create a service object for the Google Search API
    service = build("customsearch", "v1", developerKey=API_KEY)

    # Perform a search using the API
    result = service.cse().list(q=query, cx=CX).execute()  # pylint: disable=E1101

    return result.get("items", [])


def get_user_input():
    query = input("Enter a search query: ")
    return query


def write_to_csv(job_positions, csv_filename):
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Job Title", "URL"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for position in job_positions:
            writer.writerow(
                {"Job Title": position["job_title"], "URL": position["url"]}
            )


def main():
    query = get_user_input()
    job_positions = scrape_jobs(query)

    # Specify the CSV filename
    csv_filename = "job_positions.csv"

    # Write job position data to CSV
    write_to_csv(job_positions, csv_filename)

    print(f"Job positions written to '{csv_filename}' CSV file.")


if __name__ == "__main__":
    main()
