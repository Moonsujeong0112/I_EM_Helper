# 배경색은 #2c2c2c 가 좋긴함
import tkinter as tk
import tkinter.font
from PIL import Image, ImageTk
import cv2
import webbrowser
from tkinter import messagebox
from tkinter import Toplevel, Canvas

window = tk.Tk()

# GUI 크기와 제목
window.title("I' EM Helper")
window.geometry("800x600")
window.resizable(False, False)
window.configure(bg = 'black')

# 타이틀 I'EM Helper
title_font = tk.font.Font(family = "Helvetica", size = 25, weight = "bold")

label_title = tk.Label(window, 
                 text = "I' EM Helper",
                 font = title_font,
                 bg='black',
                 fg='white',
                 padx = 40, pady=20)
label_title.grid(row = 0, column = 0)

# 사이렌 그림
image_path1 = "C:/Users/user/Desktop/Capstone_GUI_png/siren.jpg"
siren_image_pil = Image.open(image_path1)
siren_image_tk = ImageTk.PhotoImage(siren_image_pil)

siren_image_pil_resized = siren_image_pil.resize((50, 50))
siren_image_tk_resized = ImageTk.PhotoImage(siren_image_pil_resized)

label_siren = tk.Label(window, 
                       image=siren_image_tk_resized,
                       bg='black')
label_siren.place(x = 350, y = 20)

# 벨 그림
image_path2 = "C:/Users/user/Desktop/Capstone_GUI_png/bell.jpg"
bell_image_pil = Image.open(image_path2)
bell_image_tk = ImageTk.PhotoImage(bell_image_pil)

bell_image_pil_resized = bell_image_pil.resize((40, 40))
bell_image_tk_resized = ImageTk.PhotoImage(bell_image_pil_resized)

label_bell = tk.Label(window, 
                       image=bell_image_tk_resized,
                       bg = 'black')
label_bell.place(x = 670, y = 30)

# 영상이 나올 화면 만들기
video_frm = tk.Frame(window, bg = "#2c2c2c", width = 700, height = 350) # 영상나올 화면 프레임
video_frm.place(x = 50, y = 100)
"""video_lbl = tk.Label(video_frm)
video_lbl.pack(fill = tk.BOTH, expand=True)""" # 링크 넣으면 필요없는 부분이어서 일단 뺌

# 영상 링크 만들기
"""def callback(url):
   webbrowser.open_new_tab(url)

link = tk.Label(window, text="https://youtu.be/Y6mP8mLYQuU",font=('Helveticabold', 10), fg="blue", cursor="hand2")
link.place(x = 200, y = 500)
link.bind("<Button-1>",
          lambda e: 
          callback("https://youtu.be/Y6mP8mLYQuU"))"""

# 버튼1 동작 1
def open_link():
    url = "https://youtu.be/Y6mP8mLYQuU"
    webbrowser.open_new(url)

# 버튼1 생성
btn1_path = "C:/Users/user/Desktop/Capstone_GUI_png/btn1.jpg"
btn1_image_pil = Image.open(btn1_path)
btn1_image_tk = ImageTk.PhotoImage(btn1_image_pil)

btn1_image_pil_resized = btn1_image_pil.resize((300, 70))
btn1_image_tk_resized = ImageTk.PhotoImage(btn1_image_pil_resized)

btn1 = tk.Button(window,
                 image = btn1_image_tk_resized,
                 bg = 'black',
                 bd = 0,
                 command = open_link)  # 클릭 시 실행될 함수 지정

btn1.place(x = 55, y = 480)

# 버튼2 동작 1
def open_popup():
    top = Toplevel(window)
    top.geometry("600x400")
    top.title("신고 팝업")
    top.resizable(False, False)

    canvas = Canvas(top, width=600, heigh=400, bg='white', bd=2)
    canvas.pack()   # 이 코드가 있으면 popup에서 image가 보이지 않음
    
    img=ImageTk.PhotoImage(file="image\pop_pup.JPG")
    popup_image_pil = Image.open("image\pop_pup.JPG")
    popup_image_tk = ImageTk.PhotoImage(popup_image_pil)

    popup_image_pil_resized = popup_image_pil.resize((600, 400))
    popup_image_tk_resized = ImageTk.PhotoImage(popup_image_pil_resized)    
    canvas.create_image(300,200, image=popup_image_tk_resized)

    btn3_path = "image/btn3.png"
    btn3_image_pil = Image.open(btn3_path)
    btn3_image_tk = ImageTk.PhotoImage(btn3_image_pil)

    btn3_image_pil_resized = btn3_image_pil.resize((250, 100))
    btn3_image_tk_resized = ImageTk.PhotoImage(btn3_image_pil_resized)
    btn3 = tk.Button(top,
                 image = btn3_image_tk_resized,
                 bg = 'white',
                 bd = 0,
                 command =lambda: info3(top))
    btn3.place(x = 30, y = 280)

    btn4_path = "image/btn4.png"
    btn4_image_pil = Image.open(btn4_path)
    btn4_image_tk = ImageTk.PhotoImage(btn4_image_pil)

    btn4_image_pil_resized = btn4_image_pil.resize((270, 110))
    btn4_image_tk_resized = ImageTk.PhotoImage(btn4_image_pil_resized)
    btn4 = tk.Button(top,
                 image = btn4_image_tk_resized,
                 bg = 'white',
                 bd = 0,
                 command =lambda: info4(top))
    btn4.place(x = 300, y = 270)
    
    top.mainloop()   # 이 코드가 있으면 popup에서 image가 보이지 않음

# 버튼3 동작 
def info3(top):
    messagebox.showinfo("신고창", "정상적으로 신고가 접수 되었습니다.")
    top.destroy()

# 버튼4 동작
def info4(top):
    messagebox.showinfo("신고창", "신고 접수가 취소 되었습니다.")
    top.destroy()
    
# 버튼2 생성
btn2_path = "C:/Users/user/Desktop/Capstone_GUI_png/btn2.jpg"
btn2_image_pil = Image.open(btn2_path)
btn2_image_tk = ImageTk.PhotoImage(btn2_image_pil)

btn2_image_pil_resized = btn2_image_pil.resize((300, 70))
btn2_image_tk_resized = ImageTk.PhotoImage(btn2_image_pil_resized)

btn1 = tk.Button(window,
                 image = btn2_image_tk_resized,
                 bg = 'black',
                 bd = 0,
                 command = open_popup)  # 클릭 시 실행될 함수 지정

btn1.place(x = 430, y = 480)

window.mainloop()