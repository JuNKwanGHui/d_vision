import cv2
def main(bbox_ff):
    event_frame = bbox_ff[1]
    video_file = '#'
    cnt = 0
    cap = cv2.VideoCapture(video_file)
    if cap.isOpened():
        while True:
            ret, img = cap.read()
            cnt += 1
            if ret:
                if event_frame == cnt:
                    crop_image = img[bbox_ff[3]:bbox_ff[3]+bbox_ff[5], bbox_ff[2]:bbox_ff[2]+bbox_ff[4]]
                    cv2.imwrite('traffic_light.jpg',img)

                    # cv2.imshow(video_file, img)
                    # cv2.waitKey(33)
            else:
                break
    else:
        print('cannot open the file')
    
    cap.release()
    cv2.destroyAllWindows()