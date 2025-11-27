from tkinter import *
from tkinter import DoubleVar
from os import mkdir, listdir, rmdir,remove
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
        if not MP3(path).tags is None:
            if MP3(path).tags.getall('APIC'):
                apic = MP3(path).tags.getall('APIC')[0]
                image = ImageTk.PhotoImage(Image.open(io.BytesIO(apic.data)).resize((90,90)))
                return image
            else:
                print('Нет обложки')
                return ICONS['default']
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
        if not wave.WAVE(path).tags is None:
            if wave.WAVE(path).tags.getall('APIC'):
                apic = wave.WAVE(path).tags.getall('APIC')[0]
                image = ImageTk.PhotoImage(Image.open(io.BytesIO(apic.data)).resize((90, 90)))
                return image
            else:
                print('Нет обложки')
                return ICONS['default']
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
        ttk.Button(self.newscreen, width=15, command=self.dismiss, text='Отмена').place(anchor=NW, x=500,y=220)
        ttk.Button(self.newscreen,width=15,command=self.confirm,text='Принять').place(anchor=NW,x=400,y=220)


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
        self.path_label['text'] = self.absolut_path if len(self.absolut_path) <= 65 \
            else '...'+self.absolut_path[::-1][:65][::-1]
        self.icon_music = get_metadata_icon(self.absolut_path,self.extansion)
        print(self.icon_music.width(),self.icon_music.height())
        self.image_canvas.create_image(5,5,image=self.icon_music,anchor=NW,tags = 'image')
        metadata = get_metadata(self.absolut_path,self.extansion)
        if type(metadata) is dict:
            if 'name' in metadata.keys():
                self.name_track.set(f'{metadata['name']}' if len(f'{metadata['name']}') < 20 else f'{metadata['name']}'[:20])
            if 'author' in metadata.keys():
                self.author_track.set(metadata['author'] if len(f'{metadata['author']}') < 20 else f'{metadata['author']}'[:20])
                print(metadata['author'])
            if 'genre' in metadata.keys():
                self.genre_track.set(metadata['genre'] if len(f'{metadata['genre']}') < 20 else f'{metadata['author']}'[:20])
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

    @staticmethod
    def check_len_text(text):
        if len(text) <= 20 and (not  (text[-1] if len(text) > 0 else [''])  in  ('/',"\\" ,':','?','*','<','>','"','|','#','$','{','}','!','[',']','(',')',"'")):
            return True
        return False

    def confirm(self):
        self.dismiss()
        if self.name_track.get() is None or self.name_track.get() == '':
            showerror('Ошибка',"Имя трека не может быть пустым")
            print('Пустое имя файла')
            return
        if self.absolut_path is None or self.absolut_path == '':
            showerror('Ошибка', "Необходимо выбрать файл")
            print('Пустой путь к файлу')
            return
        print(self.name_track.get(),self.extansion,self.absolut_path,self.check_copy.get(),self.changed_icon,self.author_track.get(),self.genre_track.get())
        init_albums.track_list.add_music(self.name_track.get(),self.extansion,self.absolut_path,self.check_copy.get(),self.changed_icon,self.author_track.get(),self.genre_track.get())

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

    @staticmethod
    def check_len_text(text):
        if len(text) <= 20 and (not (text[-1] if len(text) > 0 else ['']) in ('/',"\\" ,':','?','*','<','>','"','|','#','$','{','}','!','[',']','(',')',"'")):
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

    def alb_func_constr_for_select(self,album):
        return lambda event: self.select_album(event,album)

    def alb_func_constr_for_get_track(self,album):
        return lambda event: self.get_track_list(event,album)

    def select_album(self,_,album):
        self.unselect_album('NonEvent')
        # search_coords = []
        # if len(self.albums_coords_size) != 1:
        #     if event.x >= 150:
        #         search_coords.append(160)
        #     else:
        #         search_coords.append(40)
        #     coff = round(event.y / 140)
        #     if coff < 1:
        #         search_coords.append(40)
        #     else:
        #         row_list = []
        #         for row in range(len(self.albums_coords_size)):
        #             row_list.append((30+140*row,130+140*row))
        #         row_album = None
        #         for row in range(len(row_list)):
        #             if event.y == row_list[row][0]:
        #                 row_album = row_list[row]
        #                 break
        #             elif event.y < row_list[row][0]:
        #                 row_album = row_list[row-1]
        #                 break
        #         if row_album is None:
        #             return
        #         search_coords.append(row_album[0]+10)
        # else:
        #     search_coords.append(40)
        #     search_coords.append(40)
        coords_tuple = (self.canvas.coords(self.albums[album]))
        self.selected_album = album
        select_rectangle = self.canvas.create_rectangle(coords_tuple[0]-10,coords_tuple[1]-10,
                                                        coords_tuple[0]+100,coords_tuple[1]+100,
                                                        fill='',outline='yellow',dash=(4,2) ,tags='select',width=3)
        if self.open_album is None:
            self.canvas.tag_lower(select_rectangle)
        else:
            self.canvas.tag_lower(select_rectangle)
            self.canvas.tag_raise(select_rectangle,'opened')


    def get_track_list(self,_,album):
        print('получен трек лист')
        self.canvas.delete('opened')
        music_menu.entryconfig('Добавить трек',state=ACTIVE)
        music_menu.entryconfig('Удалить выбранный трек', state=ACTIVE)
        # search_coords = []
        # if event.x >= 150:
        #     search_coords.append(160)
        # else:
        #     search_coords.append(40)
        # coff = round(event.y / 140)
        # if coff < 1:
        #     search_coords.append(40)
        # else:
        #     row_list = []
        #     for row in range(len(self.albums_coords_size)):
        #         row_list.append((30 + 140 * row, 130 + 140 * row))
        #     row_album = None
        #     for row in range(len(row_list)):
        #         if event.y == row_list[row][0]:
        #             row_album = row_list[row]
        #             break
        #         elif event.y < row_list[row][0]:
        #             row_album = row_list[row - 1]
        #             break
        #     if row_album is None:
        #         return
        #     search_coords.append(row_album[0] + 10)
        search_coords_tuple = (self.canvas.coords(self.albums[album]))
        self.open_album = album
        open_rectangle = self.canvas.create_rectangle(search_coords_tuple[0] - 5, search_coords_tuple[1] - 5,
                                                        search_coords_tuple[0] + 95, search_coords_tuple[1] + 95,
                                                        fill='', outline='purple',width=3, tags='opened')
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
                self.albums_image[f'{album}'] = ImageTk.PhotoImage(Image.open('icons/iconPlayer.png').resize((90,90)))
                print('Ошибка, файл не найден')

            print(coords,album,self.albums,self.canvas)
            self.albums[album] = self.canvas.create_image(coords[0],coords[1],image=self.albums_image[f'{album}'],anchor=NW,)
            self.albums_coords_size[coords] = album
            print(self.albums_image[album],album,'<<<')
            temp = Label(self.canvas,text=f'{album[:20]+'...' if len(album) > 20 else album}')
            temp.config(bg='grey90')
            self.canvas.create_window(coords[0],coords[1]+self.albums_image[f'{album}'].height(),anchor=NW,window=temp,tags=[f'{album}',f'label'])
            if not self.open_album is None:
                for key in self.albums_coords_size:
                    print(key,self.albums_coords_size[key], "<<<<<<<<<><><><><")
                    if self.open_album == self.albums_coords_size[key]:
                        self.canvas.coords('opened',key[0]-15,key[1]-15,key[0]+105,key[1]+105)
            self.canvas.tag_bind(self.albums[f'{album}'],'<Button-1>',self.alb_func_constr_for_select(album))
            self.canvas.tag_bind(self.albums[f'{album}'], '<Button-3>', self.unselect_album)
            self.canvas.tag_bind(self.albums[f'{album}'], '<Double-Button-1>', self.alb_func_constr_for_get_track(album))
            self.canvas.update_idletasks()
            self.canvas.configure(scrollregion=album_list.bbox(ALL))

    def del_album(self,name):
        if not self.albums:
            showerror("Ошибка", "Нет альбомов для удаления.")
            return

        if not f'{name}' in self.albums.keys():
            print('KeyError:такого альбома нет')
            showerror('KeyError','Такого альбома несуществует или альбом не выбран')
            return

        if listdir(f'albums/{name}'):
            showerror('Ошибка', "Для удаления альбом должен быть пуст")
            return

        if self.open_album == name:
            showerror('Ошибка', "Невозможно удалить открытый альбом")
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
                self.unselect_album()
                self.albums.pop(f'{name}')
                self.albums_image.pop(f'{name}')
                self.canvas.delete(f'{name}')
                self.albums_coords_size.clear()
                rmdir(f'albums/{name}')
                self.canvas.update_idletasks()

        except Exception as e:
            print('нет, альбомов',e)
            showerror('Ошибка','Нет, альбомов' )
            return
        self.update_list_albums()



class MusicList:
    def __init__(self,canvas):
        self.canvas = canvas
        self.musiclist = {}
        self.icon_list = {}
        self.icon_list_id = {}
        self.selected_music = None
        self.chosen_music_in_list = None
        self.canvas.bind('<Button-3>', self.unselected_music)
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
            temp.save()

        if extensions == 'flac':
            temp = flac.FLAC(f'albums/{init_albums.open_album}/{name}.{extensions}')
            if not (new_icon is None):
                temp.clear_pictures()
                new_pic = flac.Picture()
                with open(new_icon,'rb') as f:
                    new_pic.data = f.read()
                    new_pic.mime = 'image/png'
                    new_pic.type = 3
                temp.add_picture(new_pic)
                temp['title'] = [f'{name}']
                temp['artist'] = [f'{author}']
                temp['genre'] = [f'{genre}']
                temp.save()
        if extensions == 'wav':
            temp = wave.WAVE(f'albums/{init_albums.open_album}/{name}.{extensions}')
            if not (new_icon is None):
                print(temp.keys())
                if 'APIC:' in temp.keys():
                    del temp['APIC:']
                with open(new_icon, 'rb') as f:
                    data = f.read()
                temp['APIC'] = APIC(encoding=3, mime='image/png', data=bytes(data))
            temp['TIT2'] = TIT2(encoding=3, text=[f'{name}'])
            temp['TPE1'] = TPE1(encoding=3, text=[f'{author}'])
            temp['TCON'] = TCON(encoding=3, text=[f'{genre}'])
            temp.save()
        self.update_musiclist()
        # self.musiclist[f'{name}.{extensions}'] = f'albums/{init_albums.open_album}/{name}.{extensions}'


    def del_music(self):
        if self.selected_music is None:
            return

        if (not self.chosen_music_in_list is None) and (self.selected_music == list(self.chosen_music_in_list.values())[0]) and list(self.chosen_music_in_list.keys())[0] == init_albums.open_album:
            showerror('Ошибка', "Нельзя удалить выбранный трек")
            return

        try:
            remove(f'albums/{init_albums.open_album}/{self.selected_music}')
        except FileNotFoundError as e:
            showerror('Ошибка', "Такого файла несуществует")
            return

        self.unselected_music()
        self.update_musiclist()

    def unselected_music(self,event=None):
        if self.selected_music is None:
            return
        self.musiclist[f'{self.selected_music}'].config(bg='grey90')
        self.selected_music = None

    def select_music(self,event,music):
        self.unselected_music()
        print(event,music,'xxx')
        self.musiclist[f'{music}'].config(bg='pale green')
        self.selected_music = f'{music}'


    def func_constr_for_select(self,music):
         return lambda event:self.select_music(event,music)

    def func_constr_for_chose(self,music):
         return lambda event:self.chose_music(event,music)

    def chose_music(self,_,music):
        if  not self.chosen_music_in_list is None:
            if list(self.chosen_music_in_list.values())[0] in self.musiclist.keys():
                self.musiclist[list(self.chosen_music_in_list.values())[0]].delete('opened')
        # self.canvas.create_rectangle(self.musiclist[f'{music}'].winfo_x()-320,self.musiclist[f'{music}'].winfo_y(),
        #                              self.musiclist[f'{music}'].winfo_x()-315,self.musiclist[f'{music}'].winfo_y()+102,
        #                              fill='red',tags='opened')
        self.musiclist[f'{music}'].create_rectangle(
            int(self.musiclist[f'{music}'].winfo_width()) - 10, 0,
            int(self.musiclist[f'{music}'].winfo_width()),
            int(self.musiclist[f'{music}'].winfo_height()), fill='red',
            tags='opened')
        self.chosen_music_in_list = {f'{init_albums.open_album}':f'{music}'}
        update_chose_music()



    def update_musiclist(self):
        self.canvas.delete('music_main_canvas')
        self.canvas.delete('opened')
        self.unselected_music()
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
                coords = (30,30+120*len(self.musiclist))
            for i in range(len(music) - 1, 0, -1):
                if music[i] == '.':
                    break
                extension += music[i]
            extension = extension[::-1]
            metadata = get_metadata(f'{path_album}/{music}', extension)
            print(metadata)
            self.icon_list[f'{music}'] =  get_metadata_icon(f'{path_album}/{music}',extension)
            self.musiclist[f'{music}'] = Canvas(self.canvas,width=int(self.canvas.cget('width'))-30,height=100,bg='grey90')
            self.canvas.create_window(coords[0],coords[1], window=self.musiclist[f'{music}'],tags='music_main_canvas',anchor=NW)
            self.icon_list_id[f'{music}'] =  self.musiclist[f'{music}'].create_image(5,5,image=self.icon_list[f'{music}'],anchor=NW)
            self.musiclist[f'{music}'].create_text(100,10,text=f'{metadata['name']}',anchor=NW,font='arial 20 bold')
            self.musiclist[f'{music}'].create_text(100,40, text=f'{metadata['author']}', anchor=NW,font='arial 15')
            self.musiclist[f'{music}'].create_text(100, 65, text=f'{metadata['genre']}', anchor=NW, font='arial 15 italic')
            self.musiclist[f'{music}'].bind('<Button-1>',self.func_constr_for_select(f'{music}'))
            self.musiclist[f'{music}'].bind('<Button-3>', self.unselected_music)
            self.musiclist[f'{music}'].bind('<Double-Button-1>', self.func_constr_for_chose(f'{music}'))
            self.canvas.config(scrollregion=self.canvas.bbox(ALL))
            print(self.icon_list)
            print(self.icon_list_id)

        if not self.chosen_music_in_list is None:
            if list(self.chosen_music_in_list.keys())[0] == init_albums.open_album:
                print('Music_list> ' ,self.musiclist)
                # print(int(self.musiclist[f'{list(self.chosen_music_in_list.values())[0]}'].cget('width'))-320,self.musiclist[f'{list(self.chosen_music_in_list.values())[0]}'].winfo_y(),
                #                              self.musiclist[f'{list(self.chosen_music_in_list.values())[0]}'].cget('width'))-315,self.musiclist[f'{list(self.chosen_music_in_list.values())[0]}'].winfo_y()+100)
                print(int(self.musiclist[f'{list(self.chosen_music_in_list.values())[0]}'].cget('width'))-(int(self.canvas.cget('width'))-50),int(self.musiclist[f'{list(self.chosen_music_in_list.values())[0]}'].cget('height'))+40,
                                             int(self.musiclist[f'{list(self.chosen_music_in_list.values())[0]}'].cget('width'))-(int(self.canvas.cget('width'))-60),int(self.musiclist[f'{list(self.chosen_music_in_list.values())[0]}'].cget('height'))+160)
                print('listdir> ',list_music.index(f'{list(self.chosen_music_in_list.values())[0]}'))
                self.musiclist[f'{list(self.chosen_music_in_list.values())[0]}'].create_rectangle(int(self.musiclist[f'{list(self.chosen_music_in_list.values())[0]}'].cget('width'))-10,0,
                                                                                                  int(self.musiclist[f'{list(self.chosen_music_in_list.values())[0]}'].cget('width')),
                                                                                                  int(self.musiclist[f'{list(self.chosen_music_in_list.values())[0]}'].cget('height')),fill='red', tags='opened')
                # int(self.musiclist[f'{list(self.chosen_music_in_list.values())[0]}'].cget('width'))-(int(self.canvas.cget('width'))-55),30+120*list_music.index(f'{list(self.chosen_music_in_list.values())[0]}'),
                #                              int(self.musiclist[f'{list(self.chosen_music_in_list.values())[0]}'].cget('width'))-(int(self.canvas.cget('width'))-60),132+120*list_music.index(f'{list(self.chosen_music_in_list.values())[0]}'),



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
    init_albums.track_list.canvas.itemconfig('music_main_canvas', width=music_list.winfo_width() - 25)
    if not init_albums.track_list.chosen_music_in_list is None:
        if init_albums.open_album == list(init_albums.track_list.chosen_music_in_list.keys())[0]:
            init_albums.track_list.musiclist[f'{list(init_albums.track_list.chosen_music_in_list.values())[0]}'].coords('opened',(
                init_albums.track_list.musiclist[f'{list(init_albums.track_list.chosen_music_in_list.values())[0]}'].winfo_width()-10,
                0,
                init_albums.track_list.musiclist[f'{list(init_albums.track_list.chosen_music_in_list.values())[0]}'].winfo_width(),
                init_albums.track_list.musiclist[f'{list(init_albums.track_list.chosen_music_in_list.values())[0]}'].winfo_height()))
    music_list.update_idletasks()


def update_place_widgets(event):
    play_button.update_coords((chosen_music.winfo_width() // 2, chosen_music.winfo_height() // 2))
    next_button.update_coords((chosen_music.winfo_width() // 2 + 50, chosen_music.winfo_height() // 2))
    prev_button.update_coords((chosen_music.winfo_width() // 2 - 55, chosen_music.winfo_height() // 2-1))
    repeat_button.update_coords((chosen_music.winfo_width() // 2 +100, chosen_music.winfo_height() // 2 +2))
    volume_button.update_coords((chosen_music.winfo_width()-270, chosen_music.winfo_height() // 2 +2))
    chosen_music.coords(volume_scale_id, chosen_music.winfo_width() -190, chosen_music.winfo_height() // 2-6)
    chosen_music.itemconfig(progress_track_bar_id,width=chosen_music.winfo_width() -120)
    chosen_music.coords(time_label,chosen_music.winfo_width() -130, chosen_music.winfo_height()-75)

def set_active_canvas(canvas):
    global active_canvas
    active_canvas = canvas

def on_mousewheel(event):
    if active_canvas is None:
        return
    if event.num == 4 or event.delta > 0:
        active_canvas.yview_scroll(-1, "units")
    elif event.num == 5 or event.delta < 0:
        active_canvas.yview_scroll(1, "units")


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


def new_window_add_album():
    window = AddAlbum()

def delete_album():
    init_albums.del_album(init_albums.selected_album)

def new_window_add_music():
    if init_albums.open_album is None:
        return
    window = AddMusic()

def delete_music():
    init_albums.track_list.del_music()

def seek_position_in_progress_bar(event):
    percent_progress = (event.x / int(progress_track_bar.winfo_width()))*100
    if percent_progress < 0 or percent_progress > 100:
        return
    progress_track_bar.config(value=percent_progress)

def test():
    # Чисто тестовая функция для проверки работаспособности update_time_label
    import random
    update_time_label(random.randint(1,10000),random.randint(1,10000))
    screen.after('idle',test)

def update_time_label(seconds,duration_seconds):
    hours = seconds // 3600
    minutes = seconds // 60 - hours*60
    duration_hours = duration_seconds // 3600
    duration_minutes = duration_seconds // 60 - duration_hours * 60
    chosen_music.itemconfig(time_label,text=f'{hours if hours >= 10 else f'0{hours}'}:{minutes if minutes >= 10 else f'0{minutes}'}:{seconds%60 if seconds%60 >= 10 else f'0{seconds%60}'}/{duration_hours if duration_hours >= 10 else f'0{duration_hours}'}:{duration_minutes if duration_minutes >= 10 else f'0{duration_minutes}'}:{duration_seconds%60 if duration_seconds%60 >= 10 else f'0{duration_seconds%60}'}')

def update_chose_music():
    if init_albums.track_list.chosen_music_in_list is None:
        return
    global chosen_music_path
    global chosen_music_icon
    chosen_music_path = f'albums/{list(init_albums.track_list.chosen_music_in_list.keys())[0]}/{list(init_albums.track_list.chosen_music_in_list.values())[0]}'
    extension = ''
    for i in range(len(chosen_music_path)-1,0,-1):
        if chosen_music_path[i] == '.':
            break
        extension += chosen_music_path[i]
    extension = extension[::-1]
    chosen_music_icon = get_metadata_icon(chosen_music_path,extension)
    chosen_music.itemconfig(icon_chosen_music_id,image=chosen_music_icon)
    metadata = get_metadata(chosen_music_path,extension)
    chosen_music.itemconfig(music_name_label,text=metadata['name'])
    chosen_music.itemconfig(album_name_label, text=f'{list(init_albums.track_list.chosen_music_in_list.keys())[0]}')
    chosen_music.itemconfig(music_author_label, text=metadata['author'])

def get_info(event):
    print([main_canvas.winfo_width(), main_canvas.winfo_height()], [screen.winfo_width(), screen.winfo_height()])
    print(event)

def enter_canvas(event)-> None:
    print(event.x,event.y)

screen = Tk()
screen.geometry(f'{SCREEN_SIZE[0]}x{SCREEN_SIZE[1]}')
screen.title("MusicPlayer")
screen.minsize(800,400)
try:
    icon = PhotoImage(file="icons/iconPlayer.png")
    screen.iconphoto(True, icon)
except FileNotFoundError:
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
active_canvas = None
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
album_list.bind('<Enter>',lambda event: set_active_canvas(album_list))

menu = Menu(bg='grey90',tearoff=0)
album_menu = Menu(bg='grey90',tearoff=0)
album_menu.add_command(label='Добавить альбом',command=new_window_add_album)
album_menu.add_command(label='Удалить выбранный альбом',command=delete_album)
music_menu = Menu(bg='grey90',tearoff=0)
music_menu.add_command(label='Добавить трек',command=new_window_add_music,state=DISABLED)
music_menu.add_command(label='Удалить выбранный трек',command=delete_music,state=DISABLED)
menu.add_cascade(label='Альбомы',menu=album_menu)
menu.add_cascade(label='Треки',menu=music_menu)
screen.config(menu=menu)
# button_add_album = ttk.Button(width=10,text='+',command=new_window_add_album)
# album_list.create_window(10,10,anchor=NW,window=button_add_album)
# button_add_album = ttk.Button(width=10,text='-',command=delete_album)
# album_list.create_window(90,10,anchor=NW,window=button_add_album)

# for i in range(1,100):
#     album_list.create_rectangle(0, 0 + i * 100, 100, 100 + i * 100, fill='pink')

music_frame = Frame(main_canvas)
music_list = Canvas(music_frame, background='white', width=int(main_canvas.cget('width')) - 335, height=main_canvas.cget('height'))
scroll_bar_music = Scrollbar(music_frame, orient=VERTICAL, command=music_list.yview, width=15, background='grey90')
music_list.config(yscrollcommand=scroll_bar_music.set)
music_list.grid(row=0, column=2, sticky='nsew')
scroll_bar_music.grid(row=0, column=3, sticky=NS)
music_frame.grid_rowconfigure(2, weight=1)
music_frame.grid_columnconfigure(2, weight=1)
music_list_id = main_canvas.create_window(315, 0, window=music_frame, anchor=NW)
music_list.bind('<Enter>',lambda event: set_active_canvas(music_list))
# music_list.configure(scrollregion=music_list.bbox(ALL))
# test_button = ttk.Button(width=15,command=test_def)
# music_list.create_window(100,100,window=test_button,anchor=NW)

init_albums = Albums(album_list,music_list)
init_albums.update_list_albums()





chosen_music = Canvas(bg="gray90", width=SCREEN_SIZE[0], height=100)
chosen_music.pack(anchor=S, expand=True,fill='x')
chosen_music_path = None
chosen_music_icon = None
volume_var = DoubleVar(value=50.0)
last_volume_var = DoubleVar()
repeat_var = None
play_button = ImageButton(chosen_music,((int(chosen_music.cget("width"))// 2,int(chosen_music.cget('height'))// 2)),ICONS['play'],get_info)
next_button = ImageButton(chosen_music,((int(chosen_music.cget("width"))// 2+50,int(chosen_music.cget('height'))// 2)),ICONS['next'],get_info)
prev_button = ImageButton(chosen_music,((int(chosen_music.cget("width"))// 2-55,int(chosen_music.cget('height'))// 2-1)),ICONS['prev'],get_info)
repeat_button = ImageButton(chosen_music,((int(chosen_music.cget("width"))// 2+100,int(chosen_music.cget('height'))// 2+2)),ICONS['repeat_off'],update_repeat)
volume_button = ImageButton(chosen_music,((int(chosen_music.cget("width"))-270,int(chosen_music.cget('height'))// 2+2)),ICONS['volume'],volume_off_on)
volume_scale = Scale(orient=HORIZONTAL,length=100,from_=0,to=100,bg='grey90',highlightbackground='grey90',variable=volume_var,command=update_volume)
volume_scale_id = chosen_music.create_window(int(chosen_music.cget("width"))-190,int(chosen_music.cget('height'))// 2-6,anchor=CENTER,window=volume_scale)
time_label = chosen_music.create_text(900,20,anchor=NW,text='00:00:00/00:00:00',font='Arial 10 italic',activefill='grey60')
icon_chosen_music_id = chosen_music.create_image(50, 50, image=ICONS['default'], anchor=CENTER)
music_name_label = chosen_music.create_text(100,25,text='Название трека',anchor=NW,font='arial 16 bold')
album_name_label = chosen_music.create_text(100,50,text='Альбом',anchor=NW,font='arial 12')
music_author_label = chosen_music.create_text(100,70,text='Автор',anchor=NW,font='arial 12 italic')
progress_track_bar_var = DoubleVar()
style_for_progress_bar = ttk.Style(screen)
style_for_progress_bar.theme_use('clam')
style_for_progress_bar.theme_settings('clam',settings={
    'TButton':{
        'configure':{
            'background': 'grey99',
            'bordercolor':"grey99",
            'darkcolor':'grey10'
        }
    }
})
style_for_progress_bar.configure("Custom.Vertical.TProgressbar",
                background='lightblue',
                troughcolor='gray',
                bordercolor='darkblue')

style_for_progress_bar.map("Custom.Vertical.TProgressbar",
          background=[('active', 'green'),
                     ('disabled', 'gray')])
progress_track_bar = ttk.Progressbar(chosen_music,style='Custom.Vertical.TProgressbar', orient=HORIZONTAL,value=progress_track_bar_var.get())
progress_track_bar.bind('<Double-Button-1>',seek_position_in_progress_bar)
progress_track_bar.bind('<ButtonPress-1>',lambda event: progress_track_bar.bind('<Motion>',seek_position_in_progress_bar))
progress_track_bar.bind('<ButtonRelease-1>',lambda event: progress_track_bar.unbind('<Motion>'))
progress_track_bar_id =  chosen_music.create_window(100,5,anchor=NW,window=progress_track_bar,width=int(chosen_music.cget('width'))-120)


screen.bind("<Configure>", update_size)
chosen_music.bind("<Configure>",update_place_widgets)
screen.bind_all('<MouseWheel>',on_mousewheel)
# screen.protocol('WM_FULLSCREEN_WINDOW',on_fullscreen)

Interval_south = Canvas(screen, height=INTERVAL)
Interval_south.pack(anchor=S,fill="x", expand=False)

screen.mainloop()


