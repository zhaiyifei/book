#coding=utf-8
"""工具模块"""
import os
import imghdr
import shutil

def replace_img():
    '''替换不正常图片为默认封面图片'''
    #封面图片文件夹
    base_path = os.getcwd().split('ESBook')[0]
    file_path = r'ESBook\data\img'
    fengmian_path = r'ESBook\data\img_fengmian\fengmian.gif'
    img_file = ''.join([base_path,file_path])
    #print img_file
    #默认封面图片
    fengmiam_img = ''.join([base_path,fengmian_path])
    img_name_list = os.listdir(img_file)
    #print img_name_list
    for img_name in img_name_list:
        #拼接成完整图片绝对路径
        img_path = os.path.join(img_file,img_name)
        #判断图片文件是否为真实图片类型文件
        if not imghdr.what(img_path):
            print img_path
            #将不是图片文件的文件替换为默认封面图片文件
            shutil.copyfile(fengmiam_img,img_path)

#replace_img()

