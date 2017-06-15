'''Draw Audiogram App'''
'''
TO DO:
    1. Add Technique for Audiometry - Std, CPA, VRA, 
    2. In Speech have Material [Spondee, CVC, HINT, MLV], Score Type [SDT, SRT,PRT,WRT, MCL, UCL], ?SNR, also comments section
    3. Add images for ART
    3b. for ART input have popup widget with roulette (default 90 +5), select present or noreponse or cancel passes info to
        a custom widget textinput and small label which shows elevated symbol or just type NR which is easier
    4. Report
    '''


from itertools import izip as zip

from fpdf import FPDF
from kivy.app import App
# from kivy.garden.roulette import Roulette, CyclicRoulette
from kivy.graphics import Color, Line
from kivy.properties import ObjectProperty, DictProperty, NumericProperty, StringProperty, ListProperty
from kivy.uix.actionbar import ActionBar
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]


# Make a Navigation Bar


class NavigationBar(ActionBar):
    def generateAudioChart(self):
        self.parent.parent.manager.get_screen('audio').currentAudioChart.export_to_png('tmp/audio.png')
        print 'in gen audio'

    def goToSpeechScreen(self):
        self.generateAudioChart()
        self.parent.parent.manager.get_screen('speech').speechAudioID.reload()
        self.parent.parent.manager.current = 'speech'
    pass


# Add the screens we need as subclasses


class PatientScreen(Screen):
    patientInput = ObjectProperty()

    pass


class AudioScreen(Screen):
    current_audiogram = ObjectProperty()
    currentAudioChart = ObjectProperty()
    drawlineDrawer = ObjectProperty()
    patientLabel = ObjectProperty()

    # patientLabel.text = App.get_running_app().patientdetails
    # patientLabelText = StringProperty()




    def searchAndDestroy(self, akey, alist):
        for dict_element in alist:
            if akey in dict_element:
                dict_element[akey].points = []
        return alist

    def getLineType(self, input):
        App.get_running_app().lineType = input

    def clearRedLine(self):
        App.get_running_app().linesDictList = self.searchAndDestroy('redline', App.get_running_app().linesDictList)

    def clearBlueLine(self):
        App.get_running_app().linesDictList = self.searchAndDestroy('blueline', App.get_running_app().linesDictList)

    pass


class SpeechScreen(Screen):
    speechAudioImage = StringProperty()
    speechAudioImage = 'tmp/audio.png'
    speechAudioID = ObjectProperty()
    pass


class ImmittanceScreen(Screen):
    tympImage = ObjectProperty()
    tympData = ObjectProperty()
    reflexImage = ObjectProperty()

    pass


class ReportScreen(Screen):
    def save_audiogram(self):
        self.manager.get_screen('audio').current_audiogram.export_to_png('testpng.png')

    def makeAudiogramReportPDF(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(40, 10, 'Audiometry Results')

        # get the patient information and put it into a cell
        name = self.manager.get_screen('patient').patientInput.patientName
        dob = self.manager.get_screen('patient').patientInput.patientDOB
        sex = self.manager.get_screen('patient').patientInput.patientSex
        filenumber = self.manager.get_screen('patient').patientInput.patientFile

        # get the test information from the audio screen
        # test_type = self.manager.get_screen('audio').controlle


        #  insert the Audiogram Image
        pdf.image('tmp/audio.png', x=10, y=20, w=130, h=100)

        #  create tmp images
        self.manager.get_screen('immittance').tympImage.tympDrawID.export_to_png('tmp/tymp.png')
        self.manager.get_screen('immittance').reflexImage.export_to_png('tmp/reflex.png')

        # insert the other images
        pdf.image('tmp/tymp.png', x=10, y=150, w=60, h=50)
        pdf.image('tmp/reflex.png', x=80, y=150, w=60, h=50)

        pdf.output('test.pdf', 'F')

    pass


def reCodeStringToButton(currentSymbol):
    index = 'RAC'
    value = [0, 0]

    if currentSymbol[0] == 'ra':
        index = 'RAC'
    elif currentSymbol[0] == 'rb':
        index = 'RBC'
    elif currentSymbol[4] == 'la':
        index = 'LAC'
    elif currentSymbol[4] == 'lb':
        index = 'LBC'

    if currentSymbol[0][0] == 'r':
        if currentSymbol[1] == '-' and currentSymbol[2] == '--':  # threshold
            value = [1, currentSymbol[3]]
        elif currentSymbol[1] == 'm' and currentSymbol[2] == '--':  # maskedthreshold
            value = [2, currentSymbol[3]]
        elif currentSymbol[1] == '-' and currentSymbol[2] == 'nr':  # nrthreshold
            value = [3, currentSymbol[3]]
        elif currentSymbol[1] == 'm' and currentSymbol[2] == 'nr':  # nrmaskedthreshold
            value = [4, currentSymbol[3]]

    else:
        if currentSymbol[5] == '-' and currentSymbol[6] == '--':  # threshold
            value = [1, currentSymbol[7]]
        elif currentSymbol[5] == 'm' and currentSymbol[6] == '--':  # maskedthreshold
            value = [2, currentSymbol[7]]
        elif currentSymbol[5] == '-' and currentSymbol[6] == 'nr':  # nrthreshold
            value = [3, currentSymbol[7]]
        elif currentSymbol[5] == 'm' and currentSymbol[6] == 'nr':  # nrmaskedthreshold
            value = [4, currentSymbol[7]]

    output = [index, value]

    return output


def ButtonDictToString(value):
    '''reads input (ButtonDict) and returns a list of strings in the format:
     [[rightBCcode], [centreACcode], [leftBCcode]]
    '''

    # output base

    string_dict = {}

    start_key = {'RAC': 'ra', 'LAC': 'la', 'RBC': 'rb', 'LBC': 'lb'}
    symbol_key = {0: '---', 1: '---', 2: 'm--', 3: '-nr', 4: 'mnr'}

    for key in value:
        # determine if value is 0 and then put '--' in string
        if value[key][0] == 0:
            string_dict[key] = '--' + symbol_key[value[key][0]]
        else:
            string_dict[key] = start_key[key] + symbol_key[value[key][0]]

    RBCcode = string_dict['RBC'] + str(value['RBC'][1]) + '-----0'
    LBCcode = '-----0' + string_dict['LBC'] + str(value['LBC'][1])
    ACcode = string_dict['RAC'] + str(value['RAC'][1]) + string_dict['LAC'] + str(value['LAC'][1])

    return [RBCcode, ACcode, LBCcode]


# buttons create
class AudioButton(Button):
    level = NumericProperty(0)
    bLev = ObjectProperty(None)
    airconduction = ObjectProperty(None)
    rightboneconduction = ObjectProperty(None)
    leftboneconduction = ObjectProperty(None)
    mipmap = True

    # dictionary that stores contents, numeric values = [0-empty, 1-threshold, 2-maskedthreshold 3-threshnoresp, 4maskenoresp],[ 0-no note,1-note1, 2-note2, 3-note3]]
    contents = DictProperty({'LAC': [0, 0], 'RAC': [0, 0], 'LBC': [0, 0], 'RBC': [0, 0]})

    # create a method that on click reports position of button, gives level, gets frequencycolumn label
    def changeImage(self):
        currentSymbol = App.get_running_app().controllerOutput
        print currentSymbol


        # adds the symbol to the Button dictProperty "contents"
        # print reCodeStringToButton(currentSymbol)
        new_content_list = reCodeStringToButton(currentSymbol)
        print 'this is the content list: '
        print new_content_list
        self.contents[new_content_list[0]] = new_content_list[1]

        # decode contents
        symbolList = ButtonDictToString(self.contents)
        print 'this is the symbolList: '
        print symbolList

        self.airconduction.source = 'Images/' + symbolList[1] + '.png'

        # only do BC for BC frequencies alternatively could have a second method for intermediate freq
        if self.parent.parent.frequencyLabel in ['125', '250', '500', '1000', '2000', '4000']:
            self.rightboneconduction.source = 'Images/' + symbolList[0] + '.png'
            self.leftboneconduction.source = 'Images/' + symbolList[2] + '.png'


        print self.text  # references the level,
        print self.parent.parent.frequencyLabel  # references the frequency


        return



    def on_touch_down(self, touch):
        if (self.collide_point(*touch.pos) and touch.is_double_tap == False
            and self.parent.parent.parent.parent.parent.parent.parent.ids.drawlineDrawer.collapse == False):
            # that is a long parent string isn't it!
            with self.parent.parent.parent.canvas:
                # logic to change initial colour and line
                if App.get_running_app().lineType == 'right':
                    Color(1, 0, 0, 1)
                    touch.ud['redline'] = Line(points=(self.center_x, self.center_y))
                elif App.get_running_app().lineType == 'left':
                    Color(0, 0, 1, 1)
                    touch.ud['blueline'] = Line(points=(self.center_x, self.center_y), dash_offset=5)
                # adds the touch to the line Dict List
                App.get_running_app().linesDictList.append(touch.ud)

        elif self.collide_point(*touch.pos) and not touch.is_double_tap:
            super(AudioButton, self).on_touch_down(touch)
            # print self.text  # references the level,
            # print self.parent.parent.frequencyLabel  #
            # print self.parent.parent.parent.parent.ids
            #
            # print '-' * 10
            # print self.parent.parent.parent.parent.ids['audiogramW'].ids

        #     double tap
        if self.collide_point(*touch.pos) and touch.is_double_tap:
            currentSymbol = App.get_running_app().controllerOutput
            print currentSymbol
            new_content_list = reCodeStringToButton(currentSymbol)
            self.contents[new_content_list[0]] = [0, 0]  # removes item from list
            symbolList = ButtonDictToString(self.contents)  # this is the

            self.airconduction.source = 'Images/' + symbolList[1] + '.png'

            # only do BC for BC frequencies alternatively could have a second method for intermediate freq
            if self.parent.parent.frequencyLabel in ['125', '250', '500', '1000', '2000', '4000']:
                self.rightboneconduction.source = 'Images/' + symbolList[0] + '.png'
                self.leftboneconduction.source = 'Images/' + symbolList[2] + '.png'
            #self.airconduction.source = 'Icons\EMPTY.png'
            print "popped"  # will need to implement a time delay
        return

    def on_touch_move(self, touch):
        if (self.parent.parent.parent.parent.parent.parent.parent.ids.drawlineDrawer.collapse == False
            and self.collide_point(*touch.pos)):

            # add logic to change line colour if NR to clear
            if App.get_running_app().lineType == 'right':
                if self.contents['RAC'][0] != 0:
                    touch.ud['redline'].points += [self.airconduction.center_x, self.center_y]
                    # add logic to change the colour in here

            if App.get_running_app().lineType == 'left':
                if self.contents['LAC'][0] != 0:
                    # if self.contents['LAC'][0] == 3 or 4: # if values have NR then make pen clear

                    # touch.ud['blueline'].width = 0.0
                    touch.ud['blueline'].points += [self.airconduction.center_x, self.center_y]
                    # add logic to change the colour in here

                    # print self.ids

                    # touch.ud['line'].points += [touch.x, touch.y]

                    # def on_touch_up(self, touch):
                    #     if (self.parent.parent.parent.parent.parent.parent.parent.parent.ids.drawlineDrawer.collapse == False
                    #         and self.collide_point(*touch.pos)):
                    #         print str(self.text) + ' * ' + str(self.parent.parent.frequencyLabel) + ' was lifted'
                    #         touch.ud['line'].points += [self.airconduction.center_x, self.center_y]


class FrequencyColumn(Widget):
    frequencyLabel = StringProperty("")


class HalfFrequencyColumn(Widget):
    frequencyLabel = StringProperty("")


class AudiogramW(Widget):
    audiogramw = ObjectProperty()
    soll = NumericProperty(0)
    # def on_touch_up(self, touch):


# frequency column create
# class


class PatientDetails(Widget):
    # takes input for the patient database
    patientName = ListProperty(["", ""])
    patientDOB = ListProperty(['', '', ''])
    patientSex = StringProperty('')
    patientFile = StringProperty()

    def updatePatientDOB(self, dd='dd', mm='mm', yyyy='yyyy'):
        # print self.parent.parent.parent.ids #finding the parent
        if dd.isdigit():
            self.patientDOB[0] = 'D.O.B.: ' + str(dd)

        if mm.isdigit():
            self.patientDOB[1] = '/' + str(mm)

        if yyyy.isdigit():
            self.patientDOB[2] = '/' + str(yyyy)

    def addlabeltext(self):

        patientLabelText = (
        " Patient: " + str(self.patientName[0]) + ' ' + str(self.patientName[1]) + '   ' + self.patientSex + '   ' +
        self.patientDOB[0] + self.patientDOB[1] + self.patientDOB[2] + '      ' + self.patientFile)

        self.parent.parent.parent.ids.audio_screen.patientLabel.text = patientLabelText


class SpeechInput(Widget):
    speechInputID = ObjectProperty(None)


    # Material[Spondee, CVC, HINT, MLV], Score
    # Type[SDT, SRT, PRT, WRT, MCL, UCL], ?SNR, also
    #comments



class TympInput(Widget):
    tympInputID = ObjectProperty(None)
    tympDrawID = ObjectProperty(None)
    tympDrawCtrlID = ObjectProperty(None)



class TympDraw(Widget):
    def on_touch_down(self, touch):

        if self.parent.parent.ids.tympDrawCtrlID.selectedTymp is 'right':
            color = (1, 0, 0)
        elif self.parent.parent.ids.tympDrawCtrlID.selectedTymp is 'left':
            color = (0, 0, 1)
        else:
            color = (1, 1, 1, 0)
        with self.canvas:
            Color(*color)
            d = 30.
            # Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            if self.parent.parent.ids.tympDrawCtrlID.selectedTymp is 'right':
                touch.ud['tympRedline'] = Line(points=(touch.x, touch.y))
            elif self.parent.parent.ids.tympDrawCtrlID.selectedTymp is 'left':
                touch.ud['tympBlueline'] = Line(points=(touch.x, touch.y))

            App.get_running_app().linesDictList.append(touch.ud)

    def on_touch_move(self, touch):
        if self.parent.parent.ids.tympDrawCtrlID.selectedTymp is 'right':
            touch.ud['tympRedline'].points += [touch.x, touch.y]
        elif self.parent.parent.ids.tympDrawCtrlID.selectedTymp is 'left':
            touch.ud['tympBlueline'].points += [touch.x, touch.y]

    def clearLine(self):
        if self.parent.parent.ids.tympDrawCtrlID.selectedTymp is 'right':
            # App.get_running_app().linesDictList.append(touch.ud)
            App.get_running_app().linesDictList = self.searchAndDestroy('tympRedline',
                                                                        App.get_running_app().linesDictList)
            # touch.ud['tympRedline'].points = []
        elif self.parent.parent.ids.tympDrawCtrlID.selectedTymp is 'left':
            App.get_running_app().linesDictList = self.searchAndDestroy('tympBlueline',
                                                                        App.get_running_app().linesDictList)
            # touch.ud['tympBlueline'].points = []

    def searchAndDestroy(self, akey, alist):
        for dict_element in alist:
            if akey in dict_element:
                dict_element[akey].points = []
        return alist



class TympDrawCtrl(Widget):
    tympDrawCtrlID = ObjectProperty()
    selectedTymp = StringProperty('')


    pass


class ReflexInputR(Widget):
    reflexInputID = ObjectProperty(None)


class ReflexInputL(Widget):
    reflexInputID = ObjectProperty(None)


class ReflexType(DropDown):
    pass


class ReBut(Button):
    def __init__(self, **kwargs):
        super(ReBut, self).__init__(**kwargs)
        self.reflex_type_list = None

        self.reflex_type_list = ReflexType()
        # self.reflex_type_list = DropDown() #old code for text drop down
        # types = ['CNT', 'DNT', 'Present', 'Abnormal', 'Blank','Elevated']
        #
        #
        # for i in types:
        #     # print(i)
        #
        #     btn = Button(text=i, size_hint_y=None, height=50)
        #     btn.bind(on_release=lambda btn: self.reflex_type_list.select(btn.text))
        #     with btn.canvas:
        #         btn.rect = Rectangle(pos=self.pos, size = (self.height,self.height), source = 'Images/reflexes/'+i+'.png')
        #         btn.bind(pos=self.update_rect, size=self.update_rect)
        #     self.reflex_type_list.add_widget(btn)
        self.bind(on_release=self.reflex_type_list.open)
        self.background_normal = 'Images/reflexes/Blank.png'
        self.background_color = (1, 1, 1, 1)
        self.border = (1, 1, 1, 1)
        # self.reflex_type_list.bind(on_select=lambda instance, x: setattr(self, 'text', x))
        self.reflex_type_list.bind(on_select=lambda instance, x: setattr(self, 'background_normal', x))


class RePop(Popup):
    def __init__(self, **kwargs):
        self.caller = kwargs.get('caller')
        super(RePop, self).__init__(**kwargs)
        print self.caller

class Controller(Widget):
    # select symbols and modifiers, print, and save,load dialog, erase, clear and line markup
    controlID = ObjectProperty(None)
    controllerNR = ObjectProperty(None)
    controllerNote = ObjectProperty(None)
    mipmap = True

    def getControllerInput(self, symbol):
        # reinit the list on button press - but keep notes and NR
        App.get_running_app().controllerOutput[0:3] = ['--', '-', '--']
        App.get_running_app().controllerOutput[4:7] = ['--', '-', '--']
        # assign values to list
        if symbol == 'ra-':
            App.get_running_app().controllerOutput[0] = 'ra'
            App.get_running_app().controllerOutput[1] = '-'
        elif symbol == 'la-':
            App.get_running_app().controllerOutput[4] = 'la'
            App.get_running_app().controllerOutput[5] = '-'
        elif symbol == 'ram':
            App.get_running_app().controllerOutput[0] = 'ra'
            App.get_running_app().controllerOutput[1] = 'm'
        elif symbol == 'lam':
            App.get_running_app().controllerOutput[4] = 'la'
            App.get_running_app().controllerOutput[5] = 'm'
        elif symbol == 'rb-':
            App.get_running_app().controllerOutput[0] = 'rb'
            App.get_running_app().controllerOutput[1] = '-'
        elif symbol == 'lb-':
            App.get_running_app().controllerOutput[4] = 'lb'
            App.get_running_app().controllerOutput[5] = '-'
        elif symbol == 'rbm':
            App.get_running_app().controllerOutput[0] = 'rb'
            App.get_running_app().controllerOutput[1] = 'm'
        elif symbol == 'lbm':
            App.get_running_app().controllerOutput[4] = 'lb'
            App.get_running_app().controllerOutput[5] = 'm'

        # self.ids.nr.getControllerNR(self.ids.nr.getControllerNR.state)
        # reset notes and NR widgets on new item select
        self.ids.controllerNR.state = 'normal'
        self.ids.controllerNote.text = 'No Note'
        # App.get_running_app().symbolType = symbol
        # print(App.get_running_app().symbolType)
        print(App.get_running_app().controllerOutput)

        # will need to change this so I'm inputting to a list property at a certain position but yay!

    def getControllerNote(self, note):

        # reinit controller Output note info
        App.get_running_app().controllerOutput[3] = '0'
        App.get_running_app().controllerOutput[7] = '0'

        # set pos of list to be relapced based on l or r input
        if App.get_running_app().controllerOutput[0] != '--':
            pos = 3
        else:
            pos = 7

        if note == 'No Note':
            App.get_running_app().controllerOutput[pos] = '0'
            print 'Note0'
        elif note == 'Note 1':
            App.get_running_app().controllerOutput[pos] = '1'
            print 'Note1'
        elif note == 'Note 2':
            App.get_running_app().controllerOutput[pos] = '2'
            print 'Note2'
        elif note == 'Note 3':
            App.get_running_app().controllerOutput[pos] = '3'
            print 'Note1'

        print App.get_running_app().controllerOutput

    def getControllerNR(self, state):
        # Note NR state resets when the getControllerInput method is called
        no_response_text = '--'
        if state == 'normal':
            App.get_running_app().controllerOutput[2] = '--'
            App.get_running_app().controllerOutput[6] = '--'
        if state == 'down':
            no_response_text = 'nr'

        if App.get_running_app().controllerOutput[0] != '--':
            App.get_running_app().controllerOutput[2] = no_response_text
            App.get_running_app().controllerOutput[6] = '--'
        if App.get_running_app().controllerOutput[4] != '--':
            App.get_running_app().controllerOutput[6] = no_response_text
            App.get_running_app().controllerOutput[2] = '--'

            # print App.get_running_app().controllerOutput

            #print(state)

        # get input from widgets and pass to the audiogram button widgets




class DrawAudioApp(App):
    symbolType = StringProperty()
    controllerOutput = ListProperty(['--', '-', '--', '0', '--', '-', '--', '0'])
    lineType = StringProperty()
    clearRed = ObjectProperty()
    clearBlue = ObjectProperty()
    linesDictList = ListProperty()





    def build(self):
        return



if __name__ == '__main__':
    DrawAudioApp().run()
