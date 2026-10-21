from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager

class vhod(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        label = Label(
            text='Добро пожаловать!',
            font_size='24sp',
            size_hint=(None, None),
            pos=(330, 400)
        )
        layout.add_widget(label)

        label_info1 = Label(
            text='Вход',
            font_size='18sp',
            size_hint=(None, None),
            pos=(320, 300)
        )
        layout.add_widget(label_info1)

        label_ent1 = Label(
            text='Имя пользователя',
            font_size='14sp',
            size_hint=(None, None),
            pos=(140, 220)
        )
        layout.add_widget(label_ent1)

        name_reg = TextInput(
            multiline=False,
            hint_text='Введите имя пользователя',
            size_hint=(None, None),
            size=(250, 40),
            pos=(260, 250)
        )
        layout.add_widget(name_reg)

        label_reg2 = Label(
            text='Введите пароль',
            font_size='14sp',
            size_hint=(None, None),
            pos=(140, 180)
        )
        layout.add_widget(label_reg2)

        pass_reg = TextInput(
            multiline=False,
            password=True,
            hint_text='Введите пароль',
            size_hint=(None, None),
            size=(250, 40),
            pos=(260, 210)
        )
        layout.add_widget(pass_reg)

        submit_btn = Button(
            text='Войти',
            size_hint=(None, None),
            size=(210, 30),
            pos=(260, 160)

        )
        layout.add_widget(submit_btn)

        btn_reg = Button(
            text='Регистрация',
            size_hint=(None, None),
            size=(210, 30),
            pos=(260, 120)
        )
        layout.add_widget(btn_reg)
        btn_reg.bind(on_press=self.open_reg_window)
        submit_btn.bind(on_press=self.open_main_window)

        self.add_widget(layout)
    def open_reg_window(self, instance):
        self.manager.current = "RegistrWindow"
    def open_main_window(self, instance):
        self.manager.current = "First_Window"


class RegistrWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        name_reg = TextInput(
            multiline=False,
            hint_text='Введите имя пользователя',
            size_hint=(None, None),
            size=(250, 40),
            pos=(260, 250)
        )
        layout.add_widget(name_reg)

        label_ent1 = Label(
            text='Имя пользователя',
            font_size='14sp',
            size_hint=(None, None),
            pos=(140, 220)
        )
        layout.add_widget(label_ent1)

        pass_reg = TextInput(
            multiline=False,
            password=True,
            hint_text='Введите пароль',
            size_hint=(None, None),
            size=(250, 40),
            pos=(260, 210)
        )
        layout.add_widget(pass_reg)

        label_reg2 = Label(
            text='Введите пароль',
            font_size='14sp',
            size_hint=(None, None),
            pos=(140, 180)
        )
        layout.add_widget(label_reg2)

        button_reg = Button(
            text='Зарегистрироваться',
            size_hint=(None, None),
            size=(210, 30),
            pos=(260, 160)
        )
        layout.add_widget(button_reg)

        reg_info = Label(
            text='Регистрация',
            font_size='18sp',
            size_hint=(None, None),
            pos=(320, 300)
        )
        layout.add_widget(reg_info)

        self.add_widget(layout)

class First_Window(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()
        main_screen_text = Label(
            text="Стройбат",
            font_size='28sp',
            size_hint=(None, None),
            pos=(340, 500)
        )
        layout.add_widget(main_screen_text)

        projects_btn = Button(
            text="Открыть список проектов",
            size_hint=(None, None),
            size=(200, 30),
            pos=(280, 300)
        )
        layout.add_widget(projects_btn)

        calc_btn = Button(
            text="Открыть калькулятор смет",
            size_hint=(None, None),
            size=(200, 30),
            pos=(280, 250)
        )
        layout.add_widget(calc_btn)




        exit_btn = Button(
            text="Выйти",
            size_hint=(None, None),
            size=(200, 30),
            pos=(280, 100)
        )
        layout.add_widget(exit_btn)

        projects_btn.bind(on_press=self.open_projects)
        calc_btn.bind(on_press=self.open_calc)
        exit_btn.bind(on_press=self.exit_app)
        self.add_widget(layout)

    def open_projects(self, instance):
        self.manager.current = "Projects"
    def open_calc(self, instance):
        self.manager.current = "Calculator"
    def exit_app(self, instance):
        App.get_running_app().stop()

class Projects(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        main_text = Label(
            text="Список текущих проектов",
            font_size='20sp',
            size_hint=(None, None),
            pos=(320, 500)
        )
        layout.add_widget(main_text)

        back_btn = Button(
            text="Назад",
            size_hint=(None, None),
            size=(100, 30),
            pos=(10, 500)
        )
        layout.add_widget(back_btn)
        back_btn.bind(on_press=self.get_back)
        self.add_widget(layout)

    def get_back(self, instance):
        self.manager.current = "First_Window"


class Calculator(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        main_text = Label(
            text='Калькулятор Смет',
            font_size='20sp',
            size_hint=(None, None),
            pos=(320, 500)
        )
        layout.add_widget(main_text)

        back_btn = Button(
            text="Назад",
            size_hint=(None, None),
            size=(100, 30),
            pos=(10, 500)
        )
        layout.add_widget(back_btn)
        back_btn.bind(on_press=self.get_back)


        self.add_widget(layout)

    def get_back(self, instance):
        self.manager.current = "First_Window"

class MainWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Stroybat(App):
    def build(self):
        manager = ScreenManager()
        manager.add_widget(vhod(name="vhod"))
        manager.add_widget(RegistrWindow(name="RegistrWindow"))
        manager.add_widget(First_Window(name="First_Window"))
        manager.add_widget(Projects(name="Projects"))
        manager.add_widget(Calculator(name="Calculator"))
        return manager


Stroybat().run()