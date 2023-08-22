# Web Scraping Job Positions


#### Description:
This Python program utilizes web scraping to extract job positions and URLs from search results related to a user-provided query. It uses the Google Custom Search API to fetch search results and extracts relevant job positions using BeautifulSoup. The extracted job positions and URLs are stored in a CSV file for further reference.

## How to Use
1. Clone this repository to your local machine.
2. Install the required libraries using the command: `pip install -r requirements.txt`.
3. Set your Google API Key and CX as environment variables in a `.env` file.
4. Run the `webscan.py` script: `python webscan.py`.
5. Follow the prompts to enter a search query.
6. The extracted job positions and URLs will be saved in a CSV file named "job_positions.csv".

## Project Structure
- `webscan.py`: The main script containing the web scraping and CSV writing functionality.
- `test_webscan.py`: Test cases for the custom functions using the unit test.
- `README.md`: This file explains the project and how to use it.
- `requirements.txt`: List of pip-installable libraries required for the project.
- `job_positions.csv`: List of actual scrapped job positions.
