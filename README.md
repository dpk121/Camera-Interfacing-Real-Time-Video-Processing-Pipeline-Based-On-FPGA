# Camera-Interfacing-Real-Time-Video-Processing-Pipeline-Based-On-FPGA

#####   Boot SD Card with PYNQ image
• Download the PYNQ image pynq z2 v2.6 using Link: ”https://www.tulembedded.com/FPGA/ProductsPYNQ-Z2.html”
• Write the image to SD card usingWin32Disk Imager. DownloadWin32Disk Imager using Link ”https://sourceforge.net/projects/win32diskimager/”
• Do not format disk whenevr it ask after completion of write image

##### Project hardware design named with dma_ex

---- two seperate IP merged 1) PS GPIO 2) DMA data transfer IP
---- vivado tool 2019.2


######### PYNQ contains predefined code for using base overlay and other hardware ports. 

############ Regarding Python Script
----- run the jupyter web page using either static or router connection.
----- keep depth.py and distance.py file in same folder where python script is written to use realsense camera
----- python script is fully commented for better understanding. 
----- to use overlay in PS, generate bitstream file of IP using vivado tool and keep .bit and .hwh file in pynq overlay folder.
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
------ realsense require high power. So use power adapter for using realsense. Sometimes camera throws error when starting, restart board in such case.
