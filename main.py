import pygame as pag
import Utilidades as uti
import Utilidades_pygame as uti_pag
import random
import configparser

from Utilidades_pygame.base_app_class import Base_class

from Tile import Tile


configuraciones = configparser.ConfigParser()
configuraciones.read("config.ini")

TILE_SIZE = int(configuraciones["TILE"]["TILE_SIZE"])
TILE_NUM = int(configuraciones["TILE"]["TILE_NUM"])
MINE_NUM = int(configuraciones["TILE"]["MINE_NUM"])


class Buscaminas(Base_class):
    def otras_variables(self):
        self.draw_mode = "always"
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

    def generate_board(self):
        for x in range(TILE_NUM):
            l = []
            for y in range(TILE_NUM):
                l.append(Tile(pag.Vector2(x*TILE_SIZE, y*TILE_SIZE)))
            self.board.append(l.copy())
            l.clear()
            
        
    def draw_after(self, actual_screen):
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
                            elif x.state == "pinged":
                                x.state = "idle"
                        elif evento.button == 1:
                            if x.mine:
                                x.state = "mine"
                                self.running = False
                            elif x.state != "idle":
                                pass
                            else:
                                self.set_adjacent_neightbors(i, i2)


    def set_adjacent_neightbors(self, x, y):
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
                    self.set_adjacent_neightbors(x+x2, y+y2)
        else:
            self.board[x][y].state = f"num{self.board[x][y].neightbors}"

    def adyacent_neightbors(self, x, y):
        neightbors = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if x+i < 0 or x+i > TILE_NUM-1 or y+j < 0 or y+j > TILE_NUM-1:
                    continue
                neightbors += self.board[x+i][y+j].mine == True
        return neightbors
    
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
            window_resize=False
        )
    )