#! python3
import os
from setuptools import setup, find_packages

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup (
	name = "links_verification",
	version = "1.0.0", 
	description = "Verify that all the external/absolute links within a web page work correctly.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "Dari Developer",
	author_email = "hernandezdarifrancisco@gmail.com",
	license = "MIT",
	keywords = "scraping, links, verify, verify links, external links, request, bas4, beautiful soup 4, testing",
	project_urls = {
		"Documentation": "https://github.com/DariHernandez/links_verification/blob/master/README.md",
		"Funding": "https://www.paypal.com/paypalme/FranciscoDari",
		"Source": "https://github.com/DariHernandez/links_verification"
		},
	packages = find_packages(include=["links_verification", "links_verification.*"]),
	install_requires = ["requests", "beautifulsoup4"],
	python_requires = ">=3.7"
)
