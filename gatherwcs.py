#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
检索目录下所有以wcs结尾文件, 从文件头收集信息汇总为一个txt文件
KEYWORD  |  Description
CRVAL1
CRVAL2
CRPIX1
CRPIX2
CD1_1
CD1_2
CD2_1
CD2_2
IMAGEW
IMAGEH
A_ORDER
A_0_0
A_0_1
A_0_2
A_1_0
A_1_1
A_2_0
B_ORDER
B_0_0
B_0_1
B_0_2
B_1_0
B_1_1
B_2_0
'''
import math
import sys
import os

D2R = math.pi / 180.0;   # 系数: 角度转换为弧度
R2D = 180.0 / math.pi;   # 系数: 角度转换为弧度
AS2R = math.pi / 648000; # 系数: 角秒转换为弧度
R2AS = 648000 / math.pi; # 系数: 弧度转换为角秒
AS2D = 1.0 / 3600.0;     # 系数: 角秒转换为角度
D2AS = 3600.0;           # 系数: 角度转换为角秒

def read_wcs(filepath):
    '''
    从WCS文件头中读取参数项
    '''

#-----------------------------------------------------------------------------#
# 主函数
# 命令行参数:
# 参数1: x
# 参数2: y
# 参数无效时直接退出
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: gatherwcs <directory name>";
        sys.exit(1);

    # 目录名称, 检查该目录下所有wcs文件, 并将提前信息存储为result.txt
    pathroot = sys.argv[1];
    fd = open("result.txt", 'w');
    
    # 遍历目录
    for filename in os.listdir(pathroot):
        filepath = os.path.join(pathroot, filename);
        if os.path.isfile(filepath):
            name, ext = os.path.splitext(filename);
            if ext == ".wcs":
                print filename;
                read_wcs(filepath);
    
    # 退出, 关闭文件            
    fd.close();
    