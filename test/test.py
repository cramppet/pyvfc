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
