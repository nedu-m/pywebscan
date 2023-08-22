# Import necessary libraries and modules

# pylint: disable=C0116
# pylint: disable=C0114
import os
import re
import time
import csv
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

# Fetch API key and CX from environment variables
API_KEY = os.getenv("API_KEY")
CX = os.getenv("CX")

# Set user-agent header for requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}


# Write extracted job positions to a CSV file
def write_to_csv(job_positions, csv_filename):
    # Open CSV file for writing
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Job Title", "Job URL", "Website URL"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write CSV header
        writer.writeheader()

        # Write each job position as a row in CSV
        for position in job_positions:
            writer.writerow(
                {
                    "Job Title": position["job_title"],
                    "Job URL": position["job_url"],
                    "Website URL": position["website_url"],
                }
            )


# Fetch search results from Google Custom Search API
# pylint: disable=E1101
def get_search_results(query):
    # Build service object for Google Custom Search API
    service = build("customsearch", "v1", developerKey=API_KEY)

    # Perform search using the API
    result = service.cse().list(q=query, cx=CX).execute()  # pylint: disable=E1101

    # Return search result items
    return result.get("items", [])


# Parse job links from HTML content
def parse_job_links(soup, url):
    job_positions = {}  # Use a dictionary to avoid duplicate URLs

    job_links = soup.find_all("a", href=True)

    for link in job_links:
        job_title = link.get_text().strip()
        job_url = link["href"]

        if re.search(
            r"(apply|jobs?|careers?|positions?|opportunities?)", job_url, re.I
        ):
            if job_url.startswith("/"):
                job_url = "https://" + job_url[1:]

            job_positions[job_url] = {
                "job_title": job_title,
                "job_url": job_url,
                "website_url": url,
            }

    return list(job_positions.values())  # Convert back to a list


# pylint: disable=C0103
# Scrape HTML content from a URL and parse with BeautifulSoup
def scrape_job_details(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            return soup

    except requests.exceptions.RequestException as e:
        if (
            isinstance(e, requests.exceptions.HTTPError)
            and e.response.status_code == 403
        ):
            print(f"Access to {url} is forbidden. Skipping...")
        else:
            print(f"Error while scraping {url}: {e}")

    return None


# Perform search using Google Custom Search API
def google_api_search(query):
    # Build service object for Google Custom Search API
    service = build("customsearch", "v1", developerKey=API_KEY)

    # Perform search using the API
    result = service.cse().list(q=query, cx=CX).execute()  # pylint: disable=E1101

    # Return search result items
    return result.get("items", [])


# Get user input for search query
def get_user_input():
    query = input("Enter a search query: ")
    return query


# Main function to coordinate the scraping process
def main():
    # Get user's search query
    query = get_user_input()

    # Fetch search results using Google API
    search_results = get_search_results(query)

    # List to store extracted job positions
    job_positions = []

    # Iterate through search results and extract job positions
    for result in search_results:
        url = result.get("link")
        published_date_str = (
            result.get("pagemap", {}).get("metatags", [{}])[0].get("pubdate")
        )

        # Check if published date is within the last three weeks
        if published_date_str:
            try:
                published_date = datetime.strptime(
                    published_date_str, "%Y-%m-%dT%H:%M:%SZ"
                )
                if datetime.now() - published_date > timedelta(weeks=3):
                    continue
            except ValueError:
                pass

        # Scrape HTML content and parse job links
        soup = scrape_job_details(url)
        if soup:
            job_positions += parse_job_links(soup, url)
            time.sleep(2)

    # Specify CSV filename
    csv_filename = "job_positions.csv"

    # Write job position data to CSV
    write_to_csv(job_positions, csv_filename)

    print(f"Job positions written to '{csv_filename}' CSV file.")


if __name__ == "__main__":
    main()
