#! python3
import os
from setuptools import setup, find_packages

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup (
	name = "selective_copy_files",
	version = "1.0.0", 
	description = "Copy to a specific folder, all files within a directory, that match a particular extension",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "Dari Developer",
	author_email = "hernandezdarifrancisco@gmail.com",
	license = "MIT",
	keywords = "copy, slective copy, filter files, auto copy, selective-copy, filter-files, auto-copy",
	project_urls = {
		"Documentation": "https://github.com/DariHernandez/selective_copy_files/blob/master/README.md",
		"Funding": "https://www.paypal.com/paypalme/FranciscoDari",
		"Source": "https://github.com/DariHernandez/selective_copy_files"
		},
	packages = find_packages(include=["selective_copy_files", "selective_copy_files.*"]),
	install_requires = [],
	python_requires = ">=3.7"
)
