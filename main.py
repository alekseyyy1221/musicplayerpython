from tkinter import *
from tkinter.ttk import *
SCREEN_SIZE = (1000,600)
INTERVAL = 10
def get_info():
    print( [album_list.winfo_width(),album_list.winfo_height()],[screen.winfo_width(),screen.winfo_height()])
def enter_canvas(event):
    print(event.x,event.y)

screen = Tk()
screen.geometry(f'{SCREEN_SIZE[0]}x{SCREEN_SIZE[1]}')
screen.title("MusicPlayer")
try:
    icon = PhotoImage(file="icon.png")
    screen.iconphoto(True, icon)
except:
    print("Файл иконки не найден")


album_list = Canvas(bg="gray90", width=396, height=(SCREEN_SIZE[1] - 100 - INTERVAL*2))
album_list.pack(anchor=SW,expand=True,fill='y')

chosen_music = Canvas(bg="gray90", width=SCREEN_SIZE[0], height=100)
chosen_music.pack(anchor=S, expand=True,fill='x')

button = Button(text='123', command=get_info)

chosen_music.create_window((int(chosen_music.cget("width"))// 2),(int(chosen_music.cget('height'))// 2),anchor=CENTER, window=button)
chosen_music.bind("<Motion>",enter_canvas)



Interval_south = Canvas(screen, height=INTERVAL)
Interval_south.pack(anchor=S,fill="x", expand=False)


screen.mainloop()


