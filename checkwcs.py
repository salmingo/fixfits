#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
校验astrometry-net与蒋兆基程序天文定位参数的关系
1. 样本
来源: 50BiN
原始文件: N2169150207V0001.fit
astrometry-net处理结果: tN2169150207V0001.new. 前置操作: 过图像中心X轴镜像
蒋兆基处理结果:          pN2169150207V0001.fit

2. 采样数据
  X    Y    RA(1)      DEC(1)     RA(2)      DEC(2)
1077 1139  90.274125  23.338742  90.274200  23.338644
 565  661  90.363400  23.262019  90.363454  23.261908
1880  679  90.133967  23.265056  90.134004  23.264958

3. 参数
Astrometry-net
CRPIX1   X轴参考原点, 量纲: 像元
CRPIX2   Y轴参考原点
CRVAL1   RA参考原点, 量纲: 角度
CRVAL2   DEC参考原点
CD1_1    RA, 转换矩阵系数
CD1_2    RA, 转换矩阵系数
CD2_1    DEC, 转换矩阵系数
CD2_2    DEC, 转换矩阵系数
A_0_0    X轴改正系数
A_0_1    X轴改正系数
A_0_2    X轴改正系数
A_1_0    X轴改正系数
A_1_1    X轴改正系数
A_2_0    X轴改正系数
B_0_0    Y轴改正系数
B_0_1    Y轴改正系数
B_0_2    Y轴改正系数
B_1_0    Y轴改正系数
B_1_1    Y轴改正系数
B_2_0    Y轴改正系数

蒋兆基程序
CRPIX1   X轴参考原点, 量纲: 像元
CRPIX2   Y轴参考原点
CRVAL1   RA参考原点, 量纲: 角度
CRVAL2   DEC参考原点
CDELT1   ?
CDELT2   ?
CROTA2   ?
A81-A86  ?
A87      ? RA, 量纲: 弧度
A88      ? DEC, 量纲: 弧度

'''
import pyfits
from astropy.wcs import WCS;
from astropy.io import fits;

def coordinates1(pathname, x, y):
    '''
    使用astrometry-net参数, 计算[x,y]对应的赤道坐标
    '''
    hdu = pyfits.open(pathname)
    header = hdu[0].header;
    ra0  = header['CRVAL1'];
    dec0 = header['CRVAL2'];
    x0   = header['CRPIX1'];
    y0   = header['CRPIX2'];
    cd11 = header['CD1_1'];
    cd12 = header['CD1_2'];
    cd21 = header['CD2_1'];
    cd22 = header['CD2_2'];
    a00  = header['A_0_0'];
    a01  = header['A_0_1'];
    a02  = header['A_0_2'];
    a10  = header['A_1_0'];
    a11  = header['A_1_1'];
    a20  = header['A_2_0'];
    b00  = header['B_0_0'];
    b01  = header['B_0_1'];
    b02  = header['B_0_2'];
    b10  = header['B_1_0'];
    b11  = header['B_1_1'];
    b20  = header['B_2_0'];

    u0 = x - x0;
    v0 = y - y0;
    du = a00 + a01 * v0 + a02 * v0 * v0 + a10 * u0 + a11 * u0 * v0 + a20 * u0 * u0;
    dv = b00 + b01 * v0 + b02 * v0 * v0 + b10 * u0 + b11 * u0 * v0 + b20 * u0 * u0;
    u = u0 + du;
    v = v0 + dv;
    ra = ra0 + cd11 * u + cd12 * v;
    dec= dec0 + cd21 * u + cd22 * v;
    return [ra, dec];

def coordinates1_astropy(pathname, x, y):
    '''
    使用astropy.wcs, 计算[x,y]对应的赤道坐标
    '''
    w = WCS(pathname);
    print(w.wcs.name);
#    w.wcs.print_contents();

def coordinates2(pathname, x, y):
    '''
    使用Jiang参数, 计算[x,y]对应的赤道坐标
    '''
    hdu = pyfits.open(pathname)
    header = hdu[0].header;
    ra0  = header['CRVAL1'];
    dec0 = header['CRVAL2'];
    x0   = header['CRPIX1'];
    y0   = header['CRPIX2'];

#-----------------------------------------------------------------------------#
# 主函数
if __name__ == '__main__':
#     x = [1077, 565, 1880];
#     y = [1139, 661, 679];
#     ra1  = [90.274125, 90.363400, 90.133967];
#     dec1 = [23.338742, 23.262019, 23.265056];
#     ra2  = [90.274200, 90.363454, 90.134004];
#     dec2 = [23.338644, 23.261908, 23.264958];
#     n = len(x);
# 
#     coordinates1_astropy('/Users/lxm/data/50BiN/tN2169150207V0001.new', x[0], y[0]);
#     
#     print "astrometry-net result:"
#     for i in range(n):
#         [ra, dec] = coordinates1('/Users/lxm/data/50BiN/tN2169150207V0001.new', x[i], y[i]);
#         print "x = %4d, y = %4d, ra0 = %10.6f, dec0 = %10.6f ==> %10.6f, %10.6f" % (x[i], y[i], ra1[i], dec1[i], ra, dec);
    
    # print "Jiang result:"
    # for i in range(n):
    #     [ra, dec] = coordinates1('/Users/lxm/data/50BiN/tN2169150207V0001.new', x[i], y[i]);
    #     print "x = %4d, y = %4d, ra0 = %10.6f, dec0 = %10.6f ==> %10.6f, %10.6f" % (x[i], y[i], ra1[i], dec1[i], ra, dec);
    
# ccmap parameters ==> WCS
    