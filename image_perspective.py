#!/usr/bin/env python
# encoding: utf-8

# Transforms an image based on the target image corners inside of a bounding box.
# Useful for accurately displaying non-georectified satellite imagery in a bounding box.
# Given a list of points, it determines the 4 corners, the shift from each corner to the bounding box corner,
# and applies the shift to the image.
#

# Copyright (c) 2013 Nathan Cahill

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the
# following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import math
import numpy
from PIL import Image

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

def find_points(points):
    # Define the initial corners and sides to compare
    ll = points[0]
    lr = points[0]
    ul = points[0]
    ur = points[0]

    l = points[0][0]
    r = points[0][0]
    t = points[0][1]
    b = points[0][1]

    # Initial high and low angles
    ha = math.degrees(math.atan(points[0][1] / points[0][0]))
    la = math.degrees(math.atan(points[0][1] / points[0][0]))

    # Initial long and short hypotenuse
    llh = math.sqrt(ll[0] * ll[0] + ll[1] * ll[1])
    urh = math.sqrt(ur[0] * ur[0] + ur[1] * ur[1])

    for point in points:
        # Find the sides
        if point[0] < l:
            l = point[0]
        elif point[0] > r:
            r = point[0]

        if point[1] < b:
            b = point[1]
        elif point[1] > t:
            t = point[1]

        # Calculate hypotenuse and the angle
        h = math.sqrt(point[0] * point[0] + point[1] * point[1])
        a = math.degrees(math.atan(point[1] / point[0]))

        # Find the corners from the long and short hypotenuse
        if h < llh:
            llh = h
            ll = point
        elif h > urh:
            urh = h
            ur = point

        # Find the corners from the high and low angle
        if a > ha:
            ha = a
            ul = point
        elif a < la:
            la = a
            lr = point

    # Return the points and bounding box as a tuple (points, bounding)
    return ({'ul': ul, 'ur': ur, 'lr': lr, 'll': ll}, {'ul': [l, t], 'ur': [r, t], 'lr': [r, b], 'll': [l, b]})

if __name__ == '__main__':
    points = [[30.70879392217805, 37.59353197545942], [31.44646572320749, 37.62727445270031], [31.446043712726865, 37.255240910762176], [30.709370206423532, 37.2209786602704], [30.70879392217805, 37.59353197545942]]
    points, bounding = find_points(points)

    width = bounding['ur'][0] - bounding['ul'][0]
    height = bounding['ur'][1] - bounding['lr'][1]

    shift_ul = ((points['ul'][0] - bounding['ul'][0]) / width, (points['ul'][1] - bounding['ur'][1]) / height)
    shift_ur = ((points['ur'][0] - bounding['ur'][0]) / width, (points['ur'][1] - bounding['ur'][1]) / height)
    shift_ll = ((points['ll'][0] - bounding['ul'][0]) / width, (points['ll'][1] - bounding['lr'][1]) / height)
    shift_lr = ((points['lr'][0] - bounding['ur'][0]) / width, (points['lr'][1] - bounding['lr'][1]) / height)

    img = Image.open(sys.argv[1])
    width, height = img.size

    coeffs = find_coeffs(
                [
                    (0, 0),
                    (width, 0),
                    (width, height),
                    (0, height)
                ],
                [
                    (0 + (width * shift_ul[0]), 0 + (height * shift_ul[1])),
                    (width + (width * shift_ur[0]), 0 + (height * shift_ur[1])),
                    (width + (width * shift_lr[0]), height + (height * shift_lr[1])),
                    (0 + (width * shift_ll[0]), height + (height * shift_ll[0]))
                ])

    img.transform((width, height), Image.PERSPECTIVE, coeffs, Image.BICUBIC).save(sys.argv[1])
