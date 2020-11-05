#!/usr/bin/python3
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
VitesseBalle = 5
VitesseCurseur = 15
#Taille Police
TaillePolice = round(30*F)

#zone de jeu
global ZoneJeu
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
image3 = Image.open("Data/Barre_3.png")
image3 = image3.resize((round(200*F), round(25*F)), Image.ANTIALIAS) 
ImgCurseur1 = ImageTk.PhotoImage(image3)
global Curseur
Curseur = ZoneJeu.create_image(RésX//2, 800*F,image=ImgCurseur1)

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
global LabGagne
LabGagne = NONE
global LabPerdu
LabPerdu = NONE
global Initialisation
Initialisation = False
global précédent
précédent = -1
global ListeBrique
ListeBrique = []
global ScoreNumber
ScoreNumber = 0
global Score
Score = ZoneJeu.create_text(RésX//2,50*F, text=ScoreNumber, font=Font(size=30), fill="white")

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

#Autres fonctions 
def DetecterCollision(i):
    global x
    global y
    if ZoneJeu.coords(i)[0]-45*F <= ZoneJeu.coords(Balle)[0] <= ZoneJeu.coords(i)[0]+45*F:
        y = -y 
    elif ZoneJeu.coords(i)[1]-35*F <= ZoneJeu.coords(Balle)[1] <= ZoneJeu.coords(i)[1]+35*F:
        x = -x          
    else:
        x=-x
        y=-y
    ZoneJeu.delete(i)

def CasserBlock(detruit):
    global x
    global y
    global précédent
    global ScoreNumber
    global Score
    
    if len(detruit) > 2 and detruit[2] not in ListeNon:
        i = detruit[2]
        try :
            NiveauBrique = ZoneJeu.itemcget(i,'image')
        except :
            pass
        if NiveauBrique == 'pyimage5':
            if i > 4:
                DetecterCollision(i)
                ScoreNumber += 1
                try :  
                    ListeBrique.remove(i)
                except :
                    pass
        elif NiveauBrique == 'pyimage4':
            ZoneJeu.itemconfigure(i,image=ListeBriqueImage[1])
            if i > 4:
                if ZoneJeu.coords(i)[0]-45*F <= ZoneJeu.coords(Balle)[0] <= ZoneJeu.coords(i)[0]+45*F:
                    y = -y 
                elif ZoneJeu.coords(i)[1]-35*F <= ZoneJeu.coords(Balle)[1] <= ZoneJeu.coords(i)[1]+35*F:
                    x = -x          
                else:
                    x=-x
                    y=-y
            ScoreNumber += 2
        elif NiveauBrique == 'pyimage6':
            ZoneJeu.itemconfigure(i,image=ListeBriqueImage[0])
            if i > 4:
                if ZoneJeu.coords(i)[0]-45*F <= ZoneJeu.coords(Balle)[0] <= ZoneJeu.coords(i)[0]+45*F:
                    y = -y 
                elif ZoneJeu.coords(i)[1]-35*F <= ZoneJeu.coords(Balle)[1] <= ZoneJeu.coords(i)[1]+35*F:
                    x = -x          
                else:
                    x=-x
                    y=-y
            ScoreNumber += 3
        précédent = detruit[2]
        ZoneJeu.itemconfigure(Score, text=ScoreNumber)
    for j in detruit:
        if j == 2:
            if ZoneJeu.coords(Curseur)[0]-100*F <= ZoneJeu.coords(Balle)[0] <= ZoneJeu.coords(Curseur)[0]+100*F:
                y = -y
                if (ZoneJeu.coords(Curseur)[0]-100*F) <= ZoneJeu.coords(Balle)[0] <= (ZoneJeu.coords(Curseur)[0]-50*F):
                    x = -abs(x) 
                
                elif (ZoneJeu.coords(Curseur)[0]+100*F) >= ZoneJeu.coords(Balle)[0] >= (ZoneJeu.coords(Curseur)[0]+50*F):
                    x= abs(x)
                
                else :
                    x = x
                    
            if ZoneJeu.coords(Curseur)[1]-20*F <= ZoneJeu.coords(Balle)[1] <= ZoneJeu.coords(Curseur)[1]+20*F:
                x = -x  
                
        
def MoveCurseur():
    if MoveCurseurDroit == True and ZoneJeu.coords(Curseur)[0]<=RésX-100*F:
        ZoneJeu.move(Curseur,VitesseCurseur*F,0)
    if MoveCurseurGauche == True and ZoneJeu.coords(Curseur)[0]>=100*F:
        ZoneJeu.move(Curseur,-VitesseCurseur*F,0)

def Gagner():
    global Demarrer
    global Points
    global LabGagne
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
    global LabPerdu
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
    global Score
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
    

#Démarrer
global Demarrer
Demarrer = False
def FctDemarrer2(event):
    global Demarrer
    Demarrer=True

#définition de la balle *3*
image2 = Image.open("Data/Balle4.png")
image2 = image2.resize((round(35*F), round(35*F)), Image.ANTIALIAS) 
ImgBalle = ImageTk.PhotoImage(image2)
Balle = ZoneJeu.create_image(RésX//2, 775*F,image=ImgBalle)

#lier les touches
ecr.bind("<KeyPress-Left>",FctCurseurPressG)
ecr.bind("<KeyPress-Right>",FctCurseurPressD)
ecr.bind("<KeyRelease-Left>",FctCurseurRelG)
ecr.bind("<KeyRelease-Right>",FctCurseurRelD)
ecr.bind("<space>",FctDemarrer2)
ecr.bind("<Escape>",FctBoutonQuitter)

#Vitesse de la balle
x=VitesseBalle
y=VitesseBalle

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


#placement curseur initial
ZoneJeu.coords(Curseur, RésX//2, 800*F)

#Taille de la balle
sizeBalle = 17.5*F
global Recommencer
Recommencer = True
LabHello = ZoneJeu.create_text(RésX//2, RésY//2, text="-----Bonjour----- ", fill='white', font=Font(size=100))
ZoneJeu.pack()
ecr.update()
time.sleep(1)
ZoneJeu.delete(LabHello)

#initialisation
while Quitter == False:
    if Initialisation == False:

        Vie = 10
        ScorePoint = ZoneJeu.create_text(1650*F,50*F,text="Nombre de Victoires : {}".format(Points), font=Font(size=TaillePolice), fill="white")
        ScoreVie = ZoneJeu.create_text(200*F, 50*F, text="Nombre de vies : {}".format(Vie), font=Font(size=TaillePolice), fill="white")
        ZoneJeu.itemconfigure(Score, text=ScoreNumber) 
        block = 90
        #Affichage des briques
        for j in range(6):    
            for i in range(15):
                NbrAlea = random.randint(0,2)
                Coucou = ZoneJeu.create_image(300*F+100*F*i,150*F+75*F*j,image=ListeBriqueImage[NbrAlea])
                ListeBrique.append(Coucou)

        #Destruction de certaines briques
        for i in range(40):
            NbrItem = ZoneJeu.find_all()[len(ZoneJeu.find_all())-1]
            Nbr_a_detruire = random.randint(NbrItem-block,NbrItem)
            ListeNon = [ScoreVie,Curseur,Balle,FondEcrand,ScorePoint,Score]
            if Nbr_a_detruire not in ListeNon:
                ZoneJeu.delete(Nbr_a_detruire)
            block-=1
            ZoneJeu.pack()
            try :
                ListeBrique.remove(Nbr_a_detruire)
            except:
                pass
        Initialisation = True
        

    #boucle en attente
    while Initialisation == True and Demarrer == False and Quitter == False:
        if Vie == 0 :
                Perdre()
        time.sleep(0.017)
        ZoneJeu.coords(Balle, ZoneJeu.coords(Curseur)[0], ZoneJeu.coords(Curseur)[1]-28*F)
        ecr.update()
        MoveCurseur()
        #Boucle lancé        
        while Initialisation == True and Demarrer == True and Quitter == False:
            ListeNon = [ScoreVie,Curseur,Balle,FondEcrand,ScorePoint,Score]
            ChangerCouleurs()
            time.sleep(0.017)
            detruit = ZoneJeu.find_overlapping(ZoneJeu.coords(Balle)[0]-sizeBalle*F,ZoneJeu.coords(Balle)[1]-sizeBalle*F,ZoneJeu.coords(Balle)[0]+sizeBalle*F,ZoneJeu.coords(Balle)[1]+sizeBalle*F)
            MoveCurseur()
            CasserBlock(detruit)
            if len(ListeBrique) == 0:
                Gagner()
            #intersection en Bas
            if ZoneJeu.coords(Balle)[1] >= 880*F:
                Vie -= 1
                ZoneJeu.delete(ecr,ScoreVie)
                ScoreVie = ZoneJeu.create_text(200*F, 50*F, text="Nombre de vies : {}".format(Vie), font=Font(size=TaillePolice), fill="white")
                Demarrer = False

            #intersection en Haut
            if ZoneJeu.coords(Balle)[1] <= 35*F:
                y=-y

            #intersection Côtés
            if ZoneJeu.coords(Balle)[0] >= RésX-35*F or ZoneJeu.coords(Balle)[0] <= 35*F :
                x=-x

            #déplacement balle
            ZoneJeu.move(Balle,x,y)

            ecr.update()
    #effacer tout
for i in ListeBrique:
    ZoneJeu.delete(i)
ZoneJeu.delete(LabPerdu,LabGagne)
LabGoodbye = ZoneJeu.create_text(RésX//2, RésY//2, text="-----Aurevoir----- ", fill='white', font=Font(size=100))
ZoneJeu.delete(ScoreVie)
ecr.update()
time.sleep(0.5)

ecr.quit()