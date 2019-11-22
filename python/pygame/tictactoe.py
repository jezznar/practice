__description__ = 'A ditry-coded Tictactoe game made from pygame'
__requirements__ = [ 'pygame' ]
__version__ = '0.0.1'

import pygame
import time

SCREEN_SIZE = (1024, 768)

def reset_tictactoe():
    tictactoe = []
    for x in range(3):
        tictactoe.append(['','',''])
    return tictactoe

def draw_divisions(game_display, screen_size):
    for i in range(1,3):
        x = (screen_size[0] / 3) * i
        y = (screen_size[1] / 3) * i
        pygame.draw.line(
            game_display, pygame.Color('blue'), (x,0), 
            (x,screen_size[1]), 3
        )
        pygame.draw.line(
            game_display, pygame.Color('blue'), (0,y), 
            (screen_size[0],y), 3
        )
    pygame.display.update()
    return True

def draw_xo(player, position_points, game_font, game_display):
    text = game_font.render(player[0].upper(), True, 
        pygame.Color('white')
    )
    upper_position_points, lower_position_points = position_points
    x = int((lower_position_points[0] + upper_position_points[0] - \
        game_font.get_height())/2
    )
    y = int((lower_position_points[1] + upper_position_points[1] - \
        game_font.get_height())/2
    )
    game_display.blit(text,(x,y))
    pygame.display.update()
    return True

def draw_player_turn(player, status_font, game_display):
    text = 'Player {}\'s turn'.format(player)
    cover = pygame.Rect((0, SCREEN_SIZE[1] - status_font.get_height()),
        (status_font.size(text)[0],status_font.get_height())
    )  
    rendered_text = status_font.render(text, True, pygame.Color('white'))
    game_display.blit(rendered_text, (0,SCREEN_SIZE[1] - status_font.get_height()))
    pygame.display.update()
    pygame.draw.rect(game_display, pygame.Color('black'), cover)
    return True

def get_position_information(mouse_position, position_points):
    x = mouse_position[0]
    y = mouse_position[1]
    for position in range(len(position_points)):
        upper_position_points = position_points[position][0]
        lower_position_points = position_points[position][1]
        position_index = position_points[position][2]
        if x < lower_position_points[0] and \
            y < lower_position_points[1] and \
                x > upper_position_points[0] and \
                    y > upper_position_points[1]:
            return position_index, (upper_position_points, lower_position_points)
        else:
            continue

def is_game_end(player, tictactoe):
    status_code = 0
    status = ''
    #Check for horizontal
    for row in tictactoe:
        if list(set([player]) ^ set(row)) == []:
            status_code = 1
            break
    
    #Check for vertical
    if status_code == 0:
        verts = reset_tictactoe()
        for i in range(len(tictactoe)):
            for j in range(len(tictactoe[i])):
                verts[j].append(tictactoe[i][j])
        for vert in verts:
            if list(set([player]) ^ set(vert)) == []:
                status_code = 1
                break
    #Check for diagonal
    if status_code == 0:
        diags = [
            [
                tictactoe[0][0],
                tictactoe[1][1],
                tictactoe[2][2],
            ],
            [
                tictactoe[0][2],
                tictactoe[1][1],
                tictactoe[2][0],
            ],
        ]
        for diag in diags:
            if list(set([player]) ^ set(diag)) == []:
                status_code = 1
                break
    #Check for draw
    if status_code == 0:
        count = 0
        for row in tictactoe:
            for i in row:
                if i != '':
                    count += 1
        if count == 9:
            status_code = 2
    if status_code:
        if status_code == 1:
            status = '{} WINS!'.format(player)
        else:
            status = 'IT IS A DRAW!'
    return status

def calculate_position_points(screen_size, game_display):
    position_points = []
    for y in range(3):
        for x in range(3):
            p1 = (x * screen_size[0]/3,y * screen_size[1]/3)
            p1 = [int(x) for x in p1]
            p2 = ((x+1) * screen_size[0]/3,(y+1)* screen_size[1]/3)
            p2 = [int(x) for x in p2]
            position_points.append([p1,p2,[y,x]])
    return position_points

def update_tictac_toe(player, position_index, tictactoe):
    tictactoe[position_index[0]][position_index[1]] = player     
    return tictactoe

def is_move_valid(position_index, tictactoe):
    if tictactoe[position_index[0]][position_index[1]] != '':
        return False
    return True

def draw_final(game_status, game_font, screen_size, game_display):
    cover = pygame.Rect(
        (
            (SCREEN_SIZE[0] - game_font.size(game_status)[0])/2, (SCREEN_SIZE[1] - game_font.get_height())/2
        ),
        (
            game_font.size(game_status)[0], game_font.get_height()
        )
    )  
    pygame.draw.rect(game_display, pygame.Color('white'), cover)
    rendered_text = game_font.render(game_status, True, pygame.Color('green'))
    game_display.blit(rendered_text, (
        (SCREEN_SIZE[0] - game_font.size(game_status)[0])/2, (SCREEN_SIZE[1] - game_font.get_height())/2
    ))
    pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    TICTACTOE = reset_tictactoe()
    GAME_FONT = pygame.font.SysFont(None, 100)
    STATUS_FONT = pygame.font.SysFont(None, 20)
    GAME_DISPLAY = pygame.display.set_mode(SCREEN_SIZE)
    GAME_DISPLAY.fill(pygame.Color('black'))
    draw_divisions(GAME_DISPLAY, SCREEN_SIZE)
    POSITION_POINTS = calculate_position_points(SCREEN_SIZE, GAME_DISPLAY)
    players = ['X','O']
    GAME_STATUS = ''
    while GAME_STATUS == '':      
        for player in players:
            draw_player_turn(player, STATUS_FONT, GAME_DISPLAY)
            player_drawn = False
            while not player_drawn:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        position_index, position_points = \
                            get_position_information(
                                pygame.mouse.get_pos(), 
                                POSITION_POINTS
                            )
                        if is_move_valid(position_index, TICTACTOE):
                            TICTACTOE = update_tictac_toe(
                                player, position_index, TICTACTOE
                            )
                            player_drawn = draw_xo(
                                player, position_points, GAME_FONT, GAME_DISPLAY
                            )
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    else:
                        continue
            GAME_STATUS = is_game_end(player, TICTACTOE)
            if GAME_STATUS != '':
                break
    draw_final(GAME_STATUS, GAME_FONT, SCREEN_SIZE, GAME_DISPLAY)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
            
            
