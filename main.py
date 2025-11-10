from tkinter import *
from tkinter import DoubleVar
from os import mkdir, listdir, rmdir
import json
from tkinter.messagebox import showinfo, showerror
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from PIL import Image,ImageTk
from shutil import move,copy
from mutagen.mp3 import *
import mutagen.flac as flac
import mutagen.wave as wave
from mutagen.id3 import APIC,TIT2,TPE1,TCON
import io

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

# def format_image(image) -> PhotoImage:
#     if image.width() > 90 and image.height() > 90:
#         image = image.subsample(round(image.width() / 90),round(image.height() / 90))
#     elif image.width() > 90:
#         image = image.subsample(round(image.width() / 90), 1)
#     elif image.height() > 90:
#         image = image.subsample(1, round(image.height() / 90))
#     if image.width() < 90 and image.height() < 90:
#         image = image.zoom(round(90 / image.width()),round(90 / image.height()))
#     elif image.width() < 90:
#         image = image.zoom(90 / round(image.width()), 1)
#     elif image.height() < 90:
#         image = image.zoom(1, 90 / round(image.height()))
#     return image

def get_metadata_icon(path,extansion) -> PhotoImage:
    if extansion == 'mp3':
        if MP3(path).tags.getall('APIC'):
            apic = MP3(path).tags.getall('APIC')[0]
            image = ImageTk.PhotoImage(Image.open(io.BytesIO(apic.data)).resize((90,90)))
            return image
        else:
            print('Нет обложки')
            return ICONS['default']
    if extansion == 'flac':
        if flac.FLAC(path).pictures:
            image_raw = flac.FLAC(path).pictures[0].data
            image = ImageTk.PhotoImage(Image.open(io.BytesIO(image_raw)).resize((90,90)))
            return image
        else:
            print('Нет обложки')
            return ICONS['default']
    if extansion == 'wav':
        if wave.WAVE(path).tags.getall('APIC'):
            apic = wave.WAVE(path).tags.getall('APIC')[0]
            image = ImageTk.PhotoImage(Image.open(io.BytesIO(apic.data)).resize((90, 90)))
            return image
        else:
            print('Нет обложки')
            return ICONS['default']

    print(f'Неизвестное расширение {extansion}')
    return ICONS['default']

def get_metadata(path,extansion):
    dict_metadata = {}
    if extansion == 'mp3':
        temp = MP3(path)
        if temp:
            if 'TIT2' in temp.keys():
                dict_metadata['name'] = temp['TIT2']
            if 'TPE1' in temp.keys():
                dict_metadata['author'] = temp['TPE1']
            if 'TCON' in temp.keys():
                dict_metadata['genre'] = temp['TCON']
            return dict_metadata
        else:
            print('Нет метаданных')
            return
    if extansion == 'flac':
        temp = flac.FLAC(path)
        if temp:
            if 'title' in temp.keys():
                dict_metadata['name'] = temp['title'][0]
            if 'artist' in temp.keys():
                dict_metadata['author'] = temp['artist'][0]
            if 'genre' in temp.keys():
                dict_metadata['genre'] = temp['genre'][0]
            return dict_metadata
        else:
            print('Нет метаданных')
            return
    if extansion == 'wav':
        temp = wave.WAVE(path)
        if temp:
            if 'TIT2' in temp.keys():
                dict_metadata['name'] = temp['TIT2']
            if 'TPE1' in temp.keys():
                dict_metadata['author'] = temp['TPE1']
            if 'TCON' in temp.keys():
                dict_metadata['genre'] = temp['TCON']
            return dict_metadata
        else:
            print('Нет метаданных')
            return

    print(f'Неизвестное расширение {extansion}')
    return

class AddMusic:
    def __init__(self):
        self.newscreen = Toplevel()
        self.newscreen.geometry('600x250')
        self.newscreen.title('Добавление нового трека')
        self.newscreen.protocol("WM_DELETE_WINDOW", lambda: self.dismiss())

        self.absolut_path = None
        self.icon_music = None
        self.extansion = ''
        self.changed_icon = None
        check = (self.newscreen.register(self.check_len_text), "%P")

        self.image_canvas = Canvas(self.newscreen,width=100,height=100,bg='white')
        self.image_canvas.pack(anchor=NW,pady=10,padx=10,side=LEFT)

        self.path_label = Label(self.newscreen,text='',bg='grey90')
        self.path_label.pack(anchor=NW,pady=13,padx=1,side=LEFT)
        chose_button = ttk.Button(self.newscreen,width=15,command=self.get_path,text='Выбрать файл')
        chose_button.pack(anchor=NW, pady=10, padx=1,side=LEFT)

        self.name_track = StringVar()
        self.author_track = StringVar()
        self.genre_track = StringVar()
        Label(self.newscreen,text='Название:').place(anchor=NW, x=122, y=40)
        name_track_entry = ttk.Entry(self.newscreen, width=50, validate='key', validatecommand=check,
                                          textvariable=self.name_track)
        name_track_entry.place(anchor=NW, x=122, y=60)
        Label(self.newscreen, text='Автор:').place(anchor=NW, x=122, y=85)
        author_track_entry = ttk.Entry(self.newscreen, width=50, validate='key', validatecommand=check,
                                     textvariable=self.author_track)
        author_track_entry.place(anchor=NW, x=122, y=105)
        Label(self.newscreen, text='Жанры:').place(anchor=NW, x=122, y=130)
        genre_track_entry = ttk.Entry(self.newscreen, width=50, validate='key', validatecommand=check,
                                     textvariable=self.genre_track)
        genre_track_entry.place(anchor=NW, x=122, y=150)
        self.new_icon_button = ttk.Button(self.newscreen, width=15, command=self.change_icon, text='Изменить обложку',state=DISABLED)
        self.new_icon_button.place(anchor=NW,x=10,y=120)
        self.newscreen.grab_set()
        self.check_copy = BooleanVar(value=False)
        ttk.Checkbutton(self.newscreen,text='Удалить исходный файл?',variable=self.check_copy).place(anchor=NW,x=122,y=180)
        ttk.Button(self.newscreen, width=15, command=self.dismiss, text='Отмена').pack(anchor=SE, padx=10, pady=10,side=RIGHT)
        ttk.Button(self.newscreen,width=15,command=self.confirm,text='Принять').pack(anchor=SE,padx=10,pady=10,side=RIGHT)


    def get_path(self):
        self.absolut_path = askopenfilename(filetypes=[('audio files',('*.MP3','*.WAV','*.FLAC'))])
        if self.absolut_path == '':
            return
        self.new_icon_button.config(state='')
        self.image_canvas.delete('image')
        self.extansion = ''
        for i in range(len(self.absolut_path) - 1, 0, -1):
            if self.absolut_path[i] == '.':
                break
            self.extansion += self.absolut_path[i]
        self.extansion = self.extansion[::-1]
        self.path_label['text'] = self.absolut_path
        self.icon_music = get_metadata_icon(self.absolut_path,self.extansion)
        print(self.icon_music.width(),self.icon_music.height())
        self.image_canvas.create_image(5,5,image=self.icon_music,anchor=NW,tags = 'image')
        metadata = get_metadata(self.absolut_path,self.extansion)
        if type(metadata) is dict:
            if 'name' in metadata.keys():
                self.name_track.set(f'{metadata['name']}.{self.extansion}')
            if 'author' in metadata.keys():
                self.author_track.set(metadata['author'])
                print(metadata['author'])
            if 'genre' in metadata.keys():
                self.genre_track.set(metadata['genre'])
                print(metadata['genre'])

    def change_icon(self):
        path_to_icon = askopenfilename(filetypes=[('image files', '*.png')])
        if path_to_icon == '':
            return
        try:
            self.icon_music = ImageTk.PhotoImage(Image.open(path_to_icon).resize((90,90)))
            self.changed_icon = path_to_icon
            self.image_canvas.delete('image')
            self.image_canvas.create_image(5, 5, image=self.icon_music, anchor=NW, tags='image')
        except FileNotFoundError:
            print('Файл ненайден')


    def check_len_text(self, text):
        if len(text) <= 20:
            return True
        return False
    def confirm(self):
        pass
    def dismiss(self):
        self.newscreen.grab_release()
        self.newscreen.destroy()




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
        self.Button_cancel = ttk.Button(self.newscreen, text='Отмена', command=self.dismiss)
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
    def __init__(self,canvas,canvas_for_music):
        self.albums = {}
        self.canvas = canvas
        self.albums_image = {}
        self.albums_coords_size = {}
        self.albums_track_list = {}
        self.track_list = MusicList(canvas_for_music)
        self.selected_album =None
        self.open_album = None

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
        self.albums_track_list['name'] = MusicList(self.canvas)
        self.unselect_album()
        self.update_list_albums()

    def unselect_album(self,event=None):
        if self.selected_album is None:
            return
        self.selected_album = None
        self.canvas.delete('select')

    def select_album(self,event):
        self.unselect_album('NonEvent')
        search_coords = []
        if len(self.albums_coords_size) != 1:
            if event.x >= 150:
                search_coords.append(160)
            else:
                search_coords.append(40)
            coff = round(event.y / 140)
            if coff < 1:
                search_coords.append(40)
            else:
                row_list = []
                for row in range(len(self.albums_coords_size)):
                    row_list.append((30+140*row,130+140*row))
                row_album = None
                for row in range(len(row_list)):
                    if event.y == row_list[row][0]:
                        row_album = row_list[row]
                        break
                    elif event.y < row_list[row][0]:
                        row_album = row_list[row-1]
                        break
                if row_album is None:
                    return
                search_coords.append(row_album[0]+10)
        else:
            search_coords.append(40)
            search_coords.append(40)
        search_coords_tuple = (search_coords[0],search_coords[1])
        self.selected_album = self.albums_coords_size[search_coords_tuple]
        select_rectangle = self.canvas.create_rectangle(search_coords_tuple[0]-10,search_coords_tuple[1]-10,
                                                        search_coords_tuple[0]+100,search_coords_tuple[1]+100,
                                                        fill='yellow',outline='yellow',tags='select')
        if self.open_album is None:
            self.canvas.tag_lower(select_rectangle)
        else:
            self.canvas.tag_lower(select_rectangle)
            self.canvas.tag_raise(select_rectangle,'opened')


    def get_track_list(self,event):
        print('получен трек лист')
        self.canvas.delete('opened')
        search_coords = []
        if event.x >= 150:
            search_coords.append(160)
        else:
            search_coords.append(40)
        coff = round(event.y / 140)
        if coff < 1:
            search_coords.append(40)
        else:
            row_list = []
            for row in range(len(self.albums_coords_size)):
                row_list.append((30 + 140 * row, 130 + 140 * row))
            row_album = None
            for row in range(len(row_list)):
                if event.y == row_list[row][0]:
                    row_album = row_list[row]
                    break
                elif event.y < row_list[row][0]:
                    row_album = row_list[row - 1]
                    break
            if row_album is None:
                return
            search_coords.append(row_album[0] + 10)
        search_coords_tuple = (search_coords[0], search_coords[1])
        self.open_album = self.albums_coords_size[search_coords_tuple]
        open_rectangle = self.canvas.create_rectangle(search_coords_tuple[0] - 15, search_coords_tuple[1] - 15,
                                                        search_coords_tuple[0] + 105, search_coords_tuple[1] + 105,
                                                        fill='purple', outline='purple', tags='opened')
        if self.selected_album is None:
            self.canvas.tag_lower(open_rectangle)
        else:
            self.canvas.tag_lower(open_rectangle,'select')
        self.track_list.update_musiclist()



    def update_list_albums(self):
        dict_path_icon_album = None
        try:
            with open('storage_icon/path_icon_album.json') as file:
                dict_path_icon_album = json.load(file)
        except:
            print('нет, альбомов')
        self.canvas.delete('albums')
        self.canvas.delete('label')
        self.albums.clear()
        self.albums_image.clear()
        for album in sorted(listdir('albums')):
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
                self.albums_image[f'{album}'] = ImageTk.PhotoImage(Image.open(str(dict_path_icon_album[album])).resize((90,90)))
            except FileNotFoundError:
                self.albums_image[f'{album}'] = ICONS['default']
                print('Ошибка, файл не найден')

            print(coords,album,self.albums,self.canvas)
            self.albums[album] = self.canvas.create_image(coords[0],coords[1],image=self.albums_image[f'{album}'],anchor=NW,)
            self.albums_coords_size[coords] = album
            print(self.albums_coords_size)
            temp = Label(text=f'{album[:20]+'...' if len(album) > 20 else album}')
            temp.config(bg='grey90')
            self.canvas.create_window(coords[0],coords[1]+self.albums_image[f'{album}'].height(),anchor=NW,window=temp,tags=[f'{album}',f'label'])
            print(self.albums,'<><><><><>')
            self.canvas.tag_bind(self.albums[f'{album}'],'<Button-1>',self.select_album)
            self.canvas.tag_bind(self.albums[f'{album}'], '<Button-3>', self.unselect_album)
            self.canvas.tag_bind(self.albums[f'{album}'], '<Double-Button-1>', self.get_track_list)

    def del_album(self,name):
        if not f'{name}' in self.albums.keys():
            print('KeyError:такого альбома нет')
            showerror('KeyError','такого альбома нет')
            return
        if listdir(f'albums/{name}'):
            showerror('Ошибка', "Альбом не пуст")
            return
        if self.open_album == name:
            showerror('Ошибка', "НЕвозможно удалить открытый альбом")
            return
        dict_path_icon_album = {}
        try:
            with open('storage_icon/path_icon_album.json') as file:
                dict_path_icon_album = json.load(file)
            dict_path_icon_album.pop(f'{name}')
            with open('storage_icon/path_icon_album.json', 'w') as file:
                json.dump(dict_path_icon_album,file,sort_keys=True)
                self.canvas.tag_unbind(self.albums[f'{name}'],'<Button-1>')
                self.canvas.tag_unbind(self.albums[f'{name}'], '<Button-3>')
                self.canvas.tag_unbind(self.albums[f'{name}'], '<Double-Button-1>')
                self.albums.pop(f'{name}')
                self.albums_image.pop(f'{name}')
                self.canvas.delete(f'{name}')
                self.albums_coords_size.clear()
                self.unselect_album()
                rmdir(f'albums/{name}')

        except:
            print('нет, альбомов')
            showerror('Ошибка','Нет, альбомов' )
            return
        self.update_list_albums()

class MusicList:
    def __init__(self,canvas):
        self.canvas = canvas
        self.musiclist = {}
        self.icon_list = {}
        self.icon_list_id = {}
        print(self.musiclist)

    def add_music(self,name,extensions,absolute_path,copying,new_icon,author,genre):
        if not copying:
            try:
                copy(absolute_path,f'albums/{init_albums.open_album}/{name}.{extensions}')
            except:
                print('Ненайден файл')
        else:
            try:
                move(absolute_path,f'albums/{init_albums.open_album}/{name}.{extensions}')
            except:
                print('Ненайден файл')
        if extensions == 'mp3':
            temp = MP3(f'albums/{init_albums.open_album}/{name}.{extensions}')
            if not (new_icon is None):
                print(temp.keys())
                if 'APIC:' in temp.keys():
                    del temp['APIC:']
                with open(new_icon,'rb') as f:
                    data = f.read()
                temp['APIC'] = APIC(encoding=3, mime='image/png', data=bytes(data))
                temp['TIT2'] = TIT2(encoding=3,text=[f'{name}'])
                temp['TPE1'] = TPE1(encoding=3,text=[f'{author}'])
                temp['TCON'] = TCON(encoding=3,text=[f'{genre}'])







        # self.musiclist[f'{name}.{extensions}'] = f'albums/{init_albums.open_album}/{name}.{extensions}'

    def update_musiclist(self):
        self.canvas.delete('music_main_canvas')
        self.musiclist.clear()
        self.icon_list.clear()
        self.icon_list_id.clear()
        path_album = f'albums/{init_albums.open_album}'
        try:
            list_music = listdir(path_album)
        except FileNotFoundError:
            print('альбом не был найден')
            return
        for music in list_music:
            coords = ()
            extension = ''
            if len(self.musiclist) == 0:
                coords = (30,30)
            else:
                coords = (30+100*len(self.musiclist),20+100*len(self.musiclist))
            for i in range(len(music) - 1, 0, -1):
                if music[i] == '.':
                    break
                extension += music[i]
            extension = extension[::-1]
            metadata = get_metadata(f'{path_album}/{music}', extension)
            print(metadata)
            self.icon_list[f'{music}'] =  get_metadata_icon(f'{path_album}/{music}',extension)
            self.musiclist[f'{music}'] = Canvas(width=int(self.canvas.cget('width'))-30,height=100,bg='grey90')
            self.canvas.create_window(coords[0],coords[1], window=self.musiclist[f'{music}'],tags='music_main_canvas',anchor=NW)
            self.icon_list_id[f'{music}'] =  self.musiclist[f'{music}'].create_image(5,5,image=self.icon_list[f'{music}'],anchor=NW)
            self.musiclist[f'{music}'].create_text(100,10,text=f'{metadata['name']}',anchor=NW,font='arial 20')
            self.musiclist[f'{music}'].create_text(100,40, text=f'{metadata['author']}', anchor=NW,font='arial 15')
            self.musiclist[f'{music}'].create_text(100, 65, text=f'{metadata['genre']}', anchor=NW, font='arial 15')
            print(self.icon_list)
            print(self.icon_list_id)










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
    music_list.config(width=(main_canvas.winfo_width() - 335), height=main_canvas.winfo_height())


def update_place_widgets(event):
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

def delete_album():
    init_albums.del_album(init_albums.selected_album)

def new_window_add_music():
    window = AddMusic()

def delete_music():
    pass



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
    'default':ImageTk.PhotoImage(Image.open('icons/iconPlayer.png').resize((90,90))),
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
menu = Menu(bg='grey90',tearoff=0)
album_menu = Menu(bg='grey90',tearoff=0)
album_menu.add_command(label='Добавить альбом',command=new_window_add_album)
album_menu.add_command(label='Удалить выбранный альбом',command=delete_album)
music_menu = Menu(bg='grey90',tearoff=0)
music_menu.add_command(label='Добавить трек',command=new_window_add_music)
music_menu.add_command(label='Удалить выбранный трек',command=delete_music)
menu.add_cascade(label='album list',menu=album_menu)
menu.add_cascade(label='music list',menu=music_menu)
screen.config(menu=menu)
button_add_album = ttk.Button(width=10,text='+',command=new_window_add_album)
album_list.create_window(10,10,anchor=NW,window=button_add_album)
button_add_album = ttk.Button(width=10,text='-',command=delete_album)
album_list.create_window(90,10,anchor=NW,window=button_add_album)

# for i in range(1,100):
#     album_list.create_rectangle(0, 0 + i * 100, 100, 100 + i * 100, fill='pink')
album_list.configure(scrollregion=album_list.bbox(ALL))

music_frame = Frame(main_canvas)
music_list = Canvas(music_frame, background='white', width=int(main_canvas.cget('width')) - 335, height=main_canvas.cget('height'))
scroll_bar_music = Scrollbar(music_frame, orient=VERTICAL, command=music_list.yview, width=15, background='grey90')
music_list.config(yscrollcommand=scroll_bar_music.set)
music_list.grid(row=0, column=2, sticky='nsew')
scroll_bar_music.grid(row=0, column=3, sticky=NS)
music_frame.grid_rowconfigure(2, weight=1)
music_frame.grid_columnconfigure(2, weight=1)
music_list_id = main_canvas.create_window(315, 0, window=music_frame, anchor=NW)
music_list.configure(scrollregion=music_list.bbox(ALL))
# test_button = ttk.Button(width=15,command=test_def)
# music_list.create_window(100,100,window=test_button,anchor=NW)

init_albums = Albums(album_list,music_list)
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


