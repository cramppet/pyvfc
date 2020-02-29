# PyVFC - Vector Field Consensus (VFC) bindings for Python3

## What is VFC?

Vector Field Consensus (VFC) is a powerful point pairing algorithm developed
in 2014 by Jiayi Ma, Ji Zhao, Jinwen Tian, Alan L. Yuille, and Zhuowen Tu.

VFC is similar to algorithms like **RANSAC** and **PROSAC** whereby we perform
a series of operations on feature matched keypoints in order to determine which
set of keypoints are so-called "inliers" and which are "outliers".

Unlike the two previously mentioned however, VFC is extremely robust and tolerant 
to very high levels of outliers with only a minimal number of inliers. To quote 
the abstract from their paper:

> Our algorithm starts by creating a set of putative correspondences which can 
> contain a very large number of false correspondences, or outliers, in addition 
> to a limited number of true correspondences (inliers).

- Find [their original paper here](https://sites.google.com/site/drjizhao/MaJ_2014_TIP.pdf?attredirects=0)
- Find [their original source code here](https://sites.google.com/site/drjizhao/vfc_opencv.zip?attredirects=0)

I have created these Python3 bindings for their algorithm using their C++ code 
which I modified very slightly to work with native Python types.

**NOTE:** The algorithm and this package, is targeted at OpenCV users. Users of 
other frameworks can leverage this package, but they will have to install OpenCV
in order to run this algorithm.

## Installation

**NOTE**: As of 3/1/2020 I have only tested the installation on Ubuntu-based
GNU/Linux distributions.

0. `apt install libopencv-dev`
1. `pip3 install pyvfc`

## Example usage

```python3
#!/usr/bin/env python3

import cv2
import pyvfc

im1 = cv2.imread('church1.jpg', 0)
im2 = cv2.imread('church2.jpg', 0)
orb = cv2.ORB_create()
vfc = pyvfc.VFC()

kp1, desc1 = orb.detectAndCompute(im1, None)
kp2, desc2 = orb.detectAndCompute(im2, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(desc1, desc2)

out = cv2.drawMatches(im1, kp1, im2, kp2, matches, None)
cv2.imwrite('initial_match.png', out)

pts1 = [kp1[match.queryIdx].pt for match in matches]
pts2 = [kp2[match.trainIdx].pt for match in matches]

if vfc.setData(pts1, pts2):
    vfc.optimize()
    match_idx = vfc.obtainCorrectMatch()
    good_matches = [matches[idx] for idx in match_idx]
    out = cv2.drawMatches(im1, kp1, im2, kp2, good_matches, None)
    cv2.imwrite('vfc_results.png', out)
    print('VFC ratio %d/%d' % (len(match_idx), len(matches)))
```
