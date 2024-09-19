# python pytorch-CycleGAN-and-pix2pix/datasets/combine_A_and_B.py --fold_A datasets/SSA_Both_Holdout/A
# python datasets/combine_A_and_B.py --fold_A datasets/SSA_Both_Holdout/A --fold_B datasets/SSA_Both_Holdout/B --fold_AB datasets/SSA_Both_Holdout
python datasets/combine_A_and_B.py --fold_A datasets/2024-08-24_Holdout/A --fold_B datasets/2024-08-24_Holdout/B --fold_AB datasets/2024-08-24_Holdout --no_multiprocessing
