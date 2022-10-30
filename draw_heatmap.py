# -*- coding: utf-8 -*-
import sys
import os
import csv
import cv2
import numpy as np
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
            gazedatas = get_fixed_gaze_data(
                width, image, list(csv.reader((f)))[1:])
            draw_heatmap(image, gazedatas)
            return

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
    print(filename)
    annotated = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)

    # 真っ黒な画像を生成
    black_img = np.zeros(annotated.shape, np.uint8)
    for j, row in enumerate(black_img):
        for i, column in enumerate(row):
            black_img[j][i][3] = 255
    # 計算用
    cal_img = black_img.copy()
    cal_img = cal_img.astype(np.int64)

    # 円でくり抜くところをカウント
    for gazedata in gazedatas:
        for i in range(1, 16):
            for_add = black_img.copy()
            cv2.circle(for_add, tuple(gazedata), 5*i, color=(
                10, 10, 10), thickness=-1)
            cal_img += for_add
    alphas = np.full(img.shape, 0.0, dtype=float)
    for j in range(len(cal_img)):
        for i in range(len(cal_img[j])):
            alphas[j][i] = np.array(
                [val / 255 if val < 255 else 1.0 for val in cal_img[j][i][:3]])
    for j in range(len(annotated)):
        for i in range(len(annotated[j])):
            annotated[j][i] = annotated[j][i] * alphas[j][i][0] + \
                black_img[j][i]*(1-alphas[j][i][0])
    cv2.imshow('', annotated)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
