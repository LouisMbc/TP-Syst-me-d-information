from Class_joueur import Joueur
from Class_plateau import Plateau
from tkinter import *

def draw_plateau(canvas, plateau, joueur, loup):
    cell_size = 40 
    for i in range(plateau.get_nb_lignes()):
        for j in range(plateau.get_nb_colonnes()):
            x0, y0 = j * cell_size, i * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            if (j, i) in plateau.get_pos_obstacles():
                draw_bomb(canvas, x0, y0, x1, y1)
                canvas.create_rectangle(x0, y0, x1, y1, fill=None, outline="black") 

            elif (j, i) == (joueur.get_co_x(),joueur.get_co_y()):
                draw_smiley(canvas, x0, y0, x1, y1)
                canvas.create_rectangle(x0, y0, x1, y1, fill=None, outline="black") 

            elif (j, i) == (loup.get_co_x(),loup.get_co_y()):
                canvas.create_oval(x0, y0, x1, y1, fill="red")
                canvas.create_rectangle(x0, y0, x1, y1, fill=None, outline="black") 


            else:
                canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black") 

def draw_bomb(canvas, x0, y0, x1, y1):
    center_x = (x0 + x1) / 2
    center_y = (y0 + y1) / 2
    radius = (x1 - x0) / 4
    canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill="black")
    canvas.create_line(center_x, y0 + 10, center_x, y0 + 5, fill="red", width=2)

def draw_smiley(canvas, x0, y0, x1, y1):
    canvas.create_oval(x0, y0, x1, y1, fill="yellow", outline="black")
    eye_size = (x1 - x0) / 8
    eye_x_offset = (x1 - x0) / 4
    eye_y_offset = (y1 - y0) / 4
    canvas.create_oval(x0 + eye_x_offset, y0 + eye_y_offset, x0 + eye_x_offset + eye_size, y0 + eye_y_offset + eye_size, fill="black")
    canvas.create_oval(x1 - eye_x_offset - eye_size, y0 + eye_y_offset, x1 - eye_x_offset, y0 + eye_y_offset + eye_size, fill="black")
    canvas.create_arc(x0 + eye_x_offset, y1 - eye_y_offset - eye_size, x1 - eye_x_offset, y1 - eye_y_offset, start=0, extent=-180, style=ARC, outline="black", width=2)

def joueur_haut(canvas, plateau, joueur,loup):
    if joueur.get_co_y() > 0 and (joueur.get_co_x(), joueur.get_co_y() - 1) not in plateau.get_pos_obstacles():
        joueur.set_co_y(joueur.get_co_y() - 1)
        print("haut")
    draw_plateau(canvas, plateau, joueur,loup)

def joueur_bas(canvas, plateau, joueur,loup):
    if joueur.get_co_y() < plateau.get_nb_lignes() - 1 and (joueur.get_co_x(), joueur.get_co_y() + 1) not in plateau.get_pos_obstacles():
        joueur.set_co_y(joueur.get_co_y() + 1)
        print("bas")
    draw_plateau(canvas, plateau, joueur,loup)

def joueur_droite(canvas, plateau, joueur,loup):
    if joueur.get_co_x() < plateau.get_nb_colonnes() - 1 and (joueur.get_co_x()+1, joueur.get_co_y()) not in plateau.get_pos_obstacles():
        joueur.set_co_x(joueur.get_co_x() + 1)
        print("droite")
    draw_plateau(canvas, plateau, joueur,loup)

def joueur_gauche(canvas, plateau, joueur,loup):
    
    if joueur.get_co_x() > 0 and (joueur.get_co_x()-1, joueur.get_co_y()) not in plateau.get_pos_obstacles():
        joueur.set_co_x(joueur.get_co_x() - 1)
        print("gauche")
    draw_plateau(canvas, plateau, joueur, loup)


def main():
    fenetre = Tk()
    fenetre.title("Plateau de Jeu")

    joueur = Joueur(1, "villageois", 0, 0, "OK", 0)
    print(joueur)

    loup = Joueur(1, "loup", 4, 4, "OK", 0)
    print(loup)

    plateau = Plateau(nb_colonnes=5, nb_lignes=5, nb_obstacles=3)
    print(plateau)

    canvas = Canvas(fenetre, width=plateau.get_nb_colonnes() * 40, height=plateau.get_nb_lignes() * 40)
    canvas.pack()

    button_haut = Button(text="haut",command = lambda : joueur_haut(canvas, plateau, joueur,loup))
    button_haut.place(x=670, y=400, width=160, height=50)

    button_bas = Button(text="bas",command = lambda : joueur_bas(canvas, plateau, joueur,loup))
    button_bas.place(x=670, y=450, width=160, height=50)

    button_droite = Button(text="droite",command = lambda : joueur_droite(canvas, plateau, joueur,loup))
    button_droite.place(x=670, y=500, width=160, height=50)

    button_gauche = Button(text="gauche",command = lambda : joueur_gauche(canvas, plateau, joueur,loup))
    button_gauche.place(x=670, y=550, width=160, height=50)

    draw_plateau(canvas, plateau, joueur, loup)
    fenetre.mainloop()

if __name__ == "__main__":
    main()