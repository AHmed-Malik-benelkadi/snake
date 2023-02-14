#!/usr/bin/python3
# -*- coding: utf-8 -*-
#  ╔═══════════════════════════════════════╗
#  ║               Snake game              ║
#  ║               Crée par                ║
#  ║          Ahmed Malik Ben elkadi       ║
#  ╚═══════════════════════════════════════╝

import pygame  # Importation de la bibliothèque pygame pour le jeu en lui-même et les fonctions de base de pygame
import random  # Importation de la bibliothèque random pour les fonctions aléatoires
import time   # Importation de la bibliothèque time pour les fonctions de temps
import os  # Importation de la bibliothèque os pour les fonctions du système d'exploitation
import sys  # Importation de la bibliothèque sys pour les fonctions du système

# Initialisation de pygame

pygame.init()
""" Définition des couleurs """
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 155, 0)
GREEN_SKIN = (0, 197, 15)
ALIEN = (0, 51, 90)
MENU = (128, 255, 128)

#Définition des dimensions de la fenêtre
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))

# Définition du titre de la fenêtre
pygame.display.set_caption("SNAKE")
icon = pygame.image.load('img/icone_jogo.png') #icone
pygame.display.set_icon(icon)

# Définition des images du jeu
img = pygame.image.load('img/snakehead2.png')
img2 = pygame.image.load('img/snakebody2.png')
img3 = pygame.image.load('img/snakehead_green.png')
img4 = pygame.image.load('img/snakebody1_green.png')
img5 = pygame.image.load('img/apple_normal.png')
img6 = pygame.image.load('img/coca.png')
img7 = pygame.image.load('img/rotten_apple2.png')
art1 = pygame.image.load('img/snake_venom.png')
art2 = pygame.image.load('img/snake_green.png')
art3 = pygame.image.load('img/Snake.jfif')
art4 = pygame.image.load('img/background.png')
art5 = pygame.image.load('img/winnerv3.png')
art6 = pygame.image.load('img/background2.jpg')


clock = pygame.time.Clock()

# Déclarer des variables pour les fonctions,  boucle.


flag = 0
lis = [0]
cont = 0
sorte = 0
azar = 0
snakeCm = 0
respawn = time.localtime()
respawnR = time.localtime()
tempoR = 0
AppleThickness = 30
block_size = 20
block_apple = 30
FPS = 30

direction = 'right' # direction de départ du serpent

#  Définition de la police d'écriture
smallfont = pygame.font.Font("game_over.ttf", 30)
medfont = pygame.font.Font("game_over.ttf", 50)
largefont = pygame.font.Font("game_over.ttf", 100)

def text_objects(text, color, size):
    global textSurface
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0,
                      size="small"):  # msg = str, colour = colour, position du msg au centre y, size = taille
    textSurf, textRect = text_objects(msg, color, size) # textSurf = surface de texte, textRect = rectangle de texte
    textRect.center = (display_width / 2), (display_height / 2) + y_displace # position du msg au centre y
    gameDisplay.blit(textSurf, textRect) # afficher le msg


def message_to_screen_left(msg, color, y_displace=0,
                           size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 6), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)


def message_to_screen_right(msg, color, y_displace=0,
                            size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 1.2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)



def pause():
    """loop du menu pause du jeu """
    paused = True # variable pour la boucle

    while paused:  # boucle du menu pause du jeu
        for event in pygame.event.get(): # boucle pour quitter le jeu
            if event.type == pygame.QUIT:   # si on clique sur la croix rouge
                pygame.quit() # quitter le jeu
                quit() # quitter le programme
            if event.type == pygame.KEYDOWN: # si on appuie sur une touche
                if event.key == pygame.K_c: # si on appuie sur c
                    paused = False # quitter la boucle
                elif event.key == pygame.K_q: # si on appuie sur q
                    pygame.quit() # quitter le jeu
                    quit()
        gameDisplay.fill(WHITE)  # couleur de fond
        gameDisplay.blit(art3, [270, 200]) # afficher l'image de l'art3
        best_score(lis[-1]) # afficher la meilleur score
        message_to_screen("EN PAUSE", BLACK, -200, 'large')   # afficher le msg
        message_to_screen('Pressre sur c pour jouer ou q pour quité !', BLACK, 200, 'medium')  # afficher le msg
        pygame.display.update() # mettre à jour l'affichage
        clock.tick(5)

def score(score):
    """afficher le score du joueur """
    text = medfont.render(f"Score: {score}", True, BLACK) # afficher le score en noir
    gameDisplay.blit(text, [20, 0]) # afficher le score en haut à gauche



def best_score(score, color=BLACK):
    """afficher la meilleur score du joueur """
    text = medfont.render(f"Best Score: {score}", True, color) # afficher la meilleur score en noir
    gameDisplay.blit(text, [600, 0]) # afficher la meilleur score en haut à droite


def vali_score(cont):
    """valider le score du joueur """
    if cont > lis[0]:
        lis.pop()
        lis.append(cont)

def valida_coca():
    """valider la randomisation de la coca """
    global sorte
    sorte = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    return sorte



def valida_rootten():
    """valider la randomisation de la pomme pourrie """
    global azar
    azar = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    return azar


def randAppleGen():
    """randomisation de la pomme """
    randAppleX = random.randrange(30, display_width - block_apple)
    randAppleY = random.randrange(30, display_height - block_apple)

    return randAppleX, randAppleY


def randCocaGen():
    """randomisation de la coca """
    cocaX = random.randrange(30, display_width - block_apple)
    cocaY = random.randrange(30, display_height - block_apple)

    return cocaX, cocaY


def randRottenApple():
    """randomisation de la pomme pourrie"""
    rottenX = random.randrange(30, display_width - block_apple)
    rottenY = random.randrange(30, display_height - block_apple)

    return rottenX, rottenY


def valida_tempo(respawn):
    """valider le temps de surface du coca"""
    global tempo
    if tempo > 60:
        tempo = 60
    if respawn.tm_sec == tempo:
        valida_coca()


def valida_tempo_rotten(respawnR):
    """valider le temps de surface de la pomme pourrie"""
    global tempoR
    if tempoR > 60:
        tempoR = 60
    if respawnR.tm_sec == tempoR:
        valida_rootten()



def game_intro():
    """loop du menu d'intro du jeu """
    intro = True

    while intro:  # boucle du menu d'intro du jeu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(WHITE)  # couleur de fond
        gameDisplay.blit(art3, [270, 20]) # afficher l'image de l'art3
        gameDisplay.blit(img5, (750, 40))    # afficher l'image de l'img5
        gameDisplay.blit(img6, (750, 80))   # afficher l'image de l'img6
        gameDisplay.blit(img7, (750, 120))  # afficher l'image de l'img7
        message_to_screen("BIENVENUE AU JEU SNAKE",
                          GREEN,
                          -15, 'large')
        message_to_screen("Le but du jeu est de manger des pommes. !",
                          BLACK,
                          80, 'medium')
        message_to_screen("Plus tu manges, plus tu grandis !",
                          BLACK,
                          100, 'medium')
        message_to_screen("Si vous vous heurtez à vous-même ou aux murs, vous perdez ! ",
                          BLACK,
                          130, 'medium')
        message_to_screen("Pressre sur c pour jouer ou q pour quité!",
                          RED,
                          250, 'large')
        message_to_screen_left("CONTROLES :",
                               RED,
                               -270, 'medium')
        message_to_screen_left("FLÈCHE VERS LE HAUT | w",
                               RED,
                               -250, 'medium')
        message_to_screen_left("FLÈCHE VERS LE BAS | s",
                               RED,
                               -230, 'medium')
        message_to_screen_left("SETA PARA ESQUERDA | A",
                               RED,
                               -210, 'medium')
        message_to_screen_left("SETA PARA DIREITA | D",
                               RED,
                               -190, 'medium')
        message_to_screen_left("PAUSAR O JOGO = P",
                               RED,
                               -170, 'medium')

        message_to_screen_right('1 POINT ----', BLACK, -250, 'medium') # afficher le score en haut à droite
        message_to_screen_right('5 POINTS ----', BLACK, -210, 'medium') # afficher le score en haut à droite
        message_to_screen_right('-1 POINTS ----', BLACK, -170, 'medium') # afficher le score en haut à droite
        pygame.display.update()
        clock.tick(15) # vitesse de l'intro du jeu


def choose_difficulty():
    """loop du menu de choix de difficulté"""
    global FPS
    choose_dif = True
    while choose_dif:
        for event in pygame.event.get(): # boucle du menu de choix de difficulté
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    FPS = 10
                    choose_dif = False
                elif event.key == pygame.K_2:
                    FPS = 20
                    choose_dif = False
                elif event.key == pygame.K_3:
                    FPS = 30
                    choose_dif = False

        gameDisplay.fill(MENU) # couleur de fond
        message_to_screen("Choisissez la difficulté:", BLACK, -200, 'large') # afficher le message
        message_to_screen_left("facile", GREEN, 100, 'large') # afficher le message
        message_to_screen_left('1', GREEN, 150, 'large')
        message_to_screen('Moyen', ALIEN, 100, 'large')
        message_to_screen('2', ALIEN, 150, 'large')
        message_to_screen_right('Hard', RED, 100, 'large')
        message_to_screen_right('3', RED, 150, 'large')
        pygame.display.update()


def choose_skin():
    """loop du menu de choix de skin"""
    global img, img2, flag
    choose_sk = True
    while choose_sk:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    img = img3
                    img2 = img4
                    flag = 1
                    choose_sk = False
                elif event.key == pygame.K_2:
                    img = pygame.image.load('img/snakehead2.png')
                    img2 = pygame.image.load('img/snakebody2.png')
                    flag = 0
                    choose_sk = False

        gameDisplay.fill(BLACK)
        gameDisplay.blit(art2, [0, 300])
        gameDisplay.blit(art1, [550, 300])
        message_to_screen("Choisissez votre skin: ", RED, -180, 'large')
        message_to_screen_left("1", GREEN, 200, 'large')
        message_to_screen_right('2', ALIEN, 200, 'large')
        pygame.display.update()


def winner_loop():
    """loop de la victoire du jeu"""
    global lis, snakeCm, score
    winner = True
    while winner:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    snakeCm += 60
                    winner = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.blit(art6, (0, 0))
        gameDisplay.blit(art5, (80, 55))
        message_to_screen('Félicitations, vous avez battu le jeu!'.upper(), MENU, -250, 'large')
        message_to_screen('C pour continuer à jouer !', MENU, 200, 'large')
        message_to_screen('Q pour fermer le jeu!', MENU, 250, 'large')
        pygame.display.update()


def snake_grow(block_size, snakeList):
    """fonction qui permet au serpent de grandir"""
    global flag, gameOver
    if direction == 'right':
        head = img
        body = img2

    if direction == 'left':
        head = pygame.transform.rotate(img, 180)
        body = pygame.transform.rotate(img2, 177)

    if direction == 'up':
        head = pygame.transform.rotate(img, 90)
        body = pygame.transform.rotate(img2, 87)
    if direction == 'down':
        head = pygame.transform.rotate(img, 270)
        body = pygame.transform.rotate(img2, 267)
    # afficher le serpent en fonction de la direction dans laquelle il va et de la taille du serpent
    try:
        gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
    except IndexError:
        gameOver = True
    for XnY in snakeList[:-1]:
        if flag == 0:
            pygame.draw.rect(gameDisplay, ALIEN, [XnY[0], XnY[1], block_size, block_size])
        elif flag == 1:
            pygame.draw.rect(gameDisplay, GREEN_SKIN, [XnY[0], XnY[1], block_size, block_size])
        gameDisplay.blit(body, (XnY[0], XnY[1]))




def gameLoop():
    """fonction principale du jeu"""
    global direction, cont, lis, flag, sorte, tempo, respawn, azar, tempoR, respawnR, snakeCm
    direction = 'right'

    gameExit = False  # loop principal du jeu
    gameOver = False  # loop de la fin du jeu

    # # Commencez au milieu de l'écran
    lead_x = display_width / 2
    lead_y = display_height / 2

     # Commencez à ne pas bouger (pas de changement) au début
    lead_x_change = 10
    lead_y_change = 0

    snakeList = []
    snakeCm = 1

    # Générez une pomme aléatoire pour commencer le jeu
    randAppleX, randAppleY = randAppleGen()
    cocaX, cocaY = randCocaGen()
    rottenX, rottenY = randRottenApple()
    valida_rootten()
    # Tant que gameExit n'est pas True, le jeu continue
    while not gameExit:  # loop principal du jeu

        #  Si gameOver est True, le jeu s'arrête
        while gameOver == True:
            # Affichez le message de fin de jeu
            gameDisplay.fill(BLACK)
            message_to_screen("Game over",
                              RED,
                              -50,
                              size="large")

            message_to_screen("Appuyez sur C pour rejouer!", RED, 50, size="medium")
            message_to_screen("Appuyez sur 1 pour changer de Skin!", RED, 100, size="medium")
            message_to_screen("Appuyez sur 2 pour changer de difficulté !", RED, 150, size="medium")
            message_to_screen("Appuyez sur Q pour quitter!", RED, 200, size="medium")
            best_score(lis[-1], RED)
            pygame.display.update()

            # Si l'utilisateur appuie sur Q, le jeu s'arrête et ferme la fenêtre du jeu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        # gameOver = False
                        gameExit = True
                        gameOver = False
                    # Si l'utilisateur appuie sur C, le jeu recommence
                    elif event.key == pygame.K_c:
                        gameLoop()
                    elif event.key == pygame.K_1:
                        choose_skin()
                    elif event.key == pygame.K_2:
                        choose_difficulty()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    direction = 'left'
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    direction = 'right'
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    direction = 'up'
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    direction = 'down'
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()
            # Si l'utilisateur relâche la touche, le serpent ne bouge pas
            if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
                gameOver = True
                cont = 0
            if snakeCm == 0:
                gameOver = True

        if 200 <= snakeCm <= 250:
            winner_loop()

        # Si la tête du serpent touche la pomme, la pomme est générée à un autre endroit aléatoire
        lead_x += lead_x_change
        lead_y += lead_y_change

        # Afficher le fond d'écran et la pomme et la coca et la pomme pourrie
        gameDisplay.blit(art4, (0, 0))


        # Afficher le score et le meilleur score

        gameDisplay.blit(img5, (randAppleX, randAppleY))
        if sorte == 1 or sorte == 5:
            gameDisplay.blit(img6, (cocaX, cocaY))
        if azar == 1:
            gameDisplay.blit(img7, (rottenX, rottenY))

        #  Afficher le serpent
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
        if len(snakeList) > snakeCm:
            snakeList.pop(0)
        # Gestion des éventuelles erreurs d'indexation en dehors de la plage de la liste.
        try:
            if len(snakeList) > snakeCm:
                snakeList.pop()
        except IndexError:
            gameOver = True
        snake_grow(block_size, snakeList)

        # Si la tête du serpent touche le corps du serpent, le jeu s'arrête
        for cadasegment in snakeList[:-1]:
            if cadasegment == snakeHead:
                gameOver = True
                cont = 0

        score(snakeCm - 1)
        best_score(lis[-1])
        vali_score(cont)

        # Mettre à jour l'écran à chaque itération du jeu pour afficher les changements effectués à l'écran
        pygame.display.update()

        # Si la tête du serpent touche la pomme, la pomme est générée à un autre endroit aléatoire
        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or \
                lead_x + block_size > randAppleX and lead_x < randAppleX + AppleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness:
                if sorte == 1 or sorte == 5:
                    sorte = 1
                elif sorte != 1 or sorte != 5:
                    valida_coca()
                elif azar == 1 or azar == 5 or azar == 7 or azar == 3:
                    azar = 1
                elif azar != 1 or azar != 5 or azar == 7 or azar != 3:
                    valida_rootten()


                randAppleX, randAppleY = randAppleGen()
                snakeCm += 1
                cont += 1
                valida_rootten()
                valida_rootten()
            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:
                if sorte == 1 or sorte == 5:
                    sorte = 1
                elif sorte != 1 or sorte != 5:
                    valida_coca()
                elif azar == 1 or azar == 5 or azar == 7 or azar == 3:
                    azar = 1
                elif azar != 1 or azar != 5 or azar != 7 or azar != 3:
                    valida_rootten()

                randAppleX, randAppleY = randAppleGen()
                snakeCm += 1
                cont += 1
                valida_rootten()

        # Traitement pour l'incision du COCA, la collision et autres.
        if sorte == 1 or sorte == 5:
            respawn = time.localtime()
            valida_tempo(respawn)
            if lead_x > cocaX and lead_x < cocaX + AppleThickness or \
                    lead_x + block_size > cocaX and lead_x < cocaX + AppleThickness:
                if lead_y > cocaY and lead_y < cocaY + AppleThickness:
                    cocaX, cocaY = randCocaGen()
                    snakeCm += 5
                    cont += 5
                    valida_coca()
                elif lead_y + block_size > cocaY and lead_y + block_size < cocaY + AppleThickness:
                    cocaX, cocaY = randCocaGen()
                    snakeCm += 5
                    cont += 5
                    valida_coca()
        else:
            # Mise à jour des secondes, en même temps que le traitement du temps, il devient statique dès que le tirage est validé.
            # Si vous passez les secondes sont igausi dans validate_time, il reviendra à cet autre, où il changera
            # la position de la coke aussi
            respawn = time.localtime()
            tempo = respawn.tm_sec + 4
            cocaX, cocaY = randCocaGen()
        # Traitement pour l'incision de la pomme pourrie, la collision et autres.
        if azar == 1 or azar == 5:
            respawnR = time.localtime()
            valida_tempo_rotten(respawnR)
            if lead_x > rottenX and lead_x < rottenX + AppleThickness or \
                    lead_x + block_size > rottenX and lead_x < rottenX + AppleThickness:
                if lead_y > rottenY and lead_y < rottenY + AppleThickness:
                    rottenX, rottenY = randRottenApple()
                    snakeCm -= 1
                    valida_rootten()
                    cont -= 1

                elif lead_y + block_size > rottenY and lead_y + block_size < rottenY + AppleThickness:
                    rottenX, rottenY = randRottenApple()
                    snakeCm -= 1
                    valida_rootten()
                    cont -= 1
        else:
            respawnR = time.localtime()
            tempoR = respawnR.tm_sec + 3
            rottenX, rottenY = randRottenApple()

        clock.tick(FPS)



    #  Afficher le message de fin de jeu et attendre que l'utilisateur appuie sur une touche pour quitter
    pygame.quit()
    quit()


#  Fonction principale

game_intro()
choose_difficulty()
choose_skin()
gameLoop()

# Fin du programme

# Crédits : https://github.com/AHmed-Malik-benelkadi