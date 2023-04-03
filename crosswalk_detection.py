import cv2
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob

def distortion_factors():
    # Prepare object points
    # From the provided calibration images, 9*6 corners are identified 
    nx = 11 #9 , 11
    ny = 8 #6 , 8
    objpoints = []
    imgpoints = []
    # Object points are real world points, here a 3D coordinates matrix is generated
    # z coordinates are 0 and x, y are equidistant as it is known that the chessboard is made of identical squares
    # objp = np.zeros((6*9,3), np.float32)
    objp = np.zeros((8*11,3), np.float32)
    # objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
    objp[:,:2] = np.mgrid[0:11,0:8].T.reshape(-1,2)
  
    # Make a list of calibration images
    os.listdir("camera_cal/")
    cal_img_list = os.listdir("camera_cal/")  
    
    # Imagepoints are the coresspondant object points with their coordinates in the distorted image
    # They are found in the image using the Open CV 'findChessboardCorners' function
    for image_name in cal_img_list:
        import_from = 'camera_cal/' + image_name
        img = cv2.imread(import_from)
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
        # If found, draw corners
        if ret == True:
            # Draw and display the corners
            cv2.drawChessboardCorners(img, (nx, ny), corners, ret)#
            imgpoints.append(corners)
            objpoints.append(objp)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    
    ###################################
    ## checking the undistored image ##
    ###################################
    # for img_name in cal_img_list:
    #     import_from = 'camera_cal/' + img_name
    #     img = cv2.imread(import_from)
    #     undist = cv2.undistort(img, mtx, dist, None, mtx)
    #     export_to = 'camera_cal_undistorted/' + img_name
    #     #save the image in the destination folder#
    #     plt.imsave(export_to, undist)
            
    return mtx, dist         


def warp(img, mtx, dist): # mts, dist
    undist = cv2.undistort(img, mtx, dist, None, mtx)
    img_size = (img.shape[1], img.shape[0])
    #print(img_size)
    offset = 150
    
    # Source points taken from images with straight lane lines, 
    # these are to become parallel after the warp transform
    # src = np.float32([
    #     (350, 1080), # bottom-left corner
    #     (845, 700), # top-left corner 
    #     (1020, 700), # top-right corner
    #     (1560, 1080) # bottom-right corner
    # ])
    src = np.float32([
        (317, 720), # bottom-left corner
        (559, 457), # top-left corner 
        (671, 457), # top-right corner
        (1026, 720) # bottom-right corner
    ])
    # src = np.float32([
    #     (int(img_size[0]*350/1920), int(img_size[1]*1080/1080)), # bottom-left corner
    #     (int(img_size[0]*845/1920), int(img_size[1]*700/1080)), # top-left corner 
    #     (int(img_size[0]*1020/1920), int(img_size[1]*700/1080)), # top-right corner
    #     (int(img_size[0]*1560/1920), int(img_size[1]*1080/1080)) # bottom-right corner
    # ])
    # Destination points are to be parallel, taken into account the image size
    dst = np.float32([
        [offset, img_size[1]],             # bottom-left corner
        [offset, 0],                       # top-left corner
        [img_size[0]-offset, 0],           # top-right corner
        [img_size[0]-offset, img_size[1]]  # bottom-right corner
    ])
    # Calculate the transformation matrix and it's inverse transformation
    M = cv2.getPerspectiveTransform(src, dst)
    M_inv = cv2.getPerspectiveTransform(dst, src)
    warped = cv2.warpPerspective(undist, M, img_size)
    
    return warped, M_inv, undist

def binary_thresholded(img):
    # Transform image to gray scale
    gray_img =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply sobel (derivative) in x direction, this is usefull to detect lines that tend to be vertical
    sobelx = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0)
    abs_sobelx = np.absolute(sobelx)
    # Scale result to 0-255
    scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
    sx_binary = np.zeros_like(scaled_sobel)
    # Keep only derivative values that are in the margin of interest
    sx_binary[(scaled_sobel >= 30) & (scaled_sobel <= 255)] = 1

    # Detect pixels that are white in the grayscale image
    white_binary = np.zeros_like(gray_img)
    white_binary[(gray_img > 200) & (gray_img <= 255)] = 1 #200,255

    # Convert image to HLS
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    H = hls[:,:,0]
    S = hls[:,:,2]
    sat_binary = np.zeros_like(S)
    # Detect pixels that have a high saturation value
    sat_binary[(S > 200) & (S <= 255)] = 1 #90 , 255

    hue_binary =  np.zeros_like(H)
    # Detect pixels that are yellow using the hue component
    hue_binary[(H > 15) & (H <= 25)] = 1 #10, 25

    # Combine all pixels detected above
    binary_1 = cv2.bitwise_or(sx_binary, white_binary)
    binary_2 = cv2.bitwise_or(hue_binary, sat_binary)
    binary = cv2.bitwise_or(binary_1, binary_2)
    #plt.imshow(binary, cmap='gray')

    return binary

def lane_finding_pipeline(img,init, mts, dist):
    binary_thresh = binary_thresholded(img)
    binary_warped, M_inv, _ = warp(binary_thresh, mts, dist)

    draw_poly_img = draw_poly_lines(binary_warped, left_fitx, right_fitx, ploty)

    return out_img, veh_pos, colorwarp_img, draw_poly_img
    

def main():

    # cap = cv2.VideoCapture('/home/amrlabs/Documents/github/1v_Advanced-Lane-Detection/sample_driving_0621-2.mp4')
    cap = cv2.VideoCapture('/Users/choehyeonseog/Desktop/Yolov5_DeepSort_Pytorch/test_sample.mp4') # test_sample.mp4
    # cap = cv2.VideoCapture('sample_driving_0621-2.mp4')
    #cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('File open failed!')
        cap.release()
        sys.exit()

    ## video out ##
    w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) 
    #delay=int(1000 / fps)

    angle=0
    img_steering = cv2.imread('steering_wheel_image.jpg')
    rows,cols,ext= img_steering.shape

    # create the `VideoWriter()` object
    out = cv2.VideoWriter('./yolov5/data/output/result_output_lane.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

    init=True
    mtx, dist = distortion_factors()

    while True:
        ret, frame =cap.read()

        if not ret:
            break
       
        img_out, angle, draw_poly_img = lane_finding_pipeline(frame, init, mtx, dist)

        if angle>1.5 or angle <-1.5:
            init=True
        else:
            init=False

        M = cv2.getRotationMatrix2D((cols/2,rows/2),-angle*10,1)
        dst = cv2.warpAffine(img_steering,M,(cols,rows))
        height, width, channel = dst.shape
        height1, width1, channel1 = img_out.shape
        out.write(img_out)    
        
        cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
        cv2.imshow('frame', img_out)
        cv2.namedWindow('draw_poly',cv2.WINDOW_NORMAL)
        cv2.imshow('draw_poly', draw_poly_img)
    
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()