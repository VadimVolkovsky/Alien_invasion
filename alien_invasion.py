from re import S
import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from person import Person


class AlienInvasion():
    """Класс для управления ресурсами и поведением игры"""
    def __init__(self) -> None:
        pygame.init
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))  # Оконный режим
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # полноэкранный режим
        # self.settings.screen_width = self.screen.get_rect().width  # обновляем ширину экрана
        # self.settings.screen_height = self.screen.get_rect().height  # обновляем высоту экрана
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)  # Создаем экземпляр Ship
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()  # Создаем флот
        self.person = Person(self.screen)  # Создаем экземпляр person

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # если клавиша нажата (DOWN)
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:  # если клавиша отпущена (UP)
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:  # если нажата стрелка вправо
            self.ship.moving_right = True  # непрерывное движение вправо
        elif event.key == pygame.K_LEFT:  # если нажата стрелка влево
            self.ship.moving_left = True  # непрерывное движение влево
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # elif event.key == pygame.K_UP:  # движение вверх
        #     self.ship.moving_up = True
        # elif event.key == pygame.K_DOWN:  # движение вниз
        #     self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False  # остановка движения вправо
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False  # остановка движения влево
        # elif event.key == pygame.K_UP:  # остановка движения вверх
        #     self.ship.moving_up = False
        # elif event.key == pygame.K_DOWN:  # остановка движения вниз
        #     self.ship.moving_down = False
    
    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды"""
        self.bullets.update()  # Обновление позиции снарядов
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)  #  Удаление снарядов вышедших за край экрана

    def _create_fleet(self):
        """Создание флота пришельцев"""
        alien = Alien(self)  # Создание одного пришельца
        alien_width, alien_height = alien.rect.size  # ширина и высота пришельца
        availabale_space_x = self.settings.screen_width - (2 * alien_width)  # Доступное пространство по горизонтали
        number_aliens_x = availabale_space_x // (2 * alien_width)  # сколько пришельцев влезает по горизонтали
        
        #  Определяет кол-во рядом помещающихся на экране
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_width) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):  # создание первого ряда пришельцев
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

            
    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран"""
        self.screen.fill(self.settings.bg_color)  # цвет фона экрана
        self.ship.blitme()
        # self.person.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)  # рисуем пришельца
        pygame.display.flip()
    
    
if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()