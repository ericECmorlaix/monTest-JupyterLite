# -*- coding: utf-8 -*-
# Un programme pour générer « aléatoirement » le dessin d’une rue de 4 immeubles dans un notebook jupyter.

# Dépendances
from math import pi
from random import randint

# ipycancas de Martin RENOU pour des canvas interractifs dans jupyter
# Depot : https://github.com/martinRenou/ipycanvas
# Documentation : https://ipycanvas.readthedocs.io/en/latest/ 
from ipycanvas import Canvas, hold_canvas 



# Définitions 

# Création d'un canvas nommé rue de 800 pixels de large par 400 pixels de haut
rue = Canvas(width = 800 , height = 400)

def affiche(canvas) :
    '''
    Efface et affiche le canvas dans le notebook
    '''
    canvas.clear()
    display(canvas) 

def trait(x1,y1,x2,y2):
    '''
    dessine un trait entre les 2 points transmis en paramètres
    Paramètres
        x1, y1 : coordonnées du début du trait
        x2, y2 : coordonnées de la fin du trait
    
    '''
    rue.begin_path()
    rue.move_to(x1,y1)
    rue.line_to(x2,y2)
    rue.stroke()

def rectangle(x,y,w,h,c):
    '''
    Dessine un rectangle avec un contour noir et rempli de la couleur passée en paramètre
    Paramètres
        x, y : coordonnées du centre de la base de rectangle
        w : largeur du rectangle
        h : hauteur du rectangle
        c : couleur du remplissage
    '''
    rue.line_width = 1
    rue.fill_style = c
    rue.fill_rect(x-w/2, y-h, w, h)
    rue.stroke_rect(x-w/2, y-h, w, h)

def couleur_aleatoire():
    '''
    Renvoie une couleur HTML valide
    au format 'rgb(rouge, vert, bleu)'
    où rouge, vert et bleu sont des entiers
    compris entre 0 et 255 choisis aléatoirement.
    
    '''
    rouge = randint(0,255)
    vert = randint(0,255)
    bleu = randint(0,255)
    return f'rgb({rouge},{vert},{bleu})'

def sol():
    '''
    Trace une ligne horizontale au niveau du sol de la rue
    d'épaisseur 3 pixels et de longueur 760 pixels
    centrée dans le canvas
            
    '''
    y_sol = rue.height-1 # ordonnée du sol de la rue
    rue.line_width = 3
    trait(20, y_sol , rue.width-40, y_sol)

def portes(x,y):
    '''
    Dessine une porte de 50 pixels en largeur et 70 pixels en hauteur
    La forme du haut de la porte est aléatoirement rectangulaire ou arrondi
    La couleur pleine de remplissage est choisi aléatoirement parmi les couleurs HTML valides
    Paramètres :
        x est l'abcisse du milieu de la base de la porte
        y est l'ordonnée du sol du niveau de la porte        
    '''          
    if randint(1, 2) == 1 :
        rectangle(x, y, 30, 50, couleur_aleatoire())
    else :
        rue.begin_path()
        rue.move_to(x+15, y)
        rue.line_to(x-15, y)
        rue.arc(x, y-35, 15, pi, 2*pi, False)
        rue.close_path()
        rue.fill_style = couleur_aleatoire()
        rue.fill()
        rue.stroke()   

def facade(x, couleur, niveau):
    '''
    Dessine un rectangle de 60 pixels de haut et 140 pixels de large
    Paramètres :
        x : abcisse du centre de la façade
        couleur : couleur de la façade choisie par l'immeuble
        niveau : numéro du niveau (0 pour les rdc, ...)
    '''
    y = rue.height - niveau * 60 # ordonnée de la base de la facade
    rectangle(x, y, 140, 60, couleur)    

def fenetre(x,y):
    '''
    Dessine une fenêtre de taille 30 pixels sur 30 pixels
    avec une vitre de couleur 'Azure' le jour
    et un contour noir. 
    Paramètres :
        x est l'abcisse du milieu de la base de la fenêtre
        y est l'ordonnée du sol du niveau de la fenetre
    '''    
    rectangle(x,y-20,30,30, 'Azure')

def balcon(x,y):
    '''
    Dessine une porte fenêtre de largeur 30 pixels et 50 pixels en hauteur
    avec une vitre de couleur 'Azure' le jour au contour noir,
    devancé d'un balcon constitué de traits noirs d'épaisseur 3 pixels.
    Paramètres :
        x est l'abcisse du milieu de la base de la porte-fenetre
        y est l'ordonnée du sol du niveau de la porte-fenetre
    '''
    # porte-fenetre
    rue.line_width = 1
    rectangle(x,y,30,50,'Azure')
    
    # balcon
    rue.line_width = 3
    rue.line_cap = 'round'
    for i in range(0,9):
        trait(x-20+i*5,y,x-20+i*5,y-25)
    trait(x-20,y,x+20,y)
    trait(x-20,y-25,x+20,y-25)
    rue.line_width = 1

def rdc(x, couleur):
    '''
    Dessine le rdc sur une facade au niveau do sol de la rue
    avec une seule porte et 2 fenêtres placées aléatoirement.
    Paramètres
        x : abscisse du milieu de la base du RDC
        couleur : couleur fixée par l'immeuble        
    '''
    # Dessine la facade
    facade(x, couleur, 0)
    
    # Choix d'une distribution :
    # => réinvestissement du CHIFOUMI, les parcours de str ont été vu mais pas les listes à ce stade ;
    # proposer d'autres solutions de random sur les str en correction et évoquer les listes...
    k = randint(1,3)
    if k == 1 :
        distribution = 'pff'
    elif k == 2 :
        distribution = 'fpf'
    else :
        distribution = 'ffp'

    for i in range(-1,2) :
        if distribution[i] == 'p' :  # dessiner une porte
            portes(x+i*40, rue.height)
        else:  # dessiner une fenetre
            fenetre(x+i*40, rue.height)


def etage(x, couleur, niveau):
    '''
    Dessine sur une facade un étage avec 3 éléments choisis aléatoirement
    parmi une fenêtre ou une porte fenêtre avec balcon.  
    
    Paramètres
        x : abscisse du milieu de la base de l'étage
        couleur : couleur fixée par l'immeuble
        niveau : numéro de l'étage en partant de 0 pour le rdc
    '''
    y = rue.height - niveau * 60 # ordonnée de la base de l'etage
    
    # Murs
    rue.line_width = 1
    facade(x, couleur, niveau)
    # Eléments
    for i in range(-1,2):
        k = randint(0,1)
        if k == 0 : # dessiner une fenetre
            fenetre(x+i*40, y)
        else : # dessiner une porte fenetre avec balcon
            balcon(x+i*40, y)
            rue.line_width = 1   


def toit1(x, niveau):
    '''
    Dessine un triangle plein de couleur noir de 40 pixels de haut
    et avec une base de 160 pixels 
    Paramètres :
        x : abcisse du centre du toit
        niveau : numero du niveau (0 pour les rdc, ...)
    '''
    y = rue.height - niveau * 60 # ordonnée de la base du toit
    rue.begin_path()
    rue.move_to(x-80, y)
    rue.line_to(x+80, y)
    rue.line_to(x, y-40)
    rue.close_path()
    rue.fill_style = 'black'
    rue.fill()    


def toit2(x, niveau):
    '''
    Paramètres :
        x : abcisse du centre du toit
        y_sol : ordonnée du sol du la rue
        niveau : num du niveau (0 pour les rdc, ...)
    '''
    y = rue.height - niveau * 60 # ordonnée de la base du toit
    # trait horizontal
    rue.line_width = 10
    rue.line_cap = 'round'
    trait(x-70, y-5, x+70, y-5)
    rue.line_width = 1


def toits(x, niveau):
    '''
    Dessine aléatoirement un toit plat ou un toit en pointe
    à l'ordonnée du niveau passé en paramètre
    Paramètres
        x : abscisse du centre de l'étage
        y_sol: ordonnée du sol
        niveau : numéro de l'étage en partant de 0 pour le rdc
    '''        
    if randint(1,2) == 1 :
        toit1(x, niveau)
    else:
        toit2(x, niveau)

def immeuble(x):
    '''
    Dessine un immeuble selon les règles urbanistiques imposées
    
    Paramètres
        x : abscisse du milieu de la base de l'immeuble
        
    '''
    # Nombre d'étage (aléatoire)
    nb_etages = randint(0,4)
    #Couleur facade (aléatoire)
    couleur_facade = couleur_aleatoire()
    
    # Dessin du RDC
    rdc(x, couleur_facade)

    # Dessin des étages
    niveau = 1
    while niveau <= nb_etages:
        etage(x, couleur_facade,niveau)
        niveau = niveau + 1

    # Dessin du toit
    toits(x, niveau)

def rue_finale(canvas):
    
    # Affichage de ma rue
    affiche(canvas)
        
    # Dessin des immeubles
    for i in range(4):
        immeuble(120+i*180) 
        
    # Dessin du sol de la rue
    sol()    

# Tests
if __name__ == '__main__':
    with hold_canvas(rue):
        rue_finale(rue)
