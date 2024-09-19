set -ex
cd ..
python train.py --dataroot ./datasets/monet2photo --name facades_pix2pix --model pix2pix --netG unet_256 --direction BtoA --lambda_L1 100 --dataset_mode aligned --norm batch --pool_size 0
