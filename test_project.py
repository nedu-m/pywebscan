# pylint: disable=C0116
# pylint: disable=C0115
# pylint: disable=C0114

from unittest.mock import patch, PropertyMock
from bs4 import BeautifulSoup
import io
import requests
from project import get_search_results, parse_job_links, scrape_job_details
import pytest


# Test for get_search_results
@pytest.mark.parametrize("query", ["job openings", "software engineer"])
def test_get_search_results(query):
    results = get_search_results(query)
    assert isinstance(results, list)
    for result in results:
        assert "link" in result
        assert "pagemap" in result
        assert isinstance(result["link"], str)
        assert isinstance(result["pagemap"], dict)


# Test for parse_job_links
@pytest.fixture
def sample_html():
    return """
    <html>
        <body>
            <a href="/jobs">Job 1</a>
            <a href="/careers">Job 2</a>
            <a href="/positions">Job 3</a>
        </body>
    </html>
    """


def test_parse_job_links(sample_html):
    soup = BeautifulSoup(sample_html, "html.parser")
    job_links = parse_job_links(soup, "https://example.com")
    assert len(job_links) == 3
    for job in job_links:
        assert "job_title" in job
        assert "job_url" in job
        assert "website_url" in job
        assert isinstance(job["job_title"], str)
        assert isinstance(job["job_url"], str)
        assert isinstance(job["website_url"], str)


# Test for scrape_job_details
@patch("requests.get")
def test_scrape_job_details(mock_get):
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response.raw = io.BytesIO(b"<html><body>Mock Content</body></html>")
    mock_get.return_value = mock_response

    url = "https://example.com"
    soup = scrape_job_details(url)

    assert soup is not None
    assert isinstance(soup, BeautifulSoup)
