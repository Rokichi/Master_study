# -*- coding: utf-8 -*-
import sys
import os
import csv
import cv2
import numpy as np
from PIL import Image
from pprint import pprint
from typing import List
from typing import Dict


isScaled = False

target_directory = 'images/'
save_directory = target_directory.replace('/', '_marged/')


def main():
    all_images = os.listdir(target_directory.replace('/', ''))
    images_dict = get_image_by_name(all_images)
    sorted_keys = sorted(images_dict.keys())
    # フォルダ作成
    try:
        os.mkdir(save_directory.replace('/', ''))
    except FileExistsError:
        pass

    for key in sorted_keys:
        images = images_dict[key]
        save_marged_image(key, images)


def save_marged_image(key: str, images: List[cv2.Mat]):
    # mkdir
    save_dir = save_directory + f'{key}/'
    try:
        os.mkdir(save_dir)
    except FileExistsError:
        pass

    # filename
    real_A_filename = f'{key}_real_A.png'
    real_B_filename = f'{key}_real_B.png'
    fake_B_filename = f'{key}_fake_B.png'

    # images
    real_A = images.pop(real_A_filename)
    real_B = images.pop(real_B_filename)
    fake_B = images.pop(fake_B_filename)

    # blend_img
    blend_img_real = get_alphas(real_B)
    blend_img_fake = get_alphas(fake_B)

    # blend
    marged_img_real = real_A * \
        (1 - blend_img_real[:, :, 3:] / 255) + \
        blend_img_real * (blend_img_real[:, :, 3:] / 255)
    marged_img_fake = real_A * \
        (1 - blend_img_fake[:, :, 3:] / 255) + \
        blend_img_fake * (blend_img_fake[:, :, 3:] / 255)

    # save
    cv2.imwrite(save_dir + real_B_filename, marged_img_real)
    cv2.imwrite(save_dir + fake_B_filename, marged_img_fake)


def get_alphas(original_img: cv2.Mat) -> cv2.Mat:
    black = [0, 0, 0]
    alphas = np.zeros(original_img.shape, np.uint8)
    for j in range(len(original_img)):
        for i in range(len(original_img[j])):
            alphas[j][i] = black + [255-original_img[j][i][0]]
    return alphas


def get_image_by_name(all_images: List[str]) -> Dict[str, Dict[str, any]]:
    splited_images = dict()
    for image_name in all_images:
        index = image_name[:4]
        is_real = '_real' in image_name
        is_A = '_A' in image_name
        image = cv2.imread('images/' + image_name, -1)
        if image.ndim == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
        if index in splited_images:
            splited_images[index][set_index_name(
                index, is_real, is_A)] = image
        else:
            splited_images[index] = {set_index_name(
                index, is_real, is_A): image}
    return splited_images


def set_index_name(index: str, is_real: bool, is_A: bool) -> str:
    index += '_real' if is_real else '_fake'
    index += '_A' if is_A else '_B'
    index += '.png'
    return index


if __name__ == '__main__':
    main()
