import os
import random
import subprocess
import math
import ImageTk
import PIL

import cv2
import numpy as np
import time
import arobot as aro
import socket,sys

import ColorDesciptor

__author__ = 'QQ860'

class Runner :

    __keepupdate = True
    method = 0
    time = 0
    scale = 2
    pic_saveName = 'screenshot.png'
    overPicPath = ''
    pic_savePath = os.getcwd()
    con_screenshot = 'screencap -p /sdcard/screenshot.png'
    con_pull = 'pull /sdcard/screenshot.png '+pic_savePath
    con_tap = 'input tap '

    img_start = 'start.png'
    img_over = 'over.png'
    img_overget = 'overget.png'
    img_restart = 'restart.png'

    huoshan_start = 'huoshan_start.png'
    huoshan_over = 'huoshan_over.png'
    huoshan_overget = 'huoshan_overget.png'
    huoshan_restart = 'huoshan_restart.png'
    huoshan_powererror = 'huoshan_powererror.png'
    huoshan_error = 'huoshan_error.png'

    aideng_start = 'aideng_start.png'
    aideng_over = 'aideng_over.png'
    aideng_overget = 'aideng_overget.png'
    aideng_restart = 'aideng_restart.png'
    aideng_powererror = 'aideng_powererror.png'
    aideng_error = 'aideng_error.png'


    ds = ''
    imglist = [img_start, img_over, img_overget, img_restart]
    huoshanlist = [huoshan_start, huoshan_over, huoshan_overget, huoshan_restart,huoshan_powererror, huoshan_error]
    aidenglist = [aideng_start, aideng_over, aideng_overget, aideng_restart,aideng_powererror, aideng_error]
    targetlist =[]
    targetFeature = {}

    def __init__(self, time, method):
        self.time = time
        self.method = method
        self.ds = ColorDesciptor.ColorDescriptor((8, 12, 3))
        if(method == 0):
            self.targetlist = self.imglist
        elif(method == 1):
            self.targetlist = self.huoshanlist
        elif(method == 2):
            self.targetlist = self.aidenglist
        for imgName in self.targetlist:
            print(imgName)
            self.targetFeature[imgName] = self.ds.describe(self.getLocalPic(imgName))
        try:
            os.remove(self.pic_savePath+'/'+self.pic_saveName)
        except WindowsError:
            pass

    def moli_run(self):
        timestart = 0
        alltimestart = time.time()
        while(self.time>0) :
            pic = self.getGamePic()
            pic_feature = self.ds.describe(pic)
            # show_pic = self.resizePic(pic, 90, 0.5)
            if(self.comparePic(pic_feature,self.img_start)):
                print('start game....')
                com  = self.con_tap+self.getPotStr(1000,1150, 470, 540)
                self.time -= 1
                aro.adbshellcommand(com)
                timestart = time.time()
                time.sleep(random.uniform(0.5, 1))
            if( self.comparePic(pic_feature, self.img_over)):
                print('over....')
                com  = self.con_tap+self.getPotStr(100, 1000, 100, 600)
                aro.adbshellcommand(com)
                time.sleep(random.uniform(0.5, 1))
                com  = self.con_tap+self.getPotStr(100, 1000, 100, 600)
                aro.adbshellcommand(com)
                time.sleep(random.uniform(0.5, 1))
                print('overGet....')
                com  = self.con_tap+self.getPotStr(580, 700, 520, 580)
                aro.adbshellcommand(com)
                time.sleep(random.uniform(0.5, 1))
                print('restart....')
                com  = self.con_tap+self.getPotStr(250, 560, 360, 420)
                aro.adbshellcommand(com)
                print('use time:'+str(time.time() - timestart))
                time.sleep(random.uniform(0.5, 1))
        print('end....time spend:'+str(time.time() - alltimestart))

    def huoshan_run(self):
        timestart = 0
        alltimestart = time.time()
        while(self.time>0) :
            pic = self.getGamePic()
            pic_feature = self.ds.describe(pic)
            # show_pic = self.resizePic(pic, 90, 0.5)
            status = self.comparePic(pic_feature)
            if(status == self.targetlist[0]):
                print('start game....')
                timestart = time.time()
                com  = self.con_tap+self.getPotStr(1000,1150, 470, 540)
                self.time -= 1
                aro.adbshellcommand(com)
                time.sleep(random.uniform(0.5, 1))
                time.sleep(10)
            elif(status == self.targetlist[1]):
                print('over....')
                com  = self.con_tap+self.getPotStr(100, 1000, 100, 600)
                aro.adbshellcommand(com)
                time.sleep(random.uniform(0.3, 0.5))
                com  = self.con_tap+self.getPotStr(100, 1000, 100, 600)
                aro.adbshellcommand(com)
                time.sleep(random.uniform(0.3, 0.5))
            elif(status == self.targetlist[2]):
                print('overGet....')
                com  = self.con_tap+self.getPotStr(460, 610, 550, 610)
                aro.adbshellcommand(com)
                time.sleep(random.uniform(0.3, 0.5))
                getAgain = self.getGamePic()
                pic_feature = self.ds.describe(getAgain)
                status = self.comparePic(pic_feature)
                if(status == self.targetlist[2]):
                    print('get again....')
                    com  = self.con_tap+self.getPotStr(860, 868, 190, 198)
                    aro.adbshellcommand(com)
                    time.sleep(random.uniform(0.3, 0.5))

            elif(status == self.targetlist[4]):
                print('power error....')
                com  = self.con_tap+self.getPotStr(450, 600, 400, 460)
                aro.adbshellcommand(com)
                time.sleep(random.uniform(0.8, 1))
                com  = self.con_tap+self.getPotStr(250, 460, 270, 480)
                aro.adbshellcommand(com)
                time.sleep(random.uniform(0.8, 1))
                com  = self.con_tap+self.getPotStr(450, 600, 400, 460)
                aro.adbshellcommand(com)
                time.sleep(1)
                com  = self.con_tap+self.getPotStr(520, 710, 400, 460)
                aro.adbshellcommand(com)
                time.sleep(random.uniform(0.8, 1))
                com  = self.con_tap+self.getPotStr(570, 700, 585, 645)
                aro.adbshellcommand(com)
                time.sleep(random.uniform(0.5, 1))
            elif(status == self.targetlist[5]):
                print('huoshan error...')
                com  = self.con_tap+self.getPotStr(710, 940, 430, 490)
                aro.adbshellcommand(com)
                time.sleep(random.uniform(0.5, 1))
                com  = self.con_tap+self.getPotStr(100, 1000, 100, 600)
                aro.adbshellcommand(com)
                time.sleep(random.uniform(0.5, 1))
                print('restart....')
                com  = self.con_tap+self.getPotStr(250, 560, 360, 420)
                aro.adbshellcommand(com)
                print('use time:'+str(time.time() - timestart))
                time.sleep(random.uniform(0.5, 1))
            elif(status == self.targetlist[3]):
                print('restart....')
                com  = self.con_tap+self.getPotStr(250, 560, 360, 420)
                aro.adbshellcommand(com)
                print('use time:'+str(time.time() - timestart))
                print(str(self.time)+' times left')
                time.sleep(random.uniform(0.3, 0.5))

        print('end....time spend:'+str(time.time() - alltimestart))

    def getPotStr(self, xstart,xend,ystart, yend):
        x = random.randint(xstart, xend)
        y = random.randint(ystart, yend)
        return ' '+str(x)+' '+str(y)

    def getGamePic(self):
        self.__keepupdate = True
        self.updatelcd_sock()
        return cv2.imread(self.pic_savePath+'/'+self.pic_saveName)

    def getLocalPic(self, name):
        return cv2.imread(self.pic_savePath+'/'+name)


    def comparePic(self, pic_feature):
        cmpareRes = {}
        status = ''
        minValue = 100
        for (k,v) in self.targetFeature.items():
            cmpareRes[k] = self.chi2_distance(pic_feature,v)
        for ck, cv in cmpareRes.items():
            if (cv < minValue) :
                minValue = cv
                status = ck
        print(status+':'+str(minValue))
        if(minValue < 2.0):
            return status
        return 'null'

    def chi2_distance(self, histA, histB, eps=1e-10):
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
                      for (a, b) in zip(histA, histB)])
        # return the chi-squared distance
        return d

    # Read adb response, if 'OKAY' turn true
    def readAdbResponse(self,s):
        if s != None:
            resp = s.recv(4)
        if len(resp) != 4:
            print 'protocol fault (no status)'
            return False

        if resp == 'OKAY':
            return True
        elif resp == 'FAIL':
            resp = s.recv(4)
            if len(resp) < 4:
                print 'protocol fault (status len)'
                return False
            else:
                length = int(resp, 16)
                resp = s.recv(length)
                if len(resp) != length:
                    print 'protocol fault (status read)'
                    return False
                else:
                    print resp
                    return False
        else:
            print "protocol fault (status %02x %02x %02x %02x?!)", (resp[0], resp[1], resp[2], resp[3])
            return False

        return False

    # Convert buffer to Int
    def getInt(self, tbuf = None):
        if (tbuf != None):
            if len(tbuf) < 4:
                print 'buff len < 4'
                return 0
            else:
                intnum = tbuf[0]
                intnum = intnum + tbuf[1]*0x100
                intnum = intnum + tbuf[2]*0x10000
                intnum = intnum + tbuf[3]*0x1000000
                return intnum
        else:
            return 0

    # Parse fb header from buffer
    def readHeader(self, tfb, ver, buf):
        if ver == 16:
            tfb.fb_bpp = 16
            tfb.fb_size = self.getInt(buf[0:4])
            tfb.fb_width = self.getInt(buf[4:8])
            tfb.fb_height = self.getInt(buf[8:12])
            tfb.red_offset = 11
            tfb.red_length = 5
            tfb.blue_offset = 5
            tfb.blue_length = 6
            tfb.green_offset = 0
            tfb.green_length = 5
            tfb.alpha_offset = 0
            tfb.alpha_length = 0
        elif ver == 1:
            tfb.fb_bpp = self.getInt(bytearray(buf[0:4]))
            tfb.fb_size = self.getInt(bytearray(buf[4:8]))
            tfb.fb_width = self.getInt(bytearray(buf[8:12]))
            tfb.fb_height = self.getInt(bytearray(buf[12:16]))
            tfb.red_offset = self.getInt(bytearray(buf[16:20]))
            tfb.red_length = self.getInt(bytearray(buf[20:24]))
            tfb.blue_offset = self.getInt(bytearray(buf[24:28]))
            tfb.blue_length = self.getInt(bytearray(buf[28:32]))
            tfb.green_offset = self.getInt(bytearray(buf[32:36]))
            tfb.green_length = self.getInt(bytearray(buf[36:40]))
            tfb.alpha_offset = self.getInt(bytearray(buf[40:44]))
            tfb.alpha_length = self.getInt(bytearray(buf[44:48]))
        else:
            return False
        return True

    # screen capture via socket from adb server
    def updatelcd_sock(self):

        dev_sn = ''
        myfb = fb()

        while self.__keepupdate:
            # Get device SerialNumber from ADB server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect(('127.0.0.1', 5037))
            except:
                os.system('adb start-server')
                time.sleep(2)
                continue

            req_msg = 'host:devices'
            s.sendall('%04x' % len(req_msg))
            s.sendall(req_msg)
            if self.readAdbResponse(s):
                len_str = s.recv(4)
                if len(len_str) < 4:
                    continue
                length = int(len_str, 16)
                dev_info = s.recv(length)
                if '\t' in dev_info:
                    dev_sn = dev_info[0:dev_info.index('\t')]
                else:
                    dev_sn = ''
            s.recv(1024) # receive all rest data
            s.close()

            if dev_sn == '':
                continue

            # Get framebuffer from ADB server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', 5037))
            req_msg = 'host:transport:%s' % dev_sn
            s.sendall('%04x' % len(req_msg))
            s.sendall(req_msg)
            if not self.readAdbResponse(s):
                s.close()
            else:
                req_msg = 'framebuffer:'
                s.sendall('%04x' % len(req_msg))
                s.sendall(req_msg)
                if not self.readAdbResponse(s):
                    s.close()
                else:
                    reply = s.recv(4)
                    if len(reply) < 4:
                        continue

                    fbver = ord(reply[0]) + \
                            ord(reply[1]) * 0x100 + \
                            ord(reply[2]) * 0x10000 + \
                            ord(reply[3]) * 0x1000000

                    # Get fb header size
                    if fbver == 16:
                        hdrsize = 3
                    elif fbver == 1:
                        hdrsize = 12
                    else:
                        hdrsize = 0;
                    # read the header
                    header = s.recv(hdrsize * 4)
                    if len(header) < (hdrsize * 4):
                        continue
                    self.readHeader(myfb, fbver, header)

                    # read fb buffer
                    rcvcnt = 0
                    readbyte = 0
                    imagebuff = []
                    while True:
                        if (rcvcnt < myfb.fb_size):
                            readbyte = myfb.fb_size - rcvcnt
                        else:
                            break
                        resp = s.recv(readbyte)
                        rcvcnt = rcvcnt + len(resp);
                        imagebuff.extend(resp)
                        if len(resp) == 0:
                            break

                    reply = s.recv(10)
                    s.close()
                    myfb.fb_data = bytearray(imagebuff)

                    if len(imagebuff) < myfb.fb_size:
                        continue

                    # convert raw-rgb to image
                    image = PIL.Image.frombuffer('RGBA',
                                             (myfb.fb_width, myfb.fb_height),
                                             myfb.fb_data,
                                             'raw',
                                             'RGBA',
                                             0,
                                             1)
                    try:
                            # save image to local path
                            image.save(self.pic_savePath+'/'+self.pic_saveName, format='PNG')
                            self.__keepupdate =False
                            s.close()
                    except:
                            continue

    def resizePic(self, pic, angle, scale=1):
        h, w = pic.shape[:2]
        rangle = np.deg2rad(angle)  # angle in radians
        nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
        nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
        rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
        rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5,0]))
        rot_mat[0,2] += rot_move[0]
        rot_mat[1,2] += rot_move[1]
        return cv2.warpAffine(pic, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4)

# Framebuffer Class
# Only record framebuffer attributs
class fb:
        fb_bpp = 0
        fb_size = 0
        fb_width = 0
        fb_height = 0
        red_offset = 0
        red_length = 0
        blue_offset = 0
        blue_length = 0
        green_offset = 0
        green_length = 0
        alpha_offset = 0
        alpha_length = 0
        fb_data = None

        def __init__(self):
            fb_bpp = 0
            fb_size = 0
            fb_width = 0
            fb_height = 0
            red_offset = 0
            red_length = 0
            blue_offset = 0
            blue_length = 0
            green_offset = 0
            green_length = 0
            alpha_offset = 0
            alpha_length = 0
            fb_data = None