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
            if (j, i) in plateau.get_pos_obstacles():
                canvas.create_rectangle(x0, y0, x1, y1, fill="red", tags="shape")
            else:
                joueur_present = False
                for joueur in joueurs:
                    if joueur.get_co_x() == j and joueur.get_co_y() == i:
                        joueur_present = True
                        if joueur.get_role() == "loup":
                            canvas.create_rectangle(x0, y0, x1, y1, fill="black", tags="shape")
                        elif joueur.get_role() == "villageois":
                            canvas.create_rectangle(x0, y0, x1, y1, fill="blue", tags="shape")
                        break
                if not joueur_present:
                    canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black", tags="shape")
    check_victoire(joueurs)







def joueur_haut(canvas, plateau, joueurs):
    for villageoi in joueurs:
        if villageoi.get_role() == "villageois":
            joueur = villageoi
    if joueur.get_co_y() > 0 and (joueur.get_co_x(), joueur.get_co_y() - 1) not in plateau.get_pos_obstacles() and joueur.get_etat() == "OK":
        joueur.set_co_y(joueur.get_co_y() - 1)
        print("haut")
    draw_plateau(canvas, plateau, joueurs)

def joueur_bas(canvas, plateau, joueurs):
    for villageoi in joueurs:
        if villageoi.get_role() == "villageois":
            joueur = villageoi
    if joueur.get_co_y() < plateau.get_nb_lignes() - 1 and (joueur.get_co_x(), joueur.get_co_y() + 1) not in plateau.get_pos_obstacles() and joueur.get_etat() == "OK":
        joueur.set_co_y(joueur.get_co_y() + 1)
        print("bas")
    draw_plateau(canvas, plateau, joueurs)

def joueur_droite(canvas, plateau, joueurs):
    for villageoi in joueurs:
        if villageoi.get_role() == "villageois":
            joueur = villageoi
    if joueur.get_co_x() < plateau.get_nb_colonnes() - 1 and (joueur.get_co_x()+1, joueur.get_co_y()) not in plateau.get_pos_obstacles() and joueur.get_etat() == "OK":
        joueur.set_co_x(joueur.get_co_x() + 1)
        print("droite")
    draw_plateau(canvas, plateau, joueurs)

def joueur_gauche(canvas, plateau, joueurs):
    for villageoi in joueurs:
        if villageoi.get_role() == "villageois":
            joueur = villageoi
    if joueur.get_co_x() > 0 and (joueur.get_co_x()-1, joueur.get_co_y()) not in plateau.get_pos_obstacles() and joueur.get_etat() == "OK":
        joueur.set_co_x(joueur.get_co_x() - 1)
        print("gauche")
    draw_plateau(canvas, plateau, joueurs)





def check_victoire(joueurs):
    villageois = []
    loups = []
    for joueur in joueurs:
        if joueur.get_role() == "villageois":
            villageois.append(joueur)
        elif joueur.get_role() == "loup":
            loups.append(joueur)
    for loup in loups:
        for villageoi in villageois:
            if loup.get_co_x() == villageoi.get_co_x() and loup.get_co_y() == villageoi.get_co_y():
                villageoi.set_etat("KO")
                print("villageois KO")
                joueurs.remove(villageoi)




def nouveau_jeu(taille_x, taille_y, nb_obstacle, nb_joueurs, nb_loup):
    print()
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
        print()
        print("---------------")
        joueurs[i].info_joueur()
    

    return plateau, joueurs




def main(taille_x, taille_y, nb_obstacle, nb_joueurs, nb_loup, first_game) :
    plateau, joueurs = nouveau_jeu(taille_x, taille_y, nb_obstacle, nb_joueurs, nb_loup)
    if (first_game == 1):
        canvas = tk.Canvas(fenetre, width=plateau.get_nb_colonnes() * 40, height=plateau.get_nb_lignes() * 40+250) 
        canvas.pack()

    button_haut = Button(text="haut",command = lambda : joueur_haut(canvas, plateau, joueurs))
    button_haut.place(x=-80+plateau.get_nb_colonnes() * 20, y=plateau.get_nb_lignes() * 40, width=160, height=50)

    button_bas = Button(text="bas",command = lambda : joueur_bas(canvas, plateau, joueurs))
    button_bas.place(x=-80+plateau.get_nb_colonnes() * 20, y=plateau.get_nb_lignes() * 40+100, width=160, height=50)

    button_droite = Button(text="droite",command = lambda : joueur_droite(canvas, plateau, joueurs))
    button_droite.place(x=plateau.get_nb_colonnes() * 20, y=plateau.get_nb_lignes() * 40+50, width=160, height=50)

    button_gauche = Button(text="gauche",command = lambda : joueur_gauche(canvas, plateau, joueurs))
    button_gauche.place(x=-160+plateau.get_nb_colonnes() * 20, y=plateau.get_nb_lignes() * 40+50, width=160, height=50)


    button_new_game = Button(text="New game",command = lambda : main(10, 10, 5, 3, 1, 0))
    button_new_game.place(x=-200+plateau.get_nb_colonnes() * 20, y=plateau.get_nb_lignes() * 40+200, width=160, height=50)

    spinbox_colonne = tk.Spinbox(fenetre, from_=2, to=15)
    spinbox_colonne.place(x=-40+plateau.get_nb_colonnes() * 20, y=plateau.get_nb_lignes() * 40+230, width=40, height=20)
    spinbox_ligne = tk.Spinbox(fenetre, from_=2, to=15)
    spinbox_ligne.place(x=plateau.get_nb_colonnes() * 20, y=plateau.get_nb_lignes() * 40+230, width=40, height=20)
    spinbox_obstacle = tk.Spinbox(fenetre, from_=0, to=75)
    spinbox_obstacle.place(x=40+plateau.get_nb_colonnes() * 20, y=plateau.get_nb_lignes() * 40+230, width=40, height=20)
    spinbox_joueurs = tk.Spinbox(fenetre, from_=2, to=20)
    spinbox_joueurs.place(x=80+plateau.get_nb_colonnes() * 20, y=plateau.get_nb_lignes() * 40+230, width=40, height=20)
    spinbox_loup = tk.Spinbox(fenetre, from_=1, to=19)
    spinbox_loup.place(x=120+plateau.get_nb_colonnes() * 20, y=plateau.get_nb_lignes() * 40+230, width=40, height=20)


    draw_plateau(canvas, plateau, joueurs)



fenetre = tk.Tk()
fenetre.title("Plateau de Jeu")

main(10, 10, 5, 3, 1, 1)
fenetre.mainloop()