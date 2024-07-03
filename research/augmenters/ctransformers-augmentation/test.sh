#!/bin/bash

#SBATCH --gpus=2

source ~/miniconda3/bin/activate lo-env

# Directory where your script is located
cd "/data/rudrea@upvnet.upv.es/work/ERASMUS_Mobility_UPV_2023/LO Clustering/augmenters/ctransformers-augmentation"

python3 ctransformers_tests.py \
