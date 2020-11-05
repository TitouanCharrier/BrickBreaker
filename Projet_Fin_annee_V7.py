#!/usr/bin/env python3
#Projet fin d'année ISN
from tkinter import *
from tkinter.font import *
import time
from PIL import Image, ImageTk
import random
from threading import Thread
import math


#résolution automatique
ecr = Tk()
ecr.attributes("-fullscreen", True)
RésX = ecr.winfo_screenwidth()
RésY = ecr.winfo_screenheight()

#Facteur de diminution et vitesse balle
global F
F = RésX/1920
FrameRate = 1/60
global VitesseBalle
VitesseBalle = 150 * FrameRate
VitesseCurseur = 2400 * FrameRate
#Taille Police
TaillePolice = round(30*F)

#Définition du décors :
imageBriqueL3 = Image.open("Data/Rectangle_1.png")
imageBriqueL2 = Image.open("Data/Rectangle_3.png")
imageBriqueL1 = Image.open("Data/Rectangle_2.png")
image = Image.open("Data/Fond_ecran.png")
imageDuCurseur = Image.open("Data/Barre_3.png")
imageDeLaBalle = Image.open("Data/Balle4.png")

#Définition des variables
global Points
Points = 0
global MoveCurseurDroit
MoveCurseurDroit = False
global MoveCurseurGauche
MoveCurseurGauche = False
global x
global y
global lancé 
lancé = False
global Initialisation
Initialisation = False
global précédent
précédent = -1
global ListeBrique
ListeBrique = []
global ScoreNumber
ScoreNumber = 0
global Demarrer
Demarrer = False
global Quitter
Quitter = False
global Recommencer
Recommencer = True
global ListeNon
ListeNon = []
global Vie
Vie = NONE
global OldPos
OldPos = [(RésX // 2)-30*F, 800*F]
global NowPos
NowPos = NONE

#définition des éléments
global ZoneJeu
ZoneJeu = Canvas(ecr, width=RésX, height=RésY, bg="#606060", bd=0, confine=True)
global LabGagne
LabGagne = NONE
global LabGoodbye
LabGoodbye = NONE
global LabPerdu
LabPerdu = NONE
global ScoreVie
ScoreVie = NONE
global ScorePoint
ScorePoint = NONE


#Créer le fond d'écran *3*
image = image.resize((RésX, RésY), Image.ANTIALIAS) 
FondEcrand = ImageTk.PhotoImage(image)
ZoneJeu.create_image(RésX//2,RésY//2,image=FondEcrand)
LabGoodbye = NONE

#définition du curseur *4*
imageDuCurseur = imageDuCurseur.resize((round(200*F), round(25*F)), Image.ANTIALIAS) 
ImgCurseur1 = ImageTk.PhotoImage(imageDuCurseur)
global Curseur
Curseur = ZoneJeu.create_image(RésX//2, 800*F,image=ImgCurseur1)

#définition de la balle *5*
imageDeLaBalle = imageDeLaBalle.resize((round(35*F), round(35*F)), Image.ANTIALIAS) 
ImgBalle = ImageTk.PhotoImage(imageDeLaBalle)
Balle = ZoneJeu.create_image(RésX//2, 775*F,image=ImgBalle)

ZoneJeu.delete

#Fonctions
def FctBoutonQuitter(event):
    global Quitter
    Quitter = True

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

def DetecterCollision(i):
    global x
    global y
    global ZoneJeu
    if ZoneJeu.coords(i)[0]-45*F <= ZoneJeu.coords(Balle)[0] <= ZoneJeu.coords(i)[0]+45*F:
        y = -y 
    elif ZoneJeu.coords(i)[1]-35*F <= ZoneJeu.coords(Balle)[1] <= ZoneJeu.coords(i)[1]+35*F:
        x = -x          
    else:
        x=-x
        y=-y
    
def InteractionBrique(i, NiveauBrique):
    global ScoreNumber
    global précédent
    global ZoneJeu
    if NiveauBrique == 'pyimage5':
        DetecterCollision(i)
        ScoreNumber += 1
        try :  
            ListeBrique.remove(i)
        except :
            pass
        ZoneJeu.delete(i) 

    elif NiveauBrique == 'pyimage4':
        ZoneJeu.itemconfigure(i,image=ListeBriqueImage[1])
        DetecterCollision(i)
        ScoreNumber += 2

    elif NiveauBrique == 'pyimage6':
        ZoneJeu.itemconfigure(i,image=ListeBriqueImage[0])
        DetecterCollision(i)
        ScoreNumber += 3

    précédent = i

def CurseurCollision():
    global Balle
    global Curseur
    global ZoneJeu
    global x
    global y
    #dessus
    if ZoneJeu.coords(Curseur)[0]-100*F <= ZoneJeu.coords(Balle)[0] <= ZoneJeu.coords(Curseur)[0]+100*F:
        print(x,y)
        x = x
        Y = -y
        print((ZoneJeu.coords(Balle)[0]-ZoneJeu.coords(Curseur)[0])//10)
    #cotés
    if ZoneJeu.coords(Curseur)[1]-20*F <= ZoneJeu.coords(Balle)[1] <= ZoneJeu.coords(Curseur)[1]+20*F:
        y = -y
def CasserBlock(detruit):
    global ScoreNumber
    global x
    global y
    ListeNon = [ScoreVie,Curseur,Balle,FondEcrand,ScorePoint,Score]

    if len(detruit) > 2 and detruit[2] not in ListeNon and detruit[2] != ScoreVie:
        i = detruit[2]
        try :
            NiveauBrique = ZoneJeu.itemcget(i,'image')
            if i > 4:
                InteractionBrique(i, NiveauBrique)
        except :
            pass

        ZoneJeu.itemconfigure(Score, text=ScoreNumber)
    for j in detruit:
        if j == 2:
            CurseurCollision()       
        
def MoveCurseur():
    if MoveCurseurDroit == True and ZoneJeu.coords(Curseur)[0]<=RésX-100*F:
        ZoneJeu.move(Curseur,VitesseCurseur*F,0)
    if MoveCurseurGauche == True and ZoneJeu.coords(Curseur)[0]>=100*F:
        ZoneJeu.move(Curseur,-VitesseCurseur*F,0)

def Gagner():
    global Demarrer
    global Points
    global Initialisation
    Demarrer = False
    Initialisation = False
    LabGagne = ZoneJeu.create_text(RésX//2, RésY//2, text="-----Gagné----- ", fill='white', font=Font(size=100))
    ecr.update()
    Points += 1
    time.sleep(1)
    ZoneJeu.delete(LabGagne,ScorePoint,ScoreVie)

def Perdre():
    global Demarrer
    global Initialisation
    global Points
    global ScoreNumber
    LabPerdu = ZoneJeu.create_text(RésX//2, RésY//2, text="-----Perdu----- ", fill='white', font=Font(size=100))
    ZoneJeu.delete(ScoreVie,ScorePoint)
    for i in ListeBrique:
        ZoneJeu.delete(i)
    Initialisation = False
    ecr.update()
    time.sleep(2)
    ZoneJeu.delete(LabPerdu)
    Points -= 1
    ScoreNumber = 0

def ChangerCouleurs():
    global ScoreNumber
    global ZoneJeu
    if 550 >= ScoreNumber == 500 and ZoneJeu.itemcget(Score,'fill') != 'red':
        ZoneJeu.itemconfigure(Score, fill='red')
    elif 350 >= ScoreNumber == 300 and ZoneJeu.itemcget(Score,'fill') != 'orange':
        ZoneJeu.itemconfigure(Score, fill='orange')
    elif 250 >= ScoreNumber == 200 and ZoneJeu.itemcget(Score,'fill') != 'yellow':
        ZoneJeu.itemconfigure(Score, fill='yellow')
    elif 150 >= ScoreNumber >= 100 and ZoneJeu.itemcget(Score,'fill') != 'green':
        ZoneJeu.itemconfigure(Score, fill='green')
    elif ScoreNumber == 0 and ZoneJeu.itemcget(Score,'fill') != 'white':
        ZoneJeu.itemconfigure(Score, fill='white')

def FctDemarrer(event):
    global Demarrer
    Demarrer=True

def CreerBrique():
    global ListeBrique
    for j in range(6):    
        for i in range(15):
            NbrAlea = random.randint(0,2)
            Coucou = ZoneJeu.create_image(300*F+100*F*i,150*F+75*F*j,image=ListeBriqueImage[NbrAlea])
            ListeBrique.append(Coucou)

def DestructionBrique(block):
    global ListeNon
    for i in range(40):
        NbrItem = ZoneJeu.find_all()[len(ZoneJeu.find_all())-1]
        Nbr_a_detruire = random.randint(NbrItem-block,NbrItem)
        if Nbr_a_detruire not in ListeNon:
            ZoneJeu.delete(Nbr_a_detruire)
        block-=1
        ZoneJeu.pack()
        try :
            ListeBrique.remove(Nbr_a_detruire)
        except:
            pass

def IntersectionEcran(ScoreVie):
    global x
    global y
    global Vie
    global ZoneJeu
    global Demarrer

    #intersection en Bas
    if ZoneJeu.coords(Balle)[1] >= 880*F:
        Vie -= 1
        print('true')
        ZoneJeu.itemconfigure(ScoreVie, text="Nombre de vies : {}".format(Vie))
        Demarrer = False

    #intersection en Haut
    if ZoneJeu.coords(Balle)[1] <= 35*F:
        y=-y

    #intersection Côtés
    if ZoneJeu.coords(Balle)[0] >= RésX-35*F or ZoneJeu.coords(Balle)[0] <= 35*F :
        x=-x

def BouclePrincipale():
    global VitesseBalle
    while Initialisation == True and Demarrer == True and Quitter == False:
        ListeNon = [ScoreVie,Curseur,Balle,FondEcrand,ScorePoint,Score]
        ChangerCouleurs()
        time.sleep(FrameRate)
        detruit = ZoneJeu.find_overlapping(ZoneJeu.coords(Balle)[0]-sizeBalle*F,ZoneJeu.coords(Balle)[1]-sizeBalle*F,ZoneJeu.coords(Balle)[0]+sizeBalle*F,ZoneJeu.coords(Balle)[1]+sizeBalle*F)
        MoveCurseur()
        CasserBlock(detruit)
        if len(ListeBrique) == 0:
            Gagner()
        IntersectionEcran(ScoreVie)
        #déplacement balle
        NowPos = ZoneJeu.coords(Balle)
        ZoneJeu.move(Balle,x,y)
        ecr.update()


def AttenteLancement():
    while Initialisation == True and Demarrer == False and Quitter == False:
        if Vie == 0 :
            Perdre()
        time.sleep(FrameRate)
        ZoneJeu.coords(Balle, ZoneJeu.coords(Curseur)[0], ZoneJeu.coords(Curseur)[1]-28*F)
        ecr.update()
        MoveCurseur()
        #Boucle principale du jeu       
        BouclePrincipale()


def Initialiser():
    global Initialisation
    global ScoreVie
    global ScorePointl
    global Vie
    if Initialisation == False:
        Vie = 1
        ScoreVie = ZoneJeu.create_text(200*F, 50*F, text="Nombre de vies : {}".format(Vie), font=Font(size=TaillePolice), fill="white")
        ScorePoint = ZoneJeu.create_text(1650*F,50*F,text="Nombre de Victoires : {}".format(Points), font=Font(size=TaillePolice), fill="white")
        ZoneJeu.itemconfigure(Score, text=ScoreNumber) 
        block = 90
        CreerBrique()
        DestructionBrique(block)
        Initialisation = True
        ZoneJeu.pack()
    
def EffacerTout():
    for i in ListeBrique:
        ZoneJeu.delete(i)
    ZoneJeu.delete(LabPerdu,LabGagne)
    LabGoodbye = ZoneJeu.create_text(RésX//2, RésY//2, text="-----Au-revoir----- ", fill='white', font=Font(size=100))
    ZoneJeu.delete(ScoreVie)
    ecr.update()
    time.sleep(0.5)

#lier les touches
ecr.bind("<KeyPress-Left>",FctCurseurPressG)
ecr.bind("<KeyPress-Right>",FctCurseurPressD)
ecr.bind("<KeyRelease-Left>",FctCurseurRelG)
ecr.bind("<KeyRelease-Right>",FctCurseurRelD)
ecr.bind("<space>",FctDemarrer)
ecr.bind("<Escape>",FctBoutonQuitter)

#Vitesse de la balle
global x
global y
x=VitesseBalle
y=VitesseBalle

#Taille de la brique
Facube = (1.5)*F

#définition des briques * de 5 à (ixj)+4 * 
imageBriqueL1 = imageBriqueL1.resize((round(53*Facube), round(38*Facube)), Image.ANTIALIAS) 
BriqueLevel1 = ImageTk.PhotoImage(imageBriqueL1)

imageBriqueL2 = imageBriqueL2.resize((round(53*Facube), round(38*Facube)), Image.ANTIALIAS) 
BriqueLevel2 = ImageTk.PhotoImage(imageBriqueL2)

imageBriqueL3 = imageBriqueL3.resize((round(53*Facube), round(38*Facube)), Image.ANTIALIAS) 
BriqueLevel3 = ImageTk.PhotoImage(imageBriqueL3)
    
ListeBriqueImage = [BriqueLevel1,BriqueLevel2
,BriqueLevel3]

#Taille de la balle
sizeBalle = 17.5*F

Score = ZoneJeu.create_text(RésX//2,50*F, text=ScoreNumber, font=Font(size=30), fill="white") 
LabHello = ZoneJeu.create_text(RésX//2, RésY//2, text="-----Bonjour----- ", fill='white', font=Font(size=100)) 
ZoneJeu.pack()
ecr.update()
time.sleep(1)
ZoneJeu.delete(LabHello)

#Algorithme
while Quitter == False:
    Initialiser()
    AttenteLancement()

EffacerTout()
ecr.quit()
