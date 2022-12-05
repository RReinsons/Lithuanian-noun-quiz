import tkinter as tk
import random
from Lithuanian_noun_list import *

# 1=as | 2=is(1st d) | 3=ys | 4=ias | 5=a | 6=ia | 7=ė | 8=is(F) | 9=is(M) | 10=us | 11=ius | 12=uo(M) | 13=uo(F)
wordList = []

currentprompt = int
wordinsingular = bool
currentcollocation = ""
currentword = ""
currentwordlv = ""
currentwordEN = ""
singularstring = ""
answerending = ""
answersolution = ""
givenanswer = ""
singularchoice = ""
answer = ""
currentturn= 0
currentscore = 0
hasguessed = True
iscorrect = bool
preword = ""
prewordLV = ""
cananswer = False

currentcollocationLV = ""
singularstringLV = ""

possiblecollocationssingle = []
possiblecollocationsplural = []

addnominative = False
addgenitive = False
adddative = False
addaccusative = False
addinstrumental = False
addlocative = False

allowsingular = False
allowplural = False

language = "EN"

launchQuiz = False

translationTextEN = "In english \"{}\" means \"{}\""
answerTextEN = "The answer was: \"{}\""

turnTextEN = "Turn: {}"
scoreTextEN = "Score: {}%"

translationTextLV = "Latviski \"{}\" nozimē \"{}\""
answerTextLV = "Pareizā atbilde ir: \"{}\""

turnTextLV = "Kārta: {}"
scoreTextLV = "Procenti: {}%"

class QuizWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("500x275")

        self.score_frame = tk.Frame(self.window, height=25, relief=tk.GROOVE, borderwidth=4)
        self.word_frame = tk.Frame(self.window, height=75, relief=tk.RAISED, borderwidth=4)
        self.note_frame = tk.Frame(self.window, height=75, relief=tk.SUNKEN, borderwidth=5)
        self.input_frame = tk.Frame(self.window, height=100)
        self.button_frame = tk.Frame(self.window)

        self.word_frame.columnconfigure(0, weight=1)
        self.word_frame.rowconfigure(0, weight=1)
        self.word_frame.rowconfigure(1, weight=1)

        self.note_frame.columnconfigure(0, weight=1)
        self.note_frame.rowconfigure(0, weight=1)
        self.note_frame.rowconfigure(1, weight=1)
        self.note_frame.rowconfigure(2, weight=1)

        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.rowconfigure(0, weight=1)

        self.score_frame.columnconfigure(0, weight=1)
        self.score_frame.columnconfigure(1, weight=1)
        self.score_frame.rowconfigure(0, weight=1)

        self.scoreLabel = tk.Label(self.score_frame, font=('Arial', 10))
        self.scoreLabel.grid(row=0, column=0, sticky="W")

        self.turnLabel = tk.Label(self.score_frame, font=('Arial', 10))
        self.turnLabel.grid(row=0, column=1, sticky="E")

        self.givenWord = tk.Label(self.word_frame, text="Word", font=('Arial', 18))

        self.givenQuestion = tk.Label(self.word_frame, text="Question", font=('Arial', 14))

        self.grade = tk.Label(self.note_frame, text="", font=('Arial', 18))

        self.noteText = tk.Label(self.note_frame, text="Answer", font=('Arial', 14))

        self.noteText2 = tk.Label(self.note_frame, text="Translation", font=('Arial', 14))

        self.inputBox = tk.Entry(self.input_frame, font=('Arial', 16), justify='center', borderwidth=3)
        self.inputBox.bind('<KeyPress>', self.answerShortcut)
        self.inputBox.pack(padx=20, fill='x')

        self.answerButton = tk.Button(self.button_frame, font=('Arial', 16), borderwidth=3, relief=tk.GROOVE, command=self.answer)
        self.nextButton = tk.Button(self.button_frame, font=('Arial', 16), borderwidth=3, relief=tk.GROOVE, command=self.next)

        if language == "EN":
            self.answerButton.configure(text="Answer")
            self.nextButton.configure(text="Start")
            self.scoreLabel.configure(text="Score: ")
            self.turnLabel.configure(text="Turn: ")
        elif language == "LV":
            self.answerButton.configure(text="Atbildēt")
            self.nextButton.configure(text="Sākt")
            self.scoreLabel.configure(text="Procenti: ")
            self.turnLabel.configure(text="Kārta: ")

        self.nextButton.grid(row=0, column=1)

        self.score_frame.pack(fill='x', pady=2)
        self.word_frame.pack(fill="x", pady=2, padx=10)
        self.note_frame.pack(fill="x")
        self.input_frame.pack(fill="x")
        self.button_frame.pack(fill="x")


        self.window.mainloop()


    def answer(self):
        global iscorrect
        global hasguessed
        global currentscore
        global cananswer
        self.grade.grid(row=0, column=0)
        if answersolution == str(self.inputBox.get()) and language == "EN":
            self.grade.configure(text='CORRECT')
            currentscore += 1
        elif not answersolution == str(self.inputBox.get()) and language == "EN":
            self.grade.configure(text='INCORRECT')

        if answersolution == str(self.inputBox.get()) and language == "LV":
            self.grade.configure(text='PAREIZI')
            currentscore += 1
        elif not answersolution == str(self.inputBox.get()) and language == "LV":
            self.grade.configure(text='NEPAREIZI')

        if currentscore != 0 and language == "EN":
            self.scoreLabel.configure(text=scoreTextEN.format(str(round(100*(currentscore / currentturn) ) ) ) )
        elif currentscore != 0 and language == "LV":
            self.scoreLabel.configure(text=scoreTextLV.format(str(round(100*(currentscore / currentturn) ) ) ) )
        elif not hasguessed and currentscore == 0 and language == "EN":
            self.scoreLabel.configure(text=scoreTextEN.format("0"))
        elif not hasguessed and currentscore == 0 and language == "LV":
            self.scoreLabel.configure(text=scoreTextLV.format("0"))

        self.noteText.grid(row=1, column=0)
        if language == "EN":
            self.noteText.configure(text=answerTextEN.format(answersolution))
        else:
            self.noteText.configure(text=answerTextLV.format(answersolution))

        self.noteText2.grid(row=2, column=0)
        if language == "EN":
            self.noteText2.configure(text=translationTextEN.format(currentword, currentwordEN))
        else:
            self.noteText2.configure(text=translationTextLV.format(currentword, currentwordlv))

        self.answerButton.grid_forget()

        hasguessed = True
        cananswer = False


    def next(self):

        global currentprompt
        global currentword
        global currentwordlv
        global currentcollocation
        global answerending
        global answersolution
        global answer
        global answerText
        global givenanswer
        global iscorrect
        global currentscore
        global currentturn
        global hasguessed
        global cananswer
        global possiblecollocationssingle
        global possiblecollocationsplural
        global currentwordEN
        global currentcollocationLV
        global singularstringLV

        currentprompt = random.randint(0, len(wordList) - 1)
        currentword = wordList[currentprompt]["LT"] + wordList[currentprompt]["Ending"]
        currentwordlv = wordList[currentprompt]["LV"]
        currentwordEN = wordList[currentprompt]["EN"]

        if allowplural and allowsingular:
            if random.randint(0, 1) == 0:
                wordinsingular = True
                singularstring = ""
                singularstringLV = ""
            else:
                wordinsingular = False
                singularstring = " and plural"
                singularstringLV = " un daudzskaitlī"
        elif allowsingular and not allowplural:
            wordinsingular = True
            singularstring = ""
            singularstringLV = ""
        else:
                wordinsingular = False
                singularstring = " and plural"
                singularstringLV = " un daudzskaitlī"
        if wordinsingular:
            currentcollocation = possiblecollocationssingle[random.randint(0, len(possiblecollocationssingle)-1)]
        else:
            currentcollocation = possiblecollocationsplural[random.randint(0, len(possiblecollocationsplural)-1)]
        # plural nominative
        if currentcollocation == "nominative" and not wordinsingular:
            if nounList[currentprompt]["declension"] in [1, 2]:
                answerending = "ai"
            if nounList[currentprompt]["declension"] in [3, 4, 5]:
                answerending = "iai"
            if nounList[currentprompt]["declension"] == 6:
                answerending = "os"
            if nounList[currentprompt]["declension"] == 7:
                answerending = "ios"
            if nounList[currentprompt]["declension"] == 8:
                answerending = "ės"
            if nounList[currentprompt]["declension"] in [9, 10]:
                answerending = "ys"
            if nounList[currentprompt]["declension"] == 11:
                answerending = "ūs"
            if nounList[currentprompt]["declension"] == 12:
                answerending = "iai"
            if nounList[currentprompt]["declension"] == 13:
                answerending = "enys"
            if nounList[currentprompt]["declension"] == 14:
                answerending = "erys"

        # genitive singular
        if currentcollocation == "genitive" and wordinsingular:
            if nounList[currentprompt]["declension"] in [1, 2]:
                answerending = "o"
            if nounList[currentprompt]["declension"] in [3, 4, 5]:
                answerending = "io"
            if nounList[currentprompt]["declension"] == 6:
                answerending = "os"
            if nounList[currentprompt]["declension"] == 7:
                answerending = "ios"
            if nounList[currentprompt]["declension"] == 8:
                answerending = "ės"
            if nounList[currentprompt]["declension"] in [9, 10]:
                answerending = "ies"
            if nounList[currentprompt]["declension"] == 11:
                answerending = "aus"
            if nounList[currentprompt]["declension"] == 12:
                answerending = "iaus"
            if nounList[currentprompt]["declension"] == 13:
                answerending = "ens"
            if nounList[currentprompt]["declension"] == 14:
                answerending = "ers"

        # genitive plural
        if currentcollocation == "genitive" and not wordinsingular:
            if nounList[currentprompt]["declension"] in [1, 2]:
                answerending = "ų"
            if nounList[currentprompt]["declension"] in [3, 4, 5]:
                answerending = "ių"
            if nounList[currentprompt]["declension"] == 6:
                answerending = "ų"
            if nounList[currentprompt]["declension"] == 7:
                answerending = "ių"
            if nounList[currentprompt]["declension"] == 8:
                answerending = "ių"
            if nounList[currentprompt]["declension"] in [9, 10]:
                answerending = "ių"
            if nounList[currentprompt]["declension"] == 11:
                answerending = "ų"
            if nounList[currentprompt]["declension"] == 12:
                answerending = "ių"
            if nounList[currentprompt]["declension"] == 13:
                answerending = "enų"
            if nounList[currentprompt]["declension"] == 14:
                answerending = "erų"

        # dative singular
        if currentcollocation == "dative" and wordinsingular:
            if nounList[currentprompt]["declension"] in [1, 2]:
                answerending = "ui"
            if nounList[currentprompt]["declension"] in [3, 4, 5]:
                answerending = "iui"
            if nounList[currentprompt]["declension"] == 6:
                answerending = "ai"
            if nounList[currentprompt]["declension"] == 7:
                answerending = "iai"
            if nounList[currentprompt]["declension"] == 8:
                answerending = "ei"
            if nounList[currentprompt]["declension"] == 9:
                answerending = "iai"
            if nounList[currentprompt]["declension"] == 10:
                answerending = "iui"
            if nounList[currentprompt]["declension"] == 11:
                answerending = "ui"
            if nounList[currentprompt]["declension"] == 12:
                answerending = "iui"
            if nounList[currentprompt]["declension"] == 13:
                answerending = "eniui"
            if nounList[currentprompt]["declension"] == 14:
                answerending = "eriai"

        # dative plural
        if currentcollocation == "dative" and not wordinsingular:
            if nounList[currentprompt]["declension"] in [1, 2]:
                answerending = "ams"
            if nounList[currentprompt]["declension"] in [3, 4, 5]:
                answerending = "iams"
            if nounList[currentprompt]["declension"] == 6:
                answerending = "oms"
            if nounList[currentprompt]["declension"] == 7:
                answerending = "ioms"
            if nounList[currentprompt]["declension"] == 8:
                answerending = "ėms"
            if nounList[currentprompt]["declension"] in [9, 10]:
                answerending = "ims"
            if nounList[currentprompt]["declension"] == 11:
                answerending = "ums"
            if nounList[currentprompt]["declension"] == 12:
                answerending = "iams"
            if nounList[currentprompt]["declension"] == 13:
                answerending = "enims"
            if nounList[currentprompt]["declension"] == 14:
                answerending = "erims"

        # accusative singular
        if currentcollocation == "accusative" and wordinsingular:
            if nounList[currentprompt]["declension"] in [1, 2]:
                answerending = "ą"
            if nounList[currentprompt]["declension"] in [3, 4]:
                answerending = "į"
            if nounList[currentprompt]["declension"] == 5:
                answerending = "ią"
            if nounList[currentprompt]["declension"] == 6:
                answerending = "ą"
            if nounList[currentprompt]["declension"] == 7:
                answerending = "ią"
            if nounList[currentprompt]["declension"] == 8:
                answerending = "ę"
            if nounList[currentprompt]["declension"] in [9, 10]:
                answerending = "į"
            if nounList[currentprompt]["declension"] == 11:
                answerending = "ų"
            if nounList[currentprompt]["declension"] == 12:
                answerending = "ių"
            if nounList[currentprompt]["declension"] == 13:
                answerending = "enį"
            if nounList[currentprompt]["declension"] == 14:
                answerending = "erį"

        # accusative plural
        if currentcollocation == "accusative" and not wordinsingular:
            if nounList[currentprompt]["declension"] in [1, 2]:
                answerending = "us"
            if nounList[currentprompt]["declension"] in [3, 4, 5]:
                answerending = "ius"
            if nounList[currentprompt]["declension"] == 6:
                answerending = "as"
            if nounList[currentprompt]["declension"] == 7:
                answerending = "ias"
            if nounList[currentprompt]["declension"] == 8:
                answerending = "es"
            if nounList[currentprompt]["declension"] in [9, 10]:
                answerending = "is"
            if nounList[currentprompt]["declension"] == 11:
                answerending = "us"
            if nounList[currentprompt]["declension"] == 12:
                answerending = "ius"
            if nounList[currentprompt]["declension"] == 13:
                answerending = "enis"
            if nounList[currentprompt]["declension"] == 14:
                answerending = "eris"

        # instrumental singular
        if currentcollocation == "instrumental" and wordinsingular:
            if nounList[currentprompt]["declension"] in [1, 2]:
                answerending = "u"
            if nounList[currentprompt]["declension"] in [3, 4, 5]:
                answerending = "iu"
            if nounList[currentprompt]["declension"] == 6:
                answerending = "a"
            if nounList[currentprompt]["declension"] == 7:
                answerending = "ia"
            if nounList[currentprompt]["declension"] == 8:
                answerending = "e"
            if nounList[currentprompt]["declension"] in [9, 10]:
                answerending = "imi"
            if nounList[currentprompt]["declension"] == 11:
                answerending = "umi"
            if nounList[currentprompt]["declension"] == 12:
                answerending = "iumi"
            if nounList[currentprompt]["declension"] == 13:
                answerending = "eniu"
            if nounList[currentprompt]["declension"] == 14:
                answerending = "erimi"

        # instrumental plural
        if currentcollocation == "instrumental" and not wordinsingular:
            if nounList[currentprompt]["declension"] in [1, 2]:
                answerending = "ais"
            if nounList[currentprompt]["declension"] in [3, 4, 5]:
                answerending = "iais"
            if nounList[currentprompt]["declension"] == 6:
                answerending = "omis"
            if nounList[currentprompt]["declension"] == 7:
                answerending = "iomis"
            if nounList[currentprompt]["declension"] == 8:
                answerending = "ėmis"
            if nounList[currentprompt]["declension"] in [9, 10]:
                answerending = "imis"
            if nounList[currentprompt]["declension"] == 11:
                answerending = "umis"
            if nounList[currentprompt]["declension"] == 12:
                answerending = "iais"
            if nounList[currentprompt]["declension"] == 13:
                answerending = "enimis"
            if nounList[currentprompt]["declension"] == 14:
                answerending = "erimis"

        # locative singular
        if currentcollocation == "locative" and wordinsingular:
            if nounList[currentprompt]["declension"] in [1, 2]:
                answerending = "e"
            if nounList[currentprompt]["declension"] in [3, 4, 5]:
                answerending = "yje"
            if nounList[currentprompt]["declension"] == 6:
                answerending = "oje"
            if nounList[currentprompt]["declension"] == 7:
                answerending = "ioje"
            if nounList[currentprompt]["declension"] == 8:
                answerending = "ėje"
            if nounList[currentprompt]["declension"] in [9, 10]:
                answerending = "yje"
            if nounList[currentprompt]["declension"] == 11:
                answerending = "uje"
            if nounList[currentprompt]["declension"] == 12:
                answerending = "iuje"
            if nounList[currentprompt]["declension"] == 13:
                answerending = "enyje"
            if nounList[currentprompt]["declension"] == 14:
                answerending = "eryje"

        # locative plural
        if currentcollocation == "locative" and not wordinsingular:
            if nounList[currentprompt]["declension"] in [1, 2]:
                answerending = "uose"
            if nounList[currentprompt]["declension"] in [3, 4, 5]:
                answerending = "iuose"
            if nounList[currentprompt]["declension"] == 6:
                answerending = "ose"
            if nounList[currentprompt]["declension"] == 7:
                answerending = "iose"
            if nounList[currentprompt]["declension"] == 8:
                answerending = "ėse"
            if nounList[currentprompt]["declension"] in [9, 10]:
                answerending = "yse"
            if nounList[currentprompt]["declension"] == 11:
                answerending = "uose"
            if nounList[currentprompt]["declension"] == 12:
                answerending = "iuose"
            if nounList[currentprompt]["declension"] == 13:
                answerending = "enyse"
            if nounList[currentprompt]["declension"] == 14:
                answerending = "eryse"

        # vocative singular
        if currentcollocation == "vocative" and wordinsingular:
            if nounList[currentprompt]["declension"] == 1:
                answerending = "e"
            if nounList[currentprompt]["declension"] == 2:
                answerending = "ai"
            if nounList[currentprompt]["declension"] == 3:
                answerending = "i"
            if nounList[currentprompt]["declension"] in [4, 5]:
                answerending = "y"
            if nounList[currentprompt]["declension"] == 6:
                answerending = "a"
            if nounList[currentprompt]["declension"] == 7:
                answerending = "ia"
            if nounList[currentprompt]["declension"] == 8:
                answerending = "e"
            if nounList[currentprompt]["declension"] in [9, 10]:
                answerending = "ie"
            if nounList[currentprompt]["declension"] == 11:
                answerending = "au"
            if nounList[currentprompt]["declension"] == 12:
                answerending = "iau"
            if nounList[currentprompt]["declension"] == 13:
                answerending = "enie"
            if nounList[currentprompt]["declension"] == 14:
                answerending = "erie"

        if currentcollocation == "vocative" and not wordinsingular:
            if nounList[currentprompt]["declension"] in [1, 2]:
                answerending = "ai"
            if nounList[currentprompt]["declension"] in [3, 4, 5]:
                answerending = "iai"
            if nounList[currentprompt]["declension"] == 6:
                answerending = "os"
            if nounList[currentprompt]["declension"] == 7:
                answerending = "ios"
            if nounList[currentprompt]["declension"] == 8:
                answerending = "ės"
            if nounList[currentprompt]["declension"] in [9, 10]:
                answerending = "ys"
            if nounList[currentprompt]["declension"] == 11:
                answerending = "ūs"
            if nounList[currentprompt]["declension"] == 12:
                answerending = "iai"
            if nounList[currentprompt]["declension"] == 13:
                answerending = "enys"
            if nounList[currentprompt]["declension"] == 14:
                answerending = "erys"

        if currentcollocation == "instrumental":
            preword = "su "
        else:
            preword = ""

        if currentcollocation == "nominative":
            currentcollocationLV = "nominatīvā"
        if currentcollocation == "genitive":
            currentcollocationLV = "ģenetīvā"
        if currentcollocation == "dative":
            currentcollocationLV = "datīvā"
        if currentcollocation == "accusative":
            currentcollocationLV = "akuzatīvā"
        if currentcollocation == "instrumental":
            currentcollocationLV = "instrumentālī"
        if currentcollocation == "locative":
            currentcollocationLV = "lokatīvā"
        if currentcollocation == "vocative":
            currentcollocationLV = "vokatīvā"

        # answer creation
        if wordList[currentprompt]["LT"][-1] == "d" and wordinsingular == True and wordList[currentprompt]["Ending"] in ["is", "ys", "ias"]:
            answersolution = preword + wordList[currentprompt]["LT"] + "ž" + answerending
        else:
            answersolution = preword + wordList[currentprompt]["LT"] + answerending

        if not hasguessed and currentscore != 0 and language == "EN":
            self.scoreLabel.configure(text=scoreTextEN.format(str(round(100*(currentscore / currentturn) ) ) ) )
        elif not hasguessed and currentscore != 0 and language == "LV":
            self.scoreLabel.configure(text=scoreTextLV.format(str(round(100*(currentscore / currentturn) ) ) ) )
        elif not hasguessed and currentscore == 0 and language == "EN":
            self.scoreLabel.configure(text=scoreTextEN.format("0"))
        elif not hasguessed and currentscore == 0 and language == "LV":
            self.scoreLabel.configure(text=scoreTextLV.format("0"))

        currentturn += 1
        hasguessed = False

        self.givenQuestion.grid(row=1, column=0)
        if language == "EN":
            self.givenQuestion.configure(text=currentcollocation + singularstring)
        elif language == "LV":
            self.givenQuestion.configure(text=currentcollocationLV + singularstringLV)

        self.givenWord.grid(row=0, column=0)
        self.givenWord.configure(text=currentword)

        if language == "EN":
            self.turnLabel.configure(text=turnTextEN.format(currentturn))
        elif language == "LV":
            self.turnLabel.configure(text=turnTextLV.format(currentturn))

        self.answerButton.grid(row=0, column=0)

        self.grade.grid_forget()
        self.noteText.grid_forget()
        self.noteText2.grid_forget()
        self.inputBox.delete(0, tk.END)
        self.nextButton.configure(text='NEXT')
        cananswer = True

    def answerShortcut(self, event):
        if event.keysym == "Return" and cananswer:
            self.answer()
        elif not cananswer and event.keysym == "Return":
            self.next()


class StartWindow():
    def __init__(self):

        global addnominative
        global addgenitive
        global adddative
        global addaccusative
        global addinstrumental
        global addlocative

        global allowsingular
        global allowplural

        global possiblecollocationssingle
        global possiblecollocationsplural

        self.window = tk.Tk()
        self.window.geometry("400x350")

        self.title_frame = tk.Frame(self.window, height=50, width=500, borderwidth=4, relief=tk.GROOVE)

        self.checkbox_frame = tk.Frame(self.window, height=600, width=700, borderwidth=4, relief=tk.SUNKEN)

        self.button_frame = tk.Frame(self.window, height=600, width=50, borderwidth=0, relief=tk.SUNKEN)

        self.titleLabel = tk.Label(self.title_frame, text="Customize your quiz", font=("Arial", 20))

        self.checkbox_frame.columnconfigure(0, weight=1)
        self.checkbox_frame.rowconfigure(0, weight=1)
        self.checkbox_frame.rowconfigure(1, weight=1)
        self.checkbox_frame.rowconfigure(2, weight=1)
        self.checkbox_frame.rowconfigure(3, weight=1)
        self.checkbox_frame.rowconfigure(4, weight=1)
        self.checkbox_frame.rowconfigure(5, weight=1)
        self.checkbox_frame.rowconfigure(6, weight=1)
        self.checkbox_frame.rowconfigure(7, weight=1)
        self.checkbox_frame.rowconfigure(8, weight=1)
        self.checkbox_frame.rowconfigure(9, weight=1)

        self.allowsingular = tk.BooleanVar()
        self.allowsingular.set(True)
        self.singular_check = tk.Checkbutton(self.checkbox_frame, text="Add singular", font=("Arial", 14), variable=self.allowsingular)
        self.singular_check.grid(row=0, column=0, sticky="W")

        self.allowplural = tk.BooleanVar()
        self.allowplural.set(True)
        self.plural_check = tk.Checkbutton(self.checkbox_frame, text="Add plural", font=("Arial", 14), variable=self.allowplural)
        self.plural_check.grid(row=1, column=0, sticky="W")

        self.spaceLabel = tk.Label(self.checkbox_frame, text="", font=("Arial", 14))
        self.spaceLabel.grid(row=2, column=0, sticky="W")

        self.addnominative = tk.BooleanVar()
        self.addnominative.set(True)
        self.nominative_check = tk.Checkbutton(self.checkbox_frame, text="Nominative case (only in plural)", font=("Arial", 14), variable=self.addnominative)
        self.nominative_check.grid(row=3, column=0, sticky="W")

        self.addgenitive = tk.BooleanVar()
        self.addgenitive.set(True)
        self.genitive_check = tk.Checkbutton(self.checkbox_frame, text="Genitive case", font=("Arial", 14), variable=self.addgenitive)
        self.genitive_check.grid(row=4, column=0, sticky="W")

        self.adddative = tk.BooleanVar()
        self.adddative.set(True)
        self.dative_check = tk.Checkbutton(self.checkbox_frame, text="Dative case", font=("Arial", 14), variable=self.adddative)
        self.dative_check.grid(row=5, column=0, sticky="W")

        self.addaccusative = tk.BooleanVar()
        self.addaccusative.set(True)
        self.accusative_check = tk.Checkbutton(self.checkbox_frame, text="Accusative case", font=("Arial", 14), variable=self.addaccusative)
        self.accusative_check.grid(row=6, column=0, sticky="W")

        self.addinstrumental = tk.BooleanVar()
        self.addinstrumental.set(True)
        self.instrumental_check = tk.Checkbutton(self.checkbox_frame, text="Instrumental case", font=("Arial", 14), variable=self.addinstrumental)
        self.instrumental_check.grid(row=7, column=0, sticky="W")

        self.addlocative = tk.BooleanVar()
        self.addlocative.set(True)
        self.locative_check = tk.Checkbutton(self.checkbox_frame, text="Locative case", font=("Arial", 14), variable=self.addlocative)
        self.locative_check.grid(row=8, column=0, sticky="W")

        self.addvocative = tk.BooleanVar()
        self.addvocative.set(True)
        self.vocative_check = tk.Checkbutton(self.checkbox_frame, text="Vocative case", font=("Arial", 14), variable=self.addvocative)
        self.vocative_check.grid(row=9, column=0, sticky="W")

        self.continue_button = tk.Button(self.button_frame, text="Continue", font=("Arial", 16), command=self.Continue_To_Quiz, width=8)
        self.continue_button.configure(height=9)

        self.language_button = tk.Button(self.button_frame, text="LV", font=("Arial", 16), command=self.Lang_Change, width=8)
        self.language_button.configure(height=3)

        self.titleLabel.pack()

        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.rowconfigure(1, weight=1)
        self.button_frame.rowconfigure(2, weight=1)
        self.button_frame.rowconfigure(3, weight=1)
        self.language_button.grid(row=0,column=0, padx=2, pady=2, sticky="we")
        self.continue_button.grid(row=1,column=0, rowspan=3, padx=2, pady=2)

        self.title_frame.pack(fill="x", side=tk.TOP)
        self.checkbox_frame.pack(fill="y", side=tk.LEFT)
        self.button_frame.pack(fill="y", side=tk.LEFT)

        self.window.mainloop()

    def Lang_Change(self):
        global language
        if language == "EN":
            language = "LV"

            self.titleLabel.configure(text="Pielāgot testu")

            self.language_button.configure(text="EN")
            self.continue_button.configure(text="Tālāk")

            self.singular_check.configure(text="Vienskaitli")
            self.plural_check.configure(text="Daudzskaitļi")

            self.nominative_check.configure(text="Nominatīvu (tikai daudzskaitļiem)")
            self.genitive_check.configure(text="Ģenitīvu")
            self.dative_check.configure(text="Datīvu")
            self.accusative_check.configure(text="Akuzatīvu")
            self.instrumental_check.configure(text="Instrumentāli")
            self.locative_check.configure(text="Lokatīvu")
            self.vocative_check.configure(text="Vokatīvu")

        else:
            language = "EN"

            self.titleLabel.configure(text="Customize your quiz")

            self.language_button.configure(text="LV", width=9)
            self.continue_button.configure(text="Continue", width=9)

            self.singular_check.configure(text="Singular")
            self.plural_check.configure(text="Plural")

            self.nominative_check.configure(text="Nominative case (only for plural)")
            self.genitive_check.configure(text="Genitive case")
            self.dative_check.configure(text="Dative case")
            self.accusative_check.configure(text="Accusative case")
            self.instrumental_check.configure(text="Instrumental case")
            self.locative_check.configure(text="Lokative case")
            self.vocative_check.configure(text="Vokative case")


    def Continue_To_Quiz(self):


        global addnominative
        global addgenitive
        global adddative
        global addaccusative
        global addinstrumental
        global addlocative

        global allowsingular
        global allowplural

        global possiblecollocationssingle
        global possiblecollocationsplural

        global launchQuiz

        if self.allowplural.get() == False and self.allowsingular.get() == False:
            self.allowplural.set(True)
            self.allowsingular.set(True)

        if self.addnominative.get() == False and self.addgenitive.get() == False and self.adddative.get() == False and self.addaccusative.get() == False and self.addinstrumental.get() == False and self.addlocative.get() == False and self.addvocative.get() == False:
            self.addnominative.set(True)
            self.addgenitive.set(True)
            self.adddative.set(True)
            self.addaccusative.set(True)
            self.addinstrumental.set(True)
            self.addlocative.set(True)
            self.addvocative.set(True)

        elif self.addnominative.get() == True and self.addgenitive.get() == False and self.adddative.get() == False and self.addaccusative.get() == False and self.addinstrumental.get() == False and self.addlocative.get() == False and self.addvocative.get() == False:
            self.allowsingular.set(False)
            self.allowplural.set(True)

        if self.allowsingular.get() == True:
            allowsingular = True

        if self.allowplural.get() == True:
            allowplural = True

        if self.addnominative.get() == True:
            possiblecollocationsplural.append("nominative")

        if self.addgenitive.get() == True:
            possiblecollocationssingle.append("genitive")
            possiblecollocationsplural.append("genitive")

        if self.adddative.get() == True:
            possiblecollocationssingle.append("dative")
            possiblecollocationsplural.append("dative")

        if self.addaccusative.get() == True:
            possiblecollocationssingle.append("accusative")
            possiblecollocationsplural.append("accusative")

        if self.addinstrumental.get() == True:
            possiblecollocationssingle.append("instrumental")
            possiblecollocationsplural.append("instrumental")

        if self.addlocative.get() == True:
            possiblecollocationssingle.append("locative")
            possiblecollocationsplural.append("locative")

        if self.addvocative.get() == True:
            possiblecollocationssingle.append("vocative")
            possiblecollocationsplural.append("vocative")

        launchQuiz = True

        self.window.destroy()


wordList = nounList

StartWindow()

if launchQuiz == True:
    QuizWindow()
