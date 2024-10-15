import curses 
# Criar um terminal isolado
# python -m pip install windows-curses (No windows precisa instalar, pois ele é por default Linux)

import random
import time

def game_loop(window, game_speed): 
    # Nomear o terminal isolado do curses

    # Setup inicial
    curses.curs_set(0) # O cursos não aparece no terminal
    snake = [ # Uma snake que é uma lista de listas | [Y, X] posição do terminal
         [12, 15],
         [11, 15],
         [10, 15],
         ]
    fruit = get_new_fruit(window=window)
    current_direction = curses.KEY_DOWN
    snake_ate_fruit = False

    score = 0

    while True:
        draw_screen(window=window)
        draw_snake(snake=snake, window=window)
        draw_actor(actor=fruit, window=window, char=curses.ACS_DIAMOND)
        direction = get_new_direction(window=window, timeout=game_speed)
        if direction is None:
            direction = current_direction
        if direction_is_opposite(direction=direction, current_direction=current_direction):
            direction = current_direction 
        move_snake(snake=snake, direction=direction, snake_ate_fruit=snake_ate_fruit)
        if snake_hit_border(snake=snake, window=window):
            break
        if snake_hit_itself(snake=snake):
            break
        if snake_hit_fruit(snake=snake, fruit=fruit):
            snake_ate_fruit = True
            fruit = get_new_fruit(window=window)
            score += 1
        else:
             snake_ate_fruit = False
        current_direction = direction    
    finish_game(score=score, window=window)

def finish_game(score, window):
     height, width = window.getmaxyx()
     s = f'Você perdeu! Coletou {score} frutas.'
     y = int(height/2)
     x = int((width - len(s)) /2)
     window.addstr(y, x, s)
     window.refresh()
     time.sleep(3)

def direction_is_opposite(direction, current_direction):
     match direction:
            case curses.KEY_UP:
                return current_direction == curses.KEY_DOWN
            case curses.KEY_LEFT:
                return current_direction == curses.KEY_RIGHT
            case curses.KEY_DOWN:
                return current_direction == curses.KEY_UP
            case curses.KEY_RIGHT:
                return current_direction == curses.KEY_LEFT     

def snake_hit_itself(snake):
     head = snake[0]
     body = snake[1:]
     return head in body

def get_new_fruit(window):
     heigth, width = window.getmaxyx()
     return [random.randint(1, heigth-3), random.randint(1, width-3)]

def snake_hit_fruit(snake, fruit):
     return fruit in snake     

def snake_hit_border(snake, window):
     head = snake[0]
     return actor_ht_border(actor=head, window=window)

def draw_screen(window):
        window.clear()
        window.border(0) # Mostrar o limite da janela do terminal

def draw_snake(snake, window):
     head = snake[0]
     draw_actor(actor=head, window=window, char= '@')
     body = snake[1:]
     for body_part in body:
          draw_actor(actor=body_part, window=window, char= '#')

def draw_actor(actor, window, char):
        window.addch(actor[0], actor[1], char)

def get_new_direction(window, timeout):
        window.timeout(timeout) # Sem interação pelo intervalo definido ele vai retornar -1 (representação de ausência)
        direction = window.getch() # Ele vai pausar a execução e aguardar algum caracter ser inserido (input) | Ele faz o refrash por padrão
        if direction in [curses.KEY_UP, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_RIGHT]:
            return direction
        return None

def move_snake(snake, direction, snake_ate_fruit):
     head = snake[0].copy() # Criar uma cópia da minha ListaSnake
     move_actor(actor=head, direction=direction) 
     snake.insert(0, head) # Inserir na minha ListaSnake esse head com o valor reduzido
     if not snake_ate_fruit:
        snake.pop() # Realizar o pop para remover da minha ListaSnake o valor final, dessa forma ele deleta o da frente e adiciona atrás (como se estivesse andando) | Ex.: 3 4 5 --(virou)--> 2 3 4

def move_actor(actor, direction):
        match direction:
            case curses.KEY_UP:
                actor[0] -= 1 # Retirar do Y o valor 1 para subir
            case curses.KEY_LEFT:
                actor[1] -= 1 # Retirar do X o valor 1 para ir paras esquerda
            case curses.KEY_DOWN:
                actor[0] += 1 # Adicionar do Y o valor 1 para descer
            case curses.KEY_RIGHT:
                actor[1] += 1 # Adicionar do X o valor 1 para ir para direita

def actor_ht_border(actor, window):
        height, width = window.getmaxyx() # Altura, Largura nessa ordem 
        if(actor[0] <=0 ) or (actor[0] >= height -1):
            return True
        if(actor[1] <= 0) or (actor[1] >= width -1):
            return True
        return False

def select_difficulty():
    difficulty = {
        '1': 1000,
        '2': 500,
        '3': 150,
        '4': 90,
        '5': 35,
    }
    while True:
        answer = input('Selecione a dificuldade de 1 a 5:')
        game_speed = difficulty.get(answer)
        if game_speed is not None:
            return game_speed
        print('Escolha a dificuldade de 1 a 5!')


if __name__ == '__main__':
    curses.wrapper(game_loop, game_speed=select_difficulty())