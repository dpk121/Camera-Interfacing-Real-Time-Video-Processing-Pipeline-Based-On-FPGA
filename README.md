# Camera-Interfacing-Real-Time-Video-Processing-Pipeline-Based-On-FPGA
#  Boot SD Card with PYNQ image
• Download the PYNQ image pynq z2 v2.6 using Link: ”https://www.tulembedded.com/FPGA/ProductsPYNQ-Z2.html”.

• Write the image to SD card usingWin32Disk Imager. DownloadWin32Disk Imager using Link ”https://sourceforge.net/projects/win32diskimager/”

• Do not format disk whenevr it ask after completion of write image

# Hardware design Project  named with dma_ex

- two seperate IP merged 1) PS GPIO 2) DMA data transfer IP

- vivado tool 2019.2
- PS GPIO Block connects hardware peripherals with GPIO to use them in Processing System(PS)
- DMA IP transfer the data between DDR memory and Stram port (FIFO in this case) using AXI master and slave.
- Genertae bitstram to use in overlay


# Python Script for camera interfacing with DMA & GPIO block IP

- run the jupyter web page using either static or router connection.

 - PYNQ contains predefined code for using base overlay and other hardware ports. 
 - CameraScript.py defines the use of DMA and PS GPIO IP in PS and transfer data from PS to data FIFO PL for hardware processing.

 - keep realsense_depth.py and detect distance.py file in same folder where python script is written to use realsense camera

 - python script is fully commented for better understanding. 

 - To use user defined IP using overlay in PS, generate bitstream file of IP using vivado tool and keep .bit and .hwh file in pynq overlay folder.
 
		To add file in pynq overlay follow below steps.
			1) Turn on the board with SD card having pynq image using either static or router connection
			2) Go to quick access in your window PC. Type ”\\pynq” and enter 
			3) Enter default username and password as ”xilinx”
			4) Go to the directory ”/pynq/overlays” 
			5) Go to the vivado project 
				Location of .bit file: ...project directory/.runs/impl_1 
				Location of .hwh file: ....project directory/.src/sources 1/bd/dma block/hw handoff
			6) Create a new folder inside "pynq/overlays" (dmaTest in this case) and copy the .bit and .hwh files from vivado project & paste here.
			Note: Keep the name of both files same. Ex: dma_block_wrapper1.bit , dma_block_wrapper1.hwh
			7) Now import overlay from pynq in jupyter. See provided code for better understanding
- realsense require high power. So use power adapter for using realsense. Sometimes camera throws error when starting, restart board in such case.

# Base Overlay in PYNQ
- base overlay defines class of different ports LEDs, buttons, switches, HDMI IN, HDMI out etc.
- CameraBase.py contains the python script of camera interfacing and display on VGA monitor.

	NOTE: PYNQ does not support two overlay instantiation at same time. So different hardware IP is created to use switch, leds using PS GPIO.
- This script shows the video frames captured from camera on VGA monitor.

# Boot time implementation method
- Read pynq_image using SD card reader
- Replace the present LEDs indication code with user desigend code. 

# Misc
- Hardware tool: PYNQ-Z2, Logitech 720, Intel realsense D435i, VGA monitor
- Software tool: Vivaod 2019.2
- Installation of pyrealsense: follow link
	https://github.com/IntelRealSense/librealsense/blob/master/doc/installation.md
	
- PYNQ-Z2 functionality

		SW0 high- Logitech camera connected and LD0 On, rest LDs off
		SW1 high- Realsense camera connected and LD1 On, rest LDs off
		SW0 & SW1 low- No camera connectd and LD2 On, rest LDs off
	
