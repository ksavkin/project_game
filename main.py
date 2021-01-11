from config import *
from building import *
import menu
import pygame
from communications import *
from board import Board
import time

# -- Local variables --
attack_to = 0
event_type = 'menu'
pygame.init()

gl_screen = pygame.display.set_mode((WIDTH, HEIGHT))  # global screen to use in other files
board_main = Board(gl_screen, (30, 30), (0, 0))
board_buildings = Board(gl_screen, (2, 8), (900, 150), buildings)

# ----- Buttons and PlainText init -----


# init players boards
player1_board_main = Board(gl_screen, (30, 30), (0, 0))
player1_board_buildings = Board(gl_screen, (3, 1), (750, 75))

# Common buttons
left_button = menu.Button((521, 262), (25, 25), (30, 30, 200), "<")
plus_minusPT = menu.PlainText((556, 262), (30, 25), (140, 140, 140), "0")
right_button = menu.Button((596, 262), (25, 25), (30, 30, 200), ">")
back_b = menu.Button((952, 690), (200, 30), (200, 30, 30), "Назад")
desc_pmPT = menu.PlainText((351, 220), (450, 30), (140, 140, 140), "Бомбим этого игрока:")
do_smthB = menu.Button((476, 300), (200, 30), (30, 30, 200), "В атаку!")
basic_choose_sc = [left_button, right_button, back_b, desc_pmPT, plus_minusPT, do_smthB]
# Next turn buttons
click_on_me_b = menu.Button((276, 312), (600, 100), (200, 30, 30), "Нажми на меня, чтобы начать следующий ход")
# winscreen buttons
winB = menu.Button((451, 350), (250, 30), (200, 30, 30), "Вернуться в меню")
winPt = menu.PlainText((376, 250), (400, 60), (100, 15, 15), "Игрок n - победитель!")
# menu buttons
button1 = menu.Button((476, 250), (200, 35), (200, 30, 30), "  Играть  ")
button2 = menu.Button((476, 300), (200, 35), (200, 30, 30), " Правила ")
button3 = menu.Button((476, 350), (200, 35), (200, 30, 30), "Настройки")
button4 = menu.Button((476, 400), (200, 35), (200, 30, 30), "  Выход  ")
menu_buttons = [button1, button2, button3, button4]
# game screen buttons
next_turn_b = menu.Button((952, 690), (200, 30), (200, 30, 30), "Следующий ход")
attack_button = menu.Button((752, 690), (150, 30), (200, 30, 30), "Атаковать")
MoneyPT = menu.PlainText((750, 10), (115, 30), (30, 135, 30), "$:")
ElectricityPT = menu.PlainText((875, 10), (115, 30), (200, 200, 0), "E:")
HeatPT = menu.PlainText((1000, 10), (115, 30), (240, 30, 30), "H:")
board_objects = [ElectricityPT, HeatPT, MoneyPT, next_turn_b, attack_button]

# -- Main game cycle --
clock = pygame.time.Clock()
running = True
while running:
    # --- events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
        # -- Events for menu --
        if event_type == 'menu':
            if button1.is_clicked(event):
                event_type = 'before game'
            if button4.is_clicked(event):
                pygame.quit()
                exit()
            if button2.is_clicked(event):
                a = 1
            if button3.is_clicked(event):
                a = 1
        # -- Events for game --
        elif event_type == 'before game':
            if left_button.is_clicked(event):
                players_amount -= 1
                if players_amount <= 1:
                    players_amount = 4
            if right_button.is_clicked(event):
                players_amount += 1
                if players_amount > 4:
                    players_amount = 2
            if back_b.is_clicked(event):
                event_type = 'menu'
            if do_smthB.is_clicked(event):
                event_type = 'board'
        elif event_type == 'board':
            if next_turn_b.is_clicked(event):
                event_type = 'nextturn'
            elif attack_button.is_clicked(event):
                event_type = 'attack'
            elif event.type == pygame.MOUSEBUTTONDOWN:

                board_buildings.get_mouse_click(event.pos)
                board_main.get_mouse_click(event.pos)
                # copy building to main board if building not empty
                if board_main.cell_selected is not None and \
                        board_main.cell_selected.building is None and \
                        board_buildings.cell_selected is not None and \
                        board_buildings.cell_selected.building is not None:
                    if buildings_db[buildings.index(board_buildings.cell_selected.building) - 1][2] <= money[turn]:
                        board_main.cell_selected.set_building(board_buildings.cell_selected.building)
                        x, y = board_main.cell_selected.position_index
                        mas[turn][y][x] = buildings.index(board_buildings.cell_selected.building)
                        money[turn] -= buildings_db[buildings.index(board_buildings.cell_selected.building) - 1][2]
                pygame.display.flip()
        elif event_type == 'nextturn':
            if click_on_me_b.is_clicked(event):
                from config import turn

                turn += 1
                turn = turn % players_amount
                e_check = coms_consuption('electricity', electricity_list, turn)
                m_check = coms_consuption('money', electricity_list, turn)
                if e_check * -1 >= 0:
                    money[turn] += m_check
                event_type = 'board'
        elif event_type == 'attack':
            if left_button.is_clicked(event):
                attack_to -= 1
                if turn == attack_to:
                    attack_to -= 1
                if attack_to < 0:
                    attack_to = players_amount - attack_to
            if right_button.is_clicked(event):
                attack_to += 1
                if turn == attack_to:
                    attack_to += 1
                if attack_to > players_amount:
                    attack_to %= players_amount
            if do_smthB.is_clicked(event):
                print('conf_attack is clicked.')
                pass
            if back_b.is_clicked(event):
                event_type = 'board'
        elif event_type == 'win screen':
            if winB.is_clicked(event):
                event_type = 'menu'

    # --- draws ---

    if event_type == 'menu':
        gl_screen.fill((230, 230, 230))
        for button in menu_buttons:
            button.draw(gl_screen)

    elif event_type == 'board':
        gl_screen.fill((245, 245, 245))
        MoneyPT.set_text("$: " + str(money[turn]), (230, 255, 230))
        h_check = coms_consuption('heat', heat_list, turn) * -1
        if h_check is None:
            h_check = 0
        HeatPT.set_text("H: " + str(h_check))
        e_check = coms_consuption('electricity', electricity_list, turn) * -1
        if e_check is None:
            e_check = 0
        ElectricityPT.set_text("E: " + str(e_check), (255, 255, 200))
        for elem in board_objects:
            elem.draw(gl_screen)
        board_buildings.render()
        board_main.render()
        board_main.render_from_mas(turn)

        # event_type = 100 / 0 # у нас тут event_type == 'board' 2 раза - надо сделать для кнопок отдельное событие?

    elif event_type == 'before game':
        gl_screen.fill((245, 245, 245))
        for object in basic_choose_sc:
            object.draw(gl_screen)
        do_smthB.set_text("Подтвердть")
        desc_pmPT.set_text('Выберите количество игроков:')
        plus_minusPT.set_text(players_amount)
    elif event_type == 'nextturn':
        gl_screen.fill((245, 245, 245))
        click_on_me_b.draw(gl_screen)
    elif event_type == 'attack':
        desc_pmPT.set_text('Бомбим этого игрока:')
        gl_screen.fill((245, 245, 245))
        if turn == attack_to:
            attack_to += 1
        attack_to %= players_amount
        plus_minusPT.set_text(str(attack_to + 1))
        do_smthB.set_text("В атаку!")
        for object in basic_choose_sc:
            object.draw(gl_screen)
    elif event_type == 'win screen':
        gl_screen.fill((245, 245, 245))
        winB.draw(gl_screen)
        winPt.set_text("Игрок " + str(turn + 1) + ' - победитель!')
        winPt.draw(gl_screen)

    pygame.display.flip()

    # --- FPS ---

    clock.tick(FPS)

# --- end ---
pygame.quit()
