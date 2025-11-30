import pygame


class Audio:
    def __init__(self):
        try:
            pygame.mixer.init()
            self.AUDIO_AVAILABLE = True
            self.is_loaded = False
            self.path = None
            self.shift_position = 0
        except Exception as e:
            print("Не удалось инициализировать звуковую систему (pygame):", e)
            self.AUDIO_AVAILABLE = False
            self.is_loaded = False
            self.path = None
        pygame.mixer.music.set_endevent()

    def load_audio(self,path):
        if not self.AUDIO_AVAILABLE:
            return
        pygame.mixer.music.load(path)
        self.path = path
        self.is_loaded = True

    def play(self,volume):
        if not self.is_loaded:
            return
        self.shift_position = 0
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(volume/100)

    def stop(self):
        if not self.is_loaded:
            return
        pygame.mixer.music.stop()

    def pause(self):
        if not self.is_loaded:
            return
        pygame.mixer.music.pause()

    def unpause(self):
        if not self.is_loaded:
            return
        pygame.mixer.music.unpause()

    @property
    def get_current_position(self):
        '''Возвращает в миллисекундах'''
        if not self.is_loaded:
            return None
        return pygame.mixer.music.get_pos() + self.shift_position*1000

    def set_position(self,seconds,is_paused=False):
        '''Принимает в секундах'''
        if not self.is_loaded:
            return
        self.shift_position = seconds
        pygame.mixer.music.stop()
        pygame.mixer.music.play()
        if is_paused:
            pygame.mixer.music.pause()
        pygame.mixer.music.set_pos(seconds)

    @property
    def get_volume(self):
        if not self.is_loaded:
            return None
        return pygame.mixer.music.get_volume()*100

    def set_volume(self,volume):
        if not self.is_loaded:
            return
        pygame.mixer.music.set_volume(volume/100)

    @property
    def get_duration(self):
        if not self.is_loaded:
            return None
        return pygame.mixer.Sound.get_length(pygame.mixer.Sound(self.path))

    @property
    def get_busy(self):
        if not self.is_loaded:
            return None
        return pygame.mixer.music.get_busy()



