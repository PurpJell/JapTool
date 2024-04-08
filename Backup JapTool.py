import re
import random
from datetime import datetime as time
    
# run with:
# python "JapTool.py"

# back-up at "Backup JapTool.py" or run back-up with
# python "Backup JapTool.py"

# simple: 0 - 45
# dakuon: 46 - 70
# combo: 71 - 104
# all: 105 - 123

################################################################################################################################################################################################################

class Settings(object):

     #settings

    minInd = 0
    maxInd = 70
    symbAmt = 1 # amt of symbols to translate in a prompt
    currDict = 'hiragana'

    # methods

    def startUp(self): # imports settings from "settings.txt"

         lines = []

         with open('settings.txt', "r") as settingsFile:
                for line in settingsFile:
                    
                    words = line.split() # splits lines into words
                    lines.append(words) #adds each line to a set (basically stores the file as lines of strings)
  
                    # !! lots of type errors?
                self.minInd = int(lines[0][2]) # [line No][word No]
                self.maxInd = int(lines[1][2])
                self.symbAmt = int(lines[2][2])
                self.currDict = lines[3][2]



    def changeSettings(self, setting): #change some settings, based on command (str setting)

        if setting == 'all':                                                                                        #all
            
            temp = 'ind'
            self.changeSettings(temp)
            temp = 'amt'
            self.changeSettings(temp)
            temp = 'dict'
            self.changeSettings(temp)

            #temp = 'read' # reads file
            #self.changeSettings(temp)

   
        elif setting == 'ind':                                                                                      #ind bounds
            self.minInd = int(input("minInd, maxInd " + str(self.minInd) + " " + str(self.maxInd) + "\n"))

            keyword = 'minInd' #filework
            change = 'minInd = ' + str(self.minInd)
            self.OWFile(keyword, change)

            self.maxInd = int(input())

            keyword = 'maxInd' #filework
            change = 'maxInd = ' + str(self.maxInd)
            self.OWFile(keyword, change)

            #temp = 'read' # reads file
            #self.changeSettings(temp)
         
        elif setting == 'amt':                                                                                      #symbAmt
            self.symbAmt = int(input("How many symbols do you want to translate?\n"))

            keyword = 'symbAmt' #filework
            change = 'symbAmt = ' + str(self.symbAmt)
            self.OWFile(keyword, change)

            #temp = 'read' # reads file
            #self.changeSettings(temp)

        elif setting == 'dict':                                                                                     #dict
            self.currDict = input("What dictionary do you want to use (H/K)?\n")

            if (self.currDict == 'H' or self.currDict == 'h'):
                self.currDict = 'hiragana'
                #print(currDict)
                #print(self.currDict)

            elif (self.currDict == 'K' or self.currDict == 'k'):
                self.currDict = 'katakana'
                #print(currDict)
                #print(self.currDict)

            else:
                self.currDict = 'hiragana'

            keyword = 'currDict' #filework
            change = 'currDict = ' + str(self.currDict)
            self.OWFile(keyword, change)

            #temp = 'read' # reads file
            #self.changeSettings(temp)
 
        elif setting == 'read':
            
            print("Reading settings file...\n")

            lines = []

            with open('settings.txt', "r") as settingsFile:
                for line in settingsFile:
                    lines.append(line) #adds each line to a set
                    line = line.split() # splits lines into words
                    #print((str(line[2])).strip())

                for line in lines: # prints each line
                    print(str(line).strip())

        elif setting == 'default':
            # DEFAULT SETTINGS
            with open('settings.txt', "w") as settingsFile: # overwrites file
                settingsFile.write('minInd = 0\nmaxInd = 70\nsymbAmt = 10\ncurrDict = hiragana')
                self.minInd = 0
                self.maxInd = 70
                self.symbAmt = 10
                self.currDict = 'hiragana'
            print("settings returned to default")
            # remember to change both, settingsFile.write() and self.property!

    def OWFile(self, keyword, change):

        lines = []

        with open('settings.txt', "r") as settingsFile:
                for line in settingsFile:
                    
                    words = line.split() # splits lines into words

                    if words[0] == keyword: # if this is the line that was changed
                        line = change # changes the line
                        #print(str(words[0]) + ' == ' + keyword + ', ' + change)
                        #print("!" + line)

                    lines.append(line) #adds each line to a set (basically stores the file as lines of strings)

        with open('settings.txt', "w") as settingsFile: # overwrites file
            for line in lines:
                settingsFile.write((line).strip() + '\n')

##################################################################################################################################################################################################################################                

class Game(object):

    inARow = 0 # amt of correct answers in a row

    promptTime = time.now()

    hana = [] # all possible words/symbols to include in prompts
    roma = []
    kata = []

    romaji = "x"
    prompt = ""

    def __init__(self):
        self.settings = Settings()
        self.settings.startUp()
        self.readFile() # reads and splits all dictionaries, adds them to respective sets (hana[], roma[]...)
        

    def readFile(self):

        with open('hiragana.txt', "r", encoding="utf-16-le") as hanaFile:

            for line in hanaFile:
                line = line.split()
                for word in line:
                    self.hana.append(word)

        with open('romaji.txt', "r") as romaFile:

            for line in romaFile:
                line = line.split()
                for word in line:
                    self.roma.append(word)

        with open('katakana.txt', "r", encoding="utf-16-le") as kataFile:

            for line in kataFile:
                line = line.split()
                for word in line:
                    self.kata.append(word)

    def getCommand(self): # gets command (input)
        command = input()
        return command


    def givePrompt(self, settings): # generates and gives a prompt
    
        self.prompt = "" #clears prompt
        self.romaji = "" #clears prompt

        for i in range(settings.symbAmt): # fetches symbAmt of symbols 
            symbInd = random.randrange(settings.minInd, settings.maxInd) # generates rng
            self.prompt = self.prompt + str(self.getSymb(symbInd, settings)) # gets symbol and adds it to the prompt
            self.romaji = self.romaji + str(self.getRomanji(symbInd)) + " " # gets romaji counterpart
               
        self.prompt = self.prompt.strip()
        #self.romaji = self.romaji.strip()
    
        print("_"*21+"\n" + self.prompt)
        #print(self.romaji)

        self.promptTime = time.now()

    def getSymb(self, symbInd, settings):

        #print("Ind = " + str(symbInd + 1) + "/" + str(len(self.dictionary) - 1 + 1))

        symb = '!'

        if (settings.currDict == "hiragana"):

            symb = self.hana[symbInd]

        elif (settings.currDict == "katakana"):

            symb = self.kata[symbInd]

        #print("symb = " + str(symb))
        return symb

    def getRomanji(self, symbInd):
        symb = self.roma[symbInd]
        return symb

    def checkAnswer(self, answer):

        temp = self.romaji.strip()
        temp = temp.replace(" ","")
        answer = answer.replace(" ","")

        correct = ""
        st = ""

        answerTime = time.now()

        deltaTimeH = answerTime.hour - self.promptTime.hour
        deltaTimeM = answerTime.minute - self.promptTime.minute
        deltaTimeS = answerTime.second - self.promptTime.second
        deltaTimeMS = answerTime.microsecond - self.promptTime.microsecond

        Time = 0
        Time += deltaTimeH * 3600 + deltaTimeM * 60 + deltaTimeS + deltaTimeMS/1000000

        Time = round(Time, 2)

        if Time >= 60:
            st = "Answered in " + str(Time / 60) + " min and " + str(Time % 60) + " seconds, "
        else:
            st = "Answered in " + str(Time % 60) + " seconds, "

        if answer == temp:
            print("                                         prompt: "+self.prompt)
            print("                                    your answer: "+answer)
            self.inARow += 1
            

            return st, True
        else:

            if len(answer) < len(temp):
                shorter = len(answer)
            else:
                shorter = len(temp)

            for i in range(shorter):
                if answer[i] == temp[i]:
                    correct = correct + "*"
                else:
                    correct = correct + temp[i].capitalize()

            print(" "*41 + "prompt: "+self.prompt)
            print(" "*33 + "correct answer: "+correct)
            print(" "*36 + "your answer: "+answer)
            

            return st, False
            
################################################################################################################################################################################################################### 

game = Game()

timePassed = ""

while (True):

    if game.romaji == 'x': # first cycle?
        print("\n\n\n\nAwaiting input\n\n(x) - exit, (s) - settings, (ent) - next\n")
    if game.romaji != 'x': # not first cycle?
        command = game.getCommand() #gets command
        if command == 'x':
            break
        elif command == 's':
            setting = str(input("\nWhat do you want to change?\n ind | amt | dict | all | read | default\n"))
            game.settings.changeSettings(setting)
            print("Settings changed!\n") #!! if no TypeError
            game.givePrompt(game.settings)
            continue

        timePassed, answer = game.checkAnswer(command) #checks answer
        if answer == True:                                      # correct
            print(" "*49 + "CORRECT.\n" + timePassed + str(game.inARow) + " correct in a row!")
        else:                                                   # incorrect
            print(" "*49 + "INCORRECT!\n" + " "*49 + "Lost streak of " + str(game.inARow) +"\n" + game.romaji)
            game.inARow = 0

    game.givePrompt(game.settings)


    # incorporate romaji +
    # add timer + 
    # add katakana +
    # include alphabet options +
    # make settings folder +
    # add GUI
    # add record tracker
    # catch TypeErrors with each input
    # create kanji and full word files (?)

    # 30 symb speedtype best - 41.66s