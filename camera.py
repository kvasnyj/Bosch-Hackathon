import time
import numpy as np
import cv2
from PIL import Image
import requests
from io import BytesIO


def define_warper(img):
        h,w = img.shape[0], img.shape[1]
        basex = 550
        width = 500
        height = 500

        src = np.float32([
            [90, basex],
            [w-90, basex],
            [340, 390],
            [w-340, 390]
        ])

        dst = np.float32([
            [(w-width)/2, basex],
            [w - (w-width)/2, basex],
            [(w-width)/2, basex-height],
            [w - (w-width)/2, basex-height]
        ])

        return src, dst

def warper(img):
    h,w = img.shape[0], img.shape[1]
    warp_src, warp_dst = define_warper(img)
    # Compute and apply perpective transform
    M = cv2.getPerspectiveTransform(warp_src, warp_dst)
    img = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_NEAREST)  # keep same size as input image

    M = cv2.getRotationMatrix2D((w/2,h/2),-15,1)
    img = cv2.warpAffine(img,M,(w,h))

    return img


def define_position(warped):
    h,w = img.shape[0], img.shape[1]
    pts = np.argwhere(warped[:, :])
    position = w/2
    left  = np.mean(pts[(pts[:,1] < position) & (pts[:,0] > 410)][:,1])
    right = np.mean(pts[(pts[:,1] > position) & (pts[:,0] > 410)][:,1])
    position = 0
    if left>0 and right>0:
        position = left + (right-left)/2
    elif left > 0:
        position = left
    else:
        position = right 

    position = position - 650
    print("left: %s, right: %s, position: %s" % (left, right, position))

    return position    

#url = "https://raw.githubusercontent.com/kvasnyj/Bosch-Hackathon/master/img/1.jpg"
url = "http://10.0.126.9/snapshot.jpg"

while True:
    response = requests.get(url, auth=('admin', '1234'))
    b = BytesIO(response.content)
    img = Image.open(b)
    im_arr = np.fromstring(img.tobytes(), dtype=np.uint8)
    im_arr = im_arr.reshape((img.size[1], img.size[0], 3))       
    
    img = cv2.cvtColor(im_arr, cv2.COLOR_BGR2HSV)

    img = img[:,:, 1]

    img = cv2.Canny(img, 20, 200)

    img = warper(img)

    pos = define_position(img)


