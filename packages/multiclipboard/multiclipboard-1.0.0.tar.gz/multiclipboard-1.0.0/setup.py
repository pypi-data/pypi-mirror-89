#! python3
import os
from setuptools import setup, find_packages

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup (
	name = "multiclipboard",
	version = "1.0.0", 
	description = "Saves and loads pices of text to the clipboard, via a database in a .db file",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "Dari Developer",
	author_email = "hernandezdarifrancisco@gmail.com",
	license = "MIT",
	keywords = "clipboard, multiclipboard, multi-clipboard",
	project_urls = {
		"Documentation": "https://github.com/DariHernandez/multiclipboard/blob/master/README.md",
		"Funding": "https://www.paypal.com/paypalme/FranciscoDari",
		"Source": "https://github.com/DariHernandez/multiclipboard"
		},
	packages = find_packages(include=["multiclipboard", "multiclipboard.*"]),
	install_requires = ["pyperclip"],
	python_requires = ">=3.7"
)
