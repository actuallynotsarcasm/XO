from socket import timeout
import pygame as pg, sys, time, ftplib, os

black = (0, 0, 0)
white = (255, 255, 255)
indigo = (75, 0, 130)
dark_slate_grey = (47, 79, 79)
green = (0, 255, 0)
aqua = (0, 255, 255)
blue = (0, 0, 255)
yellow = (255, 255, 0)

x = 1535
y = 800

pg.font.init()
pg.display.init()
window = pg.display.set_mode((x, y), pg.RESIZABLE)
pg.display.set_icon(pg.transform.scale(pg.image.load('XO_icon.jpg'), (32, 32)))
pg.display.set_caption('Крестики-нолики')
fps = 60
fps_clock = pg.time.Clock()
background = pg.image.load('XO_bg.jpg')
bg_pos = background.get_rect()

class button:
    
    def __init__(self, width, height, rounding, color, text, text_color, text_size, text_font, x, y):
        self.width = width
        self.height = height
        self.rounding = rounding
        self.color = color 
        self.x = x   
        self.y = y
        self.text = text
        self.text_size = text_size
        self.output = pg.font.Font(text_font, text_size).render(text, 1, text_color)

    def draw(self):
        pg.draw.rect(window, self.color, (self.x + self.rounding, self.y, self.width - 2 * self.rounding, self.height))
        pg.draw.rect(window, self.color, (self.x, self.y + self.rounding, self.width, self.height - 2 * self.rounding))
        pg.draw.circle(window, self.color, (self.x + self.rounding, self.y + self.rounding), self.rounding)
        pg.draw.circle(window, self.color, (self.x + self.width - self.rounding, self.y + self.rounding), self.rounding)
        pg.draw.circle(window, self.color, (self.x + self.width - self.rounding, self.y + self.height - self.rounding), self.rounding)
        pg.draw.circle(window, self.color, (self.x + self.rounding, self.y + self.height - self.rounding), self.rounding)
        window.blit(self.output, (self.x + self.width // 2 - int(0.26 * self.text_size) * len(self.text), self.y + (self.height - self.text_size) // 2 - int(self.text_size * 0.13)))  

    def check_click(self, pos):
        if pos[0] >= self.x and pos[0] <= self.x + self.width and pos[1] >= self.y and pos[1] <= self.y + self.height:
            return True
        else:
            return False

def five_in_a_row(coordinates, last_move):
    horiz = sorted([i[0] for i in filter(lambda x: x[1] == last_move[1], coordinates)])
    vert = sorted([i[1] for i in filter(lambda x: x[0] == last_move[0], coordinates)])
    diag_1 = sorted([i[0] for i in filter(lambda x: x[1] - x[0] == last_move[1] - last_move[0], coordinates)])
    diag_2 = sorted([i[0] for i in filter(lambda x: x[1] + x[0] == last_move[1] + last_move[0], coordinates)])
    if len(horiz) > 4:
        if horiz[0] == last_move[0] or horiz[-1] == last_move[0]:
            if horiz[:5] == [last_move[0] + i for i in range(5)] or horiz[-5:] == [last_move[0] - 4 + i for i in range(5)]:
                return True
        elif horiz[horiz.index(last_move[0]) + 1] == last_move[0] + 1 or horiz[horiz.index(last_move[0]) - 1] == last_move[0] - 1:
            if horiz[horiz.index(last_move[0]) + 1] != last_move[0] + 1:
                if len(horiz[:horiz.index(last_move[0])]) > 3:
                    if horiz[horiz.index(last_move[0]) - 4:horiz.index(last_move[0]) + 1] == [last_move[0] - 4 + i for i in range(5)]:
                        return True
            elif horiz[horiz.index(last_move[0]) - 1] != last_move[0] - 1:
                if len(horiz[horiz.index(last_move[0]):]) > 4:
                    if horiz[horiz.index(last_move[0]):horiz.index(last_move[0]) + 5] == [last_move[0] + i for i in range(5)]:
                        return True
            elif horiz[0] == last_move[0] - 1 or horiz[-1] == last_move[0] + 1:
                if horiz[:5] == [last_move[0] - 1 + i for i in range(5)] or horiz[-5:] == [last_move[0] - 3 + i for i in range(5)]:
                    return True
            elif horiz[horiz.index(last_move[0]) + 2] == last_move[0] + 2 or horiz[horiz.index(last_move[0]) - 2] == last_move[0] - 2:
                if horiz[horiz.index(last_move[0]) + 2] != last_move[0] + 2:
                    if len(horiz[:horiz.index(last_move[0])]) > 2:
                        if horiz[horiz.index(last_move[0]) - 3:horiz.index(last_move[0]) + 2] == [last_move[0] - 3 + i for i in range(5)]:
                            return True
                elif horiz[horiz.index(last_move[0]) - 2] != last_move[0] - 2:
                    if len(horiz[horiz.index(last_move[0]):]) > 3:
                        if horiz[horiz.index(last_move[0]) - 1:horiz.index(last_move[0]) + 4] == [last_move[0] - 1 + i for i in range(5)]:
                            return True
                elif horiz[horiz.index(last_move[0]) - 2:horiz.index(last_move[0]) + 3] == [last_move[0] - 2 + i for i in range(5)]:
                    return True
    if len(vert) > 4:
        if vert[0] == last_move[1] or vert[-1] == last_move[1]:
            if vert[:5] == [last_move[1] + i for i in range(5)] or vert[-5:] == [last_move[1] - 4 + i for i in range(5)]:
                return True
        elif vert[vert.index(last_move[1]) + 1] == last_move[1] + 1 or vert[vert.index(last_move[1]) - 1] == last_move[1] - 1:
            if vert[vert.index(last_move[1]) + 1] != last_move[1] + 1:
                if len(vert[:vert.index(last_move[1])]) > 3:
                    if vert[vert.index(last_move[1]) - 4:vert.index(last_move[1]) + 1] == [last_move[1] - 4 + i for i in range(5)]:
                        return True
            elif vert[vert.index(last_move[1]) - 1] != last_move[1] - 1:
                if len(vert[vert.index(last_move[1]):]) > 4:
                    if vert[vert.index(last_move[1]):vert.index(last_move[1]) + 5] == [last_move[1] + i for i in range(5)]:
                        return True
            elif vert[0] == last_move[1] - 1 or vert[-1] == last_move[1] + 1:
                if vert[:5] == [last_move[1] - 1 + i for i in range(5)] or vert[-5:] == [last_move[1] - 3 + i for i in range(5)]:
                    return True
            elif vert[vert.index(last_move[1]) + 2] == last_move[1] + 2 or vert[vert.index(last_move[1]) - 2] == last_move[1] - 2:
                if vert[vert.index(last_move[1]) + 2] != last_move[1] + 2:
                    if len(vert[:vert.index(last_move[1])]) > 2:
                        if vert[vert.index(last_move[1]) - 3:vert.index(last_move[1]) + 2] == [last_move[1] - 3 + i for i in range(5)]:
                            return True
                elif vert[vert.index(last_move[1]) - 2] != last_move[1] - 2:
                    if len(vert[vert.index(last_move[1]):]) > 3:
                        if vert[vert.index(last_move[1]) - 1:vert.index(last_move[1]) + 4] == [last_move[1] - 1 + i for i in range(5)]:
                            return True
                elif vert[vert.index(last_move[1]) - 2:vert.index(last_move[1]) + 3] == [last_move[1] - 2 + i for i in range(5)]:
                    return True
    if len(diag_1) > 4:
        if diag_1[0] == last_move[0] or diag_1[-1] == last_move[0]:
            if diag_1[:5] == [last_move[0] + i for i in range(5)] or diag_1[-5:] == [last_move[0] - 4 + i for i in range(5)]:
                return True
        elif diag_1[diag_1.index(last_move[0]) + 1] == last_move[0] + 1 or diag_1[diag_1.index(last_move[0]) - 1] == last_move[0] - 1:
            if diag_1[diag_1.index(last_move[0]) + 1] != last_move[0] + 1:
                if len(diag_1[:diag_1.index(last_move[0])]) > 3:
                    if diag_1[diag_1.index(last_move[0]) - 4:diag_1.index(last_move[0]) + 1] == [last_move[0] - 4 + i for i in range(5)]:
                        return True
            elif diag_1[diag_1.index(last_move[0]) - 1] != last_move[0] - 1:
                if len(diag_1[diag_1.index(last_move[0]):]) > 4:
                    if diag_1[diag_1.index(last_move[0]):diag_1.index(last_move[0]) + 5] == [last_move[0] + i for i in range(5)]:
                        return True
            elif diag_1[0] == last_move[0] - 1 or diag_1[-1] == last_move[0] + 1:
                if diag_1[:5] == [last_move[0] - 1 + i for i in range(5)] or diag_1[-5:] == [last_move[0] - 3 + i for i in range(5)]:
                    return True
            elif diag_1[diag_1.index(last_move[0]) + 2] == last_move[0] + 2 or diag_1[diag_1.index(last_move[0]) - 2] == last_move[0] - 2:
                if diag_1[diag_1.index(last_move[0]) + 2] != last_move[0] + 2:
                    if len(diag_1[:diag_1.index(last_move[0])]) > 2:
                        if diag_1[diag_1.index(last_move[0]) - 3:diag_1.index(last_move[0]) + 2] == [last_move[0] - 3 + i for i in range(5)]:
                            return True
                elif diag_1[diag_1.index(last_move[0]) - 2] != last_move[0] - 2:
                    if len(diag_1[diag_1.index(last_move[0]):]) > 3:
                        if diag_1[diag_1.index(last_move[0]) - 1:diag_1.index(last_move[0]) + 4] == [last_move[0] - 1 + i for i in range(5)]:
                            return True
                elif diag_1[diag_1.index(last_move[0]) - 2:diag_1.index(last_move[0]) + 3] == [last_move[0] - 2 + i for i in range(5)]:
                    return True
    if len(diag_2) > 4:
        if diag_2[0] == last_move[0] or diag_2[-1] == last_move[0]:
            if diag_2[:5] == [last_move[0] + i for i in range(5)] or diag_2[-5:] == [last_move[0] - 4 + i for i in range(5)]:
                return True
        elif diag_2[diag_2.index(last_move[0]) + 1] == last_move[0] + 1 or diag_2[diag_2.index(last_move[0]) - 1] == last_move[0] - 1:
            if diag_2[diag_2.index(last_move[0]) + 1] != last_move[0] + 1:
                if len(diag_2[:diag_2.index(last_move[0])]) > 3:
                    if diag_2[diag_2.index(last_move[0]) - 4:diag_2.index(last_move[0]) + 1] == [last_move[0] - 4 + i for i in range(5)]:
                        return True
            elif diag_2[diag_2.index(last_move[0]) - 1] != last_move[0] - 1:
                if len(diag_2[diag_2.index(last_move[0]):]) > 4:
                    if diag_2[diag_2.index(last_move[0]):diag_2.index(last_move[0]) + 5] == [last_move[0] + i for i in range(5)]:
                        return True
            elif diag_2[0] == last_move[0] - 1 or diag_2[-1] == last_move[0] + 1:
                if diag_2[:5] == [last_move[0] - 1 + i for i in range(5)] or diag_2[-5:] == [last_move[0] - 3 + i for i in range(5)]:
                    return True
            elif diag_2[diag_2.index(last_move[0]) + 2] == last_move[0] + 2 or diag_2[diag_2.index(last_move[0]) - 2] == last_move[0] - 2:
                if diag_2[diag_2.index(last_move[0]) + 2] != last_move[0] + 2:
                    if len(diag_2[:diag_2.index(last_move[0])]) > 2:
                        if diag_2[diag_2.index(last_move[0]) - 3:diag_2.index(last_move[0]) + 2] == [last_move[0] - 3 + i for i in range(5)]:
                            return True
                elif diag_2[diag_2.index(last_move[0]) - 2] != last_move[0] - 2:
                    if len(diag_2[diag_2.index(last_move[0]):]) > 3:
                        if diag_2[diag_2.index(last_move[0]) - 1:diag_2.index(last_move[0]) + 4] == [last_move[0] - 1 + i for i in range(5)]:
                            return True
                elif diag_2[diag_2.index(last_move[0]) - 2:diag_2.index(last_move[0]) + 3] == [last_move[0] - 2 + i for i in range(5)]:
                    return True
    return False

def exit_game():
    pg.quit()
    sys.exit(0)

def connect(server, number_of_try = 1):
    try:
        server.connect('192.168.1.88', timeout=2)
        server.login('jrm', 'Dumaesh 2005')
        server.getwelcome()
        return True
    except Exception:
        if number_of_try < 3:
            connect(server, number_of_try + 1)
        else:
            print('3 tries done')
            return False

def start_searching(server, nickname):
    server.cwd('XO')
    if 'p.txt' in server.nlst():
        print('file on server')
        with open('players.txt', 'wb') as f:
            server.retrbinary('RETR p.txt', f.write)
    else:
        print('file not on server')
        with open('players.txt', 'w') as f:
            f.write('')
        with open('players.txt', 'rb') as f:
            server.storbinary('STOR p.txt', f)
    players_file = open('players.txt', 'r')
    players_file_lines = players_file.readlines()
    print(players_file_lines)
    if players_file_lines == []:
        players_file.close()
        players_file = open('players.txt', 'w')
        players_file.writelines(nickname + ' waiting\n')
        print('v1')
    elif nickname not in ''.join(players_file_lines):
        players_file.close()
        players_file_lines.append(nickname + ' searching\n')
        players_file = open('players.txt', 'w')
        players_file.writelines(players_file_lines)
        print('v2')
    else:
        print('v3')
        for i in range(len(players_file_lines)):
            if nickname in players_file_lines[i]:
                players_file_lines[i] = nickname + ' searching\n'
                break
        players_file.close()
        players_file = open('players.txt', 'w')
        players_file.writelines(players_file_lines)
    players_file.close()
    print(players_file_lines)
    with open('players.txt', 'rb') as f:
        server.storbinary('STOR p.txt', f)

def create_session(server, nickname, enemy_nickname):
    server.cwd('/home/jrm/XO/sessions')
    directory = server.nlst()
    if directory != []:
        number = max([int(i[-1]) for i in directory]) + 1
    else:
        number = 0
    server.mkd('session' + str(number))
    server.cwd('/home/jrm/XO')
    with open('players.txt', 'wb') as f:
        server.retrbinary('RETR p.txt', f.write)
    players_file = open('players.txt')
    players_file_lines = players_file.readlines()
    for i in range(len(players_file_lines)):
        if nickname in players_file_lines[i]:
            self_index = i
            break
    for i in range(len(players_file_lines)):
        if enemy_nickname in players_file_lines[i]:
            enemy_index = i
            break
    players_file_lines[self_index] = nickname + ' playing ' + str(number) + '\n'
    players_file_lines[enemy_index] = enemy_nickname + ' playing ' + str(number) + '\n'
    players_file.close()
    players_file = open('players.txt', 'w')
    players_file.writelines(players_file_lines)
    players_file.close()
    with open('players.txt', 'rb') as f:
        server.storbinary('STOR p.txt', f)


def join_session(server, nickname):
    with open('players.txt', 'wb') as f:
        server.retrbinary('RETR p.txt', f.write)
    players_file = open('players.txt')
    players_file_lines = players_file.readlines()
    for i in range(len(players_file_lines)):
        if nickname in players_file_lines[i]:
            self_index = i
            break
    server.cwd('/home/jrm/XO/sessions')
    number = int(players_file_lines[self_index].split()[-1])
    server.cwd('session' + str(number))

def search_for_players(server, nickname):
    with open('players.txt', 'wb') as f:
        server.retrbinary('RETR p.txt', f.write)
    players_file = open('players.txt', 'r')
    players_file_lines = players_file.readlines()
    players_file_states = [i.split()[1] for i in players_file_lines]
    for i in range(len(players_file_lines)):
        if nickname in players_file_lines[i]:
            self_index = i
            break
    if (nickname + ' searching') in players_file_lines[self_index]:
        if len(players_file_lines) > 1:
            found = False
            for i in range(len(players_file_lines)):
                if i != self_index and players_file_states[i] == 'waiting':
                    players_file_lines[i] = players_file_lines[i].split()[0] + ' request ' + nickname + '\n'
                    found = True
                    break
            if not found:
                players_file_lines[self_index] = nickname + ' waiting\n'
        else:
            players_file_lines[self_index] = nickname + ' waiting\n'
        players_file.close()
        players_file = open('players.txt', 'w')
        players_file.writelines(players_file_lines)
        print(players_file_lines)
        players_file.close()
        with open('players.txt', 'rb') as f:
            server.storbinary('STOR p.txt', f)
    elif (nickname + ' request') in players_file_lines[self_index]:
        enemy_nickname = ' '.join(players_file_lines[self_index].split()[2:-1])
        for i in range(len(players_file_lines)):
            if enemy_nickname in players_file_lines[i]:
                enemy_index = i
                break
        if len(players_file_lines[self_index].split()) >= 4 and ('request ' + nickname) in players_file_lines[enemy_index]:
            symbol = 'O'
            create_session(server, nickname, enemy_nickname)
        else:
            players_file_lines[enemy_index] == enemy_nickname + ' request ' + nickname + ' a\n'
            symbol = 'X'
            players_file.close()
            players_file = open('players.txt', 'w')
            players_file.writelines(players_file_lines)
            players_file.close()
            with open('players.txt', 'rb') as f:
                server.storbinary('STOR p.txt', f)
        return symbol, enemy_nickname
    players_file.close()

def wait_for_session(server, nickname):
    with open('players.txt', 'wb') as f:
        server.retrbinary('RETR p.txt', f.write)
    players_file = open('players.txt')
    players_file_lines = players_file.readlines()
    for i in range(len(players_file_lines)):
        if nickname in players_file_lines[i]:
            self_index = i
            break
    if (nickname + ' playing') in players_file_lines[self_index]:
        join_session(server, nickname)
        return True
    else:
        return False

def send_coordinates(server, coordinates, symbol):
    with open('move_' + symbol + '1.txt', 'w') as f:
        f.writelines([str(i) for i in coordinates])
    with open('move_' + symbol + '1.txt', 'rb') as f:
        server.storbinary('STOR m_' + symbol + '.txt', f)

def get_coordinates(server, symbol):
    if symbol == 'X':
        symbol = 'O'
    else:
        symbol = 'X'
    directory = server.nlst()
    if 'move_' + symbol + '.txt' in directory:
        with open('move_' + symbol + '1.txt', 'wb') as f:
            server.retrbinary('m_' + symbol + '.txt', f.write)
        with open('move_' + symbol + '1.txt') as f:
            coordinates = f.readlines()
        server.delete('m_' + symbol + '.txt')
        return coordinates

def main():
    x_coords = []
    o_coords = []
    turn = True
    win = False
    winner = None
    scale_default = y // 10
    scale = scale_default
    field_offset = (0, 0)
    mouse_pos = (0, 0)
    timer_start = time.time()
    text_size = 20
    score = (0, 0)
    win_window = button(800, 500, 10, dark_slate_grey, '', black, 0, 'Fixedsys.ttf', x//2 - 400, y//2 - 250)
    end_game_button = button(100, 50, 5, black, 'end game', white, 20, 'Fixedsys.ttf', x//2 - 50 - 200, y//2 + 100)
    restart_button = button(100, 50, 5, black, 'restart', white, 20, 'Fixedsys.ttf', x//2 - 50 + 200, y//2 + 100)
    button_play_offline = button(300, 150, 10, aqua, 'Играть оффлайн', blue, 40, 'Fixedsys.ttf', x - 150 - 400, (y - 100) // 2)
    button_play_online = button(300, 150, 10, aqua, 'Играть онлайн', blue, 40, 'Fixedsys.ttf', x - 150 - 400, (y - 100) // 2 + 200)
    button_quit = button(75, 75, 10, aqua, 'Выйти', blue, 20, 'Fixedsys.ttf', x + 10 - 75, y + 10 - 75)
    button_back = button(75, 75, 10, aqua, 'Назад', blue, 20, 'Fixedsys.ttf', x + 10 - 75, - 10)
    screen = 'main_menu'
    game_mode = 'offline'
    symbol = 'X'
    nickname = 'host'
    enemy_nickname = 'just a player'
    server = ftplib.FTP()
    connected = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit_game()

            if screen == 'game':
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1 and not win and (game_mode == 'offline' or turn) and event.pos[1] > 70:
                        field_pos = ((event.pos[0] + field_offset[0])//scale, (event.pos[1] + field_offset[1])//scale)
                        if not (field_pos in x_coords) and not (field_pos in o_coords):
                            if (turn and game_mode == 'offline') or (game_mode == 'online' and symbol == 'X'):
                                if game_mode == 'online' and connected:
                                    send_coordinates(server, field_pos, 'X')
                                x_coords.append(field_pos)
                                if five_in_a_row(x_coords, field_pos):
                                    win = True
                                    winner = nickname + '(X)'
                                    win_text = button(0, 0, 0, black, winner + ' is a winner', green, 50, 'Fixedsys.ttf', x//2, y//2 - 175)
                                    score = score[0] + 1, score[1]
                            else:
                                if game_mode == 'online' and connected:
                                    send_coordinates(server, field_pos, 'O')
                                o_coords.append(field_pos)
                                if five_in_a_row(o_coords, field_pos):
                                    win = True
                                    winner = enemy_nickname + '(O)'
                                    win_text = button(0, 0, 0, black, winner + ' is a winner', green, 50, 'Fixedsys.ttf', x//2, y//2 - 175)
                                    score = score[0], score[1] + 1
                            turn = not turn
                    elif win:
                        if end_game_button.check_click(event.pos):
                            exit_game()
                        elif restart_button.check_click(event.pos):
                            win = False
                            winner = None
                            x_coords = []
                            o_coords = []
                            scale = scale_default
                            field_offset = (0, 0)
                            timer_start = time.time()
                    if event.button == 1 and button_back.check_click(event.pos):
                        screen = 'main_menu'
                        win = False
                        winner = None
                        x_coords = []
                        o_coords = []
                        scale = scale_default
                        field_offset = (0, 0)
                        timer_start = time.time()
                        turn = True
                        score = (0, 0)

                if event.type == pg.MOUSEWHEEL:
                    if scale > scale_default // 10 and event.y == -1:
                        field_offset = (scale - scale_default//10)*(mouse_pos[0] + field_offset[0])//scale - mouse_pos[0], (scale - scale_default//10)*(mouse_pos[1] + field_offset[1])//scale - mouse_pos[1]
                        scale -= scale_default // 10
                    elif scale < scale_default * 2 and event.y == 1:
                        field_offset = (scale + scale_default//10)*(mouse_pos[0] + field_offset[0])//scale - mouse_pos[0], (scale + scale_default//10)*(mouse_pos[1] + field_offset[1])//scale - mouse_pos[1]
                        scale += scale_default // 10

                if event.type == pg.MOUSEMOTION:
                    if bool(event.buttons[2]):
                        field_offset = field_offset[0] - event.rel[0], field_offset[1] - event.rel[1]
                    mouse_pos = event.pos
            elif screen == 'main_menu':
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if button_play_offline.check_click(event.pos):
                            screen = 'game'
                            game_mode = 'offline'
                        if button_play_online.check_click(event.pos):
                            screen = 'game'
                            game_mode = 'online'
                        if button_quit.check_click(event.pos):
                            exit_game()

        if screen == 'game':
            if game_mode == 'online':
                if not connected:
                    turn = False
                    print(1)
                    server = ftplib.FTP()
                    if connect(server):
                        print(2)
                        start_searching(server, nickname)
                        search = True
                        begin = False
                        connected = True
                        print(3)
                elif search:
                    search_result = search_for_players(server, nickname)
                    if bool(search_result):
                        symbol, enemy_nickname = search_result
                        search = False
                        print(4)
                elif not begin:
                    if wait_for_session(server, nickname):
                        if symbol == 'X':
                            turn = True
                        begin = True
                        print(5)
                elif not turn:
                    if symbol == 'X':
                        coords_received = get_coordinates(server, 'X')
                        if bool(coords_received):
                            x_coords.append(coords_received)
                            turn = not turn
                    else:
                        coords_received = get_coordinates(server, 'O')
                        if bool(coords_received):
                            o_coords.append(coords_received)
                            turn = not turn
            window.fill(black)
            for i in range(y//scale + 1):
                pg.draw.line(window, white, (0, -field_offset[1] % scale + scale*i), (x, -field_offset[1] % scale + scale*i), 1)
            for i in range(x//scale + 1):
                pg.draw.line(window, white, (-field_offset[0] % scale + scale*i, 0), (-field_offset[0] % scale + scale*i, y), 1)
            for i in x_coords:
                pg.draw.line(window, white, (-field_offset[0] + i[0]*scale + scale//2 - (scale//2 - scale//5), -field_offset[1] + i[1]*scale + scale//2 + (scale//2 - scale//5)), (-field_offset[0] + i[0]*scale + scale//2 + (scale//2 - scale//5), -field_offset[1] + i[1]*scale + scale//2 - (scale//2 - scale//5)), scale//20 + int(scale<20))
                pg.draw.line(window, white, (-field_offset[0] + i[0]*scale + scale//2 + (scale//2 - scale//5), -field_offset[1] + i[1]*scale + scale//2 + (scale//2 - scale//5)), (-field_offset[0] + i[0]*scale + scale//2 - (scale//2 - scale//5), -field_offset[1] + i[1]*scale + scale//2 - (scale//2 - scale//5)), scale//20 + int(scale<20))
            for i in o_coords:
                pg.draw.circle(window, white, (-field_offset[0] + i[0]*scale + scale//2, -field_offset[1] + i[1]*scale + scale//2), (scale//2 - scale//5), scale//25 + int(scale<25))
            pg.draw.rect(window, dark_slate_grey, pg.Rect(0, 0, x, 70))
            window.blit(pg.font.Font('Fixedsys.ttf', text_size).render('Time: ', 1, green), (25, 25))
            window.blit(pg.font.Font('Fixedsys.ttf', text_size).render(int((time.time() - timer_start) // 60 < 10) * '0' + str(int(time.time() - timer_start) // 60) + ':' + int(time.time() - timer_start < 10) * '0' + str(int(time.time() - timer_start) % 60), 1, green), (85, 25))
            window.blit(pg.font.Font('Fixedsys.ttf', text_size).render('Score: ', 1, green), (x//2 - 240, 70 // 2  - text_size // 2 - int(text_size * 0.13)))
            window.blit(pg.font.Font('Fixedsys.ttf', text_size).render(nickname+' (X)  :  '+enemy_nickname+' (O)', 1, green), (x//2 - int(0.26 * text_size) * len(nickname+' (X)  :  '+enemy_nickname+' (O)'), 10))
            window.blit(pg.font.Font('Fixedsys.ttf', text_size).render(str(score[0]) + '  :  ' + str(score[1]), 1, green), (x//2 - int(0.26 * text_size) * len(str(score[0]) + '  :  ' + str(score[1])), 35))
            button_back.draw()
            if win:
                win_window.draw()
                win_text.draw()
                end_game_button.draw()
                restart_button.draw()

        elif screen == 'main_menu':
            window.fill(black)
            window.blit(background, bg_pos)
            button_play_online.draw()
            button_play_offline.draw()
            button_quit.draw()
            button(0, 0, 0, white, 'Крестики-нолики', yellow, 100, 'FIxedsys.ttf', x - 400, 100).draw()
            button(0, 0, 0, white, '2.0', yellow, 150, 'FIxedsys.ttf', x - 400, 225).draw()

        pg.display.update()
        fps_clock.tick(fps)

main()