# How to create and train models using my workflow

### by Sasank Desaraju

## Data Wrangling

Stage 1: raw image format to pytorch-CycleGAN-and-pix2pix/img_src/[dataset name e.g. date]/ with vis/ and icg/ subdirectories with paired image names
- Maybe also a info.txt that has info about the dataset
- This must be implemented differently for each raw data modality (e.g. screenshots, full videos)
- For screenshots, this is implemented in ICG Study/Code/process.py
- For full videos, this is implemented in ___

Stage 2: pytorch-CycleGAN-and-pix2pix/img_src/[dataset name] to P2P dataset
- This should be the same for screenshots, full videos, etc.
- This is implemented in ICG Study/Code/prepDataset.py

Stage 3: Edit and run combine_A_and_B.sh

## Model Training

* Place all the raw images in Raw Images
* Have a data CSV that looks like 'Dose and Dissection Timepoint for AI.csv'
* Run process.py (in ICG Study/Code) with the raw image root, CSV, and desired model data parameters. This readies the images (??) for a given model.
    * This creates a directory in ICG Study/ModelData with ICG, VIS, (empty) Images, readme.txt, model_images.csv
* Run prepDataset.py (in ICG Study/Code) to create a P2P dataset folder and populate it.
    * TODO: prepDataset.py seems to get the test images ready as well? Need to look into this.
    * Edit this to change your TTV the way you want it. E.g., using all images for train/val and none for test.
    * TODO: Maybe make a prepDataset_Inference.py
* Run combine_A_and_B.py (in P2P repo /datasets) to create the AB combined images.
    * Use pytorch-CycleGAN[blah blah]/combine_A_and_B.sh
* Run training

To train a model:
1. Run process.py (from ICG Study) to create your model dataset in ICG Study/ModelData.
1.5. (Optional) Remove holdout set image names the ModelData model_images.csv so that they don't get used in the normal TTV split.
2. Run prepDataset.py (from ICG Study) to create your TTV split and create your pix2pix dataset in pix2pix/datasets.
2.5 (Optional) Copy holdout set images to A/test and B/test directories
3. Run combine_A_and_B.sh
3. Run sasank_train.sh from the pix2pix directory.


## Model Inference

### This is for when there is no "B" ICG image.
### For example, this is used when we are predicting the ICG output of Madani's curated GNGNet test images.

* Use prepDataset_Inference.py to create a proper dataset where none of the images are in train or val.
    * Additionally, the real A images are copied to the real B so that it fits the format of a normal dataset.
* Run test.py on this new dataset.

To test a model:
1. Run sasank_test.sh from the pix2pix directory.
