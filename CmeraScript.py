##########################  python full code############################

import numpy as np
from pynq import allocate   # to create dma input and output buffer
from pynq import Overlay    # to use PL IP in processing system
import cv2
import time
#%matplotlib inline 
from matplotlib import pyplot as plt
import pyrealsense2 
from realsense_depth import *

overlay = Overlay('/home/xilinx/pynq/overlays/dmaTest/dma_block_wrapper1.bit') # method to import overlay

def myfunc(): ###### function to check index error for logitech camera. Ignore if you don not get this error
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()
        index += 1
    return arr

# monitor (output) frame buffer size
frame_out_w = 1920
frame_out_h = 1080
# camera (input) configuration
frame_in_w = 640 # frame resolution 640*480
frame_in_h = 480
w = 640
h = 480
fname ="pic"
fnumber = 0;
from pynq import GPIO  ## to use PS GPIO pin
# assign GPIO pin to PL peripherals. GPIO pin configuration provided in report appendix.
switch0 = GPIO(GPIO.get_gpio_pin(4), 'in') 
switch1 = GPIO(GPIO.get_gpio_pin(5), 'in')
led0 = GPIO(GPIO.get_gpio_pin(6), 'out')
led1 = GPIO(GPIO.get_gpio_pin(7), 'out')
led2 = GPIO(GPIO.get_gpio_pin(8), 'out')
led3 = GPIO(GPIO.get_gpio_pin(9), 'out')
led0.write(0)
led1.write(0)
led2.write(0)
led3.write(0)

dma = overlay.axi_dma_0 # method to use axi dma
data_size=480*640*3
input_buffer = allocate(shape=(data_size,), dtype=np.uint8) # create buffer DDR memory using allocate 
output_buffer = allocate(shape=(data_size,), dtype=np.uint8)

videoIn, dc = None, None
while(True):
    #start = time.time()
    if(switch0.read() == 0 and switch1.read()==0): # both switch off means no camera connected. LED2 will glow
        led0.write(0)
        led1.write(0)
        led2.write(1)
        print("Both switch off")
        continue
    if(switch0.read() == 1 and switch1.read()==0): # sw0 high means logitech camera connected. LED0 will glow
        if(dc):
            print("dc release")
            try:
                dc.release()
                dc = None
            except:
                dc = None
        led1.write(0)
        led2.write(0)
        if(not videoIn):
            print(myfunc())
            videoIn = cv2.VideoCapture(0)
            time.sleep(0.5)
            videoIn.set(cv2.CAP_PROP_FRAME_WIDTH, frame_in_w);
            videoIn.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_in_h);
#             while (not videoIn.isOpened()):
#                 time.sleep(0.5)
#                 videoIn = cv2.VideoCapture(0)
#                 videoIn.set(cv2.CAP_PROP_FRAME_WIDTH, frame_in_w);
#                 videoIn.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_in_h);
            print("Logitech device is open: " + str(videoIn.isOpened()))
        led0.write(1)
        start = time.time()
        ret, frame_vga = videoIn.read()
        if(ret):
            #start = time.time()
            temp2d = np.reshape(frame_vga, (h*w*3,)) # Reshape in 1D
            #start = time.time()
            input_buffer[:] = temp2d # method to store data in input buffer
### Transfer the input buffer to the DMA using sendchannel and receive the data into output buffer using recvchannel from DMA            
            dma.sendchannel.transfer(input_buffer)
            dma.recvchannel.transfer(output_buffer)
#### Use wait() method to ensure the completion of data transfer with DMA
            dma.sendchannel.wait()
            dma.recvchannel.wait()
        
            temp2d = output_buffer[:]
            temp2d1 = np.reshape(temp2d, (h,w,3))
            end = time.time()
            elapsed_time=end-start
            print("Logitech Device FPS: ", 1/elapsed_time)
            cv2.imwrite("logitech_frame{}.jpg".format(int(time.time()*1000000)), temp2d1)
            
            ############ Frame sharing method
#             fstr = fname+str(fnumber)+".png"
#             cv2.imwrite(fstr,temp2d1)  
#             osstr = "tar cf - "+fstr+" --remove-files | nc 192.168.0.102 80"
#             print("logitech tar")
#             os.system(osstr) 
#             fnumber+=1
            
            ###############
        else:
            raise RuntimeError("Failed to read from Logitech camera.")
#     else:
#         videoIn.release()
#         led0.write(0)
    elif(switch1.read() == 1 and switch0.read()==0):
        if(videoIn):
            print("videoin release")
            videoIn.release()
            videoIn = None
        led0.write(0)
        led2.write(0)
        if(not dc):
            dc = DepthCamera()
        #led1.write(1)
        start = time.time()
        ret, depth_frame, color_frame = dc.get_frame()
        led1.write(1)
        if(ret):
            #start = time.time()
            temp2d = np.reshape(color_frame, (h*w*3,))
            #start = time.time()
            input_buffer[:] = temp2d
        
            dma.sendchannel.transfer(input_buffer)
            dma.recvchannel.transfer(output_buffer)
            dma.sendchannel.wait()
            dma.recvchannel.wait()
        
            temp2d = output_buffer[:]
            temp2d1 = np.reshape(temp2d, (h,w,3))
                         
            end = time.time()
            elapsed_time=end-start
            print("Realsense Device FPS: ", 1/elapsed_time)
            cv2.imwrite("realsense_frame{}.jpg".format(int(time.time()*1000000)), temp2d1)
            
            ################### Frame sharing method. 
                       
#             fstr = fname+str(fnumber)+".png"
#             cv2.imwrite(fstr,temp2d1)  
#             osstr = "tar cf - "+fstr+" --remove-files | nc 192.168.0.102 80"
#             print("logitech tar")
#             os.system(osstr) 
#             fnumber+=1
            
            
            ####################
        else:
            raise RuntimeError("Failed to read from Relasense camera.")         
#     else:
#         dc.release()
#         led0.write(0)
