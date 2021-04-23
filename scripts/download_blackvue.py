import boto3
import smart_open
import datetime
from dateutil.tz import tzutc
import json
import argparse
import os
import random

import pdb

blacklist = ['20201027_065859_NF',  #rainy
             '20201027_080320_NF',  #rainy
             '20201027_082408_NF',  #rainy
             '20201103_074854_NF',  #1/3 traffic
             '20201106_073658_NF',  #3/4 traffic
             '20201111_090127_NF',  #3/4 traffic
             '20201113_060336_NF',  #1/4 traffic
             '20201113_062855_NF']  #1/2 traffic

already_dl = ['20201029_102615_NF',
              '20201029_104844_NF',
              '20201030_084927_NF',
              '20201030_085029_NF',
              '20201030_085755_NF',
              '20201103_080414_EF',
              '20201103_083141_NF',
              '20201106_081936_NF',
              '20201106_082441_NF',
              '20201106_082612_NF',
              '20201106_084009_NF',
              '20201111_080319_EF',
              '20201112_060110_NF',
              '20201112_070029_NF',
              '20201112_071957_NF',
              '20201112_072805_NF',
              '20201113_060814_EF',
              '20201113_061724_NF',
              '20201113_062027_NF',
              '20201115_080910_NF',
              '20201115_081321_NF',
              '20201115_083606_EF',
              '20201115_084139_EF',
              '20201115_095813_EF']

def parse_args():
    parser =  argparse.ArgumentParser()
    parser.add_argument("-o", "--out_dir", type=str, required=True, help="Output directory")
    parser.add_argument("-b", "--bucket", type=str, default="ground-based-swarm", help="s3 bucket where blackvue videos are stored")
    parser.add_argument("-n", "--num_frames", type=int, default=50000, help="Target number of video frames.")
    return parser.parse_args()

def get_all_s3_objects(s3, **base_kwargs):
    continuation_token = None
    while True:
        list_kwargs = dict(MaxKeys=1000, **base_kwargs)
        if continuation_token:
            list_kwargs['ContinuationToken'] = continuation_token
        response = s3.list_objects_v2(**list_kwargs)
        yield from response.get('Contents', [])
        if not response.get('IsTruncated'):  # At the end of the list?
            break
        continuation_token = response.get('NextContinuationToken')

def get_filenames(s3, bucket_name):
  keys_to_read = []
  for key in get_all_s3_objects(s3, Bucket=bucket_name, Prefix="New Orleans"):
    _, file_ext = os.path.splitext(key['Key'])
    if (file_ext == ".mp4"):
      keys_to_read.append(key['Key'])

  return keys_to_read

def download_video(bucket, video_file, output_path):
  output_path_dir = os.path.dirname(output_path)
  if not os.path.exists(output_path_dir):
      os.makedirs(output_path_dir)
  s3.download_file(bucket, video_file, output_path)

def count_frames(video_path):
  cmd = "ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of" + \
       " default=nokey=1:noprint_wrappers=1 '" + str(video_path) + "' 2>/dev/null"
  return int(os.popen(cmd).read().strip())

def blacklisted(video_file):
  basename = os.path.basename(video_file)
  return os.path.splitext(basename)[0] in blacklist

def downloaded(video_file):
  basename = os.path.basename(video_file)
  return os.path.splitext(basename)[0] in already_dl

if __name__ == "__main__":
  args = parse_args()
  s3 = boto3.client('s3')
  keys_to_read = get_filenames(s3, args.bucket)
  total_frames = 0
  total_videos = 0
  while total_frames < args.num_frames:
    # pdb.set_trace()
    vid_idx = random.randint(0, len(keys_to_read) - 1)
    vid_file = keys_to_read.pop(vid_idx)
    if not blacklisted(vid_file) and not downloaded(vid_file):
      out_path = os.path.join(args.out_dir, vid_file)
      download_video(args.bucket, vid_file, out_path)
      total_frames += count_frames(out_path)
      total_videos += 1

  print("Total number of videos downloaded: ", total_videos)
  print("Total number of frames downloaded: ", total_frames)
