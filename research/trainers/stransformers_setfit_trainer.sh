#!/bin/bash

# Define experiment name
EXP_NAME="poc-training-mpnet-v1"

#SBATCH --job-name=$EXP_NAME --gpus=1 --cpus-per-task=4 --mem=51200 --output="${EXP_NAME}_output.txt"

# Activate the virtual environment
source ~/miniconda3/bin/activate lo-env

# Directory where your script is located
cd "/data/rudrea@upvnet.upv.es/work/ERASMUS_Mobility_UPV_2023/LO Clustering"

# Run the Python script with required arguments
python3 "trainers/stransformers_setfit_trainer.py" \
--exp-name "$EXP_NAME" \
--train-dataset-path "data/wiki_train.xlsx" \
--eval-dataset-path "data/wiki_eval.xlsx" \
--test-dataset-path "data/wiki_test.xlsx" \
--model "all-mpnet-base-v1" \
--body-training-strategy "cosine" \
--body-batch-size 16 \
--body-epochs 1 \
--classif-batch-size 16 \
--classif-epochs 2 \
--l2-weight 0.01 \
--seed 42 \
--metric "accuracy" \
--sampling-strategy "undersampling" \
--save-steps 1000 \
--eval-steps 1000 \
--logging-steps 500 \