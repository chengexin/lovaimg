# coding:utf-8
import os
import re
import time

import cv2
import query_lovetalk
import random
from PIL import ImageDraw, ImageFont, Image

"""
1.随机选择图片
2.剪裁图片 返回图片 X,Y
3.获取土味情书
4.格式化土味情书
5.根据情书长短，计算留白空间
"""


# 创建背景图
# 传入创建背景图像素参数
def get_background(x, y):
    # 创建一张照片，大小为1100*1100 单位像素，颜色为白色
    img = Image.new('RGBA', (x, y), (255, 255, 255))
    img = img.convert("RGB")
    background = ('.\\process\\' + "background.jpg")
    img.save(background)
    return background


# 剪裁图片
# 以图片中心开始按比例剪裁
def get_foreground(picture_path):
    # 打开图片
    img = Image.open(picture_path)
    # 获取图片分辨率
    x, y = img.size
    # 图片分辨率大于1000，按1000，小于1000按最小的边像素
    if (x > 1000) and (y > 1000):
        # 获取X中间点，
        center_x = int(x / 2)
        # 获取y中间点
        center_y = int(y / 2)
        img = cv2.imread(picture_path)
        # x,y中间点加减500
        y0 = center_y - 500
        y1 = center_y + 500
        x0 = center_x - 500
        x1 = center_x + 500
        cropped = img[y0:y1, x0:x1]  # 裁剪坐标为[y0:y1, x0:x1]
        # 获得剪裁后尺寸
        # 保存图片
        # 获取剪裁后图片尺寸
        x = x1 - x0
        y = y1 - y0
        foreground = ('.\\process\\' + "foreground.jpg")
        cv2.imwrite(foreground, cropped)
    if y < x:
        # 获取X中间点，
        center_x = int(x / 2)
        # 获取y中间点
        center_y = int(y / 2)
        img = cv2.imread(picture_path)
        y0 = center_y - int(y / 2)
        y1 = center_y + int(y / 2)
        x0 = center_x - int(y / 2)
        x1 = center_x + int(y / 2)
        cropped = img[y0: y1, x0:x1]  # 裁剪坐标为[y0:y1, x0:x1]
        y = y1 - y0
        x = y
        foreground = ('.\\process\\' + "foreground.jpg")
        cv2.imwrite(foreground, cropped)
    if y > x:
        # 获取X中间点，
        center_x = int(x / 2)
        # 获取y中间点
        center_y = int(y / 2)
        img = cv2.imread(picture_path)
        y0 = center_y - int(x / 2)
        y1 = center_y + int(x / 2)
        x0 = center_x - int(x / 2)
        x1 = center_x + int(x / 2)
        cropped = img[y0: y1, x0:x1]  # 裁剪坐标为[y0:y1, x0:x1]
        x = x1 - x0
        y = x
        foreground = ('.\\process\\' + "foreground.jpg")
        cv2.imwrite(foreground, cropped)
    return foreground, x, y


# 两图片叠加
def get_overlay_img(background, foreground):
    background_image = Image.open(background)
    foregroun_image = Image.open(foreground)
    # (25,25) 叠加起始像素位置
    background_image.paste(foregroun_image, (25, 25))
    overlay_img = ('.\\process\\' + "overlay_img.jpg")
    background_image.save(overlay_img)
    return overlay_img


# ('需要添加文字的图片路径','文字','文字离左边缘距离','文字离上边缘距离','文字颜色','文字大小')
def image_add_text(img_path, text, left, top, text_color, text_size):
    img = Image.open(img_path)
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    fontStyle = ImageFont.truetype("SourceHanSansCN-Medium.otf", text_size, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, text_color, font=fontStyle)
    img_name = get_time() + '.jpg'
    img.save(r'.\\result\\' + img_name)
    return r'.\\result\\' + img_name


# 获取时间
def get_time():
    ticks = time.time()
    now = time.strftime('%y%m%d%H%M%S')
    return now


# 去除字符串的标点符号，替换为换行符
def replace_all_blank(value):
    """
    去除value中的所有非字母内容，包括标点符号、空格、换行、下划线等
    :param value: 需要处理的内容
    :return: 返回处理后的内容
    """
    # \W 表示匹配非数字字母下划线
    result = re.sub('\W+', '\n\n', value).replace("_", '\n\n')
    # print(result[0:3])
    if result[0:2] == '\n\n':
        result = result[2:]
    if result[-2:len(result)] == '\n\n':
        result = result[0:-2]
    # 获取行数
    row = result.count('\n\n') + 1
    return result, row


def get_love_picture(love_talk, foreground_path):
    text, row = replace_all_blank(love_talk)
    foreground, x, y = get_foreground(foreground_path)
    # 计算背景图的大小x,y
    x0 = x + 50
    y0 = y + 70 + (int(row) * 85)
    background = get_background(x0, y0)
    # 叠加背景图与前景图
    overlay_img = get_overlay_img(background, foreground)
    # 计算文字添加位置
    left = 30
    top = y + 60
    # 添加文字
    ptcture_name = image_add_text(overlay_img, text, left, top, (102, 102, 102), 45)
    ptcture_name = os.path.abspath(ptcture_name)
    print('图片已生成......')
    return ptcture_name


if __name__ == '__main__':
    path = os.listdir(r'.\picture\\')
    picture = random.sample(path, 1)[0]
    get_love_picture(query_lovetalk.love(), r'.\picture\\' + picture)
