import numpy as np
from sklearn.preprocessing import normalize
import argparse

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import pdb

parser =  argparse.ArgumentParser()
parser.add_argument("--h", type=int, help="Template height")
parser.add_argument("--w", type=int, help="Template width")
parser.add_argument("--o", type=str, help="Output file name without extension")
parser.add_argument("--crop", type=int, help="Optional. Crop template after initialization")
parser.add_argument("--normType",  
                    type=str,   
                    choices=['packnet', 'l2'],  
                    help="Packnet: z=1 (ie divide by 'z' component of each vector). OR l2 norm for each vector")
args = parser.parse_args()

w = args.w
h = args.h

fx = cx = w/2
fy = cy = h/2

K = np.array([[fx,  0, cx],
              [ 0, fy, cy],
              [ 0,  0,  1]])
Kinv = np.linalg.inv(K)

p = []
for v in range(h):                  #row
    for u in range(w):              #col
        p.append(np.array([u,v,1]))

p = np.stack(p)         #p.shape = (w*h, 3)
Q = Kinv @ p.T          #Q.shape = (3, w*h)

if args.normType == 'l2
    Q_norm = normalize(Q, axis=0)   #Q.shape = (3, w*h) 
elif args.normType == 'packnet':
    Q_norm = Q / Q[2, :]
else:
    sys.exit('Wrong normalization type')

Q_ray_surface = np.zeros((1,3,h,w))
for v in range(w*h):
    idx = p[v,:]
    Qw = idx[0]
    Qh = idx[1]
    ray = Q_norm[:, v]
    Q_ray_surface[0, :, Qh, Qw] = ray

if args.crop:
    Q_ray_surface = Q_ray_surface[:,:,0:args.crop,:]

fname = args.o
with open(fname + '.npy', 'wb') as f:
    np.save(f, Q_ray_surface.astype('float32'))
