"""
비디오 관심영역(ROI) 지정
"""
import cv2

#img = cv2.imread('#')

video_file = '/Users/choehyeonseog/Desktop/test_sample.mp4'
 
cap = cv2.VideoCapture(video_file)
if cap.isOpened():
    while True:
        ret, img = cap.read()
        if ret:
            cv2.imshow(video_file, img)
            x_pos,y_pos,width,height = cv2.selectROI("location", img, False)
            print("x position, y position :" , x_pos, y_pos)
            print("width, height :", width, height)

            cv2.destroyAllWindows()
            cv2.waitKey(33)
        else:
            break
else:
    print('cannot open the file')

cap.release()
cv2.destroyAllWindows()