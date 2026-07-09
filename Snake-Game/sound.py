import pygame

pygame.mixer.init()

eat_sound = pygame.mixer.Sound(r"assest\eating-apple-81019- (mp3cut.net).wav")
game_over_sound = pygame.mixer.Sound(r"assest\game-over-arcade-6435.wav")
game_sound = pygame.mixer.Sound(r"assest\8-bit-game-music-122259 (mp3cut.net).wav")
game_sound.set_volume(1.0)
eat_sound.set_volume(1.0)
game_over_sound.set_volume(0.7)