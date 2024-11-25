# python pytorch-CycleGAN-and-pix2pix/datasets/combine_A_and_B.py --fold_A datasets/SSA_Both_Holdout/A
# python datasets/combine_A_and_B.py --fold_A datasets/SSA_Both_Holdout/A --fold_B datasets/SSA_Both_Holdout/B --fold_AB datasets/SSA_Both_Holdout
python datasets/combine_A_and_B.py --fold_A datasets/10-01/A --fold_B datasets/10-01/B --fold_AB datasets/10-01 --no_multiprocessing
