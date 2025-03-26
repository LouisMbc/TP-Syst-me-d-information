import tkinter as tk
from tkinter import *
from tkinter.messagebox import *
from random import randint
from Class_joueur import Joueur
from Class_plateau import Plateau


def draw_plateau(canvas, plateau, joueurs):
    cell_size = 40
    for i in range(plateau.get_nb_lignes()):
        for j in range(plateau.get_nb_colonnes()):
            x0, y0 = j * cell_size, i * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size

            # Vérifie si la position (j, i) est un obstacle
            if (j, i) in plateau.get_pos_obstacles():
                canvas.create_rectangle(x0, y0, x1, y1, fill="red")
            else:
                # Vérifie si un joueur est à la position (j, i)
                joueur_present = False
                for joueur in joueurs:
                    if joueur.get_co_x() == j and joueur.get_co_y() == i:
                        joueur_present = True
                        if joueur.get_role() == "loup":
                            canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                        elif joueur.get_role() == "villageois":
                            canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
                        break

                # Si aucun joueur n'est présent, dessine une case vide
                if not joueur_present:
                    canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")





def joueur_haut(canvas, plateau, joueurs):
    joueur = joueurs[1]
    if joueur.get_co_y() > 0 and (joueur.get_co_x(), joueur.get_co_y() - 1) not in plateau.get_pos_obstacles():
        joueur.set_co_y(joueur.get_co_y() - 1)
        print("haut")
    draw_plateau(canvas, plateau, joueurs)

def joueur_bas(canvas, plateau, joueurs):
    joueur = joueurs[1]
    if joueur.get_co_y() < plateau.get_nb_lignes() - 1 and (joueur.get_co_x(), joueur.get_co_y() + 1) not in plateau.get_pos_obstacles():
        joueur.set_co_y(joueur.get_co_y() + 1)
        print("bas")
    draw_plateau(canvas, plateau, joueurs)

def joueur_droite(canvas, plateau, joueurs):
    joueur = joueurs[1]
    if joueur.get_co_x() < plateau.get_nb_colonnes() - 1 and (joueur.get_co_x()+1, joueur.get_co_y()) not in plateau.get_pos_obstacles():
        joueur.set_co_x(joueur.get_co_x() + 1)
        print("droite")
    draw_plateau(canvas, plateau, joueurs)

def joueur_gauche(canvas, plateau, joueurs):
    joueur = joueurs[1]
    if joueur.get_co_x() > 0 and (joueur.get_co_x()-1, joueur.get_co_y()) not in plateau.get_pos_obstacles():
        joueur.set_co_x(joueur.get_co_x() - 1)
        print("gauche")
    draw_plateau(canvas, plateau, joueurs)






def nouveau_jeu(taille_x, taille_y, nb_obstacle, nb_joueurs, nb_loup):
    print("----nouveau jeu----")
    plateau = Plateau(taille_x, taille_y, nb_obstacle)
    print(plateau)
    joueurs = []
    for i in range(nb_joueurs):
        x = 0
        y = 0
        while((x,y) in plateau.get_pos_obstacles()):
                x = randint(0, taille_x - 1)
                y = randint(0, taille_y - 1)
        if i <= nb_loup-1:
            joueurs.append(Joueur(i, "loup", x, y, "OK", 0))
        else:
            joueurs.append(Joueur(i, "villageois", x, y, "OK", 0))
        joueurs[i].info_joueur()
    print(len(joueurs))

    return plateau, joueurs







def main():
    fenetre = tk.Tk()
    fenetre.title("Plateau de Jeu")

    plateau, joueurs = nouveau_jeu(10, 10, 5, 2, 1)

    canvas = tk.Canvas(fenetre, width=plateau.get_nb_colonnes() * 40, height=plateau.get_nb_lignes() * 40)
    canvas.pack()

    button_haut = Button(text="haut",command = lambda : joueur_haut(canvas, plateau, joueurs[-1]))
    button_haut.place(x=670, y=400, width=160, height=50)

    button_bas = Button(text="bas",command = lambda : joueur_bas(canvas, plateau, joueurs[-1]))
    button_bas.place(x=670, y=450, width=160, height=50)

    button_droite = Button(text="droite",command = lambda : joueur_droite(canvas, plateau, joueurs[-1]))
    button_droite.place(x=670, y=500, width=160, height=50)

    button_gauche = Button(text="gauche",command = lambda : joueur_gauche(canvas, plateau, joueurs[-1]))
    button_gauche.place(x=670, y=550, width=160, height=50)

    draw_plateau(canvas, plateau, joueurs)
    fenetre.mainloop()

if __name__ == "__main__":
    main()