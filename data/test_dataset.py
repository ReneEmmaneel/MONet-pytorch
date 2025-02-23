import os

import torchvision.transforms.functional as TF

from data.base_dataset import BaseDataset
from data.image_folder import make_dataset
from PIL import Image

import numpy as np
import torch

class TestDataset(BaseDataset):
    """This dataset class can load a set of images specified by the path --dataroot /path/to/data.

    It can be used for generating CycleGAN results only for one side with the model option '-model test'.
    """

    @staticmethod
    def modify_commandline_options(parser, is_train):
        parser.set_defaults(input_nc=3, output_nc=3,
                            crop_size=192, # crop is done first
                            load_size=64,  # before resize
                            num_slots=11, display_ncols=11)
        return parser

    def __init__(self, opt):
        """Initialize this dataset class.

        Parameters:
            opt (Option class) -- stores all the experiment flags; needs to be a subclass of BaseOptions
        """
        BaseDataset.__init__(self, opt)
        max_dataset_size = opt.max_dataset_size if opt.max_dataset_size else 10
        self.images = [torch.zeros(3, 64, 64, dtype=torch.float) for _ in range(max_dataset_size)]

    def _transform(self, img):
        img = TF.resized_crop(img, 64, 29, self.opt.crop_size, self.opt.crop_size, self.opt.load_size)
        img = TF.to_tensor(img)
        img = TF.normalize(img, [0.5] * self.opt.input_nc, [0.5] * self.opt.input_nc)
        return img

    def __getitem__(self, index):
        """Return a data point and its metadata information.

        Parameters:
            index - - a random integer for data indexing

        Returns a dictionary that contains A and A_paths
            A(tensor) - - an image in one domain
            A_paths(str) - - the path of the image
        """
        A = self.images[index]
        return {'A': A, 'A_paths': ''}

    def __len__(self):
        """Return the total number of images in the dataset."""
        return len(self.images)
