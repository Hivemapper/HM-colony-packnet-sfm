import argparse
import os

from glob import glob
from cv2 import imread, imwrite, waitKey, imshow

# from packnet_sfm.utils.image import load_image, write_image

import pdb

parser =  argparse.ArgumentParser()
parser.add_argument("--dir", type=str, required=True, help="Directory containing images to be cropped")
parser.add_argument("--crop", type=int, required=True, help="Final height of cropped images. Crops from bottom up.")
args = parser.parse_args()


subfolders = os.listdir(args.dir)
files = []
for s in subfolders:
    for ext in ['png', 'jpg']:
        files.extend(glob((os.path.join(args.dir, s, '*.{}'.format(ext)))))
    files.sort()

# pdb.set_trace()
crop = args.crop
for f in files: 
    image = imread(f, 1) 
    _, w, _= image.shape
    # image = image.crop(box=(0, 0, w, crop))
    # imshow("full", image)
    # waitKey(0)
    image = image[0:crop, 0:w]
    # imshow("cropped", image)
    # waitKey(0)
    # break
    imwrite(f, image)



