import socket
import json
import sys
import pyrealsense2 as rs
from binary_fractions import TwosComplement, Binary
import math  
import transformations as tf
import numpy as np

PI = 3.141592653589793
pipe = rs.pipeline()

cfg = rs.config()
cfg.enable_stream(rs.stream.pose)

def floatToBytes(number, bitsOfIntegral):
    number = str(number)
    # convert floating number in string
    # to two complement with variable
    # length of integral part. Always 
    # 24bits, and returns 3 bytes
    whole, dec = str(number).split(".") 
   # if int(whole)> (1<<bitsOfIntegral)/2:
    #    whole = str((1<<bitsOfIntegral)/2)
  #      whole = whole[0:3]
  #  elif int(whole)< -(1<<bitsOfIntegral)/2:
   #     whole = "-" + str((1<<bitsOfIntegral)/2)
   #     whole = whole[0:4]
  
    newNumber = TwosComplement(float(whole + "."+dec))
    try:
        idx = newNumber.index(".")
    except ValueError:
        newNumber ="0.0"
    whole, dec = str(newNumber).split(".") 
    insert ="0"
    if number[0]=="-":
        insert ="1"
    if len(whole)< (bitsOfIntegral+1):
        for i in range(0,(bitsOfIntegral+1-len(whole))):
            whole =insert + whole
     
    if len(dec)>(24-bitsOfIntegral-1):
        dec = dec[0:(24-bitsOfIntegral-1)]
    elif len(dec)<(24-bitsOfIntegral-1):
        for i in range(0,((24-bitsOfIntegral-1)-len(dec))):
            dec = dec + "0"
          
    final = whole+dec
    return int(final,2).to_bytes(3, byteorder='big')

try:
    IPs = sys.argv[1:]
except IndexError:
    IPs = ["127.0.0.1"]



print("Realsense T265 sending to" , IPs, " in FreeD protocol")
TCP_PORT = 40000
BUFFER_SIZE = 1024

starting_height = 1 # starting height in meters
pos_scale = 1000
rot_scale =  128
threshold = 0.0005

pipe.start(cfg)

frames = pipe.wait_for_frames()

    # Fetch pose frame
pose = frames.get_pose_frame()
if pose:
    data = pose.get_pose_data()

H_aeroRef_T265Ref = np.array([[0,0,-1,0],[1,0,0,0],[0,-1,0,0],[0,0,0,1]])
H_T265body_aeroBody = np.linalg.inv(H_aeroRef_T265Ref)

try:
    while True:

        my_bytes = bytearray()
        # Wait for the next set of frames from the camera
        frames = pipe.wait_for_frames()

        # Fetch pose frame
        pose = frames.get_pose_frame()
        if pose:
            data = pose.get_pose_data()
            q = data.rotation
            data.translation.y += starting_height
            H_T265Ref_T265body = tf.quaternion_matrix([data.rotation.w, data.rotation.x,data.rotation.y,data.rotation.z]) # in transformations, 
            H_aeroRef_aeroBody = H_aeroRef_T265Ref.dot( H_T265Ref_T265body.dot( H_T265body_aeroBody ))
            rpy_rad = np.array( tf.euler_from_matrix(H_aeroRef_aeroBody, 'rxyz') )
        
            my_bytes.extend((bytes.fromhex('D1'))) # message type
            my_bytes.extend((bytes.fromhex('01'))) #camera id
            my_bytes.extend(floatToBytes(rpy_rad[2]*(180/PI),8)) # tilt
            my_bytes.extend(floatToBytes((rpy_rad[1])*(180/PI),8)) # pan 0 pitch
            my_bytes.extend(floatToBytes((rpy_rad[0])*(180/PI),8)) # pan 0 pitch
            my_bytes.extend(floatToBytes(pos_scale*data.translation.x,17))
            my_bytes.extend(floatToBytes(pos_scale*-data.translation.z,17))
            my_bytes.extend(floatToBytes(pos_scale*data.translation.y,17))
            my_bytes.extend(floatToBytes('120.0',17))
            my_bytes.extend(floatToBytes("120.0",17))
            my_bytes.extend((bytes.fromhex('F1'))) # message type
            my_bytes.extend((bytes.fromhex('A1'))) # message type
            chkInit = 40
            for byte in my_bytes:
                chkInit -= byte # The checksum is calculated by subtracting (modulo 256) each byte of themessage, including the message type, from 40 
            my_bytes.extend((chkInit % 256).to_bytes(1, byteorder='big')) # message type
            
            for IP in IPs:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect((IP, TCP_PORT))
                s.send(my_bytes)
                s.close()
    
finally:
    pipe.stop()

