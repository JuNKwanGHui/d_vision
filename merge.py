import cv2

# 첫 번째 영상 불러오기
video1 = cv2.VideoCapture('/Users/choehyeonseog/Desktop/pre_stop1.mp4')

# 두 번째 영상 불러오기
video2 = cv2.VideoCapture('/Users/choehyeonseog/Desktop/stop1.mp4')

out2

# 영상 크기 확인
width = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 새로운 비디오 생성
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (width*2, height))

# 영상 합치기
# while True:
#     ret1, frame1 = video1.read()
#     ret2, frame2 = video2.read()

#     if not ret1 or not ret2:
#         break

#     # 영상 이어붙히기
#     frame = cv2.hconcat([frame1, frame2])

#     # 결과 비디오에 프레임 추가
#     out.write(frame)

#     # 화면에 출력
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# 종료
video1.release()
video2.release()
out.release()
cv2.destroyAllWindows()
