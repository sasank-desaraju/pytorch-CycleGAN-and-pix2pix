#!/bin/bash

# Sasank's test script which he edits every time to change model name, dataroot, etc.

# Removed --no_dropout
# python test.py --dataroot datasets/BothDose_10_19/ --name BothDose_10_19 --model pix2pix --direction AtoB --num_test 5000 --eval --use_wandb
python test.py --dataroot datasets/SSA_LowDose_Holdout/ --name SSA_LowDose_Holdout --model pix2pix --direction AtoB --num_test 5000 --eval
