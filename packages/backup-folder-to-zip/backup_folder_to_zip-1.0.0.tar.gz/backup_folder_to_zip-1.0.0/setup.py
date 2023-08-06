#! python3
import os
from setuptools import setup, find_packages

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup (
	name = "backup_folder_to_zip",
	version = "1.0.0", 
	description = "Copies an entire folder and its contains into a zip file whose filename increments.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "Dari Developer",
	author_email = "hernandezdarifrancisco@gmail.com",
	license = "MIT",
	keywords = "extract, re, phones, emails",
	project_urls = {
		"Documentation": "https://github.com/DariHernandez/backup_folder_to_zip/blob/master/README.md",
		"Funding": "https://www.paypal.com/paypalme/FranciscoDari",
		"Source": "https://github.com/DariHernandez/backup_folder_to_zip/blob/master/README.md"
		},
	packages = find_packages(include=["backup_folder_to_zip", "backup_folder_to_zip.*"]),
	install_requires = ["zipfile"],
	python_requires = ">=3.7"
)
