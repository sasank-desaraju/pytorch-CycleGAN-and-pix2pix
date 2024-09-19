# This is for testing the ICG models

python test.py \
    --dataroot ./datasets/ICG_Video/ \
    --name HighDose_10_19 \
    --model pix2pix \
    --direction AtoB \
    --num_test 1968 \
    --use_wandb
