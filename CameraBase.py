# Camera- Logitech 720p

# overlay load
from pynq.overlays.base import BaseOverlay
from pynq.lib.video import *
base = BaseOverlay("base.bit")

# monitor configuration: 640*480 @ 60Hz
Mode = VideoMode(640,480,24)
hdmi_out = base.video.hdmi_out
hdmi_out.configure(Mode,PIXEL_BGR)
hdmi_out.start()

# monitor (output) frame buffer size
frame_out_w = 1920
frame_out_h = 1080
# camera (input) configuration
frame_in_w = 640
frame_in_h = 480

# initialize camera from OpenCV
import cv2
import time
videoIn = cv2.VideoCapture(0)
videoIn.set(cv2.CAP_PROP_FRAME_WIDTH, frame_in_w);
videoIn.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_in_h);

print("Capture device is open: " + str(videoIn.isOpened()))

fps_start_time=0
fps=0
# Capture webcam image
import numpy as np


while(True):
    if(base.buttons[0].read()==0):
        ret, frame_vga = videoIn.read()
        fps_end_time=time.time()
        time_diff=fps_end_time-fps_start_time
        fps=1/time_diff
        fps_start_time=fps_end_time
    
        fps_text="FPS: {:.2f}".format(fps)
        cv2.putText(frame_vga,fps_text,(5,30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),1)
# Display webcam image via HDMI Out
        if (ret): 
            if (base.buttons[1].read()==1):
                videoIn.release()
                hdmi_out.stop()
                del hdmi_out
            else:
                outframe = hdmi_out.newframe()
                outframe[0:480,0:640,:] = frame_vga[0:480,0:640,:]
                hdmi_out.writeframe(outframe)
        else:
            raise RuntimeError("Failed to read from camera.")
