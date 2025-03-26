class Joueur:
    def __init__(self, id : int, role : str, co_x : int, co_y : int, etat : str, deplacement : int):
        self.__id = id
        self.__role = role
        self.__co_x = co_x
        self.__co_y = co_y
        self.__etat = etat
        self.__deplacement = deplacement

    def get_id(self):
        return self.__id
    
    def get_role(self):
        return self.__role
    
    def get_co_x(self): 
        return self.__co_x
    
    def get_co_y(self):
        return self.__co_y
    
    def get_etat(self):
        return self.__etat
    
    def get_deplacement(self):
        return self.__deplacement
    
    def set_id(self, id):
        self.__id = id

    def set_role(self, role):
        self.__role = role
    
    def set_co_x(self, co_x):
        self.__co_x = co_x
    
    def set_co_y(self, co_y):
        self.__co_y = co_y
    
    def set_etat(self, etat):
        self.__etat = etat
    
    def set_deplacement(self, deplacement):
        self.__deplacement = deplacement
    
    def __str__(self):
        return (f"ID: {self.__id}\n"
            f"Role: {self.__role}\n"
            f"Coordonnee x: {self.__co_x}\n"
            f"Coordonnee y: {self.__co_y}\n"
            f"Etat: {self.__etat}\n"
            f"Deplacement: {self.__deplacement}")

