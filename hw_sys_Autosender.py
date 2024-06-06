
# last modified : 2024.05.21 tues# Author: moonsujeong
# only video file*** auto sender system
# problem 
# 1. no seperate function (video make and quto sender)
# update(new)
# 1. rec autosend system

from time import sleep, localtime
import datetime
import sys, os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from uuid import uuid4
import schedule
import cv2
import pyaudio
import wave
import os
#noisereduce&amp
import librosa
import librosa.display
import numpy as np
from scipy.io import wavfile
import noisereduce as nr
import warnings
warnings.filterwarnings('ignore')
from IPython.display import Audio, display

# matplotlib의 rcParams 설정을 위한 import 추가
from matplotlib import rcParams
rcParams['figure.figsize'] = 14, 6


def wav_pre(filename):
    # 로드

    sr = 16000

    data, rate = librosa.load(filename, duration=10)



    # 노이즈 감소

    reduced_noise = nr.reduce_noise(y=data, sr=rate, n_std_thresh_stationary=1.2, n_fft=2048, win_length=2048, hop_length=1024)

    audio_obj_ori = Audio(data, rate=rate)



    # 오디오 스케일링

    volume_multiplier = 23.0

    increased_volume = reduced_noise * volume_multiplier

    print(np.min(increased_volume), np.max(increased_volume))

    display(audio_obj_ori)



    # 볼륨 조절 후의 범위 확인

    rms_original = np.sqrt(np.mean(np.square(reduced_noise)))

    rms_half_volume = np.sqrt(np.mean(np.square(increased_volume)))

    db_reduction = 20 * np.log10(rms_half_volume / rms_original)

    print("증가한 dB:", db_reduction)
 
    # 파일 저장

    wavfile.write("recpre" + filename, rate, increased_volume.astype(np.float32))



# Dir path
dir_Path = os.path.dirname(os.path.realpath(__file__)) +"/"

#Send form
PROJECT_ID = "i-em-helper"
#my project id
 
cred = credentials.Certificate("/home/kw-moon/serverKey/i-em-helper-firebase-adminsdk-2buug-3b53a8b26d.json") #(키 이름 ) 부분에 본인의 키이름을 적어주세요.
default_app = firebase_admin.initialize_app(cred,{'storageBucket':f"i-em-helper.appspot.com"})
#버킷은 바이너리 객체의 상위 컨테이너이다. 버킷은 Storage에서 데이터를 보관하는 기본 컨테이너이다.
bucket = storage.bucket()#기본 버킷 사용

#0603:Video file uploader
def rec_fileUpload(file):
    blob = bucket.blob('rec_file/'+ "recpre" + file) #저장한 사진을 파이어베이스 storage의 recfile/ 디렉토리에 저장
    #new token and metadata 설정
    new_token = uuid4()
    metadata = {"firebaseStorageDownloadTokens": new_token} #access token이 필요하다.
    blob.metadata = metadata
 
    #upload file
    #blob.upload_from_filename(filename='/home/kw-moon/'+file, content_type='image/png') #파일이 저장된 주소와 이미지 형식(jpeg도 됨)
    #if file is video (.avi format)
    #blob.upload_from_filename(filename = file, content_type='video/avi') #파일이 저장된 주소와 data format(.avi)
    #if file is audio ()
    blob.upload_from_filename(filename= file, content_type='audio/wav') #파일이 저장된 주소와 data format(.wav)

    #debugging hello
    print("hello wav")
    print(blob.public_url)

#0603:Video file uploader
def video_fileUpload(file):
    blob = bucket.blob('video_file/'+file) #저장한 사진을 파이어베이스 storage의 send_test0510 디렉토리에 저장
    #new token and metadata 설정
    new_token = uuid4()
    metadata = {"firebaseStorageDownloadTokens": new_token} #access token이 필요하다.
    blob.metadata = metadata
 
    #upload file
    #blob.upload_from_filename(filename='/home/kw-moon/'+file, content_type='image/png') #파일이 저장된 주소와 이미지 형식(jpeg도 됨)
    #if file is video (.avi format)
    blob.upload_from_filename(filename = file, content_type='video/avi') #파일이 저장된 주소와 data format(.avi)
    #if file is audio ()
    #blob.upload_from_filename(filename='home/kw-moon/dataDeilery'+file, content_type='audio/wav') #파일이 저장된 주소와 data format(.wav)

    #debugging hello
    print("hello video")
    print(blob.public_url)

def rec_wav(suffix):
    chunk = 4096  # Record in chunks of 4096 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 10
    #영상 이름 중복 방지
    basename = "rec"
    rec_Pname = dir_Path + basename + suffix + ".wav" #사운드 파일 명 
    sendname = basename + suffix + ".wav"
    print(rec_Pname) #root check point
    print(sendname) #root check point
    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording') # rec start check point

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 5 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()
    print(rec_Pname) #root check point
    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(rec_Pname, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    print('{} saved'.format(rec_Pname))
    wav_pre(sendname)
    rec_fileUpload(sendname)
    
    
def saved_pvideo():
    
    #촬영 사이즈 상수화
    __SCREEN_WIDTH = 960
    __SCREEN_HEIGHT = 720
    
    #영상 이름 중복 방지
    basename = "video"
    suffix = datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")
    print(suffix) #root check point
    #wav file craetion
    rec_wav(suffix)
    
    #카메라 활성화
    camera = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
    #촬영 시, 사이즈 설정
    camera.set(3, __SCREEN_WIDTH)
    camera.set(4, __SCREEN_HEIGHT)

    #인코딩 파라미터 입력
    fps = 60 #영상 프레임 설정
    duration = 10 #30초 간격 비디오 저장
    fourcc = cv2.VideoWriter_fourcc(*"DIVX") #인코딩 형식 입력
    video_Pname = dir_Path + basename + suffix + ".avi" #비디오 명
    sendname =  basename + suffix + ".avi"
    print(video_Pname) #root check point
    print(sendname)
    #영상 파일 생성
    out = cv2.VideoWriter(
        f""+ video_Pname, fourcc, fps, (int(camera.get(3)), int(camera.get(4)))
    )

    for _ in range(fps * duration):
        ret, frame = camera.read()
        if ret:
            out.write(frame)
        else:
            print("Error: failed to saved video file")

    out.release() #영상 생성 종료
    print('{} saved'.format(video_Pname))
    video_fileUpload(sendname)
 
#10초 마다 실행
schedule.every(30).seconds.do(saved_pvideo)
#10분에 한번씩 실행
#schedule.every(10).minutes.do(execute_camera)
#매 시간 마다 실행
# schedule.every().hour.do(clearAll)
#기타 정해진 시간에 실행/매주 월요일에 실행/매주 수요일 몇시에 실행 등의 옵션이 있다.
 
 
while True:
   schedule.run_pending()
   sleep(1)