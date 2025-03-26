from random import *

class Plateau:
    def __init__(self, nb_colonnes: int, nb_lignes: int, nb_obstacles: int, pos_obstacles: list = None):
        self.nb_colonnes = nb_colonnes
        self.nb_lignes = nb_lignes
        self.nb_obstacles = nb_obstacles
        self.pos_obstacles = pos_obstacles if pos_obstacles is not None else self.generate_random_obstacles()
        self.joueurs = []

    # Getters
    def get_nb_colonnes(self):
        return self.nb_colonnes

    def get_nb_lignes(self):
        return self.nb_lignes

    def get_nb_obstacles(self):
        return self.nb_obstacles

    def get_pos_obstacles(self):
        return self.pos_obstacles
    
    def get_joueurs(self):
        return self.joueurs
    
    # Setters

    def set_nb_colonnes(self, nb_colonnes):
        self.nb_colonnes = nb_colonnes

    def set_nb_lignes(self, nb_lignes):
        self.nb_lignes = nb_lignes

    def set_nb_obstacles(self, nb_obstacles):
        self.nb_obstacles = nb_obstacles

    def generate_random_obstacles(self):
        obstacles = []
        for _ in range(self.nb_obstacles):
            x = 0
            y = 0
            while((x,y) in obstacles or (x,y) in [(0,0),(4,4)]):
                x = randint(0, self.nb_colonnes - 1)
                y = randint(0, self.nb_lignes - 1)
            obstacles.append((x, y))
        return obstacles

    def add_joueur(self, joueur):
        self.joueurs.append(joueur)


    def __str__(self):
        plateau = ""
        info = "Plateau de jeu de taille {}x{} avec {} obstacles\n".format(self.nb_colonnes, self.nb_lignes, self.nb_obstacles)
        info_obstacles = "Obstacles: {}\n".format(self.pos_obstacles)
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                if (j, i) in self.pos_obstacles:
                    plateau += "X"
                else:
                    plateau += "."
            plateau += "\n"
        return info + info_obstacles + plateau

