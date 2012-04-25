# app_keywords.py

Solves the problem of remembering the abstract names of applications on your Mac.
It scrapes a short description of the app from MacUpdate.com, and saves it to the app's Spotlight comments.
Then, you can easily find the app with Spotlight by searching for it's function or keyword.

### Pre-requisites

This script uses appscript and BeautifulSoup. The easiest way to install these is using pip:

    pip install appscript
    pip install beautifulsoup4

### Using the script

Simply running:
	
	python app_keywords.py

will iterate through the applications in /Applications/ folder. If the application is on MacUpdate.com, it will grab the description and save it to the Spotlight Comments field. You can edit/view this by selecting the application and hitting Command+I.

# License

Unless otherwise noted in the source file, everything is MIT licensed.