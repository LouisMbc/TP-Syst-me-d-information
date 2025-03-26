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
    
    def info_joueur(self):
        print("ID: ", self.__id)
        print("Role: ", self.__role)
        print("Coordonnee x: ", self.__co_x)
        print("Coordonnee y: ", self.__co_y)
        print("Etat: ", self.__etat)
        print("Deplacement: ", self.__deplacement)


