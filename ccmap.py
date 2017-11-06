#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
校验ccmap参数与WCS关系
'''
import sys;
import math;
from setuptools.command.easy_install import sys_executable

D2R = math.pi / 180.0;   # 系数: 角度转换为弧度
R2D = 180.0 / math.pi;   # 系数: 角度转换为弧度
AS2R = math.pi / 648000; # 系数: 角秒转换为弧度
R2AS = 648000 / math.pi; # 系数: 弧度转换为角秒
AS2D = 1.0 / 3600.0;     # 系数: 角秒转换为角度
D2AS = 3600.0;           # 系数: 角度转换为角秒

def Hour2HMS(hour):
    # 小时数转换为时分秒
    h = int(hour);
    m = int((hour - h) * 60);
    s = ((hour - h) * 60 - m) * 60;
    return [h, m, s];

def Degree2DMS(degree):
    # 角度转换为度分秒
    ch = '+';
    if degree < 0:
        ch = '-';
        degree = -degree;
    d = int(degree);
    m = int((degree - d) * 60);
    s = ((degree - d) * 60 - m) * 60;
    return [ch, d, m, s];

def Hour2String(hour):
    # 小时数转换为字符串
    # 字符串格式: hh:mm:ss.sss
    [h, m, s] = Hour2HMS(hour);
    astr = "%02d:%02d:%06.3f" % (h, m, s);
    return astr;

def Degree2String(degree):
    # 角度转换为字符串
    # 字符串格式: +/-dd:mm:ss.ss
    # 角度有效区间: [-90, +90]
    [ch, d, m, s] = Degree2DMS(degree);
    astr = "%c%02d:%02d:%05.2f" % (ch, d, m, s);
    return astr;

def PolyvalLegendre(order, x):
    # 计算各阶勒让德多项式的数值
    # order: 阶次
    # x    : 参数
    vals = [];
    if order >= 0:
        vals[0] = 1;
    if order >= 1:
        vals[1] = x;
    i = 2;
    while i < order:
        vals[i] = ((i + i - 1) * x * vals[i - 1] - (i - 1) * vals[i - 2]) / i;
        i = i + 1;

    return vals;
    
#-----------------------------------------------------------------------------#

# 主函数
# 命令行参数:
# 参数1: x
# 参数2: y
# 参数无效时直接退出
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: ccmap.py x y";
        sys.exit(1);

# 图像上的位置
    x = float(sys.argv[1]);
    y = float(sys.argv[2]);
    
# ccmap参数
# 图像坐标系参考点:
    x0 = 318.7352667484295;
    y0 = 273.9002619912411;
# 赤道坐标系参考点:
    ra0 = 202.4505358333334 * D2R;
    dc0 = 47.19815944444444 * D2R;
# ccmap转换到WCS的参数
    xmag = 0.7641733802338992 * AS2R;
    ymag = 0.7666917500560622 * AS2R;
    xrot = 179.1101291109185 * D2R;
    yrot = 358.9582148846163 * D2R;
# 勒让德多项式系数
# !!!系数数量不对: May 13, 2017
#     xorder = 6;
#     yorder = 6;
#     xmin = 500;
#     ymin = 500;
#     xmax = 2500;
#     ymax = 2500;
#     xnorm = (2 * x - (xmin + xmax)) / (xmax - xmin);
#     ynorm = (2 * y - (ymin + ymax)) / (ymax - ymin);
#     
# 系数存储方法???
#           C:0                    C:1                C:2                C:3                C:4                C:5
# cx = [
#      23.18301671500937,   20.2847141033123,    5.325058254315411, 7.107466240056687, -1.343243076617115, 0.9328821499036877, #R:0
#      -7.642813034353698, 259.2451702060431,  -38.45415356131686,  3.750757200515437, -5.110906928159874,                     #R:1
#      91.19727293750415,   21.53286097882785,  10.72059728506646, 26.26828493535132,                                          #R:2
#     -26.04054640934361,  -14.3802316915378,  -29.85336200404276,                                                             #R:3
#       5.303950860525123,  20.47722854389625,                                                                                 #R:4   
#      -5.652200973765149                                                                                                      #R:5       
#     ];
# cy = [
#     -28.39633240196996, 10.87921617816398, -154.5234456985481, 15.02015569518595, -5.155096240450269,
#      -7.929206648947201,-10.53389253990319,-201.3339834325921,-63.76085216600836,-25.5079537115036,
#      19.11761171605442,35.16691653829372, 126.8430963895821, 72.77873293093621, 53.21206429753116,
#     -46.47511904700531, -78.08589157128089, -94.32910120969898, 17.25951308060848, 66.42829891976345,
#     -18.9475944164496
#     ];

# 与ccsetwcs对照, (xrot, yrot)需变更为(-xrot, -yrot)方能一致
# 原因(??): 主动旋转与被动旋转; 坐标原点
# May 13, 2017
    xrot = -xrot;
    yrot = -yrot;

# 计算旋转矩阵
    cd1_1 = xmag * math.cos(xrot);
    cd1_2 = -ymag * math.sin(yrot);
    cd2_1 = xmag * math.sin(xrot);
    cd2_2 = ymag * math.cos(yrot);
    
# 显示旋转矩阵
#     print "CD1_1 = %+.15E" % cd1_1 * R2D;
#     print "CD1_2 = %+.15E" % cd1_2 * R2D;
#     print "CD2_1 = %+.15E" % cd2_1 * R2D;
#     print "CD2_2 = %+.15E" % cd2_2 * R2D;

# 图像坐标(x,y)相对(x0,y0)的位移
    dx = x - x0;
    dy = y - y0;
# 投影变换
    xi = cd1_1 * dx + cd1_2 * dy;
    eta= cd2_1 * dx + cd2_2 * dy;
    dr = math.atan2(xi / math.cos(dc0), 1 - eta * math.tan(dc0));
    ra = ra0 + dr;
    dc = math.atan2((eta + math.tan(dc0)) * math.cos(dr), 1 - eta * math.tan(dc0)); 
# 量纲转换
    ra = ra * R2D / 15.0; # 转换为小时
    dc = dc * R2D;        # 转换为角度
# 输出转换结果
    print "(x, y): (%7.2f, %7.2f) ==> (α, δ): (%s, %s)" % (x, y, Hour2String(ra), Degree2String(dc));
    