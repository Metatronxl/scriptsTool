#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019-03-27
# @Author : lei.X
# python2.7


# TODO 添加日志系统


from multiprocessing import Pool
import os
import sys
import subprocess
import time

cur_path = os.getcwd()
is_shell = True


reinstallFlag = 1


def run_shell():
    print "脚本名：", sys.argv[0]
    if downloadApkFile(sys.argv[1]) == 0:
        print "download success!"
    else:
        print "download error"

    #开始并发安装apk文件
    install_all_apk("~/Desktop/preInstall.apk",sys.argv[2])




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
    print devicenum_list
    return devicenum_list

# 获取最新的apk文件
def downloadApkFile(apkAddr):
    print "start download newest apk file"
    abd_proc = subprocess.Popen("curl -w  downloadApk -o ~/Desktop/preInstall.apk -O "+apkAddr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    print abd_proc
    (__output,__error) = abd_proc.communicate()
    if __output and __output.find("downloadApk") != -1:
        print "download apk file successfully"
        return 0
    print "download apk file unsuccessfully"
    return 1

# 卸载旧apk文件,安装新apk文件
def install_apk(device_num, apk_file,old_apk_file):

    # 卸载旧apk文件
    global reinstallFlag
    try:
        print "device %s start uninstalling %s" % (device_num, old_apk_file)
        adb_proc = subprocess.Popen("adb -s " + device_num + " uninstall " + old_apk_file, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        (__output, __error) = adb_proc.communicate()
        if __output and __output.find("Success") != -1:
            print "device: %s uninstall %s successfully" % (device_num,old_apk_file)
    except Exception as e :
        print "uninstall App error ，reason：doesn't exist such app："+ e.message

    # 安装新apk文件
    try:
        print "device %s start installing %s"  % (device_num,apk_file)
        adb_proc = subprocess.Popen("adb -s "+device_num+" install "+ apk_file, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        (__output, __error) = adb_proc.communicate()
        if __output and __output.find("Success") != -1:
            print "device: %s install successfully" % device_num
            return 0
        print "device: %s install unsuccessfully" % device_num
        # flag重置为1
        reinstallFlag = 1
        return 1
    except Exception as e:
        print "error message："+ e.message
        reinstallFlag +=1
        if  reinstallFlag < 4:
            time.sleep(5)
            print "reinstall app : (%s) times" % reinstallFlag
            install_apk(device_num,apk_file,old_apk_file)
        print "can't install apk file , process done :("



def install_all_apk(apk_file,old_apk_file):
    device_list = get_devicenum()
    p = Pool()
    for device_num in device_list:
        p.apply_async(install_apk,args=(device_num,apk_file,old_apk_file,))
    print "Waiting for all subprocess done..."
    p.close()
    p.join()
    print 'All subprocesses done.'


if __name__ == '__main__':
    # run_shell()

    #开始并发安装apk文件
    install_all_apk("~/Desktop/preInstall.apk","com.dianping.v1")


