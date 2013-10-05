# app_keywords.py

Solves the problem of remembering the abstract names of applications on your Mac.
It scrapes a short description of the app from MacUpdate.com, and saves it to the app's Spotlight comments.
Then, you can easily find the app with Spotlight by searching for keywords.

### Pre-requisites

This script uses BeautifulSoup for parsing data from MacUpdate.com. The easiest way to install this is with pip:

    pip install beautifulsoup4

### Using the script

Simply running:
	
	python app_keywords.py

will iterate through the applications in /Applications/ folder. If the application is on MacUpdate.com, it will grab the description and save it to the Spotlight Comments field. You can edit/view this by selecting the application and hitting Command+I.

# log_progress.py

When dealing with long running processes, especially multiprocessing ones, it's useful to see how many jobs are remaining in the queue. This script prints the remaining number of jobs in a logarithmic scale: as you near the end of the process, logging becomes more frequent.

### Using the script

Integrate the algorithm in your existing queue logic.

# License

Unless otherwise noted in the source file, everything is MIT licensed.