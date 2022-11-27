# -*- coding: utf-8 -*-

import sys
import cv2
import pydicom

filename = r"C:\Users\byrk1\AppData\Local\Google\Cloud SDK\p10\p10000032\s50414267\02aa804e-bde0afdd-112c0b34-7bc16630-4e384014.dcm"

def main():
    path = pydicom.data.get_testdata_file(filename)
    dataset = pydicom.filereader.dcmread(path)
    img = dataset.pixel_array
    cv2.imwrite(img, filename.replace('.dcm', '.png'))
    

if __name__ == '__main__':
    lines = []
    for l in sys.stdin:
        lines.append(l.rstrip('\r\n'))
    main()