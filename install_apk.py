#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-03-27
# @Author : lei.X


from multiprocessing import Pool
import os
import sys
import subprocess

cur_path = os.getcwd()
is_shell = True


def run_shell():
    print ("脚本名：", sys.argv[0])
    if downloadApkFile(sys.argv[1]) == 0:
        print ("download success!")
    else:
        print ("download error")

    #开始并发安装apk文件
    install_all_apk("~/Desktop/preInstall.apk")




# 获取所有的连接设备
def get_devicenum():
    devicenum_list=[]
    if sys.platform == 'darwin' or sys.platform == 'linux2':
        is_shell = True
        split_code = "\n"
    else:
        is_shell = False
        split_code = "\r\n"
    adb_proc = subprocess.Popen("adb devices", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=is_shell)
    (__output, __error) = adb_proc.communicate()
    if not __output:
        return devicenum_list
    output_list = __output.split(split_code)
    for line in  output_list:
        line_list = line.split("	")
        if len(line_list) == 2:
            devicenum_list.append(line_list[0])
    return devicenum_list

# 获取最新的apk文件
def downloadApkFile(apkAddr):

    abd_proc = subprocess.Popen("curl -w  downloadApk -o ~/Desktop/preInstall.apk -O "+apkAddr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (__output,__error) = abd_proc.communicate()
    if __output and __output.find("downloadApk") != -1:
        return 0
    return 1

# 安装apk文件
def install_apk(device_num, apk_file):
    for i in range(3):
        adb_proc = subprocess.Popen("adb -s "+device_num+" install -r "+ apk_file, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        (__output, __error) = adb_proc.communicate()
        if __output and __output.find("Success") != -1:
            print ("device: %s install successfully" % device_num)
            return 0
    print ("device: %s install unsuccessfully" % device_num)
    return 1


def install_all_apk(apk_file):
    device_list = get_devicenum()
    p = Pool()
    for device_num in device_list:
        p.apply_async(install_apk,args=(device_num,apk_file,))
    print ("Waiting for all subprocess done...")
    p.close()
    p.join()
    print ('All subprocesses done.')


if __name__ == '__main__':
    run_shell()



