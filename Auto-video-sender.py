# _*_ coding: utf-8 _*_
# last modified : 2024.05.21 tues
# Author: moonsujeong
# only video file*** auto sender system
# problem 
# 1. no rules of scheduler
# 2. no seperate function (video make and quto sender)
# 3. no have rec system 
from time import sleep
import datetime
import sys, os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from uuid import uuid4
import schedule
import cv2
from time import sleep
import datetime
# import send_Form as sf
# import saved_Video as sv
 
PROJECT_ID = "i-em-helper"
#my project id
 
cred = credentials.Certificate("/home/kw-moon/serverKey/i-em-helper-firebase-adminsdk-2buug-3b53a8b26d.json") #(키 이름 ) 부분에 본인의 키이름을 적어주세요.
default_app = firebase_admin.initialize_app(cred,{'storageBucket':f"i-em-helper.appspot.com"})
#버킷은 바이너리 객체의 상위 컨테이너이다. 버킷은 Storage에서 데이터를 보관하는 기본 컨테이너이다.
bucket = storage.bucket()#기본 버킷 사용

    
#0520: only video file uploader
def fileUpload(file):
    blob = bucket.blob('send_test0510/'+file) #저장한 사진을 파이어베이스 storage의 send_test0510 디렉토리에 저장
    #new token and metadata 설정
    new_token = uuid4()
    metadata = {"firebaseStorageDownloadTokens": new_token} #access token이 필요하다.
    blob.metadata = metadata
 
    #upload file
    #blob.upload_from_filename(filename='/home/kw-moon/'+file, content_type='image/png') #파일이 저장된 주소와 이미지 형식(jpeg도 됨)
    #if file is video (.avi format)
    blob.upload_from_filename(filename='/home/kw-moon/saved_video'+file, content_type='video/avi') #파일이 저장된 주소와 data format(.avi)
    #if file is audio ()
    #blob.upload_from_filename(filename='/home/kw-moon/'+file, content_type='audio/wav') #파일이 저장된 주소와 data format(.wav)

    #debugging hello
    print("hello ")
    print(blob.public_url)
    
def saved_pvideo():
    
    #촬영 사이즈 상수화
    __SCREEN_WIDTH = 960
    __SCREEN_HEIGHT = 720
    #영상 이름 중복 방지
    basename = "video"
    suffix = datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")
    #카메라 활성화
    camera = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
    #촬영 시, 사이즈 설정
    camera.set(3, __SCREEN_WIDTH)
    camera.set(4, __SCREEN_HEIGHT)

    #인코딩 파라미터 입력
    fps = 60 #영상 프레임 설정
    duration = 30 #30초 간격 비디오 저장
    fourcc = cv2.VideoWriter_fourcc(*"DIVX") #인코딩 형식 입력
    video_Pname = "".join([basename, suffix]) + ".avi" #비디오 명 

    #영상 파일 생성
    out = cv2.VideoWriter(
        f"/home/kw-moon/saved_video"+ video_Pname, fourcc, fps, (int(camera.get(3)), int(camera.get(4)))
    )

    for _ in range(fps * duration):
        ret, frame = camera.read()
        if ret:
            out.write(frame)
        else:
            print("Error: failed to saved video file")

    out.release() #영상 생성 종료
    fileUpload(video_Pname)
 
#1초 마다 실행
schedule.every(10).seconds.do(saved_pvideo)
#10분에 한번씩 실행
#schedule.every(10).minutes.do(execute_camera)
#매 시간 마다 실행
# schedule.every().hour.do(clearAll)
#기타 정해진 시간에 실행/매주 월요일에 실행/매주 수요일 몇시에 실행 등의 옵션이 있다.
 
 
 
while True:
    schedule.run_pending()
    sleep(1)