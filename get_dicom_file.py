# -*- coding: utf-8 -*-

import sys
import os
import pydicom
from matplotlib import pyplot as plt
from PIL import Image


def main():
    files = os.listdir('dicom')
    os.chdir('dicom')
    for filename in files:
        dataset = pydicom.read_file(filename)
        img = dataset.pixel_array
        gray_img = Image.fromarray((img/16).astype('uint8'), mode = 'L')
        gray_img.save(filename.replace('.dcm', '.png'))


if __name__ == '__main__':
    main()
