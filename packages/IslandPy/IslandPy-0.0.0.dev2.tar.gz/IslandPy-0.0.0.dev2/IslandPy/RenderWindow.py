import os

import pygame
from pygame.time import Clock

from IslandPy.Scenes.TestScene import TestScene


class RenderWindow:
    def __init__(self) -> None:
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption("Render Window")
        self.__screen = pygame.display.set_mode((800, 600))
        self.__clock = Clock()
        self.__done = False
        self.__pause = False
        self.__fps = 60
        self.__test_scene = TestScene(name="test")

    def start(self) -> None:
        while not self.__done:
            self.__loop()
        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__done = True
            # if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_SPACE:
                #     self.__pause = not self.__pause

            if self.__pause:
                continue

            self.__test_scene.handle_events(event)

    def draw(self) -> None:
        self.__test_scene.draw(self.__screen)

    def update(self, dt) -> None:
        if self.__pause:
            return

        self.__test_scene.update(dt)

    def __loop(self) -> None:
        dt = self.__clock.tick(self.__fps)
        self.__screen.fill((34, 34, 35))
        self.handle_events()
        self.update(dt)
        self.draw()
        pygame.display.flip()
