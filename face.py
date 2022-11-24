# Face recognition with LBP descriptors.
# See Timo Ahonen's "Face Recognition with Local Binary Patterns".
#
# Before running the example:
# 1) Download the AT&T faces database http://www.cl.cam.ac.uk/Research/DTG/attarchive/pub/data/att_faces.zip
# 2) Exract and copy the orl_faces directory to the SD card root.


import sensor, time, image, pyb, math
from pyb import UART
from pyb import Pin,ExtInt

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.B128X128) # or sensor.QQVGA (or others)
sensor.set_windowing((92,112))
sensor.skip_frames(10) # Let new settings take affect.
sensor.skip_frames(time = 2000) #等待2s



#SUB = "s1"
NUM_SUBJECTS = 1 #图像库中不同人数，一共6人
NUM_SUBJECTS_IMGS = 20 #每人有20张样本图片
p_out0 = Pin('P0',Pin.OUT_PP)
p_out1 = Pin('P1',Pin.OUT_PP)
p_in = Pin('P2', Pin.IN, Pin.PULL_UP)
uart = UART(3, 19200)

# 一直拍摄当前人脸。
while(1):
    img = sensor.snapshot()
    #img = image.Image("singtown/%s/1.pgm"%(SUB))
    d0 = img.find_lbp((0, 0, img.width(), img.height()))
    #d0为当前人脸的lbp特征
    img = None
    pmin = 999999
    num=0
    def min(pmin, a, s):
        global num
        if a<pmin:
            pmin=a
            num=s
        return pmin
    for s in range(1, NUM_SUBJECTS+1):
        dist = 0
        for i in range(2, NUM_SUBJECTS_IMGS+1):
            img = image.Image("singtown/s%d/%d.pgm"%(s, i))
            d1 = img.find_lbp((0, 0, img.width(), img.height()))
            #d1为第s文件夹中的第i张图片的lbp特征
            dist += image.match_descriptor(d0, d1)#计算d0 d1即样本图像与被检测人脸的特征差异度。
        #print("Average dist for subject %d: %d"%(s, dist/NUM_SUBJECTS_IMGS))
        pmin = min(pmin, dist/NUM_SUBJECTS_IMGS, s)#特征差异度越小，被检测人脸与此样本更相似更匹配。
        #print(pmin)
    if pmin <= 6000:
        print("welcome:%d!"%(num)) # num为当前最匹配的人的编号。
        p_out0.high()
        p_out1.low()
    else:
        continue
        #print("stranger!")
    value = p_in.value()
    if value == 0:
        p_out0.high()
        p_out1.high()
