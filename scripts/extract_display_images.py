import argparse
import numpy as np
from glob import glob
import os
from pathlib import Path
import pdb
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument("--dump_root", type=str, required=True, help="Where to dump the data")
args = parser.parse_args()

for path in Path(args.dump_root).rglob('*.mp4'):
  cmd = ["ffmpeg", "-i", str(path), "-vframes", "1", os.path.join(args.dump_root, path.with_suffix('.png').name)]
  subprocess.run(cmd)

# np.random.seed(8964)
# subfolders = os.listdir(args.dump_root)
# with open(args.dump_root + 'train.txt', 'w') as tf:
#     with open(args.dump_root + 'val.txt', 'w') as vf:
#         for s in subfolders:
#             if not os.path.isdir(args.dump_root + '/%s' % s):
#                 continue
#             imfiles = glob(os.path.join(args.dump_root, s, '*.png'))
#             frame_ids = [os.path.basename(fi).split('.')[0] for fi in imfiles]