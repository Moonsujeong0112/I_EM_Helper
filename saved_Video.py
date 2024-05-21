import cv2
from time import sleep
import datetime
import schedule
import send_Form as sf

def saved_pvideo(filename):
    video_filename = "../saved_video/" + filename
    #촬영 사이즈 상수화
    __SCREEN_WIDTH = 960
    __SCREEN_HEIGHT = 720
    
    #카메라 활성화
    camera = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
    #촬영 시, 사이즈 설정
    camera.set(3, __SCREEN_WIDTH)
    camera.set(4, __SCREEN_HEIGHT)

    #인코딩 파라미터 입력
    fps = 60 #영상 프레임 설정
    duration = 30 #30초 간격 비디오 저장
    fourcc = cv2.VideoWriter_fourcc(*"DIVX") #인코딩 형식 입력
    

    #영상 파일 생성
    out = cv2.VideoWriter(
        f""+ video_filename, fourcc, fps, (int(camera.get(3)), int(camera.get(4)))
    )

    for _ in range(fps * duration):
        ret, frame = camera.read()
        if ret:
            out.write(frame)
        else:
            print("Error: failed to saved video file")

    out.release() #영상 생성 종료
    sf.fileUpload(filename)
    