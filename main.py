from tkinter import *
from tkinter import DoubleVar
from os import mkdir, listdir, rmdir
import json
from tkinter.messagebox import showinfo, showerror
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from PIL import Image,ImageTk

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


class AddAlbum:
    def __init__(self):
        self.newscreen = Toplevel()
        self.newscreen.geometry('400x200')
        self.newscreen.title('Добавление нового альбома')
        self.newscreen.protocol("WM_DELETE_WINDOW", lambda: self.dismiss())
        Label(self.newscreen, text='Введите имя альбома:').pack(anchor=NW, padx=10, pady=10)
        check = (self.newscreen.register(self.check_len_text), "%P")
        self.album_maybe_name = StringVar()
        self.album_name_entry = ttk.Entry(self.newscreen, width=50, validate='key', validatecommand=check,
                                          textvariable=self.album_maybe_name)
        self.album_name_entry.pack(anchor=NW, padx=10)
        Label(self.newscreen, text='Выберите иконку альбома:').pack(anchor=NW, padx=10, pady=10)
        self.Button_add_path = ttk.Button(self.newscreen, text='Выбрать', command=self.get_path)
        self.Button_add_path.pack(anchor=NW, padx=10)
        self.icon_maybe_path = ''
        self.path_label = Label(self.newscreen, text=f'{self.icon_maybe_path}', background='white')
        self.path_label.pack(anchor=NW, padx=10)
        self.Button_cancel = ttk.Button(self.newscreen, text='Отмена', command=lambda: self.dismiss)
        self.Button_cancel.pack(anchor=S, padx=5, side=RIGHT)
        self.Button_ok = ttk.Button(self.newscreen, text='Принять',command=self.confirm)
        self.Button_ok.pack(anchor=SE, padx=5, side=RIGHT)
        self.newscreen.grab_set()

    def get_path(self):
        self.icon_maybe_path = askopenfilename(filetypes=[('image files', '*.png')])
        self.path_label['text'] = self.icon_maybe_path

    def confirm(self):
        data = self.album_maybe_name.get(),self.icon_maybe_path
        self.dismiss()
        init_albums.add_album(data[0],data[1])

    def check_len_text(self, text):
        if len(text) <= 20:
            return True
        return False

    def dismiss(self):
        self.newscreen.grab_release()
        self.newscreen.destroy()

class Albums:
    def __init__(self,canvas):
        self.albums = {}
        self.canvas = canvas
        self.albums_image = {}
        self.albums_coords_size = {}

    def add_album(self,name,path_image):
        if len(f'{name}') > 20:
            showerror('Ошибка', 'Слишком длинное имя альбома')
            return
        try:
            mkdir(f'albums/{name}')
        except FileExistsError:
            print('Ошибка','Такой альбом уже создан')
            showerror('Ошибка','Такой альбом уже создан')
            return

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
        self.update_list_albums()

    def select_album(self,event):
        print('ура мы получили трек',event)
        search_coords = []
        if event.x >= 150:
            search_coords.append(150)
        else:
            search_coords.append(40)


        coords =self.albums_coords_size['skelet']
        s = self.canvas.create_rectangle(coords[0][0]-5,coords[0][1]-5,coords[1][0]+5,coords[1][1]+5,fill='yellow',outline='yellow')
        self.canvas.tag_lower(s)
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
        self.canvas.delete('albums')
        self.albums.clear()
        self.albums_image.clear()
        for album in listdir('albums'):
            if not album in dict_path_icon_album.keys():
                print('Обнаружен невалидный альбом')
                continue
            coords = ()
            print(len(self.albums),'<<<<<<')
            if len(self.albums) == 0:
                coords = (40,40)
            elif len(self.albums) == 1:
                coords = (160,40)
            elif len(self.albums) % 2 == 0:
                coords = (40,40+(120+20)*((len(self.albums))//2))
            else:
                coords = (160,40+(120+20)*((len(self.albums)-1)//2))

            try:
                self.albums_image[f'{album}'] = PhotoImage(file=str(dict_path_icon_album[album]))
                self.albums_image[f'{album}'] = format_image(self.albums_image[f'{album}'])
            except TclError as e:
                self.albums_image[f'{album}'] = ICONS['default']
                print('Ошибка, файл не найден')

            print(coords,album,self.albums,self.canvas)
            self.albums[album] = self.canvas.create_image(coords[0],coords[1],image=self.albums_image[f'{album}'],anchor=NW,)
            self.albums_coords_size[album] = (coords,(self.albums_image[album].width()+coords[0],self.albums_image[album].height()+coords[1]))
            print(self.albums_coords_size)
            temp = Label(text=f'{album[:20]+'...' if len(album) > 20 else album}')
            temp.config(bg='grey90')
            self.canvas.create_window(coords[0],coords[1]+self.albums_image[f'{album}'].height(),anchor=NW,window=temp)
            self.canvas.tag_bind(self.albums[f'{album}'],'<Enter>',self.select_album)

    def del_album(self,name):
        if not f'{name}' in self.albums.keys():
            print('KeyError:такого альбома нет')
            showerror('KeyError','такого альбома нет')
            return
        if listdir(f'albums/{name}'):
            showerror('Ошибка', "Альбом не пуст")
            return
        dict_path_icon_album = {}
        try:
            with open('storage_icon/path_icon_album.json') as file:
                dict_path_icon_album = json.load(file)
            dict_path_icon_album.pop(f'{name}')
            with open('storage_icon/path_icon_album.json', 'w') as file:
                json.dump(dict_path_icon_album,file,sort_keys=True)
                self.albums.pop(f'{name}')
                self.albums_image.pop(f'{name}')
                rmdir(f'albums/{name}')

        except:
            print('нет, альбомов')
            showerror('Ошибка','Нет, альбомов' )
            return
        self.update_list_albums()





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
    elif float(value) > 0:
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


# def window_add_album():
#     album_name = None
#     album_name = new_window_add_album()
#     if album_name is None:
#         return
#     print(album_name, '<<<<<<')
    # init_albums.add_album(album_name,icon_path)


def new_window_add_album():
    window = AddAlbum()


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
    'default':PhotoImage(file='icons/iconPlayer.png').subsample(10, 10),
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
button_add_album = ttk.Button(width=10,text='+',command=new_window_add_album)
album_list.create_window(10,10,anchor=NW,window=button_add_album)

# for i in range(1,100):
#     album_list.create_rectangle(0, 0 + i * 100, 100, 100 + i * 100, fill='pink')
album_list.configure(scrollregion=album_list.bbox(ALL))

init_albums = Albums(album_list)
# b.add_album('test3','icons/next.png')
init_albums.update_list_albums()


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


