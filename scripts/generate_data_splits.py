import argparse
import numpy as np
from glob import glob
import os

import pdb

parser = argparse.ArgumentParser()
parser.add_argument("--dump_root", type=str, required=True, help="Where to dump the data")
args = parser.parse_args()

val_dir = os.path.join(args.dump_root, "val")
train_dir = os.path.join(args.dump_root, "train")

np.random.seed(8964)
subfolders = os.listdir(args.dump_root)
train = 0
val = 0
for s in subfolders:
    if not os.path.isdir(args.dump_root + '/%s' % s):
        continue
    imfiles = glob(os.path.join(args.dump_root, s, '*.png'))
    frame_ids = [os.path.basename(fi) for fi in imfiles]
    # pdb.set_trace()
    for frame_path in imfiles:
        frame_file = os.path.basename(frame_path)
        if np.random.random() < 0.001:
            val += 1
            out = os.path.join(val_dir, '%s' % s)
            if not os.path.exists(out):
                os.makedirs(out)
            os.rename(frame_path, os.path.join(out, frame_file))
            # vf.write('%s/%s.png\n' % (s, frame))
            # vf.write('%s\n' % frame)
        else:
            train += 1
            out = os.path.join(train_dir, '%s' % s)
            if not os.path.exists(out):
                os.makedirs(out)
            os.rename(frame_path, os.path.join(out, frame_file))
            # tf.write('%s/%s.png\n' % (s, frame))
            # tf.write('%s\n' % frame)

print("Training frames: ", train)
print("Validation frames: ", val)
