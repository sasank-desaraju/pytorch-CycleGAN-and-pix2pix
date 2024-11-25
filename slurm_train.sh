#!/bin/bash
#SBATCH --job-name=ExLapPrediction
#SBATCH --mail-user=sasank.desaraju@ufl.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --output ./slurm/logs/my_job-%j.log
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=32gb
#SBATCH --time=72:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:4
#SBATCH --account=prismap-ai-core
#SBATCH --qos=prismap-ai-core
echo "Date      = $(date)"
echo "host      = $(hostname -s)"
echo "Directory = $(pwd)"


# Load compiler
# module load gcc
# echo "gcc version is $(gcc --version)"

# Load env
module load conda
conda activate p2p

# HPG actually recommends prepending the path to the environment instead of loading it.
export PATH=/home/sasank.desaraju.conda/envs/p2p/bin:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/sasank.desaraju.conda/envs/llm/p2p

echo "PATH is "
echo PATH $PATH /$PATH

python train.py \
  --dataroot datasets/10-01/ \
  --name 10-01_lambda10 \
  --model pix2pix \
  --direction AtoB \
  --gpu_ids 0,1,2,3 \
  --lambda_L1 10.0
  # --output_nc 1 \ # I would need to cast all the images to grayscale first


# Commenting this out bc I think with multiple GPUs it's trying to test the model before it's created or something
# python test.py --dataroot datasets/9-23/ --name 9-25_lambda10 --model pix2pix --direction AtoB --num_test 50000 --eval
