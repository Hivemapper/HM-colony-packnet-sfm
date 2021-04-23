import argparse
import os
from pathlib import Path
import pdb
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument("--in_dir", type=str, required=True, help="Where to read the data")
parser.add_argument("--out_dir", type=str, required=True, help="Where to dump the data")
parser.add_argument("--scale", type=str, required=True, help="Dimensions to scale video to in form of 'out_width:out_height")
parser.add_argument("--crop", type=str, required=True, help="Dimensions to crop video to in form of 'out_width:out_height")
args = parser.parse_args()

scale = 'scale=' + args.scale
crop = 'crop=' + args.crop + ':0:0'
filter_arg = scale + ',' + crop  

for path in Path(args.in_dir).rglob('*.mp4'):
  im_dir = path.with_suffix('').name
  final_dir = os.path.join(args.out_dir, im_dir)
  if not os.path.exists(final_dir):
    os.makedirs(final_dir)
  cmd = ["ffmpeg", "-i", str(path), "-filter:v", filter_arg, "-start_number", "0", os.path.join(final_dir, "%06d.png")]
  subprocess.run(cmd)