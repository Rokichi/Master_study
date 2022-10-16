# -*- coding: utf-8 -*-
import sys
import os
import csv
import cv2
from PIL import Image
from pprint import pprint

isScaled = False


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
    if isScaled:
        rescale_images(images, width, height)
    img_to_csv: dict = make_dict_img_to_csv(images, csvs)
    # 画像毎にヒートマップ作成
    for image in images:
        with open(img_to_csv[image], 'r') as f:
            gazedatas = get_fixed_gaze_data(width, image, list(csv.reader((f)))[1:])
            draw_heatmap(image, gazedatas)
            

# 横のずれ直し
def get_fixed_gaze_data(width, image, gazedatas):
    datas = []
    img = Image.open(image)
    img_x, img_y = img.size
    for gazedata in gazedatas:
        data = [int(x) for x in gazedata[-2:]]
        data[0] -= (width - img_x) // 2
        datas.append(data)
    return datas


# mapを作成
def make_dict_img_to_csv(images, csvs):
    dic = dict()
    for image in images:
        replaced_image = image.replace('.', '_').replace('fig/', 'csv/')
        for csv in csvs:
            if replaced_image in csv:
                dic[image] = csv
                break
        else:
            print('Error: {} not found'.format(replaced_image))
    return dic


# 画面サイズに合わせたサイズにリサイズ
def rescale_images(images, width, height):
    for image in images:
        img = Image.open(image)
        x, y = img.size
        mag = float(height) / y
        size = (int(x * mag), int(y * mag))
        img_resize = img.resize(size)
        img_resize.save(image, quality=100)

# ヒートマップ作成
def draw_heatmap(filename, gazedatas):
    img = cv2.imread(filename)
    annotated = img.copy()
    for gazedata in gazedatas:
        cv2.circle(annotated, tuple(gazedata), 40, color=(
            100, 100, 100), thickness=-1)
    mat_img = cv2.addWeighted(annotated, 0.4, img, 0.6, 0)
    #cv2.imshow('', img)
    #cv2.waitKey(0)
    #cv2.imwrite(filename.replace('fig/', 'heatmap/').replace('.png', '_heatmap.png'), mat_img)
    cv2.imwrite(filename.replace('fig/', 'heatmap/'), mat_img)


if __name__ == '__main__':
    main()
