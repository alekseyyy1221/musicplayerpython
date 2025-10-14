from tkinter import *
from tkinter import DoubleVar
from os import mkdir,listdir
import json
from tkinter.messagebox import showinfo, showerror

import tkinter.ttk as ttk

SCREEN_SIZE = (1000,600)
INTERVAL = 10
try:
    mkdir('albums')
except:
    print("Уже создана")
try:
    mkdir('storage_icon')
except:
    print("Уже создана")
print(listdir('icons'))

def format_image(image) -> PhotoImage:
    if image.width() > 90 and image.height() > 90:
        image = image.subsample(round(image.width() / 90),round(image.height() / 90))
    elif image.width() > 90:
        image = image.subsample(round(image.width() / 90), 1)
    elif image.height() > 90:
        image = image.subsample(1, round(image.height() / 90))
    if image.width() < 90 and image.height() < 90:
        image = image.zoom(round(90 / image.width()),round(90 / image.height()))
    elif image.width() < 90:
        image = image.zoom(90 / round(image.width()), 1)
    elif image.height() < 90:
        image = image.zoom(1, 90 / round(image.height()))
    return image

class Albums:
    def __init__(self,canvas):
        self.albums = {}
        self.canvas = canvas

    def add_album(self,name,path_image):
        try:
            mkdir(f'albums/{name}')
        except FileExistsError:
            print('Ошибка','Такой альбом уже создан')

        try:
            with open('storage_icon/path_icon_album.json','r') as file:
                path_icon = json.load(file)
                path_icon[f'{name}'] = path_image
                print(path_icon)
            with open('storage_icon/path_icon_album.json', 'w') as file:
                json.dump(path_icon,file,sort_keys=True)
        except:
            with open('storage_icon/path_icon_album.json', 'w') as file:
                json.dump({f'{name}':path_image},file)

    def get_track_list(self,event):
        print('ура мы получили трек')
        pass

    def update_list_albums(self):
        dict_path_icon_album = None
        # ICONS[f'{self.name}'] = PhotoImage(file="D:/Programs/Загрузки/play.png")
        # temp_var3 = format_image(temp_var1)
        # # temp_var2 = ttk.Button(width=10,image=temp_var1,command=self.get_track_list)
        # # temp_var3 = self.canvas.create_window(20,20,anchor=NW,window=temp_var2)
        # temp_var2 = self.canvas.create_image(20,20,image=temp_var3,anchor=NW)
        # print(temp_var1,self.canvas.itemcget(temp_var2,'image'),'<<<<')
        try:
            with open('storage_icon/path_icon_album.json') as file:
                dict_path_icon_album = json.load(file)
        except:
            print('нет, альбомов')

        for album in listdir('albums'):
            coords = ()
            if len(self.albums) == 0:
                coords = (40,40)
            elif len(self.albums) % 2 == 0:
                coords = (40,40+(120+20)*(len(self.albums)-1))
            else:
                coords = (160,40+(120+20)*(len(self.albums)-1))

            ICONS[f'{album}'] = PhotoImage(file=str(dict_path_icon_album[album]))
            ICONS[f'{album}'] = format_image(ICONS[f'{album}'])
            print(coords,album,self.albums,self.canvas)
            self.albums[album] = self.canvas.create_image(coords[0],coords[1],image=ICONS[f'{album}'],anchor=NW)
            temp = Label(text=f'{album}')
            temp.config(bg='grey90')
            self.canvas.create_window(coords[0],coords[1]+ICONS[f'{album}'].height(),anchor=NW,window=temp)
            self.canvas.tag_bind(self.albums[album],'<Button-1>',self.get_track_list)




class ImageButton:
    def __init__(self,canvas,coords,image,command):
        self.canvas = canvas
        self.imagebutton = canvas.create_image(coords[0],coords[1],image=image,anchor=CENTER)
        canvas.tag_bind(self.imagebutton,'<Button-1>',command)

    def update_coords(self,new_coords):
        self.canvas.coords(self.imagebutton,new_coords[0],new_coords[1])

    def update_image(self,new_image):
        self.canvas.itemconfig(self.imagebutton,image=new_image)

    def get_image(self):
        return self.canvas.itemcget(self.imagebutton,'image')


def update_size(event):
    new_screen_size = (screen.winfo_width(),screen.winfo_height())
    main_canvas.config(width=new_screen_size[0], height=(new_screen_size[1] - 100 - INTERVAL * 2))
    album_list.config(height=main_canvas.winfo_height())


def update_place_widgets(event):
    # new_screen_size = (screen.winfo_width(), screen.winfo_height())
    # chosen_music.coords(button_play, chosen_music.winfo_width() // 2, chosen_music.winfo_height() // 2)
    play_button.update_coords((chosen_music.winfo_width() // 2, chosen_music.winfo_height() // 2))
    next_button.update_coords((chosen_music.winfo_width() // 2 + 50, chosen_music.winfo_height() // 2))
    prev_button.update_coords((chosen_music.winfo_width() // 2 - 55, chosen_music.winfo_height() // 2-1))
    repeat_button.update_coords((chosen_music.winfo_width() // 2 +100, chosen_music.winfo_height() // 2 +2))
    volume_button.update_coords((chosen_music.winfo_width()-180, chosen_music.winfo_height() // 2 +2))
    chosen_music.coords(volume_scale_id, chosen_music.winfo_width() -100, chosen_music.winfo_height() // 2-6)

def update_volume(value):
    print(volume_button.get_image())
    if float(value) == 0:
        volume_button.update_image(ICONS['volume_off'])
    elif volume_button.get_image() == 'pyimage20':
        volume_button.update_image(ICONS['volume'])
    else:
        return

def update_repeat(event):
    global repeat_var
    if repeat_var is None:
        print(repeat_var)
        repeat_var = False
        repeat_button.update_image(ICONS['repeat'])
        return
    if not repeat_var:
        print(repeat_var)
        repeat_var = True
        repeat_button.update_image(ICONS['repeat_one'])
        return
    if repeat_var:
        print(repeat_var)
        repeat_var = None
        repeat_button.update_image(ICONS['repeat_off'])
        return

def update_play(event):
    pass



def volume_off_on(event):
    global last_volume_var
    global volume_var
    if volume_var.get() != 0:
        last_volume_var.set( volume_var.get())
        volume_var.set(0)
        update_volume(volume_var.get())
    else:
        volume_var.set(last_volume_var.get())
        last_volume_var.set(0)
        update_volume(volume_var.get())


def get_info(event):
    print([main_canvas.winfo_width(), main_canvas.winfo_height()], [screen.winfo_width(), screen.winfo_height()])
def enter_canvas(event)-> None:
    print(event.x,event.y)

# def add_album(event=None):
#     album = Albums(album_list,'test',ICONS['default'],get_info,(20,20))

screen = Tk()
screen.geometry(f'{SCREEN_SIZE[0]}x{SCREEN_SIZE[1]}')
screen.title("MusicPlayer")
try:
    icon = PhotoImage(file="icons/iconPlayer.png")
    screen.iconphoto(True, icon)
except:
    print("Файл иконки не найден")

ICONS = {
    'default':PhotoImage(file='icons/iconPlayer.png'),
    'next':PhotoImage(file='icons/next.png').subsample(10, 10),
    'pause':PhotoImage(file='icons/pause.png').subsample(10,10),
    'play':PhotoImage(file='icons/play.png').subsample(10,10),
    'prev':PhotoImage(file='icons/prev.png').subsample(10,10),
    'repeat':PhotoImage(file='icons/repeat.png').subsample(10,10),
    'repeat_off':PhotoImage(file='icons/repeat_off.png').subsample(10,10),
    'repeat_one':PhotoImage(file='icons/repeat_one.png').subsample(10,10),
    'volume':PhotoImage(file='icons/volume.png').subsample(14,14),
    'volume_off':PhotoImage(file='icons/volume_off.png').subsample(16,16),
}

if ICONS['default'].width() > 90 and ICONS['default'].height() > 90:
    ICONS['default'] = ICONS['default'].subsample(round(ICONS['default'].width()/90),round(ICONS['default'].height()/90))
elif ICONS['default'].width() > 90:
    ICONS['default'] = ICONS['default'].subsample(round(ICONS['default'].width()/90),1)
elif ICONS['default'].height() > 90:
    ICONS['default'] = ICONS['default'].subsample(1,round(ICONS['default'].height()/90))

main_canvas = Canvas(bg="gray95", width=SCREEN_SIZE[0], height=(SCREEN_SIZE[1] - 100 - INTERVAL * 2))
main_canvas.pack(anchor=SW, expand=True, fill=Y)
album_frame = Frame(main_canvas)
album_list = Canvas(album_frame,background='gray90',width=int(main_canvas.cget('width'))-700,height=main_canvas.cget('height'))
scroll_bar_albums = Scrollbar(album_frame,orient=VERTICAL, command=album_list.yview, width=15,background='gray90')
scroll_bar_albums_size = 15
album_list.config(yscrollcommand=scroll_bar_albums.set)
album_list.grid(row=0,column=0,sticky='nsew')
scroll_bar_albums.grid(row=0,column=1,sticky=NS)
album_frame.grid_rowconfigure(0, weight=1)
album_frame.grid_columnconfigure(0, weight=1)
album_list_id = main_canvas.create_window(0,0,window=album_frame,anchor=NW)

# for i in range(1,100):
#     album_list.create_rectangle(0, 0 + i * 100, 100, 100 + i * 100, fill='pink')
album_list.configure(scrollregion=album_list.bbox(ALL))

b = Albums(album_list)
b.add_album('test3','icons/next.png')
b.update_list_albums()
# c = format_image(PhotoImage(file="C:/Users/bozdy/OneDrive/Pictures/Screenshots/Снимок экрана 2025-05-11 011833.png"))
# hp = album_list.create_image(40,40,image=c,anchor=NW)
album_list.configure(scrollregion=album_list.bbox(ALL))



chosen_music = Canvas(bg="gray90", width=SCREEN_SIZE[0], height=100)
chosen_music.pack(anchor=S, expand=True,fill='x')
volume_var = DoubleVar(value=50.0)
last_volume_var = DoubleVar()
repeat_var = None
play_button = ImageButton(chosen_music,((int(chosen_music.cget("width"))// 2,int(chosen_music.cget('height'))// 2)),ICONS['play'],get_info)
next_button = ImageButton(chosen_music,((int(chosen_music.cget("width"))// 2+50,int(chosen_music.cget('height'))// 2)),ICONS['next'],get_info)
prev_button = ImageButton(chosen_music,((int(chosen_music.cget("width"))// 2-55,int(chosen_music.cget('height'))// 2-1)),ICONS['prev'],get_info)
repeat_button = ImageButton(chosen_music,((int(chosen_music.cget("width"))// 2+100,int(chosen_music.cget('height'))// 2+2)),ICONS['repeat_off'],update_repeat)
volume_button = ImageButton(chosen_music,((int(chosen_music.cget("width"))-180,int(chosen_music.cget('height'))// 2+2)),ICONS['volume'],volume_off_on)
volume_scale = Scale(orient=HORIZONTAL,length=100,from_=0,to=100,bg='grey90',highlightbackground='grey90',variable=volume_var,command=update_volume)
volume_scale_id = chosen_music.create_window(int(chosen_music.cget("width"))-100,int(chosen_music.cget('height'))// 2-6,anchor=CENTER,window=volume_scale)
try:
    ICONS['icon_chosen_music'] = PhotoImage(file="C:/Users/bozdy/OneDrive/Pictures/Screenshots/Снимок экрана 2025-06-01 123922.png")
    if ICONS['icon_chosen_music'].width() > 90 and ICONS['icon_chosen_music'].height() > 90:
        ICONS['icon_chosen_music'] = ICONS['icon_chosen_music'].subsample(round(ICONS['icon_chosen_music'].width()/90),round(ICONS['icon_chosen_music'].height()/90))
    elif ICONS['icon_chosen_music'].width() > 90:
        ICONS['icon_chosen_music'] = ICONS['icon_chosen_music'].subsample(round(ICONS['icon_chosen_music'].width()/90),1)
    elif ICONS['icon_chosen_music'].height() > 90:
        ICONS['icon_chosen_music'] = ICONS['icon_chosen_music'].subsample(1,round(ICONS['icon_chosen_music'].height()/90))
    icon_chosen_music_id = chosen_music.create_image(50, 50, image=ICONS['icon_chosen_music'], anchor=CENTER)
except:
    icon_chosen_music_id = chosen_music.create_image(50, 50, image=ICONS['default'], anchor=CENTER)


main_canvas.bind("<Configure>", update_size)
chosen_music.bind("<Configure>",update_place_widgets)

Interval_south = Canvas(screen, height=INTERVAL)
Interval_south.pack(anchor=S,fill="x", expand=False)

screen.mainloop()


