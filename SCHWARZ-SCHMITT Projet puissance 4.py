# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 12:27:21 2022

@author: Gauthier et Matteo
"""

from tkinter import *
from tkinter.messagebox import *
from random import *
from time import time


fenetre = Tk()
fenetre.title("Puissance 4")
fenetre.geometry("900x900")

#fenetre.iconbitmap(r'puissance.ico')

#############################################
########## Création de la grille ############
#############################################


class Puissance_4:

    def __init__(self,a):
        """
        Constructeur qui permet :
        
        self.Zone_dessin = Permet de creer la zone de dessin / Canvas
        self.Zone_dessin= Placer le Canvas
        
        self.jeton = Permet de compter le nombre de jetons en cas d'égalité
        self.tour_joueur : savoir qui joue pour choisir la couleur des jetons
        """
        self.Zone_dessin = Canvas(fenetre,width=900,height=800,bg="white")
        self.Zone_dessin.pack()
        self.jeton=0
        self.tour_joueur = 1
        self.plateau=[["_","_","_","_","_","_","_",],
                  ["_","_","_","_","_","_","_",],
                  ["_","_","_","_","_","_","_",],
                  ["_","_","_","_","_","_","_",],
                  ["_","_","_","_","_","_","_",],
                  ["_","_","_","_","_","_","_",]]
        self.type_jeu = a

###########################################################################################
    # Fonctions permettant de créer le plateau du jeu



    def traçage(self):
        """
        Fonction qui permet de tracer la grille à l'aide de boucles while
        """
        x=0
        while x!=900:
            self.x1, self.y1 = x, 700
            self.x2, self.y2 = x, 100
            self.Zone_dessin.create_line(self.x1,self.y1,self.x2,self.y2,width=1,fill="black")
            x=x+100
            
        y=0
        while y!=800:
            self.x1, self.y1 = 100, y
            self.x2, self.y2 = 800, y
            self.Zone_dessin.create_line(self.x1,self.y1,self.x2,self.y2,width=1,fill="black")
            y=y+100

    def clic_detect(self,event):
        """
        Cette fonction permet de récupérer les coordonnées des clics puis si le clic est dans la grille de jeu alors on appele différentes fonctions:
            tout d'abord avant appeler les fonctions on détermine le numero de la colonne -1 ( voir le commentaire ligne 78 pour la raison du -1
            puis on appelle la fonction reconnaissance ligne pour connaitre le numéro de sa ligne
            ensuite on appelle la fonction placement_jeton qui permet de placer le jeton dans la grille et ensuite on rajoute 1 au nombre de jeton dans la grile
            afin de traiter le cas d'égalité
            Par la suite on appelera les différentes fonctions reconnaissance de vainqueur
            
        """

        # Récupère coordonées clic
        
        self.Clic_x,self.Clic_y = event.x,event.y
        if 100<self.Clic_x<800:
            if 100<self.Clic_y<700:
                #Appel des fonctions permettant l'apparition des jetons dans la grille
                self.numero_colonne = self.Clic_x//100-1 # Le - 1 est nécessaire car sinon j'ai un problème pour remplir la matrice
                self.reconaissance_ligne()
                self.placement_jeton()

                self.jeton+=1
                self.reconnaissance_vainqueur_horiz()
                self.reconnaissance_vainqueur_verti_diago()
            
        if self.type_jeu == '1':
            self.numero_colonne = randint(0, 6)
            self.reconaissance_ligne()
            self.placement_jeton()
            self.jeton += 1
            self.reconnaissance_vainqueur_horiz()
            self.reconnaissance_vainqueur_verti_diago()

        if self.type_jeu == '2':
            t=True
            for i in self.plateau:
                for j in range (0,len(i)-1):
                    if (i[j]=="j" and i[j+1]=="j" and i[j+2]=="j" and j<=4) or (i[j]=="r" and i[j+1]=="r" and i[j+2]=="r" and j<=4):
                        self.numero_colonne=j+3
                        t=False
            for i in range(0,7):
                for j in range (0,4):
                    if self.plateau[j][i]=="r" and self.plateau[j+1][i]=="r":
                        self.numer_colonne=i
                        t=False
            if t==True:
                if self.numero_colonne == 6:
                    self.numero_colonne -= 1
                else:
                    self.numero_colonne += 1

            self.reconaissance_ligne()
            self.placement_jeton()
            self.jeton += 1
            self.reconnaissance_vainqueur_horiz()
            self.reconnaissance_vainqueur_verti_diago()

        if self.jeton==42:
            showinfo(title='Gagne',message='Egalité !')




    def reconaissance_ligne(self):

        """
        Permet de connaitre dans quelle ligne on est:
        Grace à une recherche dans la matrice si la case est vide on stock le
        numero de la ligne sinon on remonte de 1 ligne
        
        A Noter que le numéro des lignes vont de 5 à 0

        """
        self.ligne_n_1=5
        for k in range (6):
            if self.plateau[self.ligne_n_1][self.numero_colonne]=="_":
                self.ligne=self.ligne_n_1
                return self.ligne
            else:
                self.ligne_n_1-=1
        return self.ligne
    
    def placement_jeton(self):
        """
        Fonction qui permet de placer un jeton dans la grille de différente couleur suivant le joueur 
        
        """
        if self.tour_joueur%2==0:
            
            if self.plateau[self.ligne][self.numero_colonne]=="_":
                self.Zone_dessin.create_oval(self.numero_colonne*100+120,self.ligne*100+180,self.numero_colonne*100+180,self.ligne*100+120, fill = "red")
                print("C'est au tour des jetons jaunes")
                self.plateau[self.ligne][self.numero_colonne]="r"
                self.tour_joueur+=1
                
        
        if self.tour_joueur%2!=0:
           
            
            if self.plateau[self.ligne][self.numero_colonne]=="_":
                self.Zone_dessin.create_oval(self.numero_colonne*100+120,self.ligne*100+180,self.numero_colonne*100+180,self.ligne*100+120, fill = "yellow")
                print("C'est au tour des jetons rouges")
                self.plateau[self.ligne][self.numero_colonne]="j"
                self.tour_joueur+=1

#######################################################################

    
    def reconnaissance_vainqueur_horiz(self):
        for k in self.plateau:
            for j in range(4):
                if k[j]=='j' and k[j+1]=='j' and k[j+2]== 'j' and k[j+3]=='j':
                    showinfo(title='Gagne',message='Les jaunes ont gagné !')
                    
                
                if k[j]=='r' and k[j+1]=='r' and k[j+2]== 'r' and k[j+3]=='r':
                    showinfo(title='Gagne',message='Les rouges ont gagné !')

    def reconnaissance_vainqueur_verti_diago(self):
        a=5
        for z in range(3):
                for i in range(7):


                    if self.plateau[a][i]=='j' and self.plateau[a-1][i]=="j" and self.plateau[a-2][i]== "j" and self.plateau[a-3][i]=='j':
                        showinfo(title='Gagne',message='Les jaunes ont gagné !')
                        
                    if self.plateau[a][i]=='r' and self.plateau[a-1][i]=="r" and self.plateau[a-2][i]== "r" and self.plateau[a-3][i]=='r':
                        showinfo(title='Gagne',message='Les rouges ont gagné !')
                a-=1
    
    

        a= 5
        
        for i in range (3): # hauteur
            for j in range(4):
                if self.plateau[a][j]=='j' and self.plateau[a-1][j+1]=='j' and self.plateau[a-2][j+2]=='j' and self.plateau[a-3][j+3]=='j' :
                    showinfo(title='Gagne',message='Les jaunes ont gagné !')
                if self.plateau[a][j]=='r' and self.plateau[a-1][j+1]=='r' and self.plateau[a-2][j+2]=='r' and self.plateau[a-3][j+3]=='r' :
                    showinfo(title='Gagne',message='Les rouges ont gagné !')
        
        for i in range(3):
            b= 6
            for i in range(4):
                if self.plateau[a][b]=='j' and self.plateau[a-1][b-1]=='j' and self.plateau[a-2][b-2]=='j' and self.plateau[a-3][b-3]=='j' :
                    showinfo(title='Gagne',message='Les jaunes ont gagné !')
                if self.plateau[a][b]=='r' and self.plateau[a-1][b-1]=='r' and self.plateau[a-2][b-2]=='r' and self.plateau[a-3][b-3]=='r' :
                    showinfo(title='Gagne',message='Les rouges ont gagné !')
                b-=1
                    
                    
        
            a-=1

        
        
                
                      
jeu=Puissance_4(input("Veuillez renseigner votre difficulté (0=> pas d'IA;1=> IA basique;2=>IA moyenne:"))
jeu.traçage()
jeu.Zone_dessin.bind("<Button-1>",jeu.clic_detect)






fenetre.mainloop()