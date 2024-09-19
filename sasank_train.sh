#!/bin/bash

# Sasank's train script which he edits every time to change model name, dataroot, etc.

# python train.py --dataroot datasets/Madani_Both_test/ --name Madani_Both_test_2 --model pix2pix --direction AtoB --use_wandb
python train.py --dataroot datasets/2024-08-24_Holdout/ --name 2024-08-24_Holdout --model pix2pix --direction AtoB
