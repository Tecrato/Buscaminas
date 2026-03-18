import time
import random
import configparser
import pygame as pag
import Utilidades as uti
from threading import Thread
import Utilidades_pygame as uti_pag

from Utilidades_pygame.base_app_class import Base_class

from Tile import Tile


configuraciones = configparser.ConfigParser()
configuraciones.read("config.ini")

TILE_SIZE = int(configuraciones["TILE"]["TILE_SIZE"])
TILE_NUM = int(configuraciones["TILE"]["TILE_NUM"])
MINE_NUM = int(configuraciones["TILE"]["MINE_NUM"])
ANIMATION_SPEED = int(configuraciones["ANIMATION"]["ANIMATION_SPEED"])
sleep_time = 0.1/ANIMATION_SPEED if ANIMATION_SPEED > 0 else 0


class Buscaminas(Base_class):
    def otras_variables(self):
        self.draw_mode = "always"

        # Variables mas normales
        self.mines_pinged = 0
        self.tiles_restantes = TILE_NUM*TILE_NUM


        self.objs: list[Tile] = []
        self.board = []
        self.tilesheet = pag.transform.scale(pag.image.load("./tileset.jpg"),(TILE_SIZE*4, TILE_SIZE*3))
        self.imgs = {
            "idle": pag.Rect(0, 0, TILE_SIZE, TILE_SIZE),
            "pinged": pag.Rect(TILE_SIZE, 0, TILE_SIZE, TILE_SIZE),
            "mine": pag.Rect(TILE_SIZE*2, 0, TILE_SIZE, TILE_SIZE),
            "empty": pag.Rect(TILE_SIZE*3, 0, TILE_SIZE, TILE_SIZE),
        }
        n = 1
        for y in range(1, 3):
            for x in range(4):
                self.imgs[f"num{n}"] = pag.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                n += 1
        del n

        self.generate_board()
        self.generate_mines()
            
    def generate_objs(self):
        self.main_text_win = uti_pag.Text("YOU WIN", 24, None, (-5000,-5000), "center", "green", True, "black", -1, 20)
        self.main_text_Edouard_sandoval = uti_pag.Text("Edouard Sandoval", 24, None, self.ventana_rect.bottomright, "bottomright","black")

        self.main_text_Edouard_sandoval.lista_text[0].set_alpha(128)

        # self.surf_marca_agua = pag.Surface((TILE_SIZE//2, TILE_SIZE//4), pag.SRCALPHA)
        # self.surf_marca_agua.fill((0,0,0,0))
        # self.surf_marca_agua.set_alpha(128)
        # self.main_text_Edouard_sandoval.draw(self.surf_marca_agua)

        self.lists_screens[self.inicial_screen]["draw"] = [
            self.main_text_win,
            self.main_text_Edouard_sandoval
        ]
        self.lists_screens[self.inicial_screen]["update"] =  self.lists_screens[self.inicial_screen]["draw"]

    def draw_before(self, actual_screen):
        for y in self.board:
            for x in y:
                self.ventana.blit(self.tilesheet, x.position, self.imgs[x.state])

    def otro_evento(self, actual_screen, evento):
        if evento.type == pag.KEYDOWN:
            if evento.key == pag.K_ESCAPE:
                self.running = False
        if evento.type == pag.MOUSEBUTTONDOWN and evento.button in (1, 3):
            r = pag.Rect(0, 0, TILE_SIZE, TILE_SIZE)
            for i,y in enumerate(self.board):
                for i2,x in enumerate(y):
                    r.topleft = x.position
                    if r.collidepoint(evento.pos):
                        if evento.button == 3:
                            if x.state == "idle":
                                x.state = "pinged"
                                if x.mine:
                                    self.mines_pinged += 1
                            elif x.state == "pinged":
                                x.state = "idle"
                                if x.mine:
                                    self.mines_pinged -= 1
                        elif evento.button == 1:
                            if x.mine:
                                x.state = "mine"
                                self.running = False
                            elif x.state == "idle":
                                self.set_adjacent_neightbors(i, i2)

    def update(self, actual_screen):
        if self.mines_pinged == MINE_NUM or self.tiles_restantes == MINE_NUM:
            self.win()

    # ---------------- Funciones ----------------
    def win(self):
        # self.running = False
        self.main_text_win.pos = self.ventana_rect.center


    def generate_board(self):
        for x in range(TILE_NUM):
            l = []
            for y in range(TILE_NUM):
                l.append(Tile(pag.Vector2(x*TILE_SIZE, y*TILE_SIZE)))
            self.board.append(l.copy())
            l.clear()
    def set_adjacent_neightbors(self, x, y, sleep=0):
        time.sleep(sleep)
        if self.board[x][y].state != "idle":
            return
        self.board[x][y].neightbors = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if x+i < 0 or x+i > TILE_NUM-1 or y+j < 0 or y+j > TILE_NUM-1:
                    continue
                self.board[x][y].neightbors += 1 if self.board[x+i][y+j].mine == True else 0
        if self.board[x][y].neightbors == 0:
            self.board[x][y].state = "empty"
            for x2 in range(-1, 2):
                for y2 in range(-1, 2):
                    if x2 == 0 and j == 0:
                        continue
                    if x+x2 < 0 or x+x2 > TILE_NUM-1 or y+y2 < 0 or y+y2 > TILE_NUM-1:
                        continue
                    if sleep_time > 0:
                        Thread(target=self.set_adjacent_neightbors, args=(x+x2, y+y2,sleep_time),daemon=True).start()
                    else:
                        self.set_adjacent_neightbors(x+x2, y+y2, sleep_time)
        else:
            self.board[x][y].state = f"num{self.board[x][y].neightbors}"
        self.tiles_restantes -= 1
    
    def generate_mines(self):
        for x in range(MINE_NUM):
            x = random.randint(0, TILE_NUM-1)
            y = random.randint(0, TILE_NUM-1)
            self.board[x][y].mine = True
        


if __name__ == "__main__":
    resolution = (TILE_NUM * TILE_SIZE, TILE_NUM * TILE_SIZE)

    Buscaminas(
        uti_pag.Config(
            title="Buscaminas",
            description="Ejemplo de juego de buscaminas",
            author="Edouard Sandoval",
            my_company="Edouard Sandoval",
            resolution=resolution,
            min_resolution=(resolution),
            scaled=False,
            window_resize=False,
            version="1.0",
            icon="./tileset.jpg"
        )
    )