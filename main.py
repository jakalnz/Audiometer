'''
Draw Audiogram App
July 2017 by Mike Sanders
'''


'''
TO DO:
    1. Change keyboard so that it keeps current window visible
    2. In Speech have Material [Spondee, CVC, HINT, MLV], Score Type [SDT, SRT,PRT,WRT, MCL, UCL], ?SNR, also comments section
    3b. for ART input have popup widget with roulette (default 90 +5), select present or noreponse or cancel passes info to
        a custom widget textinput and small label which shows elevated symbol or just type NR which is easier
    4. Report
    5. Geolocation https://github.com/geopy/geopy
    6. SF and Aided, fix icons
    '''

__version__ = '0.0.6'

from bisect import bisect_left
from itertools import izip as zip

from fpdf import FPDF
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
# from kivy.garden.roulette import Roulette, CyclicRoulette
from kivy.graphics import Color, Line, Point
from kivy.properties import ObjectProperty, DictProperty, NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.uix.actionbar import ActionBar
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

# Window.softinput_mode = 'pan'
Window.softinput_mode = 'below_target'

get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]


def takeClosest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before


# Make a Navigation Bar
class AudioNavigationBar(ActionBar):
    currentview = ObjectProperty()
    controlGroup = ObjectProperty()
    savedY = NumericProperty()
    linesButton = ObjectProperty()
    symbolButton = ObjectProperty()
    patientLabel = ObjectProperty()

    def generateAudioChart(self):
        # self.parent.parent.manager.get_screen('audio').currentAudioChart.export_to_png('tmp/audio.png')
        print 'in gen audio'
        sdpath = App.get_running_app().user_data_dir
        self.parent.parent.manager.get_screen('audio').currentAudioChart.export_to_png(sdpath + '/audio.png')
        # self.parent.parent.manager.get_screen('speech').speechAudioImage = sdpath + '/audio.png'
        self.parent.parent.manager.get_screen('speech').speechAudioID.source = sdpath + '/audio.png'

        print 'in gen audio'


    def goToSpeechScreen(self):
        # self.generateAudioChart()
        # self.parent.parent.manager.get_screen('speech').speechAudioID.reload()
        # self.parent.parent.manager.current = 'speech'

        print 'in speechscreen'
        self.generateAudioChart()
        #self.parent.parent.manager.get_screen('speech').updateSpeechAudioImage()
        self.parent.parent.manager.get_screen('speech').speechAudioID.reload()
        self.parent.parent.manager.current = 'speech'


    def changeWidget(self, selection):
        if selection is 'sym':
            print 'sym selected'
            self.parent.parent.manager.get_screen('audio').drawlineDrawer.disabled = True
            self.parent.parent.manager.get_screen('audio').drawlineDrawer.opacity = 0
            self.parent.parent.manager.get_screen('audio').control.opacity = 1
            self.parent.parent.manager.get_screen('audio').control.disabled = False
            self.parent.parent.manager.get_screen('audio').control.pos = (
                self.parent.parent.manager.get_screen('audio').control.parent.pos)
            App.get_running_app().audCtrlToggle = 'control'

        if selection is 'lin':
            print 'lin selected'

            self.parent.parent.manager.get_screen('audio').control.opacity = 0
            self.parent.parent.manager.get_screen('audio').control.disabled = True
            self.parent.parent.manager.get_screen('audio').drawlineDrawer.disabled = False
            self.parent.parent.manager.get_screen('audio').drawlineDrawer.opacity = 1
            self.parent.parent.manager.get_screen('audio').control.pos = (-1000, 0)

            App.get_running_app().audCtrlToggle = 'draw lines'

    pass


class NavigationBar(ActionBar):

    def generateAudioChart(self):
        sdpath = App.get_running_app().user_data_dir
        self.parent.parent.manager.get_screen('audio').currentAudioChart.export_to_png(sdpath + '/audio.png')
        self.parent.parent.manager.get_screen('speech').speechAudioID.source = sdpath + '/audio.png'
        print 'in gen audio'

    def goToAudioScreen(self):
        self.parent.parent.manager.current = 'audio'


    def goToSpeechScreen(self):
        print 'in speechscreen'
        self.generateAudioChart()
        #self.parent.parent.manager.get_screen('speech').updateSpeechAudioImage()

        self.parent.parent.manager.get_screen('speech').speechAudioID.reload()
        self.parent.parent.manager.current = 'speech'

        print 'init'


# Add the screens we need as subclasses


class PatientScreen(Screen):
    patientInput = ObjectProperty()
    pass


class AudioScreen(Screen):
    current_audiogram = ObjectProperty()
    currentAudioChart = ObjectProperty()
    drawlineDrawer = ObjectProperty()
    patientLabel = ObjectProperty()
    control = ObjectProperty()
    pass


class SpeechScreen(Screen):

    speechAudioImage = StringProperty()
    speechAudioImage = 'tmp/audio.png'
    #speechAudioImage = 'tmp/audio.png'
    speechAudioID = ObjectProperty()
    rightID = ObjectProperty()
    leftID = ObjectProperty()

    # def updateSpeechAudioImage(self):
    #     print 'updating speechAudioImage'
    #     self.speechAudioImage = App.get_running_app().user_data_dir + '/audio.png'
    #     print self.speechAudioImage

    pass


class ImmittanceScreen(Screen):
    tympImage = ObjectProperty()
    tympData = ObjectProperty()
    reflexImage = ObjectProperty()
    pass


class ReportScreen(Screen):
    def save_audiogram(self):
        sdpath = App.get_running_app().user_data_dir
        self.manager.get_screen('audio').current_audiogram.export_to_png(sdpath + '/audio.png')

    def makeAudiogramReportPDF(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(40, 10, 'Audiometry Results')

        sdpath = App.get_running_app().user_data_dir

        # get the patient information and put it into a cell
        name = self.manager.get_screen('patient').patientInput.patientName
        dob = self.manager.get_screen('patient').patientInput.patientDOB
        sex = self.manager.get_screen('patient').patientInput.patientSex
        filenumber = self.manager.get_screen('patient').patientInput.patientFile

        pdf.cell(40, 10, name[0] + ' ' + name[1])
        pdf.cell(40, 10, dob[0] + dob[1] + dob[2] + ' ' + sex + 'File: ' + filenumber)

        # get the test information from the audio screen
        transducer = self.manager.get_screen('audio').control.transducer.text
        reliability = self.manager.get_screen('audio').control.reliability.text
        test_type = self.manager.get_screen('audio').control.test_type.text
        print transducer
        print reliability
        print test_type

        #  insert the Audiogram Image
        # self.manager.get_screen('audio').current_audiogram.export_to_png(sdpath + '/audio.png')
        self.manager.get_screen('audio').currentAudioChart.export_to_png(sdpath + '/audio.png')
        pdf.image(sdpath + '/audio.png', x=10, y=20, w=130, h=100)

        #  create tmp images
        self.manager.get_screen('immittance').tympImage.tympDrawID.export_to_png(sdpath + '/tymp.png')
        self.manager.get_screen('immittance').reflexImage.export_to_png(sdpath + '/reflex.png')

        # insert the other images
        pdf.image(sdpath + '/tymp.png', x=10, y=150, w=60, h=50)
        pdf.image(sdpath + '/reflex.png', x=80, y=150, w=60, h=50)
        print sdpath

        pdf.output(sdpath + '/test.pdf', 'F')
    pass


def reCodeStringToButtonSF(currentSymbol):
    index = 'SF'
    value = [0, 0]

    if currentSymbol[0] == 'sf':
        index = 'SF'
        if currentSymbol[1] == '--':
            value = [1, currentSymbol[2]]  # [threshold, note]
        elif currentSymbol[1] == 'nr':
            value = [3, currentSymbol[2]]  # [no response, note]
    if currentSymbol[3] == 'ha':
        print 'got here'
        index = 'HA'
        if currentSymbol[4] == '--':
            value = [1, currentSymbol[5]]  # [threshold, note]
        elif currentSymbol[4] == 'nr':
            value = [3, currentSymbol[5]]  # [no response, note]

    output = [index, value]
    return output



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


def ButtonSFDictToString(value):
    #  reads input (ButtonDict) and returns a list of strings in the format:[SFHAcode]
    string_dict = {}

    start_key = {'SF': 'sf', 'HA': 'ha'}
    symbol_key = {0: '--', 1: '--', 3: 'nr'}  # no masking for SF

    for key in value:
        # determine if value is 0 and then put '--' in string
        if value[key][0] == 0:
            string_dict[key] = '--' + symbol_key[value[key][0]]
        else:
            string_dict[key] = start_key[key] + symbol_key[value[key][0]]

    SFHAcode = string_dict['SF'] + str(value['SF'][1]) + string_dict['HA'] + str(value['HA'][1])

    return SFHAcode

# buttons create


class AudioButton(Button):
    level = NumericProperty(0)
    bLev = ObjectProperty(None)
    airconduction = ObjectProperty(None)
    rightboneconduction = ObjectProperty(None)
    leftboneconduction = ObjectProperty(None)
    sflayout = ObjectProperty(None)
    mipmap = True

    # dictionary that stores contents, numeric values = [0-empty, 1-threshold, 2-maskedthreshold 3-threshnoresp, 4maskenoresp],[ 0-no note,1-note1, 2-note2, 3-note3]]
    contents = DictProperty({'LAC': [0, 0], 'RAC': [0, 0], 'LBC': [0, 0], 'RBC': [0, 0]})
    sfcontents = DictProperty({'SF': [0, 0], 'HA': [0, 0]})

    # create a method that on click reports position of button, gives level, gets frequencycolumn label
    def changeImage(self):

        if App.get_running_app().symbolType is 'nonSF':
            currentSymbol = App.get_running_app().controllerOutput
        else:
            currentSymbol = App.get_running_app().controllerSFOutput
        print currentSymbol

        if App.get_running_app().symbolType is 'nonSF':
            # adds the symbol to the Button dictProperty "contents"
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

        # for SF inputs...
        if App.get_running_app().symbolType is 'SF':
            new_content_list = reCodeStringToButtonSF(currentSymbol)
            print 'this is the SF content list: '
            print new_content_list
            self.sfcontents[new_content_list[0]] = new_content_list[1]
            symbolList = ButtonSFDictToString(self.sfcontents)
            print 'this is the symbolList: '
            print symbolList
            self.sflayout.source = 'Images/' + symbolList + '.png'
            # self.sflayout.source = 'Icons/' + 'SF' + '.png'

        # report which button was pressed
        print self.text  # references the level,
        print self.parent.parent.frequencyLabel  # references the frequency

        return



    def on_touch_down(self, touch):

        # are we drawing lines?
        if (self.collide_point(*touch.pos) and touch.is_double_tap is False
            and App.get_running_app().audCtrlToggle is not 'control'):  # self.parent.parent.parent.parent.parent.parent.parent.ids.drawlineDrawer.collapse is False):
            print 'in drawing lines method'
            # that is a long parent string isn't it!
            with self.parent.parent.parent.canvas:
                # logic to change initial colour and line
                if App.get_running_app().lineType == 'right':
                    Color(1, 0, 0, 1)
                    touch.ud['redline'] = Line(points=(self.center_x, self.center_y), width=1.1)
                elif App.get_running_app().lineType == 'left':
                    Color(0, 0, 1, 1)
                    touch.ud['blueline'] = Line(points=(self.center_x, self.center_y), dash_offset=5, width=1.1)
                elif App.get_running_app().lineType == 'sf':
                    Color(0.2, 0.2, 0.2, 1)
                    touch.ud['sfline'] = Line(points=(self.center_x, self.center_y), dash_offset=5, width=1.1)
                elif App.get_running_app().lineType == 'ha':
                    Color(0.4, 0.4, 0.4, 1)
                    touch.ud['haline'] = Line(points=(self.center_x, self.center_y), dash_offset=5, width=1.1)

                # adds the touch to the line Dict List
                App.get_running_app().linesDictList.append(touch.ud)

        # are we placing symbols?
        elif self.collide_point(*touch.pos) and not touch.is_double_tap:
            super(AudioButton, self).on_touch_down(touch)

        # are we doing a double tap
        if self.collide_point(*touch.pos) and touch.is_double_tap:
            if App.get_running_app().symbolType is 'nonSF':
                current_symbol = App.get_running_app().controllerOutput
                print current_symbol
                new_content_list = reCodeStringToButton(current_symbol)
                self.contents[new_content_list[0]] = [0, 0]  # removes item from list
                symbol_list = ButtonDictToString(self.contents)  # this is the

                self.airconduction.source = 'Images/' + symbol_list[1] + '.png'

                # only do BC for BC frequencies alternatively could have a second method for intermediate freq
                if self.parent.parent.frequencyLabel in ['125', '250', '500', '1000', '2000', '4000']:
                    self.rightboneconduction.source = 'Images/' + symbol_list[0] + '.png'
                    self.leftboneconduction.source = 'Images/' + symbol_list[2] + '.png'

            if App.get_running_app().symbolType is 'SF':
                current_symbol = App.get_running_app().controllerSFOutput
                print current_symbol
                new_content_list = reCodeStringToButtonSF(current_symbol)
                self.sfcontents[new_content_list[0]] = [0, 0]
                symbol_list = ButtonSFDictToString(self.sfcontents)
                self.sflayout.source = 'Images/' + symbol_list + '.png'

            print "popped"
        return

    def on_touch_move(self, touch):
        if (App.get_running_app().audCtrlToggle is not 'control'
            and self.collide_point(*touch.pos)):

            if App.get_running_app().lineType == 'right':
                if self.contents['RAC'][0] != 0:
                    touch.ud['redline'].points += [self.airconduction.center_x, self.center_y]

            if App.get_running_app().lineType == 'left':
                if self.contents['LAC'][0] != 0:
                    touch.ud['blueline'].points += [self.airconduction.center_x, self.center_y]

            if App.get_running_app().lineType == 'sf':
                if self.sfcontents['SF'][0] != 0:
                    touch.ud['sfline'].points += [self.sflayout.center_x, self.center_y]

            if App.get_running_app().lineType == 'ha':
                if self.sfcontents['HA'][0] != 0:
                    touch.ud['haline'].points += [self.sflayout.center_x, self.center_y]


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
    speechValuesListOfDict = ListProperty([{'Material': 'CVC', 'Type': 'SRT'}, {'Material': 'CVC', 'Type': 'SRT'},
                                           {'Material': 'CVC', 'Type': 'SRT'}, {'Material': 'CVC', 'Type': 'SRT'}])


class SpeechGraph(Widget):
    rightButtonID = ObjectProperty()
    leftButtonID = ObjectProperty()
    maskedToggleID = ObjectProperty()

    def updateMasking(self):
        if self.maskedToggleID.text == 'Unmasked':
            self.maskedToggleID.text = 'Masked'
        else:
            self.maskedToggleID.text = 'Unmasked'


class SpeechCanvas(Widget):
    floatLayerID = ObjectProperty()
    imagesList = ListProperty()
    current_touch = None
    double_tap = ListProperty()
    is_double_tap = BooleanProperty(False)
    mipmap = True
    tap_event = None

    def getX_hint_forLevel(self, level):
        levels = range(-10, 111, 5)
        origin_point = int(0.1 * self.width)
        end_point = int(origin_point + (self.width - .2 * self.width))
        axis_length = end_point - origin_point

        m = axis_length / 24

        new_x_points = [origin_point + i * m for i in range(0, 25)]
        # new_x_points = range(origin_point, end_point + 1, int(axis_length / 24))
        print new_x_points

        print
        # convert points to hints point/self.width

        level_hints = [float(x) / self.width for x in new_x_points]
        print level_hints

        the_rel_coord = level_hints[levels.index(level)] * self.width

        return int(the_rel_coord)

    def getY_hint_forScore(self, score):
        origin_point = (0.2 * self.height)
        end_point = int(origin_point + (self.height - .3 * self.height))
        axis_length = end_point - origin_point
        m = axis_length / 100.0

        output = origin_point + m * score

        return output

    def getX(self, value):
        origin_point = int(0.1 * self.width)
        end_point = int(origin_point + (self.width - .2 * self.width))
        axis_length = end_point - origin_point
        m = axis_length / 24

        new_x_points = [origin_point + i * m for i in range(0, 25)]
        # new_x_points = range(origin_point, end_point + 1, int(axis_length / 24))
        print('new_x_points:' + str(new_x_points))

        new_x = takeClosest(new_x_points, value)

        new_x = self.pos[0] + new_x
        return new_x

    def getY(self, value):
        origin_point = (0.2 * self.height)
        end_point = (origin_point + (self.height - .3 * self.height))
        axis_length = end_point - origin_point
        m = axis_length / 100.00

        # for create a for loop herre to replace the range
        new_y_points = [origin_point + i * m for i in range(0, 101, 5)]
        # new_y_points = range(int(origin_point), int(end_point) + 1, int(axis_length / 10))
        print new_y_points

        new_y = takeClosest(new_y_points, value)

        return new_y

    # def on_touch_up(self, touch):
    #     if Clock.get_time() - touch.time_start > .300:
    #         Clock.schedule_once(check, 0.3)
    #         self.dtap = false

    def on_touch_down(self, touch):
        self.double_tap = touch.pos
        self.current_touch = touch

        # if self.current_touch is not None:
        if self.is_double_tap is True:
            # Clock.unschedule(self.scheduled_func)
            self.tap_event.cancel()
            self.on_double_press(touch)
            self.is_double_tap = False
            # self.current_touch = None
        else:
            self.is_double_tap = True  # if singel press this is changed to false
            # self.current_touch = touch
            self.tap_event = Clock.schedule_once(self.on_single_press, 0.5)

    def on_single_press(self, dt):
        print('dt:' + str(dt))
        touch = self.current_touch
        ud = touch.ud
        ud['group'] = g = str(touch.uid)
        print touch.ud
        pointsize = 10
        #levels = range(-10, 111, 5)
        # print levels
        # self.getX()
        # ret = super(..., self).on_touch_down(touch)
        # print touch.pos
        # print self.to_widget(touch.pos[0], touch.pos[1], True)
        touch.pos = self.to_widget(touch.pos[0], touch.pos[1], True)
        print touch.pos
        # print self.pos
        # print self.to_window(*self.pos)
        # touch.x = touch.x - self.pos[0]
        # touch.y = touch.y - self.pos[1]

        # are we drawing lines?
        # if (self.collide_point(*touch.pos) and touch.is_double_tap is False
        if (self.collide_point(*touch.pos)
            and touch.y > (self.pos[1] + 0.05 * self.height)
            and touch.x > (self.pos[0] + 0.1 * self.height)):
            with self.canvas:

                mipmap = True
                # print ("input touch coord:" + str(touch.pos))
                snap_x = self.getX(touch.pos[0])
                snap_y = self.getY(touch.pos[1])
                print(snap_x, snap_y)

                # create a new tuple that contains the touch index and the ud
                # {[x,y], type, ud} but maybe check how the audiogram does it
                #self.imagesList.append([snap_x, snap_y, type, ])

                ud['lines'] = [Point(points=(snap_x, snap_y), source='Icons/RAC.png',
                                     pointsize=pointsize, group=g, mipmap=True)]

                self.imagesList.append([snap_x, snap_y, ud['lines']])  # creates a list of elements
                print self.imagesList
        # self.current_touch = None
        self.is_double_tap = False
        # print ud

    def on_double_press(self, touch):
        # if self.collide_point(*touch.pos) and touch.is_double_tap \
        #         and touch.y > (self.pos[1] + 0.05 * self.height) \
        #         and touch.x > (self.pos[0] + 0.1 * self.height):
        if self.collide_point(*touch.pos) and touch.y > (self.pos[1] + 0.05 * self.height) \
                and touch.x > (self.pos[0] + 0.1 * self.height):
            snap_x = self.getX(touch.x)
            snap_y = self.getY(touch.y)

            self.erase_point(snap_x, snap_y, self.imagesList)

            # self.current_touch = touch

    def erase_point(self, x, y, obj_list):
        print 'im out'
        for item in obj_list:
            if item[0] == x and item[1] == y:
                print 'im in'
                obj_list.remove(item)
                # with self.canvas:
                #     ud['lines'].remove(item[3])


                #obj_list.del(item)












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


class LineDrawer(Widget):
    drawLineDrawer = ObjectProperty()

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

    def clearSFLine(self):
        App.get_running_app().linesDictList = self.searchAndDestroy('sfline', App.get_running_app().linesDictList)

    def clearHALine(self):
        App.get_running_app().linesDictList = self.searchAndDestroy('haline', App.get_running_app().linesDictList)


class Controller(Widget):
    # select symbols and modifiers, print, and save,load dialog, erase, clear and line markup
    controlID = ObjectProperty(None)
    controllerNR = ObjectProperty(None)
    controllerNote = ObjectProperty(None)
    transducer = ObjectProperty(None)
    reliability = ObjectProperty()
    test_type = ObjectProperty()

    mipmap = True

    # opacity = 0
    # disabled = True


    def getControllerInput(self, symbol):
        # reinit the list on button press - but keep notes
        App.get_running_app().controllerOutput[0:3] = ['--', '-', '--']
        App.get_running_app().controllerOutput[4:7] = ['--', '-', '--']
        # create a seperate list for SF thresholds
        App.get_running_app().controllerSFOutput[0:2] = ['--', '--']
        App.get_running_app().controllerSFOutput[3:5] = ['--', '--']
        # default symbolType to non-SF
        App.get_running_app().symbolType = 'nonSF'
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
        elif symbol == 'sf-':
            App.get_running_app().controllerSFOutput[0] = 'sf'
            App.get_running_app().symbolType = 'SF'
        elif symbol == 'ha-':
            App.get_running_app().controllerSFOutput[3] = 'ha'
            App.get_running_app().symbolType = 'SF'

        # reset notes and NR widgets on new item select
        self.ids.controllerNR.state = 'normal'
        self.ids.controllerNote.text = 'No Note'

        print(App.get_running_app().controllerOutput)
        print(App.get_running_app().controllerSFOutput)


    def getControllerNote(self, note):

        # reinit controller Output note info
        App.get_running_app().controllerOutput[3] = '0'
        App.get_running_app().controllerOutput[7] = '0'

        App.get_running_app().controllerSFOutput[2] = '0'
        App.get_running_app().controllerSFOutput[5] = '0'
        if App.get_running_app().controllerOutput[0] != '--' or App.get_running_app().controllerOutput[4] != '--':
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
            print App.get_running_app().controllerSFOutput

        # for SF
        if App.get_running_app().controllerSFOutput[0] != '--' or App.get_running_app().controllerSFOutput[3] != '--':
            if App.get_running_app().controllerSFOutput[0] != '--':
                pos = 2
            else:
                pos = 5
            if note == 'No Note':
                App.get_running_app().controllerSFOutput[pos] = '0'
                print 'Note0'
            elif note == 'Note 1':
                App.get_running_app().controllerSFOutput[pos] = '1'
                print 'Note1'
            elif note == 'Note 2':
                App.get_running_app().controllerSFOutput[pos] = '2'
                print 'Note2'
            elif note == 'Note 3':
                App.get_running_app().controllerSFOutput[pos] = '3'
                print 'Note1'

    def getControllerNR(self, state):
        # Note NR state resets when the getControllerInput method is called
        no_response_text = '--'
        if state == 'normal':
            App.get_running_app().controllerOutput[2] = '--'
            App.get_running_app().controllerOutput[6] = '--'

            App.get_running_app().controllerSFOutput[1] = '--'
            App.get_running_app().controllerSFOutput[4] = '--'

        if state == 'down':
            no_response_text = 'nr'

        if App.get_running_app().controllerOutput[0] != '--':
            App.get_running_app().controllerOutput[2] = no_response_text
            App.get_running_app().controllerOutput[6] = '--'
        if App.get_running_app().controllerOutput[4] != '--':
            App.get_running_app().controllerOutput[6] = no_response_text
            App.get_running_app().controllerOutput[2] = '--'

        if App.get_running_app().controllerSFOutput[0] != '--':
            App.get_running_app().controllerSFOutput[1] = no_response_text
            App.get_running_app().controllerSFOutput[4] = '--'
        if App.get_running_app().controllerSFOutput[3] != '--':
            App.get_running_app().controllerSFOutput[4] = no_response_text
            App.get_running_app().controllerSFOutput[1] = '--'


class drawaudioApp(App):
    symbolType = StringProperty()
    controllerOutput = ListProperty(['--', '-', '--', '0', '--', '-', '--', '0'])
    controllerSFOutput = ListProperty(
        ['--', '--', '0', '--', '--', '0'])  # list def: ['sf', 'nr', '0', 'ha', 'nr', '0']
    lineType = StringProperty()
    clearRed = ObjectProperty()
    clearBlue = ObjectProperty()
    linesDictList = ListProperty()
    audCtrlToggle = StringProperty('control')

    def build(self):
        return

if __name__ == '__main__':
    drawaudioApp().run()
