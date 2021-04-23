import argparse
import os

from glob import glob
from cv2 import imread, imwrite, resize

# from packnet_sfm.utils.image import load_image, write_image

import pdb

parser =  argparse.ArgumentParser()
parser.add_argument("--dir", type=str, required=True, help="Directory containing images to be cropped")
parser.add_argument("--w", type=int, required=True, help="Width to resize to.")
parser.add_argument("--h", type=int, required=True, help="Height to resize to.")
args = parser.parse_args()


subfolders = os.listdir(args.dir)
files = []
for s in subfolders:
    for ext in ['png', 'jpg']:
        files.extend(glob((os.path.join(args.dir, s, '*.{}'.format(ext)))))
    files.sort()

# pdb.set_trace()
for f in files: 
    image = imread(f, 1) 
    _, w, _= image.shape
    image = resize(image, (args.w, args.h), interpolation = 3)#cv2.INTER_AREA)
    imwrite(f, image)
