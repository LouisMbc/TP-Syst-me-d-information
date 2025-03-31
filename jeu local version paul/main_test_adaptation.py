import tkinter as tk
from tkinter import *
from tkinter.messagebox import *
from random import randint
from Class_joueur import Joueur
from Class_plateau import Plateau
from flask import Flask, request, g
import psycopg2

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            dbname="jeu_loup",
            user="postgres",
            password="mysecretpassword",
            host="10.1.4.227",
            port="5434"
        )
    return g.db

def get_pos_joueur(id_joueur):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT origin_position_col, origin_position_row FROM players_play wHERE id_player = {id_joueur}")
    result = cursor.fetchone()
    if result is None:
        print("Aucun joueur trouvé avec cet ID.")
        return None
    print(f"Position du joueur {id_joueur} : {result}")
    conn.commit()
    cursor.close()
    return result

def test():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM players_play")
    result = cursor.fetchall()
    if result is None:
        print("Aucun joueur trouvé.")
        return None
    conn.commit()
    cursor.close()
    return result


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def build_vision(id_joueur):
    vision = ""
    pos_joueur = get_pos_joueur(id_joueur)
    x, y = pos_joueur[0], pos_joueur[1]
    for i in range(8):
        pass


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













def draw_vision_joueur(canvas, vision):
    cell_size = 40
    j = 0
    for i in range(len(vision)): 
        if i % 3 == 0 and i != 0:
            j+=1
        y0, x0 = j * cell_size, (i-j*3) * cell_size
        x1, y1 = x0 + cell_size, y0 + cell_size
        if vision[i] == "0":
            canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black", tags="shape")
        elif vision[i] == "1":
            canvas.create_rectangle(x0, y0, x1, y1, fill="blue", tags="shape")
        elif vision[i] == "2":
            canvas.create_rectangle(x0, y0, x1, y1, fill="black", tags="shape")
        else:
            canvas.create_rectangle(x0, y0, x1, y1, fill="red", tags="shape")














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




def main() :
    fenetre = tk.Tk()
    fenetre.title("Plateau de Jeu")
    plateau, joueurs = nouveau_jeu(10, 10, 5, 5, 1)

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


    #draw_plateau(canvas, plateau, joueurs)
    draw_vision_joueur(canvas, "020010030")
    print(test())

    fenetre.mainloop()

if __name__ == "__main__":
    main()


