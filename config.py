import pygame

<<<<<<< HEAD

=======
>>>>>>> 5c5cb3c39c3c9fdab3d501fdbf0ac8d4d26e03d4
class Screen:
    def __init__(self):
        print('carregando tela...')
        self.screen = pygame.display.set_mode((640, 480), 0, 32)
        pygame.display.set_caption("ITApyghters")

    def display_update(self, newScreen):
        adjNewScreen = pygame.transform.scale2x(newScreen)
        self.screen.blit(adjNewScreen, (0, 0))
        pygame.display.update()

<<<<<<< HEAD

=======
>>>>>>> 5c5cb3c39c3c9fdab3d501fdbf0ac8d4d26e03d4
class SoundPlayer:
    def __init__(self):
        print('carregando SoundPlayer')
        self.music_vol = 0.1
        self.sound_vol = 0.2

    def play_music(self, file):
        if file.find('sound/music/') < 0:
            file = 'sound/music/' + file
        pygame.mixer.music.stop()
        while pygame.mixer.music.get_busy():
            print('wait...', end='')
        pygame.mixer.music.load(file)
        pygame.mixer.music.set_volume(self.music_vol)
        pygame.mixer.music.play(-1)

    def play_sound(self, file):
        if file.find('sound/') < 0:
            file = 'sound/'+file
        sound = pygame.mixer.Sound(file)
        sound.set_volume(self.sound_vol)
        sound.play()