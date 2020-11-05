
#Projet fin d'année ISN
from tkinter import *
from tkinter.font import *
import time
from PIL import Image, ImageTk
import random

#résolution automatique
ecr = Tk()
ecr.attributes("-fullscreen", True)
RésX = ecr.winfo_screenwidth()
RésY = ecr.winfo_screenheight()

#Facteur de diminution et vitesse balle
F = RésX/1920
Vitesse = 3

#Taille Police
TaillePolice = round(30*F)

#Définition de la fenetre
ecr.geometry("{}x{}".format(RésX, RésY))
ecr.resizable(False, False)

#zone de jeu
ZoneJeu = Canvas(ecr, width=RésX, height=RésY, bg="#606060", bd=0, confine=True)

#Créer le fond d'écran *1*
image = Image.open("Data/Fond_ecran.png")
image = image.resize((RésX, RésY), Image.ANTIALIAS) 
FondEcrand = ImageTk.PhotoImage(image)
ZoneJeu.create_image(RésX//2,RésY//2,image=FondEcrand)

#fonctions boutons
global Quitter
Quitter = False
def FctBoutonQuitter(event):
    global Quitter
    Quitter = True

#définition du curseur *2*
image3 = Image.open("Data/Barre_1.png")
image3 = image3.resize((round(200*F), round(25*F)), Image.ANTIALIAS) 
ImgCurseur = ImageTk.PhotoImage(image3)
Curseur = ZoneJeu.create_image(RésX//2,212*F,image=ImgCurseur)

#Définition des variables
global MoveCurseurDroit
MoveCurseurDroit = False
global MoveCurseurGauche
MoveCurseurGauche = False

#Fonction déplacement curseur
def FctCurseurPressD(event):
    global MoveCurseurDroit
    MoveCurseurGauche = False
    MoveCurseurDroit = True

def FctCurseurPressG(event):
    global MoveCurseurGauche
    MoveCurseurDroit = False
    MoveCurseurGauche = True

def FctCurseurRelD(event):
    global MoveCurseurDroit
    MoveCurseurDroit = False

def FctCurseurRelG(event):
    global MoveCurseurGauche
    MoveCurseurGauche = False

def MoveCurseur():
    if MoveCurseurDroit == True:
        ZoneJeu.move(Curseur,8*F,0)
    if MoveCurseurGauche == True:
        ZoneJeu.move(Curseur,-8*F,0)

#Démarrer
global Demarrer
Demarrer = False
def FctDemarrer2(event):
    global Demarrer
    Demarrer=True

#définition de la balle *3*
image2 = Image.open("Data/Balle5.png")
image2 = image2.resize((round(35*F), round(35*F)), Image.ANTIALIAS) 
ImgBalle = ImageTk.PhotoImage(image2)
Balle = ZoneJeu.create_image(RésX//2,212*F,image=ImgBalle)

#lier les touches
ecr.bind("<KeyPress-Left>",FctCurseurPressG)
ecr.bind("<KeyPress-Right>",FctCurseurPressD)
ecr.bind("<KeyRelease-Left>",FctCurseurRelG)
ecr.bind("<KeyRelease-Right>",FctCurseurRelD)
ecr.bind("<space>",FctDemarrer2)
ecr.bind("<Escape>",FctBoutonQuitter)

#Vitesse de la balle
x=Vitesse
y=Vitesse

#Texte de score *4*
Vie = 15
ScoreVie = ZoneJeu.create_text(200*F, 50*F, text="Nombre de vies : {}".format(Vie), font=Font(size=TaillePolice), fill="white")

#Taille de la brique
Facube = (1.5)*F

#définition des briques * de 5 à (ixj)+4 * 
imageBrique1 = Image.open("Data/Carré1.png")
imageBrique1 = imageBrique1.resize((round(53*Facube), round(38*Facube)), Image.ANTIALIAS) 
BriqueLevel1 = ImageTk.PhotoImage(imageBrique1)

imageBrique2 = Image.open("Data/Carré2.png")
imageBrique2 = imageBrique2.resize((round(53*Facube), round(38*Facube)), Image.ANTIALIAS) 
BriqueLevel2 = ImageTk.PhotoImage(imageBrique2)

imageBrique3 = Image.open("Data/Carré3.png")
imageBrique3 = imageBrique3.resize((round(53*Facube), round(38*Facube)), Image.ANTIALIAS) 
BriqueLevel3 = ImageTk.PhotoImage(imageBrique3)

ListeBriqueImage = [BriqueLevel1,BriqueLevel2,BriqueLevel3]

#Affichage des briques
for j in range(6):    
    for i in range(15):
        globals()['BriqueLevel1'+str(i+1)]= ZoneJeu.create_image(300+100*i,150+75*j,image=ListeBriqueImage[random.randint(0,2)])
for i in range(30):
    ZoneJeu.delete(random.randint(5,120))
ZoneJeu.pack()

#placement curseur initial
ZoneJeu.coords(Curseur, RésX//2, 800*F)

#Taille de la balle
sizeBalle = 15*F
time.sleep(1)
#boucle non-lancé 
while Demarrer == False and Quitter == False:
    time.sleep(0.005)
    ZoneJeu.coords(Balle, ZoneJeu.coords(Curseur)[0], ZoneJeu.coords(Curseur)[1]-28*F)
    ecr.update()
    MoveCurseur()
    if Vie == 0 :
            break
    #Boucle lancé        
    while Demarrer == True and Quitter == False:
        time.sleep(0.005)
        detruit = ZoneJeu.find_overlapping(ZoneJeu.coords(Balle)[0]-sizeBalle*F,ZoneJeu.coords(Balle)[1]-sizeBalle*F,ZoneJeu.coords(Balle)[0]+sizeBalle*F,ZoneJeu.coords(Balle)[1]+sizeBalle*F)
        MoveCurseur()
        if len(detruit) != 0:
            for i in detruit:
                if i > 4:
                    y=-y
                    
                    ZoneJeu.delete(i)
                    pass
                elif i == 2:
                    y=-y
                
        #intersection en Bas
        if ZoneJeu.coords(Balle)[1] >= 880*F:
            Vie -= 1
            ZoneJeu.delete(ecr,ScoreVie)
            ScoreVie = ZoneJeu.create_text(200*F, 50*F, text="Nombre de vies : {}".format(Vie), font=Font(size=TaillePolice), fill="white")
            Demarrer = False

        #intersection en Haut
        elif ZoneJeu.coords(Balle)[1] <= 35*F:
            y=-y

        #intersection Côtés
        elif ZoneJeu.coords(Balle)[0] >= RésX-35*F or ZoneJeu.coords(Balle)[0] <= 35*F :
            x=-x
        
        #déplacement balle
        ZoneJeu.move(Balle,x,y)

        ecr.update()
ecr.quit()