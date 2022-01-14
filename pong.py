import random # Pour les tirages aleatoires
import sys # Pour quitter proprement
import pygame # Le module Pygame
import pygame.freetype # Pour afficher du texte
import math

pygame.init() # initialisation de Pygame

    # Pour le texte.
pygame.freetype.init()
taille_texte = 50
myfont=pygame.freetype.SysFont(None, taille_texte)

    # Taille de la fenetre
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Proto-pong")


    #couleur cubes

BLANC = (255,255,255)
ROUGE = (200,20,20)
ORANGE = (255,97,3)
JAUNE = (255,255,0)
VERT = (118,238,0)
BLEU = (0,0,238)
VIOLET = (153,50,204)
ROSE = (238,18,137)
NOIR = (0, 0, 0)
COULEURS = [BLANC,ROSE,VIOLET,BLEU,VERT,JAUNE,ORANGE,ROUGE]

DEPART = (400, 400)
RAYON_BALLE = 10

XMIN = 100
XMAX = width - 100
YMIN = 30
YMAX = height + 2*RAYON_BALLE

clock=pygame.time.Clock()

GameContinue = True

def demarrer():
    class Raquette:
        def __init__(self):
            self.x = DEPART[0]
            self.y = YMAX - 3*RAYON_BALLE
            self.longueur = 10*RAYON_BALLE

        def afficher(self):
            pygame.draw.rect(screen, BLANC, (int(self.x-self.longueur/2), int(self.y-RAYON_BALLE), self.longueur, 2*RAYON_BALLE), 0)

        def deplacer(self, x):
            if x - self.longueur/2 < XMIN:
                self.x = XMIN + self.longueur/2
            elif x + self.longueur/2 > XMAX:
                self.x = XMAX - self.longueur/2
            else:
                self.x = x

        def collision_balle(self, balle):
            vertical = abs(self.y - balle.y) < 2*RAYON_BALLE
            horizontal = abs(self.x - balle.x) < self.longueur/2 + RAYON_BALLE
            return vertical and horizontal


    class Balle:

        def __init__(self):
            self.x, self.y = DEPART
            self.vitesse = 14
            self.vitesse_par_angle(60)
            self.stop = True
            self.sur_raquette = True
            self.rebondx = False
            self.rebondy = False

        def vitesse_par_angle(self, angle):
            self.vx = self.vitesse * math.cos(math.radians(angle))
            self.vy = -self.vitesse * math.sin(math.radians(angle))

        def rebond_raquette(self, raquette):
            diff = raquette.x - self.x
            longueur_totale = raquette.longueur/2 + RAYON_BALLE
            angle = 90 + 80 * diff/longueur_totale
            self.vitesse_par_angle(angle)

        def afficher(self):
            pygame.draw.circle (screen, BLANC, (int(self.x),int(self.y)), RAYON_BALLE)

        def deplacer(self,raquette):
            self.rebondx = False
            self.rebondy = False
            perdu = False
            if not self.stop:
                self.x += self.vx
                self.y += self.vy
                if raquette.collision_balle(self):
                    self.rebond_raquette(raquette)
                if self.x + RAYON_BALLE > XMAX and self.vx > 0:
                    self.vx = -self.vx
                if self.x - RAYON_BALLE < XMIN and self.vx < 0:
                    self.vx = -self.vx
                if self.y + RAYON_BALLE > YMAX:
                    self.vy = -self.vy
                    self.stop = True
                    perdu = True
                if self.y - RAYON_BALLE < YMIN:
                    self.vy = -self.vy
            elif self.sur_raquette:
                self.y = raquette.y - 2*RAYON_BALLE
                self.x = raquette.x
                #self.x, self.y = pygame.mouse.get_pos()
            return perdu

    class Brique:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.vie = 1
            self.longueur = 5 * RAYON_BALLE
            self.largeur = 3 * RAYON_BALLE
            self.COULEURS = random.choice(COULEURS)

        def en_vie(self):
            return self.vie > 0

        def afficher(self):
            pygame.draw.rect(screen, self.COULEURS, (int(self.x-self.longueur/2),
                                             int(self.y-self.largeur/2),
                                             self.longueur, self.largeur), 0)

        def collision_balle(self, balle):
            # on suppose que largeur<longueur
            marge = self.largeur/2 + RAYON_BALLE
            dy = balle.y - self.y
            touche = False
            if balle.x >= self.x: # on regarde a droite
                dx = balle.x - (self.x + self.longueur/2 - self.largeur/2)
                if abs(dy) <= marge and dx <= marge: # on touche
                    touche = True
                    if dx <= abs(dy):
                        if not balle.rebondy: # haut ou bas:
                            balle.vy = -balle.vy
                            balle.rebondy = True
                        #print("vertical")
                    elif not balle.rebondx: # a droite
                        balle.vx = -balle.vx
                        balle.rebondx = True
                        #print("horizontal")
            else:
                dx = balle.x - (self.x - self.longueur/2 + self.largeur/2)
                if abs(dy) <= marge and -dx <= marge: # on touche
                    touche = True
                    if -dx <= abs(dy):
                        if not balle.rebondy: # haut ou bas:
                            balle.vy = -balle.vy
                            balle.rebondy = True
                        #print("vertical")
                    elif not balle.rebondx: # a gauche
                        balle.vx = -balle.vx
                        balle.rebondx = True
                        #print("horizontal")
            if touche:
                self.vie -= 1
            return touche

    def niveau1():
        liste_briques = []
        for i in range(17):
            for j in range(8):
                liste_briques.append(Brique(XMIN+50+i*60,YMIN + 50+j*50))
        return liste_briques

    def niveau2():
        liste_briques = []
        for i in range(9):
            for j in range(12):
                liste_briques.append(Brique(XMIN+50+i*60,YMIN + 50+j*50))
        return liste_briques

    def niveau3():
        liste_briques = []
        for i in range(9):
            for j in range(20):
                liste_briques.append(Brique(XMIN+50+i*60,YMIN + 50+j*50))
        return liste_briques

    def niveau_ULTIME():
        liste_briques = []
        for i in range(9):
            for j in range(25):
                liste_briques.append(Brique(XMIN+50+i*60,YMIN + 50+j*50))
        return liste_briques

    class Jeu:
        def initialiser(self):
            self.balle = Balle()
            self.raquette = Raquette()
            self.liste_briques = niveau1()
            self.score = 0
            self.vies = 10

        def __init__(self,level):
            self.initialiser()

            if level == 0:
                liste_briques = []
                for i in range(9):
                    for j in range(5):
                        liste_briques.append(Brique(XMIN+50+i*60,YMIN + 50+j*50))
            elif level== 1:
                liste_briques = []
                for i in range(9):
                    for j in range(7):
                        liste_briques.append(Brique(XMIN+50+i*60,YMIN + 50+j*50))

        def gestion_evenements(self):
            # Gestion des evenements
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit() # Pour quitter
                elif event.type == pygame.MOUSEBUTTONDOWN: # On vient de cliquer
                    if event.button == 1: # Bouton gauche
                        if self.balle.stop:
                            if self.vies <= 0:
                                self.initialiser()
                            elif self.balle.sur_raquette:
                                self.balle.stop = False
                                self.balle.sur_raquette = False
                                self.balle.vitesse_par_angle(60)
                            else:
                                self.balle.sur_raquette = True


        def mise_a_jour(self):
            if self.vies > 0:
                x, _ = pygame.mouse.get_pos()
                perdu = self.balle.deplacer(self.raquette)
                if perdu:
                    self.vies -= 1
                self.raquette.deplacer(x)
                #if self.raquette.collision_balle(self.balle) and self.balle.vy > 0:
                #    self.balle.rebond_raquette(self.raquette)
                    #balle.vy = -balle.vy
                for brique in self.liste_briques:
                    if brique.en_vie():
                        touche = brique.collision_balle(self.balle)
                        if touche :
                            self.score += 10


        def affichage(self):
            screen.fill(NOIR)
            pygame.draw.rect(screen, BLANC, (XMIN-RAYON_BALLE, YMIN, RAYON_BALLE, height), 0)
            pygame.draw.rect(screen, BLANC, (XMAX, YMIN, RAYON_BALLE, height), 0)
            pygame.draw.rect(screen, BLANC, (XMIN-RAYON_BALLE, YMIN-RAYON_BALLE, XMAX-XMIN+2*RAYON_BALLE, RAYON_BALLE), 0)


            for brique in self.liste_briques:
                if brique.en_vie():
                    brique.afficher()
            self.balle.afficher()
            self.raquette.afficher()

            texte, rect = myfont.render("score:", BLANC, size = 20)
            rect.midleft = (10, 30)
            screen.blit(texte, rect)

            texte, rect = myfont.render(str(self.score), BLANC, size = 20)
            rect.midright = (70, 50)
            screen.blit(texte, rect)

            texte, rect = myfont.render("vies: "+str(self.vies), BLANC, size = 20)
            rect.midleft = (XMAX+RAYON_BALLE+10, 30)
            screen.blit(texte, rect)

            if self.vies <= 0:
                texte, rect = myfont.render("GAME OVER", BLANC)
                rect.center = ((XMIN+XMAX)//2, 2*height//3)
                screen.blit(texte, rect)
                GameContinue = False
                for brique in self.liste_briques:
                    brique.y = brique.y/0.1
                while self.vies <= 0:
                    print("\n\nSouhaitez-vous relancer une partie (Y/N) ?")
                    reponse = input()
                    if reponse == "y" or reponse == "Y":
                        GameContinue = True
                        self.vies = 10  # Car sinon tu repars sur le nombre de vie de la partie précédente
                        self.score = 0
                        demarrer()
                    else:
                        print("Fin de la partie !")
                        break

            if self.score==len(self.liste_briques)*10:
                texte, rect = myfont.render("YOU WON", BLANC)
                rect.center = ((XMIN+XMAX)//2, 2*height//3)
                screen.blit(texte, rect)

    jeu = Jeu(niveau1)

    while True:
        jeu.gestion_evenements()
        jeu.mise_a_jour()
        jeu.affichage()

        pygame.display.flip()
        # On attend le temps necessaire pour avoir un FPS constant
        clock.tick(60)
