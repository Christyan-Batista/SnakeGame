# Example file showing a circle moving on screen
import pygame
import random
from funcoesdb import *
# pygame setup

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.screen = pygame.display.set_mode((600, 600))
        self.change_food_position = False
        self.initial_position = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.last_key = ''
        self.game_over = False
        self.current_screen = 0  # 0 is menu screen, 1 is playscreen, 2 is gameoverscreen, 3 is records
        self.points = 0
        self.name_input = ''
        self.user_inputing_text = False
        self.blink_cursor_input = 0
        self.dbconnect = Database()
        self.snake_length = [
                                [
                                 pygame.Vector2((self.initial_position.x - 20), (self.initial_position.y - 20)),
                                 pygame.Vector2((self.initial_position.x + 0), (self.initial_position.y - 20)),
                                 pygame.Vector2((self.initial_position.x + 0), (self.initial_position.y + 0)),
                                 pygame.Vector2((self.initial_position.x - 20), (self.initial_position.y + 0))
                                ],
                                [
                                    pygame.Vector2((self.initial_position.x - 20), (self.initial_position.y + 0)),
                                    pygame.Vector2((self.initial_position.x + 0), (self.initial_position.y - 0)),
                                    pygame.Vector2((self.initial_position.x + 0), (self.initial_position.y + 20)),
                                    pygame.Vector2((self.initial_position.x - 20), (self.initial_position.y + 20))
                                ]
                            ]

        self.random_food_coordinates = pygame.Vector2((random.randrange(0, self.screen.get_width(), 20) + 10),
                                                      (random.randrange(0, self.screen.get_height(), 20) + 10))

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if self.current_screen == 0:
                self.menu_screen()
            elif self.current_screen == 1:
                self.screen.fill('#48E05F')
                self.snake_growth()
                self.snake_moves()
                self.plot_snake()
                self.spawn_food()
                self.lines()
                self.snake_colision()
                self.game_over = self.gameover()
                if self.game_over:
                    self.current_screen = 2
            elif self.current_screen == 2:
                self.gameover_screen()
            elif self.current_screen == 3:
                self.recordsreen()

            pygame.display.flip()
            self.dt = self.clock.tick(60)/1000
            self.clock.tick(7)

        pygame.quit()
        self.dbconnect.endconnection()

    def plot_snake(self):
        for polygon in self.snake_length:
            pygame.draw.polygon(self.screen, 'red', polygon)

    def snake_moves(self):
        self.keys = pygame.key.get_pressed()

        pressed_keys = [self.keys[pygame.K_UP], self.keys[pygame.K_DOWN],
                        self.keys[pygame.K_LEFT], self.keys[pygame.K_RIGHT]]

        if (self.keys[pygame.K_UP] or self.last_key == 'arrow_up') and self.last_key != 'arrow_down':
            if pressed_keys[2] or pressed_keys[3]:
                pass
            else:
                self.last_key = 'arrow_up'

                self.snake_length[len(self.snake_length) - 1][0].y = self.snake_length[0][0].y - 20
                self.snake_length[len(self.snake_length) - 1][1].y = self.snake_length[0][1].y - 20
                self.snake_length[len(self.snake_length) - 1][2].y = self.snake_length[0][1].y
                self.snake_length[len(self.snake_length) - 1][3].y = self.snake_length[0][0].y

                self.snake_length[len(self.snake_length) - 1][0].x = self.snake_length[0][0].x
                self.snake_length[len(self.snake_length) - 1][1].x = self.snake_length[0][1].x
                self.snake_length[len(self.snake_length) - 1][2].x = self.snake_length[0][2].x
                self.snake_length[len(self.snake_length) - 1][3].x = self.snake_length[0][3].x

                self.update_snake_length_positions()

        if (self.keys[pygame.K_DOWN] or self.last_key == 'arrow_down') and self.last_key != 'arrow_up':
            if pressed_keys[2] or pressed_keys[3]:
                pass
            else:
                self.last_key = 'arrow_down'

                self.snake_length[len(self.snake_length) - 1][0].y = self.snake_length[0][3].y
                self.snake_length[len(self.snake_length) - 1][1].y = self.snake_length[0][2].y
                self.snake_length[len(self.snake_length) - 1][2].y = self.snake_length[0][2].y + 20
                self.snake_length[len(self.snake_length) - 1][3].y = self.snake_length[0][3].y + 20

                self.snake_length[len(self.snake_length) - 1][0].x = self.snake_length[0][0].x
                self.snake_length[len(self.snake_length) - 1][1].x = self.snake_length[0][1].x
                self.snake_length[len(self.snake_length) - 1][2].x = self.snake_length[0][2].x
                self.snake_length[len(self.snake_length) - 1][3].x = self.snake_length[0][3].x

                self.update_snake_length_positions()

        if (self.keys[pygame.K_LEFT] or self.last_key == 'arrow_left') and self.last_key != 'arrow_right':
            self.last_key = 'arrow_left'

            self.snake_length[len(self.snake_length) - 1][0].x = self.snake_length[0][0].x - 20
            self.snake_length[len(self.snake_length) - 1][1].x = self.snake_length[0][0].x
            self.snake_length[len(self.snake_length) - 1][2].x = self.snake_length[0][3].x
            self.snake_length[len(self.snake_length) - 1][3].x = self.snake_length[0][3].x - 20

            self.snake_length[len(self.snake_length) - 1][0].y = self.snake_length[0][0].y
            self.snake_length[len(self.snake_length) - 1][1].y = self.snake_length[0][1].y
            self.snake_length[len(self.snake_length) - 1][2].y = self.snake_length[0][2].y
            self.snake_length[len(self.snake_length) - 1][3].y = self.snake_length[0][3].y

            self.update_snake_length_positions()


        if (self.keys[pygame.K_RIGHT] or self.last_key == 'arrow_right') and self.last_key != 'arrow_left':
            self.last_key = 'arrow_right'

            self.snake_length[len(self.snake_length) - 1][0].x = self.snake_length[0][1].x
            self.snake_length[len(self.snake_length) - 1][1].x = self.snake_length[0][1].x + 20
            self.snake_length[len(self.snake_length) - 1][2].x = self.snake_length[0][2].x + 20
            self.snake_length[len(self.snake_length) - 1][3].x = self.snake_length[0][2].x

            self.snake_length[len(self.snake_length) - 1][0].y = self.snake_length[0][0].y
            self.snake_length[len(self.snake_length) - 1][1].y = self.snake_length[0][1].y
            self.snake_length[len(self.snake_length) - 1][2].y = self.snake_length[0][2].y
            self.snake_length[len(self.snake_length) - 1][3].y = self.snake_length[0][3].y

            self.update_snake_length_positions()

    def update_snake_length_positions(self):
        self.temp = 0
        for position in range(0, len(self.snake_length)-1, 1):
            if position == 0:
                self.temp = self.snake_length[position+1]
                self.snake_length[position + 1] = self.snake_length[position]
                self.snake_length[position] = self.temp
            else:
                self.temp = self.snake_length[position + 1]
                self.snake_length[position + 1] = self.snake_length[0]
                self.snake_length[0] = self.temp

    def spawn_food(self):

        if self.change_food_position:
            verify = True
            while verify:
                verify = False
                self.random_food_coordinates.x = random.randrange(0, self.screen.get_width(), 20) + 10
                self.random_food_coordinates.y = random.randrange(0, self.screen.get_height(), 20) + 10
                for snake_positions in self.snake_length:
                    if snake_positions[0].x < self.random_food_coordinates.x < snake_positions[1].x:
                        if snake_positions[0].y < self.random_food_coordinates.y < snake_positions[3].y:
                            verify = True
                            break

                self.change_food_position = False

        pygame.draw.circle(self.screen, 'red', self.random_food_coordinates, 10)

    def lines(self):
        for linesx in range(20, self.screen.get_width(), 20):
            self.line_length = [pygame.Vector2(linesx, 0), pygame.Vector2(linesx, self.screen.get_height())]
            pygame.draw.line(self.screen, 'blue', self.line_length[0], self.line_length[1])

        for linesy in range(20, self.screen.get_width(), 20):
            self.line_length = [pygame.Vector2(0, linesy), pygame.Vector2(self.screen.get_width(), linesy)]
            pygame.draw.line(self.screen, 'blue', self.line_length[0], self.line_length[1])

    def snake_growth(self):
        copy = []
        if self.snake_length[0][0].x < self.random_food_coordinates.x < self.snake_length[0][1].x:
            if self.snake_length[0][0].y < self.random_food_coordinates.y < self.snake_length[0][3].y:

                for c in self.snake_length[len(self.snake_length)-1]:
                    vetor = pygame.Vector2(c.x, c.y)
                    copy.append(vetor)

                self.snake_length.append(copy)

                self.change_food_position = True
                self.points += 1
                som_comida = pygame.mixer.Sound('soundeffects/sound5.wav')
                som_comida.set_volume(0.08)
                som_comida.play()

    def snake_colision(self):
        for positions_snake in range(1, len(self.snake_length), 1):
            if self.snake_length[0] == self.snake_length[positions_snake]:
                self.current_screen = 2
                return

    def gameover(self):
        if 0 > self.snake_length[0][0].x or self.snake_length[0][1].x > self.screen.get_width():
            return True
        if 0 > self.snake_length[0][0].y or self.snake_length[0][2].y > self.screen.get_width():
            return True

    def gameover_screen(self):
        gameover_sound = pygame.mixer.Sound('soundeffects/gameover.wav')
        gameover_sound.set_volume(0.08)
        gameover_sound.play()
        while True:
            text_gameover = Text(self.screen, 'Game Over', 'white', 'Helvetica', 35, (self.screen.get_width()/2) - 100,
                                 (self.screen.get_height()/2) - 150, True)

            points_text = Text(self.screen, f'Pontuação: {self.points}', 'white', 'Helvetica', 35, (self.screen.get_width()/2) - 115,
                                 (self.screen.get_height()/2) - 100, True)
            self.screen.fill('#48E05F')
            points_text.draw()
            text_gameover.draw()

            btn_restart = Button("Jogar Novamente", '#43F0D6', 30, '#5F9B92', 260, 50, 30, 350, self.screen)
            btn_return_menu = Button("Menu Principal", '#43F0D6', 30, '#5F9B92', 260, 50, 310, 350, self.screen)
            btn_signup_record = Button('Cadastrar', '#43F0D6', 15, '#5F9B92', 90, 30, 345, 250, self.screen)
            input_text = InputText(self.screen, self.name_input, 185, 30, 150, 250)

            if btn_restart.mouse_is_over():
                btn_restart.hover_button()
            if btn_return_menu.mouse_is_over():
                btn_return_menu.hover_button()
            if btn_signup_record.mouse_is_over():
                btn_signup_record.hover_button()

            btn_restart.draw()
            btn_return_menu.draw()
            btn_signup_record.draw()
            input_text.draw()

            self.snake_length = [
                                    [
                                        pygame.Vector2((self.initial_position.x - 20), (self.initial_position.y - 20)),
                                        pygame.Vector2((self.initial_position.x + 0), (self.initial_position.y - 20)),
                                        pygame.Vector2((self.initial_position.x + 0), (self.initial_position.y + 0)),
                                        pygame.Vector2((self.initial_position.x - 20), (self.initial_position.y + 0))
                                    ],
                                    [
                                        pygame.Vector2((self.initial_position.x - 20), (self.initial_position.y + 0)),
                                        pygame.Vector2((self.initial_position.x + 0), (self.initial_position.y - 0)),
                                        pygame.Vector2((self.initial_position.x + 0), (self.initial_position.y + 20)),
                                        pygame.Vector2((self.initial_position.x - 20), (self.initial_position.y + 20))
                                    ]
                                ]

            self.last_key = ''

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if btn_restart.rect_object.collidepoint(pos):
                        self.current_screen = 1
                        return
                    if btn_return_menu.rect_object.collidepoint(pos):
                        self.current_screen = 0
                        return
                    if btn_signup_record.rect_object.collidepoint(pos):
                        if self.name_input[-1] == '|':
                            self.name_input = self.name_input.replace('|', '')
                        self.dbconnect.insert_record(str(self.name_input), int(self.points))

                    if input_text.rectangle.collidepoint(pos):
                        self.user_inputing_text = True
                    else:
                        self.user_inputing_text = False
                elif event.type == pygame.KEYDOWN and self.user_inputing_text:
                    if event.key == pygame.K_BACKSPACE and len(self.name_input) > 0:
                        self.name_input = self.name_input[0:((len(self.name_input))-1)]
                    else:
                        if (len(self.name_input)+1) < 10:
                            self.name_input += event.unicode


            if self.user_inputing_text:
                self.blink_cursor_input += 1
                if self.blink_cursor_input % 4 == 0:
                    self.name_input += '|'
                else:
                    self.name_input = self.name_input.replace('|', '')

            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(7)

    def menu_screen(self):
        while True:
            self.screen.fill('#48E05F')
            text_gamename = Text(self.screen, 'Snake Game', 'White', 'Helvetica', 35, 195, 100, True)
            text_developername = Text(self.screen, 'Developed By:', 'white', 'Helvetica', 25, 217, 425, True)
            text_developername2 = Text(self.screen, 'Christyan Batista', 'white', 'Helvetica', 25, 200, 455, True)
            text_gamename.draw()
            text_developername2.draw()
            text_developername.draw()
            play_button = Button("Jogar", '#43F0D6', 30, '#5F9B92', 260, 50, 170, 200, self.screen)
            record_button = Button("Recordes", '#43F0D6', 30, '#5F9B92', 260, 50, 170, 270, self.screen)
            exit_button = Button("Sair", '#43F0D6', 30, '#5F9B92', 260, 50, 170, 340, self.screen)

            if play_button.mouse_is_over():
                play_button.hover_button()
            if record_button.mouse_is_over():
                record_button.hover_button()
            if exit_button.mouse_is_over():
                exit_button.hover_button()

            play_button.draw()
            record_button.draw()
            exit_button.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if play_button.rect_object.collidepoint(pos):  # verify if click was on button area
                        self.current_screen = 1
                        return
                    if record_button.rect_object.collidepoint(pos):
                        self.current_screen = 3
                        return
                    if exit_button.rect_object.collidepoint(pos):
                        self.running = False
                        return

            pygame.display.update()

    def recordsreen(self):
        cont = 0
        data_records = self.dbconnect.show_records()
        while True:
            y_coord = 150
            self.screen.fill('#48E05F')
            text_gamename = Text(self.screen, 'Recordes', 'White', 'Helvetica', 35, 225, 100, True)
            text_gamename.draw()

            for num, data in enumerate(data_records):
                position_text = Text(self.screen, f'{num+1}.', 'White', 'Helvetica', 20, 200, y_coord, True)
                text_name = Text(self.screen, f'{data[0]}', 'White', 'Helvetica', 20, 250, y_coord, True)
                text_point = Text(self.screen, f'{data[1]}', 'White', 'Helvetica', 20, 380, y_coord, True)
                position_text.draw()
                text_name.draw()
                text_point.draw()
                y_coord += 25
                cont += 1
                if cont == 5:
                    break

            return_button = Button("Retorno", '#43F0D6', 30, '#5F9B92', 260, 50, 170, 400, self.screen)

            if return_button.mouse_is_over():
                return_button.hover_button()

            return_button.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if return_button.rect_object.collidepoint(pos):  # verify if click was on button area
                        self.current_screen = 0
                        return

            pygame.display.update()


class Button:
    def __init__(self, text, color_text, text_size, bg_color, width, height, x, y, draw_screen):
        self.rect_object = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont('Helvetica', text_size, True)
        self.text= text
        self.color_text = color_text
        self.bg_color = bg_color
        self.draw_screen = draw_screen
        self.hover_color_button = '#4C6169'
        self.button_sizes = [width, height]

    def draw(self):
        pygame.draw.rect(self.draw_screen, self.bg_color, self.rect_object)
        render = self.font.render(self.text, True, self.color_text)
        align_text = render.get_rect(center=self.rect_object.center)  # align the render text on rect object
        self.draw_screen.blit(render, align_text)  # This function put a render text in a position of rect

    def hover_button(self):
        self.bg_color = self.hover_color_button

    def mouse_is_over(self):
        pos = pygame.mouse.get_pos()
        pos_rect = [self.rect_object.x, self.rect_object.y]
        if pos_rect[0] < pos[0] < (pos_rect[0] + self.button_sizes[0]):
            if pos_rect[1] < pos[1] < (pos_rect[1] + self.button_sizes[1]):
                return True
            else:
                return False
        else:
            return False


class Text:
    def __init__(self, draw_screen, text, color_text, font, size_font, x, y, bold_text=False):
        self.font = pygame.font.SysFont(font, size_font, bold_text)
        self.render_text = self.font.render(text, True, color_text)
        self.drawscreen = draw_screen
        self.x = x
        self.y = y

    def draw(self):
        self.drawscreen.blit(self.render_text, [self.x, self.y])


class InputText:
    def __init__(self, draw_screen, text, width, height, x, y):
        self.rectangle = pygame.Rect(x, y, width, height)
        self.screengame = draw_screen
        self.font = pygame.font.SysFont('Helvetica', 20)
        self.text = text

    def draw(self):
        pygame.draw.rect(self.screengame, 'white', self.rectangle)
        render = self.font.render(self.text, True, 'black')
        self.screengame.blit(render, [self.rectangle.x + 10, self.rectangle.y + 5])

SnakeGame()
