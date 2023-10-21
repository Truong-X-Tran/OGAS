from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.core.window import Window

from kivy.config import Config

from genalgorithm import *
from cryptic import *
from openpyxl import *

Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '900')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView

import os
from kivy.uix.dropdown import DropDown


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class GenScreenApp(App):
    popup = ObjectProperty(None, allownone=True)
    textinput = ObjectProperty(None)
    dd_btn = ObjectProperty(None)

    def build(self):
        Window.size = (900, 900)
        self.layout = BoxLayout(padding=10, orientation='vertical')
        layout00 = BoxLayout(padding=10, orientation='horizontal')

        self.value = os.getcwd()
        self.val = Validator()

        layout10 = BoxLayout(padding=10, orientation='horizontal')
        layout100 = BoxLayout(orientation='horizontal')
        layout20 = BoxLayout(padding=10, orientation='horizontal')
        layout1 = BoxLayout(padding=10, orientation='horizontal')
        layout2 = BoxLayout(padding=10, orientation='horizontal')
        layout3 = BoxLayout(padding=10, orientation='horizontal')
        layout4 = BoxLayout(padding=10, orientation='horizontal')
        layout5 = BoxLayout(padding=10, orientation='horizontal')
        layout6 = BoxLayout(padding=10, orientation='horizontal')
        self.layout7 = BoxLayout(padding=10, orientation='horizontal')
        self.layout8 = BoxLayout(padding=10, orientation='horizontal')
        layout9 = BoxLayout(padding=10, orientation='horizontal')
        self.lbl10 = Label(text="Input File")
        layout10.add_widget(self.lbl10)
        self.txt_inputfile = TextInput(text='AbIPP-Combined-1.xlsx', multiline=False)
        btn_load = Button(text="Load")
        btn_load.bind(on_release=self._create_popup)
        layout100.add_widget(self.txt_inputfile)
        layout100.add_widget(btn_load)
        layout10.add_widget(layout100)

        self.lbl20 = Label(text="Output File")
        layout20.add_widget(self.lbl20)
        self.txt_outputfile = TextInput(text='GA_Output.xlsx', multiline=False)
        layout20.add_widget(self.txt_outputfile)

        self.lbl1 = Label(text="Population size")
        layout1.add_widget(self.lbl1)
        self.txt_pop_size = TextInput(text='200', multiline=False)
        layout1.add_widget(self.txt_pop_size)
        self.lbl2 = Label(text="# of generations")
        layout2.add_widget(self.lbl2)
        self.txt_numiter = TextInput(text='400', multiline=False)
        layout2.add_widget(self.txt_numiter)
        self.lbl3 = Label(text="Mutation Rate")
        layout3.add_widget(self.lbl3)
        self.txt_mutation = TextInput(text='0.5', multiline=False)
        layout3.add_widget(self.txt_mutation)
        self.lbl4 = Label(text="Tournament Size")
        layout4.add_widget(self.lbl4)
        self.txt_tournament = TextInput(text='2', multiline=False)
        layout4.add_widget(self.txt_tournament)

        self.lbl6 = Label(text="Lowest Score")
        layout6.add_widget(self.lbl6)

        drop_main_low = DropDown()
        self.btn_drop_main_low = Button(text='4', size_hint=(1, 1))

        for rank_value in range(10):
            btn = Button(text=str(rank_value), size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: drop_main_low.select(btn.text))
            drop_main_low.add_widget(btn)

        self.btn_drop_main_low.bind(on_release=drop_main_low.open)
        drop_main_low.bind(on_select=lambda instance, x: setattr(self.btn_drop_main_low, 'text', x))
        layout6.add_widget(self.btn_drop_main_low)


        self.lbl6 = Label(text="Highest Score")
        layout6.add_widget(self.lbl6)
        self.txt_rank_range = TextInput(text='0-10', multiline=False)

        drop_main_high = DropDown()
        self.btn_drop_main_high = Button(text='9', size_hint=(1, 1))

        for rank_value in range(10):
            btn = Button(text=str(rank_value), size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: drop_main_high.select(btn.text))
            drop_main_high.add_widget(btn)

        self.btn_drop_main_high.bind(on_release=drop_main_high.open)
        drop_main_high.bind(on_select=lambda instance, x: setattr(self.btn_drop_main_high, 'text', x))
        layout6.add_widget(self.btn_drop_main_high)

        # layout6.add_widget(self.txt_rank_range)


        self.try_diff_scores = False
        checkbox_diff = CheckBox()
        checkbox_diff.bind(active=self.on_checkbox_diff_active)
        self.lbl9 = Label(text="Try multiple range of scores")
        layout00.add_widget(self.lbl9)
        layout00.add_widget(checkbox_diff)



        self.lbl7 = Label(text="Parent 2 Low")
        self.layout7.add_widget(self.lbl7)
        self.txt_rank_range_parent1 = TextInput(text='0-4', multiline=False)

        drop_p1_low = DropDown()
        self.btn_drop_p1_low = Button(text='0', size_hint=(1, 1))

        for rank_value in range(10):
            btn = Button(text=str(rank_value), size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: drop_p1_low.select(btn.text))
            drop_p1_low.add_widget(btn)

        self.btn_drop_p1_low.bind(on_release=drop_p1_low.open)
        drop_p1_low.bind(on_select=lambda instance, x: setattr(self.btn_drop_p1_low, 'text', x))
        self.layout7.add_widget(self.btn_drop_p1_low)


        self.lbl7 = Label(text="Parent 2 High")
        self.layout7.add_widget(self.lbl7)
        drop_p1_high = DropDown()
        self.btn_drop_p1_high = Button(text='9', size_hint=(1, 1))

        for rank_value in range(10):
            btn = Button(text=str(rank_value), size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: drop_p1_high.select(btn.text))
            drop_p1_high.add_widget(btn)

        self.btn_drop_p1_high.bind(on_release=drop_p1_high.open)
        drop_p1_high.bind(on_select=lambda instance, x: setattr(self.btn_drop_p1_high, 'text', x))
        self.layout7.add_widget(self.btn_drop_p1_high)

        # self.layout7.add_widget(self.txt_rank_range_parent1)
        # self.lbl8 = Label(text="Parent 2 Rank Range")
        # self.layout8.add_widget(self.lbl8)
        # self.txt_rank_range_parent2 = TextInput(text='4-9', multiline=False)
        # self.layout8.add_widget(self.txt_rank_range_parent2)
        self.lbl5 = Label(text="License Key")
        layout5.add_widget(self.lbl5)
        self.txt_license = TextInput(text=self.val.password, multiline=False)
        layout5.add_widget(self.txt_license)
        self.layout.add_widget(layout10)
        self.layout.add_widget(layout20)
        self.layout.add_widget(layout1)
        self.layout.add_widget(layout2)
        self.layout.add_widget(layout3)
        self.layout.add_widget(layout4)
        self.layout.add_widget(layout6)
        self.layout.add_widget(layout00)
        # self.layout.add_widget(self.layout7)
        # self.layout.add_widget(self.layout8)
        self.layout.add_widget(layout5)
        btn1 = Button(text="Process")
        btn1.bind(on_press=self.buttonClicked)

        self.novelty = False
        checkbox = CheckBox()
        checkbox.bind(active=self.on_checkbox_active)
        self.lbl9 = Label(text="Use Novelty")
        layout9.add_widget(self.lbl9)
        layout9.add_widget(checkbox)
        self.layout.add_widget(layout9)
        self.layout.add_widget(btn1)
        return self.layout

    def buttonClicked(self, btn):
        if not self.val.is_valid_password(self.txt_license.text):
            exit()

        p1_rank_range = self.btn_drop_main_low.text + '-' + self.btn_drop_main_high.text
        p2_rank_range = p1_rank_range

        if self.try_diff_scores:
            p2_rank_range = self.btn_drop_p1_low.text + '-' + self.btn_drop_p1_high.text

        rank_range = '0-9'
        ga = GenAlgorithm(self.txt_inputfile.text, self.txt_outputfile.text, self.txt_pop_size.text,
            self.txt_numiter.text, self.txt_mutation.text, self.txt_tournament.text,
            rank_range, self.novelty,
            p1_rank_range, p2_rank_range)

        result = ga.apply_gen_algorithm()
        layout = BoxLayout(orientation='vertical')
        op_text = 'Distinct Salts: ' + str(result['salts']) + \
                '\nDistinct Precipitants: ' + str(result['precipitants']) + \
                '\nDistinct Families: ' + str(result['distinct_families']) + \
                '\nTop Score: ' + str(result['top_score']) + \
                '\nTop 10 Mean Score: ' + str(result['mean_score_top10']) + \
                '\nTop Salts: ' + ", ".join(result['salts_scores_avg'].keys()) + \
                '\nTop Precipitants: ' + ", ".join(result['precipitants_scores_avg'].keys())
        layout.add_widget(Label(text=op_text))
        popup = Popup(title='Done', content=layout, size_hint=(None, None), size=(700, 200))
        popup.open()

    def on_checkbox_diff_active(self, checkbox, value):
        if value:
            print('The checkbox', checkbox, 'is active')
            self.try_diff_scores = True
            self.layout.add_widget(self.layout7, 3)
        else:
            print('The checkbox', checkbox, 'is inactive')
            self.try_diff_scores = False
            self.layout.remove_widget(self.layout7)


    def on_checkbox_active(self, checkbox, value):
        if value:
            print('The checkbox', checkbox, 'is active')
            self.novelty = True
        else:
            print('The checkbox', checkbox, 'is inactive')
            self.novelty = False

    def _dismiss(self, *largs):
        if self.textinput:
            self.textinput.focus = False
        if self.popup:
            self.popup.dismiss()
        self.popup = None

    def _validate(self, instance):
        self._dismiss()
        value = self.textinput.selection

        if not value:
            return

        self.value = os.path.realpath(value[0])
        self.txt_inputfile.text = self.value
        print self.value

    def _create_popup(self, instance):
        # create popup layout
        content = BoxLayout(orientation='vertical', spacing=5)
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(
            title="Load Input File", content=content, size_hint=(None, 0.9),
            width=popup_width)

        # create the filechooser
        self.textinput = textinput = FileChooserListView(
            path=self.value, size_hint=(1, 1), dirselect=True)
        textinput.bind(on_path=self._validate)
        self.textinput = textinput

        # construct the content
        content.add_widget(textinput)

        # 2 buttons are created for accept or cancel the current value
        btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
        btn = Button(text='Ok')
        btn.bind(on_release=self._validate)
        btnlayout.add_widget(btn)
        btn = Button(text='Cancel')
        btn.bind(on_release=self._dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)

        # all done, open the popup !
        popup.open()

    def load(self, path, filename):
        print path, filename
        # self.text_input.text = stream.read()


GenScreenApp().run()


# ga = GenAlgorithm("AbIPP-Combined-1.xlsx", 'GA-Output.xlsx', 200, 400, 0.5, 2)
# ga.apply_gen_algorithm()
# ga.helper.columns['C1_Cation']
# ga.get_rank_of_reagent(4.5, ReagentType.PH)
# ga.get_rank_of_reagent('LITHIUM SULFATE', ReagentType.CHEMICAL)
# ga.get_rank_of_reagent('TRISODIUM CITRATE', ReagentType.CHEMICAL)
# ga.get_rank_of_reagent('AMMONIUM1 PHOSPHATE', ReagentType.CHEMICAL)
# ga.get_rank_of_reagent('AMMONIUM2 CITRATE', ReagentType.CHEMICAL)




# ga.get_population_from_file()
# print([r.name for r in ga.old_population.cocktails[1].candidate])

# print(ga.old_population)
