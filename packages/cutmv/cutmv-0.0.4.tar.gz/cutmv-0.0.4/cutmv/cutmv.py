#!/usr/bin/python
# -*-coding:utf-8 -*-
"""
-------------- Description: ------------------
   FileName : 此模块调用ffmpeg分割视频.py
   Author : 绒毛宝贝
   ProjectName : PyBoard
   IDE Version : PyCharm
   Date:2020/12/10 23:36
   QQ:287000822 E-mail: gomehome@qq.com
------------------- END ----------------------
"""
__author__ = 'Isaac'

import os


def video_compress(load_path, out_path, bits):
    rootdir = load_path
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in list:
        cmd = 'ffmpeg -i ' + i + ' -b ' + bits + ' ' + out_path + '压制' + bits + '_' + i
        os.system(cmd)


def video_cut(s_time, e_time, files, i_format):
    i = 0
    set_time = s_time
    end_time = e_time

    cmd = 'ffprobe -i ' + files + ' -show_entries format=duration -v quiet -of csv="p=0"'
    f = os.popen(cmd, 'r')

    math = f.read()
    gi = int('%01.f' % float(math))

    while True:
        if set_time >= gi:
            break
        else:
            cmd = 'ffmpeg -ss ' + str(set_time) + ' -i ' + files + ' -c copy -t ' + str(
                end_time) + ' ' + files + '_剪辑' + str(i) + i_format
            set_time = set_time + end_time
            i = i + 1
            os.system(cmd)
