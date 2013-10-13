## Image Perspective

Transforms an image based on the target image corners inside of a bounding box. Useful for accurately displaying non-georectified satellite imagery in a bounding box. Given a list of points, it determines the 4 corners, the shift from each corner to the bounding box corner, and applies the shift to the image.

### Theory

![Rectangle](https://raw.github.com/nathancahill/python-scripts/master/rectangle.jpg)

Given a list of points that bound the satellite image (not necessarily 4, usually around 20 from most data sources), the first task is to determine the 4 corners. The top right and the bottom left will have the longest and shortest hypotenuse respectively. The top left and the bottom right will have the biggest and smallest tan angle, respectively.

The second task, determining the bounding box is simple: it’s defined by the biggest and smallest x and y coordinates in the points.

Both of these matrices are scaled to the dimensions of the image, and the x, y percentage shift of each corner is translated to pixels. Based on Christopher Wren’s paper (http://xenia.media.mit.edu/~cwren/interpolator/), the shift coefficients can be determined and applied using PIL’s Image.transform().

### Pre-requisites

Uses numpy and PIL for transforming the image. Install:

    pip install numpy
    pip install PIL

### Using the script

Change the variable ```points``` on line 100 to the image points. Pass the image file as the first argument in the command line:

    python image_perspective.py my_image.jpg

---------------------------------------

## App Keywords

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

---------------------------------------

# Log Progress

When dealing with long running processes, especially multiprocessing ones, it's useful to see how many jobs are remaining in the queue. This script prints the remaining number of jobs in a logarithmic scale: as you near the end of the process, logging becomes more frequent.

### Using the script

Integrate the algorithm in your existing queue logic.

# License

Unless otherwise noted in the source file, everything is MIT licensed.