# -*- coding: utf-8 -*-
import sys
import os
from PIL import Image
from pprint import pprint
import csv

isScaled = True


def main():
    # get filenames
    csvs = ['csv/' + x for x in os.listdir('csv')]
    images = ['fig/' + x for x in os.listdir('fig')]

    '''
    pprint(csvs[0:5])
    pprint(images[0:5])
    '''

    csv_file = open(csvs[0], 'r')
    reader = list(csv.reader(csv_file))
    height, width = [int(x) for x in reader[1][1:3]]
    rescale_images(images, width, height)
    '''
    writer = csv.writer(csv_file)
    filenames = os.listdir('fig')
    img = Image.open(filename)
    x, y = img.size
    mag = float(height) / y
    img = pygame.image.load(filename)
    img = pygame.transform.scale(img, (int(x * mag), int(y * mag)))
    '''


def rescale_images(images, width, height):
    for image in images:
        img = Image.open(image)
        x, y = img.size
        mag = float(height) / y
        size = (int(x * mag), int(y * mag))
        img_resize = img.resize(size)
        img_resize.save(image, quality=100)


if __name__ == '__main__':
    main()
