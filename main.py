# create a grid of buttons which if pressed will inform the paint class where to paint the symbol on the canvas
# but the symbol type (AC masked/unmasked) will be based on input from other buttons
# ill need 250,500,750,1000,2000,3000,4000,6000,8000 (9 buttons) by
# (-10,-5,0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110) (25 buttons)

# create an audiogram widget with 9 frequency children [propery] each frequency child to have 25 buttons [property]
# from PIL import Image
# create an audiogram widget with 9 frequency children [propery] each frequency child to have 25 buttons [property]
# from PIL import Image
from kivy.app import App
from kivy.core.image import Image
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty, DictProperty, NumericProperty, StringProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.widget import Widget

# from kivy.input import MotionEvent
Window.clearcolor = (1, 1, 1, 1)


# Method that takes list input from button and outputs a texture that applies to the image button

# Method for overlayingImages not usefult in this context
# def overlayImage(layer1,layer2):
#
#     out_image = Image.new("RGBA", layer1.size)
#     out_image = Image.alpha_composite(out_image, layer1)
#     out_image = Image.alpha_composite(out_image, layer2)
#
#     return out_image

# method to merge textures takes path input
def makeTexture(path1, path2):
    bkimg = Image(path1)
    frimg = Image(path2)
    #
    tex = Texture.create(size=bkimg.size, colorfmt='rgba')
    tex.blit_buffer(pbuffer=bkimg.texture.pixels, colorfmt='rgba')
    # tex.blit_buffer(pbuffer=frimg.texture.pixels)
    tex.blit_buffer(pbuffer=frimg.texture.pixels, colorfmt='rgba')
    tex.save("test.png")

    return tex


# buttons create
class AudioButton(Button):
    level = NumericProperty(0)
    bLev = ObjectProperty(None)
    airconduction = ObjectProperty(None)
    rightboneconduction = ObjectProperty(None)
    leftboneconduction = ObjectProperty(None)
    # ctex = ObjectProperty(None)
    # ltex = ObjectProperty(None)
    # rtex = ObjectProperty(None)

    # dictionary that stores contents, numeric values = 0-empty, 1-threshold, 2-maskedthreshold 2-noresp, 3-absent, 4-note1, 5-note2, 6-note3
    contents = DictProperty(
        {'LAC': 0, 'RAC': 0, 'MLAC': 0, 'MRAC': 0, 'LBC': 0, 'RBC': 0, 'MLBC': 0, 'MRBC': 0, 'SF': 0, 'AID': 0,
         'CI': 0})

    # create a method that on click reports position of button, gives level, gets frequencycolumn label
    def changeImage(self):
        self.airconduction.source = 'Images/' + ''.join(App.get_running_app().controllerOutput) + '.png'

        #
        #
        #
        # self.airconduction.source = overlayImage(Image.open('RAC.png'), Image.open('LAC.png'))
        print self.text  # references the level,
        print self.parent.parent.frequencyLabel  # references the frequency

        # if touch.is_double_tap:
        # self.airconduction.source = 'BLANK.png'
        return

    def changeImage2(self):
        self.parent.ctex = makeTexture('LAC.png', 'RBC.png')
        print self.text  # references the level,
        print self.parent.parent.frequencyLabel  # references the frequency
        print self.parent.ctex

        return

    #    def changeImage(self, instance, value):
    #     def doubleTap(self,touch):
    #         print('test')
    #         print('Touch:', touch)
    #         if touch.is_double_tap == True:
    #             self.airconduction.source = 'BLUE.png'




    # def on_double_tap(self,touch): #works but does everything
    #     print('test')
    #     print('Touch:', touch)
    #     if touch.is_double_tap == True:
    #         self.airconduction.source = 'BLUE.png'
    #
    #     #print('Button:', touch.button)
    #     super(AudioButton, self).on_touch_down(touch)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and touch.is_double_tap == False:
            # self.airconduction.source = 'RED.png'
            super(AudioButton, self).on_touch_down(touch)
            # print self.text  # references the level,
            # print self.parent.parent.frequencyLabel  #
        if self.collide_point(*touch.pos) and touch.is_double_tap == True:
            self.airconduction.source = 'EMPTY.png'
            print "popped"  # will need to implement a time delay
        return


class FrequencyColumn(Widget):
    frequencyLabel = StringProperty("")


class HalfFrequencyColumn(Widget):
    frequencyLabel = StringProperty("")


class AudiogramW(Widget):
    soll = NumericProperty(0)
    # def on_touch_up(self, touch):


# frequency column create
# class


class PatientDetails(Widget):
    # takes input for the patient database
    nameLabel = StringProperty("")
    surnameLabel = StringProperty("")
    dateOfBirth = StringProperty("")
    sexLabel = StringProperty("")


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

        print App.get_running_app().controllerOutput

        print(state)

        # get input from widgets and pass to the audiogram button widgets


class MainScreen(TabbedPanel):
    pass


class DrawAudioApp(App):
    symbolType = StringProperty
    controllerOutput = ListProperty(['--', '-', '--', '0', '--', '-', '--', '0'])

    def build(self):
        return MainScreen()
        # return AudiogramW()
        # return DatePicker()


if __name__ == '__main__':
    DrawAudioApp().run()
