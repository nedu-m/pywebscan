# pylint: disable=C0116
# pylint: disable=C0115
# pylint: disable=C0114

import unittest
from bs4 import BeautifulSoup
from webscan import parse_job_links


class TestParseJobLinks(unittest.TestCase):
    def test_parse_job_links(self):
        html_content = """
        <html>
            <body>
                <a href="/example.com/careers">Career Page</a>
                <a href="/example.com/jobs">Jobs Page</a>
                <a href="/example.com/apply">Apply Now</a>
                <a href="/example.com/about">About Us</a>
            </body>
        </html>
        """

        soup = BeautifulSoup(html_content, "html.parser")
        url = "https://example.com"
        job_positions = parse_job_links(soup, url)

        expected_positions = [
            {
                "job_title": "Career Page",
                "job_url": "https://example.com/careers",
                "website_url": url,
            },
            {
                "job_title": "Jobs Page",
                "job_url": "https://example.com/jobs",
                "website_url": url,
            },
            {
                "job_title": "Apply Now",
                "job_url": "https://example.com/apply",
                "website_url": url,
            },
        ]

        self.assertEqual(job_positions, expected_positions)


if __name__ == "__main__":
    unittest.main()
