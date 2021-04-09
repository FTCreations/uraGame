#! python3
# uraGame.py -  my first text based game

import cmd
import textwrap
import sys
import os
import time
import random
import pyinputplus as pyip
import pygame
import platform


screenWidth = 100

### Player Setup
class player:
    def __init__(self):
        self.name = ''
        self.hp = 0
        self.magic = 0
        self.statusEffects = []
        self.location = 'Tet(Home)'
        self.gameOver = False
        self.role = ''
        self.gloryPoints = 0

myPlayer = player()
pygame.mixer.init()

### Title Screen
def titleScreenSelection():
    option = input('> ').lower().strip()
    if option == ('play'):
        setupGame() 
    elif option == ('help'):
        helpMenu() 
    elif option == ('quit'):
        sys.exit()
    while option not in ['play', 'help', 'quit']:
        option = input('> ').lower().strip()
        if option == ('play'):
            setupGame() 
        elif option == ('help'):
            helpMenu() 
        elif option == ('quit'):
            sys.exit()


def titleScreen():
    pygame.mixer.music.load('setupMusic.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    #pygame.mixer.music.set_volume(0.5)
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    print('=====================================================')
    print('*  Welcome Traveler! For You Have Stumbled Upon Ura *')
    print('=====================================================')
    print('                       =Play=                        ')
    print('                       =Help=                        ')
    print('                       =Quit=                        ')
    print('                 ~Copyright 2021 FT~                 ')
    titleScreenSelection()

def helpMenu():
    with open('help.txt', 'r+') as f:
        print(f.read())
    titleScreenSelection()


### Map
'''
Ca1 Uit... #player starts at Tet
--------------
|   |    |   | Monk
--------------
|   |    |   | Hiln
--------------
|   |    |   |
--------------
|   |    |   | Nun
--------------
'''
ZONENAME = ''
NAME = ''
DESCRIPTION = 'description'
INFO = 'info'
PUZZLE = 'puzzle'
ANSWER = ''
EXAMINATION = 'examine'
SOLVED = False
UP = 'up', 'north'
DOWN = 'down', 'south'
LEFT = 'left', 'west'
RIGHT = 'right', 'east'


zoneMap = {
    'Cark': {
        ZONENAME : '',
        DESCRIPTION : 'Desert\n\nDeadliest snake in the land lives here.\n\nThankfully, during the day they remain under the sand.',
        EXAMINATION : 'examine',
        INFO : '==========================================\n\nA huge gust of wind just came through.\n\nSomething shiny is poking out from the sand.\n\nIt\'s a chest!\n\n==========================================',
        PUZZLE : 'The chest reads:\n\nThis Chest Has No Key\n\nAn Answer To A Riddle Is Needed To Open Me\n\n==========================================\n\nPeople in poverty have this,\n\nif you eat it you will die.\n\n==========================================',
        SOLVED : False,
        ANSWER : '',
        UP : '',
        DOWN : 'Snead',
        LEFT : '',
        RIGHT : 'Uit'
    },
    'Uit': {
        ZONENAME : '',
        DESCRIPTION : 'Desert\n\nIt constantly smells of musk in Uit.\n\nNo one knows why.',
        EXAMINATION : 'examine',
        INFO : 'info',
        PUZZLE : '==========================================\n\nAs you are walking through town,\n\nRed eyes peer through a window.\n\nA flash!\n\nIts the Yetll',
        SOLVED : 'monster',
        ANSWER : '',
        UP : '',
        DOWN : 'Bart',
        LEFT : 'Cark',
        RIGHT : 'Varg'
    },
    'Varg': {
        ZONENAME : '',
        DESCRIPTION : 'Plains\n\n2 channels split Varg.\n\nThis is the happiest and wealthiest town.',
        EXAMINATION : 'examine',
        INFO : 'info',
        PUZZLE : '==========================================\n\nThey are having a bit of a Oeg problem\n\nand send you out to take care of it.',
        SOLVED : 'monster',
        ANSWER : '',
        UP : '',
        DOWN : 'Knol',
        LEFT : 'Uit',
        RIGHT : 'Monk'
    },
    'Monk': {
        ZONENAME : '',
        DESCRIPTION : 'Forest\n\nThe forest of Monk houses adult tigers,\n\nas small as chickens.\n\nThey are a popular attraction in this part of the land.',
        EXAMINATION : 'examine',
        INFO : '==========================================\n\nAs the people are distracted, you sneak to the town.\n\nYou stumble upon an open door...\n\nInside is a chest!\n\n==========================================',
        PUZZLE : 'The chest reads:\n\nThis Chest Has No Key\n\nAn Answer To A Riddle Is Needed To Open Me\n\n==========================================\n\nWhat is it that no one wants,\n\nbut no one wants to lose.\n\n==========================================',
        SOLVED : False,
        ANSWER : 'lawsuit',
        UP : '',
        DOWN : 'Hiln',
        LEFT : 'Varg',
        RIGHT : ''
    },
    'Snead': {
        ZONENAME : '',
        DESCRIPTION : 'Desert\n\nBeautiful sand waves cover Snead.\n\nIt is also filled with many abandoned castles...',
        EXAMINATION : 'examine',
        INFO : '',
        PUZZLE : '==========================================\n\nHmm, seems like the thing that caused the evacuations is approaching...\n\nBetter get ready...',
        SOLVED : 'monster',
        ANSWER : '',
        UP : 'Cark',
        DOWN : 'Dor',
        LEFT : '',
        RIGHT : 'Bart'
    },
    'Bart': {
        ZONENAME : 'Home',
        DESCRIPTION : 'Plains\n\nBland is a nice way to describe Bart.\n\nThe trees are pale.\n\nSky grey.\n\nEven the cows have a grey tint',
        EXAMINATION : 'examine',
        INFO : '==========================================\n\nWhile mesmorized by the originality/unorginality of Bart,\n\nYou trip and stumble face first,\n\ninto a chest!\n\n==========================================',
        PUZZLE : 'The chest reads:\n\nThis Chest Has No Key\n\nAn Answer To A Riddle Is Needed To Open Me\n\n==========================================\n\nWhat jumps when walking, but sits when standing?\n\n==========================================',
        SOLVED : False,
        ANSWER : 'kangaroo',
        UP : 'Uit',
        DOWN : 'Pit',
        LEFT : 'Snead',
        RIGHT : 'Knol'
    },
    'Knol': {
        ZONENAME : '',
        DESCRIPTION : 'Plains\n\nThis town is made up of grassy...knolls, you gussed it!\n\nThe Townspeople aren\'t too orginal...\n\nCough...',
        EXAMINATION : 'examine',
        INFO : '==========================================\n\nWhile walking around you find a slide.\n\nYou take it.\n\nAt the end there is a chest!\n\n==========================================',
        PUZZLE : 'The chest reads:\n\nThis Chest Has No Key\n\nAn Answer To A Riddle Is Needed To Open Me\n\n==========================================\n\nI am born tall, but grow short with age.\n\nWhat could I be?\n\n==========================================',
        SOLVED : False,
        ANSWER : 'pencil',
        UP : 'Varg',
        DOWN : 'Tet(Home)',
        LEFT : 'Bart',
        RIGHT : 'Hiln'
    },
    'Hiln': {
        ZONENAME : '',
        DESCRIPTION : 'Forest\n\nHiln is covered in moss,\n\ntrees 170 feet tall.',
        EXAMINATION : 'examine',
        INFO : '',
        PUZZLE : '==========================================\n\nThere lives no animals in Hiln,\n\nOnly the Seep.\n\nSSSSSSSS......\n\nUh oh! Looks like its approaching.',
        SOLVED : 'monster',
        ANSWER : '',
        UP : 'Monk',
        DOWN : 'Asher',
        LEFT : 'Knol',
        RIGHT : ''
    },
    'Dor': {
        ZONENAME : '',
        DESCRIPTION : 'Desert\n\nThere are about 1,000 Oases in Dor',
        EXAMINATION : 'examine',
        INFO : '==========================================\n\nThe first oasis you stumble upon turns out to have a chest.\n\nSmack dab in the middle.\n\n==========================================',
        PUZZLE : 'The chest reads:\n\nThis Chest Has No Key\n\nAn Answer To A Riddle Is Needed To Open Me\n\n==========================================\n\nWhen I am needed by you, you throw me away,\n\nbut when I\'m of no use, you take me back.\n\nWhat am I?\n\n==========================================',
        SOLVED : False,
        ANSWER : 'anchor',
        UP : 'Snead',
        DOWN : 'Los',
        LEFT : '',
        RIGHT : 'Pit'
    },
    'Pit': {
        ZONENAME : '',
        DESCRIPTION : 'Plains\n\nWheat and barley cover the fields of Pit.',
        EXAMINATION : 'examine',
        INFO : '',
        PUZZLE : '==========================================\n\nA shadowy figure appears as if it is getting closer in the distance.\n\nThere is no time.\n\nWhat do you do?',
        SOLVED : 'monster',
        ANSWER : '',
        UP : 'Bart',
        DOWN : 'Fin',
        LEFT : 'Dor',
        RIGHT : 'Tet(Home)'
    },
    'Tet(Home)': {
        NAME : 'Tet(Home)',
        DESCRIPTION : 'Forest\n\nYour Homestead is located atop the trees in the dense forest of Tet.\n\nAll is calm.\n\nThe Townspeople are especially nice in Tet.',
        EXAMINATION : 'examine',
        INFO : 'Your Home',
        PUZZLE : 'puzzle',
        SOLVED : True,
        ANSWER : 'car',
        UP : 'Knol',
        DOWN : 'Reft',
        LEFT : 'Pit',
        RIGHT : 'Asher'
    },
    'Asher': {
        ZONENAME : '',
        DESCRIPTION : 'Forest\n\nForest of Asher are thick and viney.',
        EXAMINATION : 'examine',
        INFO : '==========================================\n\nAs you are hacking away you stumble across a chest!\n\n==========================================',
        PUZZLE : 'The chest reads:\n\nThis Chest Has No Key\n\nAn Answer To A Riddle Is Needed To Open Me\n\n==========================================\n\nA mother and a father have four daughters and each has a brother.\n\nHow many people are in the family?\n\n==========================================',
        SOLVED : False,
        ANSWER : 'seven',
        UP : 'Hiln',
        DOWN : 'Nun',
        LEFT : 'Tet(Home)',
        RIGHT : ''
    },
    'Los': {
        ZONENAME : '',
        DESCRIPTION : 'Plains\n\nThe vast plains of Los go as far as the eye can see.',
        EXAMINATION : 'examine',
        INFO : '',
        PUZZLE : '==========================================\n\nAll of a sudden you hear and feel breathing\n\nIt is already too late.',
        SOLVED : 'monster',
        ANSWER : '',
        UP : 'Dor',
        DOWN : '',
        LEFT : '',
        RIGHT : 'Fin'
    },
    'Fin': {
        ZONENAME : '',
        DESCRIPTION : 'Plains\n\nPirarie dogs run amuck in Fin.\n\nThe settlers have all moved out.\n\nBut left all their belongings...',
        EXAMINATION : 'examine',
        SOLVED : False,
        ANSWER : 'cloud',
        INFO : '==========================================\n\nYou come acorss a town and inside the 4th home is a chest!\n\n==========================================',
        PUZZLE : 'The chest reads:\n\nThis Chest Has No Key\n\nAn Answer To A Riddle Is Needed To Open Me\n\n==========================================\n\nI fly without wings, and cry without eyes.\n\nWhenever I lead, darkness follows.\n\nWhat could I be?\n\n==========================================',
        UP : 'Pit',
        DOWN : '',
        LEFT : 'Los',
        RIGHT : 'Reft'
    },
    'Reft': {
        ZONENAME : '',
        DESCRIPTION : 'Forest\n\nApes swing high and low in Reft.',
        EXAMINATION : 'examine',
        INFO : '==========================================\n\nSome baboons are howling in a circle.\n\nYou go to check it out.\n\nYou guessed it,\n\nits a chest!\n\n==========================================',
        PUZZLE : 'The chest reads:\n\nThis Chest Has No Key\n\nAn Answer To A Riddle Is Needed To Open Me\n\n==========================================\n\nWhat is caught but never thrown?\n\n==========================================',
        SOLVED : False,
        ANSWER : 'cold',
        UP : 'Tet(Home)',
        DOWN : '',
        LEFT : 'Fin',
        RIGHT : 'Nun'
    },
    'Nun': {
        ZONENAME : '',
        DESCRIPTION : 'Forest\n\nThe tress in Nun droop and weep.',
        EXAMINATION : 'examine',
        INFO : '',
        PUZZLE : '==========================================\n\nThe tress in Nun are low\n\nbecause perched atop\n\nis the giant Meech.\n\nLook out!',
        SOLVED : 'monster',
        ANSWER : '',
        UP : 'Asher',
        DOWN : '',
        LEFT : 'Reft',
        RIGHT : ''
    }
    
}

### Game Interactivity
def printLocation():
    print('\n' + ('#' * (4 + len(myPlayer.location))))
    print('# ' + myPlayer.location.upper() + ' #')
    print(zoneMap[myPlayer.location][DESCRIPTION])
    print('\n' + ('#' * (4 + len(myPlayer.location))))

def prompt():
    print('\n' + '==========================================')
    print('\nWhat would you like to do?\n')
    acceptableActions = ['Travel', 'Examine', 'Quit']
    action = pyip.inputMenu(acceptableActions).lower().strip()
    if action == 'quit':
        sys.exit()
    elif action == 'travel':
        playerMove(action)
    elif action == 'examine':
        playerExamine(action)

def playerMove(Action):
    ask = '\nWhere would you like to move?\n'
    direction = ['North', 'South', 'East', 'West']
    dest = pyip.inputMenu(direction, ask).lower().strip()
    if dest in ['up', 'north']:
        destination = zoneMap[myPlayer.location][UP]
        if destination == '':
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('fallingSE.wav'))
            print('\n' + '==========================================')
            print('\nSeems as though that direction leads to the side of a cliff.')
            print('\nTry a different direction.')
            playerMove(Action)
        else:
            movementHandler(destination)
    elif dest in ['down', 'south']:
        destination = zoneMap[myPlayer.location][DOWN]
        if destination == '':
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('fallingSE.wav'))
            print('\n' + '==========================================')
            print('\nSeems as though that direction leads to the side of a cliff.')
            print('\nTry a different direction.')
            playerMove(Action)
        else:
            movementHandler(destination)
    elif dest in ['left', 'west']:
        destination = zoneMap[myPlayer.location][LEFT]
        if destination == '':
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('fallingSE.wav'))
            print('\n' + '==========================================')
            print('\nSeems as though that direction leads to the side of a cliff.')
            print('\nTry a different direction.')
            playerMove(Action)
        else:
            movementHandler(destination)
    elif dest in ['right', 'east']:
        destination = zoneMap[myPlayer.location][RIGHT]
        if destination == '':
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('fallingSE.wav'))
            print('\n' + '==========================================')
            print('\nSeems as though that direction leads to the side of a cliff.')
            print('\nTry a different direction.')
            playerMove(Action)
        else:
            movementHandler(destination)



def movementHandler(destination):
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('travelSounds.wav'))
    myPlayer.location = destination
    print('\n' + 'You have moved to ' + destination + '.')
    printLocation()

def playerAttack():
    chance = random.randint(3,9)
    monsterHP = 20 * chance
    while monsterHP > 0:
        print('\n' + '==========================================')
        fightResponse = pyip.inputMenu(['Attack', 'Run'], limit = 2).lower().strip()
        attackChance = random.uniform(0,1)
        monsterAttackChance = random.randint(1,9)
        attack = (myPlayer.magic * attackChance)
        monsterAttack = (2 * monsterAttackChance)
        if fightResponse == 'attack':
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('AttackSoundEffect.wav'))
            myPlayer.hp -= monsterAttack 
            monsterHP -= attack
            print('\n' + '==========================================')
            print('\nAttack did {:0,.0f}'.format(attack) + ' Damage Points')
            print('\nMonster Health Points {0:,.0f}'.format(monsterHP))
            print('\nMonster\'s Attack did ' + str(monsterAttack) + ' Damage Points to you')
            print('\nYou have ' + str(myPlayer.hp) + ' Health Points')
            checkDeath()
        else:
            chance = random.randint(0,9)
            if chance in range(0,3):
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('runningAway.wav'))
                print('\n' + '==========================================')
                print('\nYou got away safely!\n')
                print('\nHealth Points: ' + str(myPlayer.hp))  
                print('\nMagic Points: ' + str(myPlayer.magic)) 
                print('\nGlory Points To Go: ' + str(5 - myPlayer.gloryPoints))
                prompt()
            else:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('takeHit.wav'))
                print('\n' + '==========================================')
                print('\nUnfortunately due to the circumstances you do not get away.\n')
                myPlayer.hp -= 15
                print('\n' + myPlayer.name + ' took a HP hit')
                print('\nTotal Health Points: ' + str(myPlayer.hp))
                checkDeath() 
    else:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('monsterDeath.wav'))
        myPlayer.gloryPoints += 1
        print('\n==========================================')
        print('\nYou defeated the Monster!\n')
        print('\n' + myPlayer.name + ' Gained +1 Glory Points\n')
        print('\nGlory Points Total: ' + str(myPlayer.gloryPoints))
        zoneMap[myPlayer.location][SOLVED] = True
        zoneMap[myPlayer.location][INFO] = 'All is quiet...'
        checkGP()
        

def playerExamine(action):
    if zoneMap[myPlayer.location][SOLVED] == True:
        printLocation()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('examine.wav'))
        print('\n' + '==========================================')
        print('\n' + (zoneMap[myPlayer.location][INFO]))
        print('\nThere are no new happenings in this area.')
        checkGP()
    elif zoneMap[myPlayer.location][SOLVED] == 'monster':
        print('\n' + (zoneMap[myPlayer.location][PUZZLE]))
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('monsterRoar.wav'))
        playerAttack()
    else:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('chestDisc.wav'))
        print('\n' + (zoneMap[myPlayer.location][INFO]))
        print('\n' + (zoneMap[myPlayer.location][PUZZLE]) + '\n')
        puzzleAnswer = input('> ').lower().strip()
        plusHP = (2 * random.randint(1,9))
        plusMagic = (2 * random.randint(1,9))
        if puzzleAnswer == zoneMap[myPlayer.location][ANSWER]:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('chestUnlock.wav'))
            myPlayer.hp += plusHP
            myPlayer.magic += plusMagic
            print('\n' + '==========================================')
            print('\nChest Unlocked!')
            print('\nYou Gained:')
            print('\n' + str(plusHP) + ' Health Points!')
            print('\n' + str(plusMagic) + ' Magic Points!')
            zoneMap[myPlayer.location][SOLVED] = True
            zoneMap[myPlayer.location][INFO] = 'All is quiet...'
            checkGP()

        else:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('chestLock.wav'))
            print('\n' + '==========================================')
            print('\nSorry, wrong answer.\n\nI remain locked.\n\nTo Try Again, Re-Examine.')
            checkGP()


def checkGP():
    if myPlayer.location == 'Tet(Home)':
        if myPlayer.gloryPoints >= 5:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('victoryMusic.wav')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
            if platform.system() == 'Windows':
                os.system('cls')
            else:
                os.system('clear')
            ending = 'Congradulations, Hero!!!\n\nYou lift up the heads of the ' + str(myPlayer.gloryPoints) + ' monsters you\'ve slain and the townspeople go wild.\n\nThey erect a statue of you 20 feet tall.\n\nYour Journey has come to an end.\n\nYou truly found the glory you were searching for.\n\nAlways remember the path to glory is never the same...\n\n\nHope you enjoyed the game!'
            for i in ending:
                sys.stdout.write(i)
                sys.stdout.flush()
                time.sleep(0.1)
            time.sleep(5)
            titleScreen()
        elif myPlayer.hp <= 89:
            myPlayer.hp += 10
            print('\n' + '==========================================')
            print('\nWelcome home, ' + myPlayer.name + '.')
            print('\nThe townspeople greet you with tea. +10 HP')
            print('\nHealth Points: ' + str(myPlayer.hp))  
            print('\nMagic Points: ' + str(myPlayer.magic)) 
            print('\nGlory Points To Go: ' + str(5 - myPlayer.gloryPoints))
        else:
            print('\n' + '==========================================')
            print('\nWelcome home, ' + myPlayer.name + '.')
            print('\nHealth Points: ' + str(myPlayer.hp))  
            print('\nMagic Points: ' + str(myPlayer.magic)) 
            print('\nGlory Points To Go: ' + str(5 - myPlayer.gloryPoints))
            prompt()
    else:
        if myPlayer.gloryPoints >= 5:
            print('\n' + '==========================================')
            print('\nYou seem tired, head on home champ.')
            print('\nIf you would like, you can keep exploring.')
            print('\nHealth Points: ' + str(myPlayer.hp))  
            print('\nMagic Points: ' + str(myPlayer.magic))
            print('\nGlory Point Total: ' + str(myPlayer.gloryPoints))
        else:
            print('\n' + '==========================================')
            print('\nHealth Points: ' + str(myPlayer.hp))  
            print('\nMagic Points: ' + str(myPlayer.magic)) 
            print('\nGlory Points To Go: ' + str(5 - myPlayer.gloryPoints))
            print('\nYour Journey Continues!')
            prompt()



def checkDeath():
    if myPlayer.hp < 0:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('deathMusic.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
        print('\n' + '==========================================')
        deathScene = '\nYou Have Succumm To Your Injuries From The Battle....'
        light = '\nThe Light Starts To Fade...'
        death = '\nYour Journey For Glory Has Come To An End....'
        glory = '\nGlory Points Earned This Try: ' + str(myPlayer.gloryPoints)
        for i in deathScene:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        for i in light:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.07)
        for i in death:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        for i in glory:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(5)
        titleScreen()
		    




### Game Functionality

def mainGameLoop():
    while myPlayer.gameOver == False:
        prompt()
    # here handle if puzzle has been solved, boss defeated, etc.


def setupGame():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    

## Name Handling

    question1 = 'Hello, what is your name?\n'
    for character in question1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    
    myPlayer.name = pyip.inputStr('> ').strip()
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('selectChar.wav'))

## Role Handling
    question2 = '\nWhat role would you like to play as ' + myPlayer.name + '?\n'

    for character in question2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)

    validRoles = ['warrior', 'mage', 'witch', 'fairy', 'elf', 'warlock', 'dwarf', 'orc', 'ogre']
    validRolesSelect = ['Warrior', 'Mage', 'Witch', 'Fairy', 'Elf', 'Warlock', 'Dwarf', 'Orc', 'Ogre']
    playerRole = pyip.inputMenu(validRolesSelect).lower().strip()
    if playerRole in validRoles:
        myPlayer.role = playerRole
        if myPlayer.role == 'warrior':
            myPlayer.hp += 100
            myPlayer.magic += 50
        elif myPlayer.role == 'mage':
            myPlayer.hp += 70
            myPlayer.magic += 100
        elif myPlayer.role == 'witch':
            myPlayer.hp += 70
            myPlayer.magic += 100
        elif myPlayer.role == 'fairy':
            myPlayer.hp += 70
            myPlayer.magic += 90
        elif myPlayer.role == 'elf':
            myPlayer.hp += 80
            myPlayer.magic += 80
        elif myPlayer.role == 'warlock':
            myPlayer.hp += 100
            myPlayer.magic += 50
        elif myPlayer.role == 'dwarf':
            myPlayer.hp += 90
            myPlayer.magic += 40
        elif myPlayer.role == 'orc':
            myPlayer.hp += 70
            myPlayer.magic += 50
        elif myPlayer.role == 'ogre':
            myPlayer.hp += 90
            myPlayer.magic += 70
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('selectChar.wav'))
    print('\nYou are now a/n ' + playerRole + '!\n')
    print('\n' + playerRole + ' - Health Points: ' + str(myPlayer.hp) + ' Magic Points: ' + str(myPlayer.magic) + '\n')
    
    ## Player Stats
    

    ## Introduction
    question3 = '\nWelcome, ' + myPlayer.name+  ' the ' + playerRole + '!\n'
    for character in question3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    
    introSpeech1 = '\nFor You Have Stumbled Upon The Land Of Ura\n'
    for character in introSpeech1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    
    introSpeech2 = '\nTis A Treacherous Place\n'
    for character in introSpeech2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    
    introSpeech3 = '\nBut, Be Not Afraid Young Traveler...\n'
    for character in introSpeech3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    
    introSpeech4 =  '\nYour Journey For Glory Has Just Begun...\n'
    for character in introSpeech4:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    time.sleep(2)
    #pygame.mixer.music.stop()
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('openingDrop.wav'))
    print('===========================================')
    print('*         Thy Jounrey Begins Now!         *')
    print('===========================================')
    print('\nWelcome to the Land of Ura!\n\nTo navigate Ura you will be prompted with actions.\n\nPlease answer with one word.\n\nAfter that, the path to eternal glory is up to you...\n\nGood Luck and Have Fun!')

    mainGameLoop()




titleScreen()