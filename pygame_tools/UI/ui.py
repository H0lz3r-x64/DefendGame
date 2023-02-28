import pygame


class Button:
    def __init__(self, offset: tuple, size: tuple, style: int, text: str):
        self.__offset = offset
        self.__size = size
        self.__style = style
        self.__text = text

        self.__text_align = 'center'
        self.__font = 'arial'
        self.__font_size = 12

        self.__realfont = pygame.font.SysFont('Arial', self.__font_size)

        self.__button = pygame.Surface(self.__size)
        self.__rect = self.__button.get_rect(center=self.__offset)

        match self.__style:
            case 1:
                self._stylename1()
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass

    def _stylename1(self):
        self.__button.fill("red")
        text_surface = self.__realfont.render(self.__text, False, "black")
        self.__button.blit(text_surface, self.__rect)
        return self.__button

    def get_size(self):
        return self.__size

    def get_style(self):
        return self.__style

    def get_text(self):
        return self.__text

    def set_text_align(self, alignment):
        self.__text_align = alignment

    def set_font(self, font):
        self.__font = font

    def set_font_size(self, font_size):
        self.__font_size = font_size
