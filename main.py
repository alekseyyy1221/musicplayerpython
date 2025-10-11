from tkinter import *
from tkinter.ttk import *

SCREEN_SIZE = (1000,600)
INTERVAL = 10

class ImageButton:
    def __init__(self,canvas,coords,image,command):
        self.canvas = canvas
        self.imagebutton = canvas.create_image(coords[0],coords[1],image=image,anchor=CENTER)
        canvas.tag_bind(self.imagebutton,'<Button-1>',command)

    def update_coords(self,new_coords):
        self.canvas.coords(self.imagebutton,new_coords[0],new_coords[1])


def update_size(event):
    new_screen_size = (screen.winfo_width(),screen.winfo_height())
    album_list.config(height=(new_screen_size[1]-100-INTERVAL*2))

def update_size_widgets(event):
    new_screen_size = (screen.winfo_width(), screen.winfo_height())
    # chosen_music.coords(button_play, chosen_music.winfo_width() // 2, chosen_music.winfo_height() // 2)
    play_button.update_coords((chosen_music.winfo_width() // 2, chosen_music.winfo_height() // 2))



def get_info(event):
    print( [album_list.winfo_width(),album_list.winfo_height()],[screen.winfo_width(),screen.winfo_height()])
def enter_canvas(event)-> None:
    print(event.x,event.y)

screen = Tk()
screen.geometry(f'{SCREEN_SIZE[0]}x{SCREEN_SIZE[1]}')
screen.title("MusicPlayer")
try:
    icon = PhotoImage(file="icons/iconPlayer.png")
    screen.iconphoto(True, icon)
except:
    print("Файл иконки не найден")

ICONS = {
    'next':PhotoImage(file='icons/next.png').subsample(10,10),
    'pause':PhotoImage(file='icons/pause.png').subsample(10,10),
    'play':PhotoImage(file='icons/play.png').subsample(10,10),
    'prev':PhotoImage(file='icons/prev.png').subsample(10,10),
    'repeat':PhotoImage(file='icons/repeat.png').subsample(10,10)
}

album_list = Canvas(bg="gray90", width=396, height=(SCREEN_SIZE[1] - 100 - INTERVAL*2))
album_list.pack(anchor=SW,expand=True,fill=Y)




chosen_music = Canvas(bg="gray90", width=SCREEN_SIZE[0], height=100)
chosen_music.pack(anchor=S, expand=True,fill='x')
play_button = ImageButton(chosen_music,((int(chosen_music.cget("width"))// 2,int(chosen_music.cget('height'))// 2)),ICONS['play'],get_info)

# button = Button(text='123', command=get_info)
#
# button_play = chosen_music.create_window((int(chosen_music.cget("width"))// 2),(int(chosen_music.cget('height'))// 2),anchor=CENTER, window=button)

album_list.bind("<Configure>",update_size)
chosen_music.bind("<Configure>",update_size_widgets)


Interval_south = Canvas(screen, height=INTERVAL)
Interval_south.pack(anchor=S,fill="x", expand=False)


screen.mainloop()


