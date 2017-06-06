'''Draw Audiogram App'''



from itertools import izip as zip

from kivy.app import App
from kivy.garden.roulette import Roulette, CyclicRoulette
from kivy.graphics import Color, Line
from kivy.properties import ObjectProperty, DictProperty, NumericProperty, StringProperty, ListProperty
from kivy.uix.actionbar import ActionBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]

sm = ScreenManager()


# Window.clearcolor = (1, 1, 1, 1)

# Make a Navigation Bar


class NavigationBar(ActionBar):
    pass


# Add the screens we need as subclasses


class PatientScreen(Screen):
    patientInput = ObjectProperty()

    pass


class AudioScreen(Screen):
    current_audiogram = ObjectProperty()
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
    pass


class ImmittanceScreen(Screen):
    pass


class ReportScreen(Screen):
    def save_audiogram(self):
        self.manager.get_screen('audio').current_audiogram.export_to_png('testpng.png')

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


class PickDate(BoxLayout):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PickDate, self).__init__(**kwargs)

        # let's add a Widget to this layout

        self.add_widget(CyclicRoulette(cycle=30, density=2.8, zero_indexed=False))
        self.add_widget(CyclicRoulette(cycle=12, density=2.8, zero_indexed=False))
        self.add_widget(Roulette(density=2.8, selected_value=1980))
        # self.add_widget(Roulette(density=4.0, selected_value=1980))



# buttons create
class AudioButton(Button):
    level = NumericProperty(0)
    bLev = ObjectProperty(None)
    airconduction = ObjectProperty(None)
    rightboneconduction = ObjectProperty(None)
    leftboneconduction = ObjectProperty(None)
    mipmap = True
    # ctex = ObjectProperty(None)
    # ltex = ObjectProperty(None)
    # rtex = ObjectProperty(None)

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
            print('my precious you found the parent')

            # with self.parent.parent.parent.parent.parent.parent.parent.parent.canvas:
            with self.parent.parent.parent.canvas:
                # logic to change initial colour and line
                if App.get_running_app().lineType == 'right':
                    Color(1, 0, 0, 1)
                    touch.ud['redline'] = Line(points=(self.center_x, self.center_y))
                elif App.get_running_app().lineType == 'left':
                    Color(0, 0, 1, 1)
                    touch.ud['blueline'] = Line(points=(self.center_x, self.center_y), dash_offset=5)

                App.get_running_app().linesDictList.append(touch.ud)
                print 'touch.ud'
                print touch.ud
            # so now I want to reference a draw method in the audiogramW canvas I think?
            # I want it to take thes touck inputs and then take the next collide on drag for a button containing either
            # a r or l AC symbol, and draw a line between them

        elif self.collide_point(*touch.pos) and not touch.is_double_tap:
            super(AudioButton, self).on_touch_down(touch)
            # print self.text  # references the level,
            # print self.parent.parent.frequencyLabel  #

            # print self.parent.parent.parent.parent.parent.parent.parent.parent.ids  # this is it



            print self.parent.parent.parent.parent.ids

            print '-' * 10
            print self.parent.parent.parent.parent.ids['audiogramW'].ids

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








class Controller(Widget):
    # select symbols and modifiers, print, and save,load dialog, erase, clear and line markup
    controlID = ObjectProperty(None)
    controllerNR = ObjectProperty(None)
    controllerNote = ObjectProperty(None)

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
