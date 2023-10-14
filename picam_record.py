import picamera
import time
import datetime
import os

def record():
    #카메라 영상 저장 기능
    print('if you want to stop recording, press ''N''\n')
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        now = datetime.datetime.now()
        filename = now.strftime('%Y-%m-%d %H:%M:%S')
        #동영상 녹화 시작
        camera.start_recording(output = filename + '.h264')
        check_stop = input() #keboard interrupt

        while check_stop != 'N':
            camera.wait_recording()
        
        #동영상 녹화 종료
        camera.stop_recording()
    print('stop recording. save in  ' + os.getcwd())
    print('\n')


