#!/usr/bin/env python
# encoding: utf-8

#	Add keywords and descriptions to your Mac applications
#
#	Solves the problem of remembering the abstract names of applications on your computer.
#	It scrapes a short description of the app from MacUpdate.com, and saves it to the app's Spotlight comments.
#	Then, you can easily find the app with Spotlight by searching for it's function or keyword.

#	Copyright (c) 2012 Nathan Cahill

#	Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
#	associated documentation files (the "Software"), to deal in the Software without restriction, including
#	without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#	copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the
#	following conditions:

#	The above copyright notice and this permission notice shall be included in all copies or substantial
#	portions of the Software.

# 	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
#	LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
#	NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#	WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#	SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import os
import glob
import urllib2
from bs4 import BeautifulSoup

applications = '/Applications/'
macupdate_url = 'http://www.macupdate.com/find/mac/'
script = """osascript -e 'tell application "Finder" to set comment of (POSIX file "/Applications/%s" as alias) to "%s"'"""

# Loop through Applications folder
for currentFile in glob.glob(os.path.join(applications, '*.app')):
    if os.path.isdir(currentFile):
        (name, ext) = os.path.basename(currentFile).split('.app')
        print('Searching for ' + name + '...')

        # Search and scrape MacUpdate.com for the application
        html = urllib2.urlopen(macupdate_url + urllib2.quote(name)).read()
        desc = BeautifulSoup(html).find_all('span', {'class': 'shortdes'})

        if not desc:
            print('Could not find a match for ' + name)
            print(' ')

        else:
            desc = desc[0].get_text().lstrip(' - ')

            # Add description to Spotlight Comments
            os.system(script % (os.path.basename(currentFile), desc))
            print(' ')
