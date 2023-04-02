import cv2
import cartest3

def main(): 
    video_file = '/Users/choehyeonseog/Desktop/test.mp4'
    event_frame = cartest3.main()
    frame = 0
    print(event_frame)


    cap = cv2.VideoCapture(video_file)
    if cap.isOpened():
        fps = cap.get(cv2.CAP_PROP_FPS)
        f_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        f_width = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        f_height = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        codec = "DIVX"
        fourcc = cv2.VideoWriter_fourcc(*codec)
        for i in range(len(event_frame)):
            encoded_mp4 = cv2.VideoWriter("Stop.mp4", fourcc, fps, (f_width, f_height))
        while True:
            ret, image = cap.read()
            frame += 1
            if ret:
                #img가 프레임이다
                print(frame)
                if frame == event_frame[i]:
                    encoded_mp4.write(image)
                    print("그ㅂ")
                # else:
                #     pass
                cv2.waitKey(33)
            else:
                break
    else:
        print('cannot open the file')
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()