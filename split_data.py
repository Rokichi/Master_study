# -*- coding: utf-8 -*-

import sys
import os
import random
import shutil

def main():
    init_dir()
    images = ['fig/' + x for x in os.listdir('fig')]
    split_num = int(len(images) * 0.8)
    random.shuffle(images)
    for _ in range(split_num):
        image = images.pop(0)
        heatmap = image.replace('fig/', 'heatmap/')
        shutil.copy(image, r'pytorch-CycleGAN-and-pix2pix\datasets\trainB')
        shutil.copy(heatmap, r'pytorch-CycleGAN-and-pix2pix\datasets\trainA')
    for image in images:
        heatmap = image.replace('fig/', 'heatmap/')
        shutil.copy(image, r'pytorch-CycleGAN-and-pix2pix\datasets\testB')
        shutil.copy(heatmap, r'pytorch-CycleGAN-and-pix2pix\datasets\testA')


def init_dir():
    refresh_dir(r'pytorch-CycleGAN-and-pix2pix\datasets\trainA')
    refresh_dir(r'pytorch-CycleGAN-and-pix2pix\datasets\trainB')
    refresh_dir(r'pytorch-CycleGAN-and-pix2pix\datasets\testA')
    refresh_dir(r'pytorch-CycleGAN-and-pix2pix\datasets\testB')
    refresh_dir(r'pytorch-CycleGAN-and-pix2pix\datasets\test')
    refresh_dir(r'pytorch-CycleGAN-and-pix2pix\datasets\train')


def refresh_dir(dir_name):
    try:
        shutil.rmtree(dir_name)
    except:
        pass
    os.mkdir(dir_name)

if __name__ == '__main__':
    main()