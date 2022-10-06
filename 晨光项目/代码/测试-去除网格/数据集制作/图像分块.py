# https://blog.csdn.net/wanzhen4330/article/details/84317071
# https://blog.csdn.net/qq_38970783/article/details/90083142

import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import copy as cp
import random
import cv2
import os
import collections

def divide_method2(img, m, n):  # 分割成m行n列
    h, w = img.shape[0], img.shape[1]
    grid_h = int(h * 1.0 / (m - 1) + 0.5)  # 每个网格的高
    grid_w = int(w * 1.0 / (n - 1) + 0.5)  # 每个网格的宽

    # 满足整除关系时的高、宽
    h = grid_h * (m - 1)
    w = grid_w * (n - 1)

    # 图像缩放
    img_re = cv2.resize(img, (w, h),cv2.INTER_LINEAR)
    # 也可以用img_re=skimage.transform.resize(img, (h,w)).astype(np.uint8)
    # plt.imshow(img_re)
    gx, gy = np.meshgrid(np.linspace(0, w, n), np.linspace(0, h, m))
    gx = gx.astype(np.int)
    gy = gy.astype(np.int)

    # 这是一个五维的张量，前面两维表示分块后图像的位置（第m行，第n列），后面三维表示每个分块后的图像信息
    divide_image = np.zeros([m - 1, n - 1, grid_h, grid_w, 3],
                            np.uint8)
    for i in range(m - 1):
        for j in range(n - 1):
            divide_image[i, j, ...] = img_re[
                                      gy[i][j]:gy[i + 1][j + 1], gx[i][j]:gx[i + 1][j + 1], :]
    return divide_image

# 显示图片
def display_blocks(divide_image):
    m, n = divide_image.shape[0], divide_image.shape[1]
    num = 1
    for i in range(m):
        for j in range(n):
            plt.subplot(m, n, i * n + j + 1)
            plt.imshow(divide_image[i, j, :])
            plt.axis('off')
            # plt.imsave("{}/{}_{}.jpg".format(imgblock_dir,i,j), divide_image[i, j, :])
            plt.imsave("{}/{}.jpg".format(imgblock_dir,num), divide_image[i, j, :])
            print(num)
            num += 1
    plt.show()

if __name__ == "__main__":
    # --------------设置区域：
    img_name = "test2_out_8bit.bmp"
    imgblock_dir = './img_block'
    if not os.path.exists(imgblock_dir):
        os.makedirs(imgblock_dir)
    m = 6  # 行数
    n = 20  # 列数
    # --------------

    img = cv2.imread(img_name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # h, w = img.shape[0], img.shape[1]
    # fig1 = plt.figure('原始图像')
    # plt.imshow(img)
    # plt.axis('off')
    # plt.title('Original image')

    divide_image2 = divide_method2(img, m + 1, n + 1)  # 该函数中m+1和n+1表示网格点个数，m和n分别表示分块的块数
    # fig3 = plt.figure('分块后:图像缩放法')

    display_blocks(divide_image2)

    print("success")

