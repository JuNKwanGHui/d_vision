import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import glob
import os
import sys

def distortion_factors():
    # 객체 포인트 준비
    # 제공된 캘리브레이션 이미지에서 9*6 코너 식별 
    nx = 11 #9 , 11
    ny = 8 #6 , 8
    objpoints = []
    imgpoints = []
    # 객체 포인트는 실제 포인트이며 여기서 3D 좌표 행렬이 생성됩니다.
    # z 좌표는 0이고 x, y는 체스 판이 동일한 사각형으로 구성되어 있다고 알려져 있으므로 등거리입니다.
    # objp = np.zeros((6*9,3), np.float32)
    objp = np.zeros((8*11,3), np.float32)
    # objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
    objp[:,:2] = np.mgrid[0:11,0:8].T.reshape(-1,2)
  
    # 보정 이미지 목록 만들기
    os.listdir("camera_cal/")
    cal_img_list = os.listdir("camera_cal/")  
    
    # 이미지 포인트는 왜곡된 이미지에서 해당 좌표와 함께 대응하는 객체 포인트입니다.
    # Open CV 'findChessboardCorners' 기능을 사용하여 이미지에서 찾을 수 있습니다.
    for image_name in cal_img_list:
        import_from = 'camera_cal/' + image_name
        img = cv2.imread(import_from)
        # 그레이스케일로 변환
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 체스판 모서리 찾기
        ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
        # 발견되면 모서리를 그립니다.
        if ret == True:
            # 모서리 그리기 및 표시
            cv2.drawChessboardCorners(img, (nx, ny), corners, ret)#
            imgpoints.append(corners)
            objpoints.append(objp)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    
    ###################################
    ##   왜곡되지 않은 이미지 확인   ##
    ###################################
    for img_name in cal_img_list:
        import_from = 'camera_cal/' + img_name
        img = cv2.imread(import_from)
        undist = cv2.undistort(img, mtx, dist, None, mtx)
        export_to = 'camera_cal_undistorted/' + img_name
        #save the image in the destination folder#
        plt.imsave(export_to, undist)
            
    return mtx, dist  


mtx, dist = distortion_factors()
# cv2.imshow(mtx)
# cv2.imshow(dist)
cv2.waitKey()

    # while True:
    #     ret, frame =cap.read()

    #     if not ret:
    #         break
       
    #     img_out, angle, colorwarp, draw_poly_img = lane_finding_pipeline(frame, init, mtx, dist)

    #     if angle>1.5 or angle <-1.5:
    #         init=True
    #     else:
    #         init=False

    #     #Steering Image
    #     #angle = atan((180/pi)*(angle/5))
    #     M = cv2.getRotationMatrix2D((cols/2,rows/2),-angle*10,1)
    #     dst = cv2.warpAffine(img_steering,M,(cols,rows))
    #     #cv2.imshow("steering wheel", dst)
    #     height, width, channel = dst.shape
    #     height1, width1, channel1 = img_out.shape
    #     #img_out[(height1-height):height1, int(width1/2-width/2):(int(width1/2-width/2)+width)] = dst

    #     #Videowirte
    #     out.write(img_out)    
        
    #     cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
    #     cv2.imshow('frame', img_out)
    #     cv2.namedWindow('colorwarp',cv2.WINDOW_NORMAL)
    #     cv2.imshow('colorwarp', colorwarp)
    #     cv2.namedWindow('draw_poly',cv2.WINDOW_NORMAL)
    #     cv2.imshow('draw_poly', draw_poly_img)
    
    #     if cv2.waitKey(1) == 27:
    #         break


cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()