Workflow for generating a dataset and training with Packnet
All python scripts are contained in `~/packnet-sfm/scripts/`

I have been storing data in /data/datasets/blackvue/

####################################################################################
Getting the data

run: 
  `download_blackvue.py`
  pulls videos from the ground-based-swarm/New Orleans/ s3 bucket until desired number
  of frames   is reached (default 50k frames)
  -h for parameter explanations
  There is a hardcoded blacklist (videos with a large percentage of frames that don't train well)
  and previously downloaded list. Edit these as you see fit.

####################################################################################
Prepping the data
This is the annoying part

To extract and scale video frames run:
  `scale_and_crop_video.py --in_dir [dir with videos] --out_dir [dir to store images] --scale 1920:1080 --crop 1920:1080`
  The images will be stored in [out_dir]/[video_name]/
  --`scale` will scale the video to 1920x1080
  --`crop` will not crop the video (the script needs to be updated)
  
Here is where you should manually inspect each video and remove frames where the camera is static.
Alternatively, write a script to do it. Other projects have discussed using optical flow to identify static image sequences.

To generate sfm_data for each set of images, from [out_dir]
  `for f in ./*; do openMVG_main_SfMInit_ImageListing -i $f -o $f/outputs -c 5 -k "890;0;960;0;890;540;0;0;1"; done`

To edit each sfm_data and add in distortion parameters:
  `for f in ./*/outputs/sfm_data.json; do vim $f; done`
  This just opens each sfm_data.json individually in vim. You must add the distortion 
  parameters manually.
  
To undistort:
  `for d in ./*/outputs; do openMVG_main_ExportUndistortedImages	 -n 8 -i $d/sfm_data.json -o $d; done`

To scale and crop undistorted images:
  `for f in ./*/*.png; do ffmpeg -y -i $f -filter:v "scale=1088:612,crop=1088:480:0:0" $f; done`
  
####################################################################################
Get training

To split the data into training, validation:
  `generate_data_splits.py --dump_root [output_dir]`
   Will create [output_dir]/train and [output_dir]/val subdirectories
   Currently does a 99.9:0.1 train:val split

Confirm that your config yaml is setup appropriately
Confirm that `packnet_sfm/datasets/image_dataset.py` has the correct intrinsics

from home dir run `./runMe.sh` to enter docker
run:
  `train.py configs/[your_config_file.yaml]`
  
####################################################################################
WandB logging

Create an account with WandB and ensure you are logged in on your browser.
In the yaml config file:
  Give your 'project' a name. This is the top level categorization and will group all runs with the same project name together.
  Give the run a 'name'. This should be unique to each training session as this is also the directory where the logs will be stored. 
  
  Project
  |-Run 1
  |-Run 2

  Set 'entity' to your WandB to your username
  Choose the directory where you want the WandB to store logs
  Ensure 'dry_run' is set to `False`

Within the docker env but prior to training run:
  `wandb login`

