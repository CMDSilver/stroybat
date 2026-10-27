from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.spinner import Spinner
from threading import Thread
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from api_client import api, APIError



class vhod(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        label = Label(
            text='Добро пожаловать!',
            font_size='24sp',
            size_hint=(0.9, 0.10),
            pos_hint={'center_x': 0.5, 'top': 0.96}
        )
        layout.add_widget(label)

        label_info1 = Label(
            text='Вход',
            font_size='18sp',
            size_hint=(0.9, 0.07),
            pos_hint={'center_x': 0.5, 'top': 0.84}
        )
        layout.add_widget(label_info1)

        label_ent1 = Label(
            text='Имя пользователя',
            font_size='14sp',
            size_hint=(0.82, 0.05),
            pos_hint={'center_x': 0.5, 'top': 0.75}
        )
        layout.add_widget(label_ent1)

        self.name_reg = TextInput(
            multiline=False,
            hint_text='Введите имя пользователя',
            size_hint=(0.82, 0.07),
            pos_hint={'center_x': 0.5, 'top': 0.69}
        )
        layout.add_widget(self.name_reg)

        label_reg2 = Label(
            text='Введите пароль',
            font_size='14sp',
            size_hint=(0.82, 0.05),
            pos_hint={'center_x': 0.5, 'top': 0.59}
        )
        layout.add_widget(label_reg2)

        self.pass_reg = TextInput(
            multiline=False,
            password=True,
            hint_text='Введите пароль',
            size_hint=(0.82, 0.07),
            pos_hint={'center_x': 0.5, 'top': 0.53}
        )
        layout.add_widget(self.pass_reg)

        self.submit_btn = Button(
            text='Войти',
            size_hint=(0.72, 0.07),
            pos_hint={'center_x': 0.5, 'top': 0.42}
        )
        layout.add_widget(self.submit_btn)

        btn_reg = Button(
            text='Регистрация',
            size_hint=(0.72, 0.07),
            pos_hint={'center_x': 0.5, 'top': 0.32}
        )
        layout.add_widget(btn_reg)

        btn_reg.bind(on_press=self.open_reg_window)
        self.submit_btn.bind(on_press=self.login)

        self.message = Label(
            text="",
            font_size="14sp",
            size_hint=(0.9, 0.08),
            pos_hint={"center_x": 0.5, "top": 0.22}
        )
        layout.add_widget(self.message)



        self.add_widget(layout)

    def open_reg_window(self, instance):
        self.manager.current = "RegistrWindow"

    def login(self, instance):
        username = self.name_reg.text.strip()
        password = self.pass_reg.text

        if not username or not password:
            self.message.text = "Введите логин и пароль"
            return

        self.submit_btn.disabled = True
        self.message.text = "Выполняется вход..."

        Thread(
            target=self._login_request,
            args=(username, password),
            daemon=True
        ).start()

    def _login_request(self, username, password):
        try:
            user = api.login(username, password)

            Clock.schedule_once(
                lambda dt: self._login_success(user)
            )

        except Exception as error:
            message = str(error)

            Clock.schedule_once(
                lambda dt: self._login_error(message)
            )

    def _login_success(self, user):
        self.submit_btn.disabled = False
        self.message.text = ""

        # Сохраняем данные вошедшего пользователя для создания задач.
        app = App.get_running_app()
        app.current_user = user
        app.current_username = self.name_reg.text.strip()

        self.manager.current = "First_Window"

    def _login_error(self, message):
        self.submit_btn.disabled = False
        self.message.text = f"Ошибка входа: {message}"



class RegistrWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        reg_info = Label(
            text='Регистрация',
            font_size='22sp',
            size_hint=(0.9, 0.09),
            pos_hint={'center_x': 0.5, 'top': 0.90}
        )
        layout.add_widget(reg_info)

        label_ent1 = Label(
            text='Имя пользователя',
            font_size='14sp',
            size_hint=(0.82, 0.05),
            pos_hint={'center_x': 0.5, 'top': 0.78}
        )
        layout.add_widget(label_ent1)

        # Сохраняем поля в self, чтобы обращаться к ним из методов
        self.name_reg = TextInput(
            multiline=False,
            hint_text='Введите имя пользователя',
            size_hint=(0.82, 0.07),
            pos_hint={'center_x': 0.5, 'top': 0.72}
        )
        layout.add_widget(self.name_reg)

        label_reg2 = Label(
            text='Введите пароль',
            font_size='14sp',
            size_hint=(0.82, 0.05),
            pos_hint={'center_x': 0.5, 'top': 0.62}
        )
        layout.add_widget(label_reg2)

        self.pass_reg = TextInput(
            multiline=False,
            password=True,
            hint_text='Введите пароль',
            size_hint=(0.82, 0.07),
            pos_hint={'center_x': 0.5, 'top': 0.56}
        )
        layout.add_widget(self.pass_reg)

        self.button_reg = Button(
            text='Зарегистрироваться',
            size_hint=(0.82, 0.08),
            pos_hint={'center_x': 0.5, 'top': 0.43}
        )
        self.button_reg.bind(on_press=self.register)
        layout.add_widget(self.button_reg)

        self.message = Label(
            text='',
            font_size='14sp',
            size_hint=(0.9, 0.08),
            pos_hint={'center_x': 0.5, 'top': 0.32}
        )
        layout.add_widget(self.message)

        back_btn = Button(
            text='Назад ко входу',
            size_hint=(0.65, 0.07),
            pos_hint={'center_x': 0.5, 'top': 0.18}
        )
        back_btn.bind(
            on_press=lambda instance:
            setattr(self.manager, 'current', 'vhod')
        )
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def register(self, instance):
        username = self.name_reg.text.strip()
        password = self.pass_reg.text

        if not username or not password:
            self.message.text = 'Введите имя пользователя и пароль'
            return

        self.button_reg.disabled = True
        self.message.text = 'Выполняется регистрация...'

        Thread(
            target=self._register_request,
            args=(username, password),
            daemon=True
        ).start()

    def _register_request(self, username, password):
        try:
            user = api.create_user(
                username=username,
                password=password
            )

            Clock.schedule_once(
                lambda dt: self._register_success(user)
            )

        except Exception as error:
            message = str(error)

            Clock.schedule_once(
                lambda dt: self._register_error(message)
            )

    def _register_success(self, user):
        self.button_reg.disabled = False
        self.name_reg.text = ''
        self.pass_reg.text = ''

        login_screen = self.manager.get_screen('vhod')
        login_screen.message.text = (
            'Аккаунт создан. Теперь войдите.'
        )

        self.manager.current = 'vhod'

    def _register_error(self, message):
        self.button_reg.disabled = False
        self.message.text = f'Ошибка регистрации: {message}'



class First_Window(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        main_screen_text = Label(
            text="Стройбат",
            font_size='28sp',
            size_hint=(0.9, 0.12),
            pos_hint={'center_x': 0.5, 'top': 0.90}
        )
        layout.add_widget(main_screen_text)

        projects_btn = Button(
            text="Открыть список проектов",
            size_hint=(0.84, 0.09),
            pos_hint={'center_x': 0.5, 'top': 0.65}
        )
        layout.add_widget(projects_btn)

        calc_btn = Button(
            text="Открыть калькулятор смет",
            size_hint=(0.84, 0.09),
            pos_hint={'center_x': 0.5, 'top': 0.51}
        )
        layout.add_widget(calc_btn)

        exit_btn = Button(
            text="Выйти",
            size_hint=(0.65, 0.08),
            pos_hint={'center_x': 0.5, 'top': 0.20}
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


class CreateProject(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Сопоставляем имя руководителя с его ID
        self.manager_ids = {}

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        layout.add_widget(Label(
            text="Создание проекта",
            font_size="24sp",
            size_hint_y=0.12
        ))

        self.name_input = TextInput(
            hint_text="Название проекта",
            multiline=False,
            size_hint_y=0.09
        )
        layout.add_widget(self.name_input)

        self.description_input = TextInput(
            hint_text="Описание проекта",
            multiline=True,
            size_hint_y=0.16
        )
        layout.add_widget(self.description_input)

        self.status_spinner = Spinner(
            text="Новый",
            values=(
                "Новый",
                "В работе",
                "Приостановлен",
                "Завершён"
            ),
            size_hint_y=0.09
        )
        layout.add_widget(self.status_spinner)

        self.manager_spinner = Spinner(
            text="Загрузка пользователей...",
            values=(),
            size_hint_y=0.09
        )
        layout.add_widget(self.manager_spinner)

        self.message = Label(
            text="Выберите руководителя проекта",
            size_hint_y=0.12
        )
        layout.add_widget(self.message)

        self.save_btn = Button(
            text="Создать проект",
            size_hint_y=0.10
        )
        self.save_btn.bind(on_press=self.save_project)
        layout.add_widget(self.save_btn)

        back_btn = Button(
            text="Назад к проектам",
            size_hint_y=0.10
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def on_enter(self, *args):
        self.load_users()

    def load_users(self):
        self.manager_spinner.text = "Загрузка пользователей..."
        self.manager_spinner.values = ()
        self.save_btn.disabled = True

        Thread(
            target=self._fetch_users,
            daemon=True
        ).start()

    def _fetch_users(self):
        try:
            users = api.get_users()
            Clock.schedule_once(
                lambda dt: self._show_users(users)
            )
        except Exception as error:
            message = str(error)
            Clock.schedule_once(
                lambda dt: self._users_error(message)
            )

    def _show_users(self, users):
        self.manager_ids.clear()
        options = []

        for user in users:
            user_id = user.get("id")

            if user_id is None:
                continue

            name = (
                user.get("full_name")
                or user.get("username")
                or f"Пользователь {user_id}"
            )

            option = f"{user_id} — {name}"
            self.manager_ids[option] = user_id
            options.append(option)

        self.manager_spinner.values = options

        if options:
            self.manager_spinner.text = options[0]
            self.save_btn.disabled = False
            self.message.text = (
                f"Загружено пользователей: {len(options)}"
            )
        else:
            self.manager_spinner.text = "Нет пользователей"
            self.message.text = (
                "Сначала добавьте пользователя в базу данных"
            )

    def _users_error(self, message):
        self.manager_spinner.text = "Ошибка загрузки"
        self.message.text = message
        self.save_btn.disabled = True

    def save_project(self, instance):
        name = self.name_input.text.strip()
        description = self.description_input.text.strip()

        manager_id = self.manager_ids.get(
            self.manager_spinner.text
        )

        if not name:
            self.message.text = "Введите название проекта"
            return

        if manager_id is None:
            self.message.text = "Выберите руководителя"
            return

        statuses = {
            "Новый": "new",
            "В работе": "in_progress",
            "Приостановлен": "on_hold",
            "Завершён": "completed"
        }

        status = statuses[self.status_spinner.text]

        self.save_btn.disabled = True
        self.message.text = "Сохранение проекта..."

        Thread(
            target=self._create_project_request,
            args=(name, description, status, manager_id),
            daemon=True
        ).start()

    def _create_project_request(
        self, name, description, status, manager_id
    ):
        try:
            api.create_project(
                name=name,
                description=description,
                status=status,
                manager_id=manager_id
            )

            Clock.schedule_once(
                lambda dt: self._creation_success()
            )

        except Exception as error:
            message = str(error)
            Clock.schedule_once(
                lambda dt: self._creation_error(message)
            )

    def _creation_success(self):
        self.save_btn.disabled = False
        self.name_input.text = ""
        self.description_input.text = ""

        self.manager.current = "Projects"

        projects_screen = self.manager.get_screen("Projects")
        projects_screen.load_projects()

    def _creation_error(self, message):
        self.save_btn.disabled = False
        self.message.text = f"Ошибка создания: {message}"

    def go_back(self, instance):
        self.manager.current = "Projects"


class Projects(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()

        self.main_text = Label(
            text="Список проектов",
            font_size="22sp",
            size_hint=(0.8, 0.09),
            pos_hint={"center_x": 0.58, "top": 0.97}
        )
        self.layout.add_widget(self.main_text)

        back_btn = Button(
            text="Назад",
            size_hint=(0.25, 0.07),
            pos_hint={"x": 0.03, "top": 0.98}
        )
        back_btn.bind(on_press=self.get_back)
        self.layout.add_widget(back_btn)

        create_btn = Button(
            text="Создать проект",
            size_hint=(0.45, 0.07),
            pos_hint={"x": 0.03, "top": 0.88}
        )
        create_btn.bind(on_press=self.open_create_project)

        self.layout.add_widget(create_btn)
        refresh_btn = Button(
            text="Обновить",
            size_hint=(0.35, 0.07),
            pos_hint={"right": 0.97, "top": 0.88}
        )
        refresh_btn.bind(on_press=self.load_projects)
        self.layout.add_widget(refresh_btn)

        self.search_input = TextInput(
            hint_text="Поиск по названию",
            multiline=False,
            size_hint=(0.55, 0.07),
            pos_hint={"x": 0.03, "top": 0.80}
        )
        self.search_input.bind(on_text_validate=self.load_projects)
        self.layout.add_widget(self.search_input)

        self.status_filter = Spinner(
            text="Все статусы",
            values=(
                "Все статусы",
                "Новый",
                "В работе",
                "Приостановлен",
                "Завершён"
            ),
            size_hint=(0.35, 0.07),
            pos_hint={"right": 0.97, "top": 0.80}
        )
        self.status_filter.bind(
            text=lambda instance, value: self.load_projects()
        )
        self.layout.add_widget(self.status_filter)

        self.message = Label(
            text="Нажми «Обновить», чтобы загрузить проекты",
            font_size="15sp",
            size_hint=(0.9, 0.06),
            pos_hint={"center_x": 0.5, "top": 0.72}
        )
        self.layout.add_widget(self.message)

        # Область прокрутки для списка
        self.scroll = ScrollView(
            size_hint=(0.94, 0.60),
            pos_hint={"center_x": 0.5, "y": 0.04}
        )

        self.projects_list = GridLayout(
            cols=1,
            spacing=10,
            padding=8,
            size_hint_y=None
        )
        self.projects_list.bind(
            minimum_height=self.projects_list.setter("height")
        )

        self.scroll.add_widget(self.projects_list)
        self.layout.add_widget(self.scroll)

        self.add_widget(self.layout)

    def open_create_project(self, instance):
        self.manager.current = "CreateProject"

    def open_project(self, project_id):
        details_screen = self.manager.get_screen("ProjectDetails")
        details_screen.set_project(project_id)
        self.manager.current = "ProjectDetails"

    def on_enter(self, *args):
        self.load_projects()

    def load_projects(self, instance=None):
        self.message.text = "Загрузка проектов..."
        self.projects_list.clear_widgets()

        search = self.search_input.text.strip()

        statuses = {
            "Новый": "new",
            "В работе": "in_progress",
            "Приостановлен": "on_hold",
            "Завершён": "completed"
        }
        # для пункта "Все статусы" в словаре нет ключа, будет None
        status = statuses.get(self.status_filter.text)

        Thread(
            target=self._fetch_projects,
            args=(search, status),
            daemon=True
        ).start()

    def _fetch_projects(self, search=None, status=None):
        try:
            projects = api.get_projects(search=search, status=status)
            Clock.schedule_once(
                lambda dt: self._show_projects(projects)
            )
        except APIError as error:
            message = str(error)
            Clock.schedule_once(
                lambda dt: self._show_error(message)
            )
        except Exception as error:
            message = str(error)
            Clock.schedule_once(
                lambda dt: self._show_error(
                    f"Неожиданная ошибка: {message}"
                )
            )

    def _show_projects(self, projects):
        self.projects_list.clear_widgets()

        if not projects:
            self.message.text = "Проектов пока нет"
            return

        self.message.text = f"Найдено проектов: {len(projects)}"

        status_names = {
            "new": "Новый",
            "in_progress": "В работе",
            "on_hold": "Приостановлен",
            "completed": "Завершён"
        }

        for project in projects:
            project_id = project.get("id", "?")
            name = project.get("name", "Без названия")
            status = project.get("status", "не указан")
            description = project.get("description") or ""

            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=150,
                padding=10,
                spacing=5
            )

            title = Label(
                text=f"#{project_id} — {name}",
                font_size="17sp",
                halign="left",
                valign="middle",
                size_hint_y=0.4
            )
            title.bind(
                size=lambda widget, value:
                setattr(widget, "text_size", value)
            )

            status_label = Label(
                text=f"Статус: {status_names.get(status, status)}",
                font_size="14sp",
                size_hint_y=0.3
            )

            description_label = Label(
                text=description or "Описание отсутствует",
                font_size="13sp",
                size_hint_y=0.3
            )

            card.add_widget(title)
            card.add_widget(status_label)
            card.add_widget(description_label)

            open_btn = Button(
                text="Открыть проект",
                size_hint_y=None,
                height=38
            )
            open_btn.bind(
                on_press=lambda instance, pid=project_id:
                self.open_project(pid)
            )
            card.add_widget(open_btn)

            card.height = 190

            self.projects_list.add_widget(card)

    def _show_error(self, message):
        self.message.text = "Не удалось загрузить проекты"

        popup = Popup(
            title="Ошибка загрузки",
            content=Label(
                text=message,
                text_size=(300, None),
                halign="center",
                valign="middle"
            ),
            size_hint=(0.85, 0.4)
        )
        popup.open()

    def get_back(self, instance):
        self.manager.current = "First_Window"


class Calculator(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        main_text = Label(
            text='Калькулятор смет',
            font_size='20sp',
            size_hint=(0.85, 0.10),
            pos_hint={'center_x': 0.58, 'top': 0.92}
        )
        layout.add_widget(main_text)

        back_btn = Button(
            text="Назад",
            size_hint=(0.25, 0.07),
            pos_hint={'x': 0.03, 'top': 0.97}
        )
        layout.add_widget(back_btn)

        back_btn.bind(on_press=self.get_back)

        self.add_widget(layout)

    def get_back(self, instance):
        self.manager.current = "First_Window"


class MainWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ProjectDetails(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.project_id = None
        self.project = None

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=12
        )

        self.title_label = Label(
            text="Информация о проекте",
            font_size="22sp",
            size_hint_y=0.15
        )
        layout.add_widget(self.title_label)

        self.info_label = Label(
            text="Выберите проект",
            halign="left",
            valign="top"
        )
        self.info_label.bind(
            size=lambda widget, value:
            setattr(widget, "text_size", value)
        )
        layout.add_widget(self.info_label)

        self.stages_label = Label(
            text="Этапы проекта появятся здесь",
            size_hint_y=0.2
        )
        layout.add_widget(self.stages_label)

        self.stages_list = GridLayout(
            cols=1,
            spacing=8,
            padding=5,
            size_hint_y=None
        )
        self.stages_list.bind(
            minimum_height=self.stages_list.setter("height")
        )

        stages_scroll = ScrollView(
            size_hint_y=0.35
        )
        stages_scroll.add_widget(self.stages_list)
        layout.add_widget(stages_scroll)

        add_stage_btn = Button(
            text="Добавить этап",
            size_hint_y=0.12
        )
        add_stage_btn.bind(on_press=self.open_add_stage)
        layout.add_widget(add_stage_btn)

        project_buttons = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=0.12
        )

        edit_project_btn = Button(text="Изменить проект")
        edit_project_btn.bind(on_press=self.open_edit_project)
        project_buttons.add_widget(edit_project_btn)

        delete_project_btn = Button(text="Удалить проект")
        delete_project_btn.bind(on_press=self.confirm_delete_project)
        project_buttons.add_widget(delete_project_btn)

        layout.add_widget(project_buttons)

        back_btn = Button(
            text="Назад к проектам",
            size_hint_y=0.12
        )
        back_btn.bind(
            on_press=self.go_back
        )
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def set_project(self, project_id):
        self.project_id = project_id
        self.title_label.text = f"Проект #{project_id}"
        self.info_label.text = (
            f"ID проекта: {project_id}\n"
            "Загрузка информации..."
        )

        Thread(
            target=self._fetch_project,
            daemon=True
        ).start()

    def _fetch_project(self):
        try:
            project = api.get_project(self.project_id)
            Clock.schedule_once(
                lambda dt: self._show_project(project)
            )
        except Exception as error:
            message = str(error)
            Clock.schedule_once(
                lambda dt: self._show_project_error(message)
            )

    def _fetch_stages(self):
        try:
            stages = api.get_stages(self.project_id)

            Clock.schedule_once(
                lambda dt: self._show_stages(stages)
            )

        except Exception as error:
            message = str(error)

            Clock.schedule_once(
                lambda dt: self._show_stages_error(message)
            )

    def _show_stages(self, stages):
        self.stages_list.clear_widgets()

        if not stages:
            self.stages_label.text = "Этапов пока нет"
            return

        self.stages_label.text = "Выберите этап, чтобы открыть задачи"

        status_names = {
            "new": "Новый",
            "in_progress": "В работе",
            "completed": "Завершён",
            "on_hold": "Приостановлен"
        }

        for stage in stages:
            stage_id = stage.get("id")
            name = stage.get("name", "Без названия")
            status = stage.get("status", "не указан")

            stage_btn = Button(
                text=(
                    f"{name}\n"
                    f"Статус: {status_names.get(status, status)}"
                ),
                size_hint_y=None,
                height=65
            )

            stage_btn.bind(
                on_press=lambda instance,
                                sid=stage_id,
                                sname=name: self.open_stage_tasks(sid, sname)
            )

            self.stages_list.add_widget(stage_btn)

    def open_stage_tasks(self, stage_id, stage_name):
        if stage_id is None:
            return

        screen = self.manager.get_screen("StageTasks")
        screen.set_stage(stage_id, stage_name)
        self.manager.current = "StageTasks"

    def _show_stages_error(self, message):
        self.stages_label.text = (
            f"Ошибка загрузки этапов:\n{message}"
        )

    def open_add_stage(self, instance):
        layout = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        name_input = TextInput(
            hint_text="Название этапа",
            multiline=False,
            size_hint_y=0.2
        )

        description_input = TextInput(
            hint_text="Описание этапа",
            multiline=True,
            size_hint_y=0.3
        )

        status_spinner = Spinner(
            text="Новый",
            values=("Новый", "В работе", "Завершён"),
            size_hint_y=0.2
        )

        message = Label(
            text="",
            size_hint_y=0.15
        )

        save_btn = Button(
            text="Создать этап",
            size_hint_y=0.2
        )

        layout.add_widget(name_input)
        layout.add_widget(description_input)
        layout.add_widget(status_spinner)
        layout.add_widget(message)
        layout.add_widget(save_btn)

        popup = Popup(
            title="Новый этап",
            content=layout,
            size_hint=(0.9, 0.75)
        )

        statuses = {
            "Новый": "new",
            "В работе": "in_progress",
            "Завершён": "completed"
        }

        def save_stage(instance):
            name = name_input.text.strip()
            description = description_input.text.strip()

            if not name:
                message.text = "Введите название этапа"
                return

            save_btn.disabled = True
            message.text = "Сохранение..."

            Thread(
                target=self._create_stage_request,
                args=(
                    name,
                    description,
                    statuses[status_spinner.text],
                    popup,
                    save_btn,
                    message
                ),
                daemon=True
            ).start()

        save_btn.bind(on_press=save_stage)
        popup.open()

    def _create_stage_request(
            self, name, description, status,
            popup, save_btn, message
    ):
        try:
            api.create_stage(
                project_id=self.project_id,
                name=name,
                description=description,
                status=status
            )

            Clock.schedule_once(
                lambda dt: self._stage_created(popup)
            )

        except Exception as error:
            error_message = str(error)

            Clock.schedule_once(
                lambda dt: self._stage_creation_error(
                    error_message, save_btn, message
                )
            )

    def _stage_created(self, popup):
        popup.dismiss()

        # Обновляем этапы проекта с сервера
        Thread(
            target=self._fetch_stages,
            daemon=True
        ).start()

    def _stage_creation_error(self, error, save_btn, message):
        save_btn.disabled = False
        message.text = f"Ошибка: {error}"

    def _show_project(self, project):
        self.project = project

        status_names = {
            "new": "Новый",
            "in_progress": "В работе",
            "on_hold": "Приостановлен",
            "completed": "Завершён"
        }

        name = project.get("name", "Без названия")
        description = (
            project.get("description") or "Нет описания"
        )
        status = project.get("status", "не указан")

        self.title_label.text = name
        self.info_label.text = (
            f"ID: {self.project_id}\n"
            f"Название: {name}\n"
            f"Статус: {status_names.get(status, status)}\n"
            f"Описание: {description}"
        )

        self.stages_label.text = "Загрузка этапов..."

        Thread(
            target=self._fetch_stages,
            daemon=True
        ).start()

    def show_message(self, title, text):
        content = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10
        )

        content.add_widget(Label(
            text=text,
            halign="center",
            valign="middle"
        ))

        close_btn = Button(
            text="Закрыть",
            size_hint_y=None,
            height=42
        )
        content.add_widget(close_btn)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.88, 0.42)
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def open_edit_project(self, instance):
        if self.project is None:
            return

        layout = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        name_input = TextInput(
            text=self.project.get("name") or "",
            hint_text="Название проекта",
            multiline=False,
            size_hint_y=0.2
        )

        description_input = TextInput(
            text=self.project.get("description") or "",
            hint_text="Описание проекта",
            multiline=True,
            size_hint_y=0.3
        )

        status_names = {
            "new": "Новый",
            "in_progress": "В работе",
            "on_hold": "Приостановлен",
            "completed": "Завершён"
        }

        statuses = {
            "Новый": "new",
            "В работе": "in_progress",
            "Приостановлен": "on_hold",
            "Завершён": "completed"
        }

        status_spinner = Spinner(
            text=status_names.get(self.project.get("status"), "Новый"),
            values=(
                "Новый",
                "В работе",
                "Приостановлен",
                "Завершён"
            ),
            size_hint_y=0.2
        )

        message = Label(
            text="",
            size_hint_y=0.15
        )

        save_btn = Button(
            text="Сохранить изменения",
            size_hint_y=0.2
        )

        layout.add_widget(name_input)
        layout.add_widget(description_input)
        layout.add_widget(status_spinner)
        layout.add_widget(message)
        layout.add_widget(save_btn)

        popup = Popup(
            title="Изменение проекта",
            content=layout,
            size_hint=(0.9, 0.75)
        )

        def save_project(instance):
            name = name_input.text.strip()
            description = description_input.text.strip()

            if not name:
                message.text = "Введите название проекта"
                return

            save_btn.disabled = True
            message.text = "Сохранение..."

            Thread(
                target=self._update_project_request,
                args=(
                    name,
                    description,
                    statuses[status_spinner.text],
                    popup,
                    save_btn,
                    message
                ),
                daemon=True
            ).start()

        save_btn.bind(on_press=save_project)
        popup.open()

    def _update_project_request(
            self, name, description, status,
            popup, save_btn, message
    ):
        try:
            project = api.update_project(
                self.project_id,
                name=name,
                description=description or None,
                status=status
            )

            Clock.schedule_once(
                lambda dt: self._project_updated(project, popup)
            )

        except Exception as error:
            error_message = str(error)

            Clock.schedule_once(
                lambda dt: self._project_update_error(
                    error_message, save_btn, message
                )
            )

    def _project_updated(self, project, popup):
        popup.dismiss()
        self._show_project(project)
        self.show_message("Готово", "Изменения сохранены")

    def _project_update_error(self, error, save_btn, message):
        save_btn.disabled = False
        message.text = f"Ошибка: {error}"

    def confirm_delete_project(self, instance):
        if self.project_id is None:
            return

        layout = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10
        )

        name = (
            self.project.get("name", "Без названия")
            if self.project else f"#{self.project_id}"
        )

        layout.add_widget(Label(
            text=(
                f"Удалить проект «{name}»?\n"
                "Этапы и сметы проекта тоже будут удалены."
            ),
            halign="center"
        ))

        buttons = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=45
        )

        confirm_btn = Button(text="Удалить")
        cancel_btn = Button(text="Отмена")

        buttons.add_widget(confirm_btn)
        buttons.add_widget(cancel_btn)
        layout.add_widget(buttons)

        popup = Popup(
            title="Подтверждение удаления",
            content=layout,
            size_hint=(0.88, 0.4),
            auto_dismiss=False
        )

        confirm_btn.bind(
            on_press=lambda *_: self._start_delete_project(
                popup, confirm_btn
            )
        )
        cancel_btn.bind(on_press=popup.dismiss)

        popup.open()

    def _start_delete_project(self, popup, button):
        button.disabled = True
        button.text = "Удаление..."

        Thread(
            target=self._delete_project_request,
            args=(popup,),
            daemon=True
        ).start()

    def _delete_project_request(self, popup):
        try:
            api.delete_project(self.project_id)

            Clock.schedule_once(
                lambda dt: self._project_deleted(popup)
            )

        except Exception as error:
            error_text = str(error)

            Clock.schedule_once(
                lambda dt: self._project_delete_error(error_text, popup)
            )

    def _project_deleted(self, popup):
        popup.dismiss()
        self.manager.current = "Projects"
        self.show_message("Готово", "Проект удалён")

    def _project_delete_error(self, error, popup):
        popup.dismiss()
        self.show_message("Ошибка удаления", error)

    def _show_project_error(self, message):
        self.info_label.text = (
            f"Не удалось загрузить проект:\n{message}"
        )

    def go_back(self, instance):
        self.manager.current = "Projects"



class StageTasks(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.stage_id = None
        self.assignee_ids = {"Без исполнителя": None}

        self.status_names = {
            "new": "Новая",
            "in_progress": "В работе",
            "completed": "Завершена"
        }

        self.status_values = {
            "Новая": "new",
            "В работе": "in_progress",
            "Завершена": "completed"
        }

        self.priority_names = {
            "low": "Низкий",
            "medium": "Средний",
            "high": "Высокий"
        }

        self.priority_values = {
            "Низкий": "low",
            "Средний": "medium",
            "Высокий": "high"
        }

        layout = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        self.title_label = Label(
            text="Задачи этапа",
            font_size="22sp",
            size_hint_y=None,
            height=45
        )
        layout.add_widget(self.title_label)

        self.message = Label(
            text="Выберите этап",
            size_hint_y=None,
            height=35
        )
        layout.add_widget(self.message)

        add_task_btn = Button(
            text="Создать задачу",
            size_hint_y=None,
            height=45
        )
        add_task_btn.bind(on_press=self.open_create_task)
        layout.add_widget(add_task_btn)

        self.tasks_list = GridLayout(
            cols=1,
            spacing=10,
            padding=5,
            size_hint_y=None
        )
        self.tasks_list.bind(
            minimum_height=self.tasks_list.setter("height")
        )

        scroll = ScrollView(size_hint_y=1)
        scroll.add_widget(self.tasks_list)
        layout.add_widget(scroll)

        back_btn = Button(
            text="Назад к этапу",
            size_hint_y=None,
            height=42
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def set_stage(self, stage_id, stage_name):
        self.stage_id = stage_id
        self.title_label.text = f"Задачи: {stage_name}"
        self.message.text = "Загрузка задач..."
        self.tasks_list.clear_widgets()

        Thread(
            target=self._fetch_tasks,
            daemon=True
        ).start()

    def _fetch_tasks(self):
        try:
            tasks = api.get_tasks(stage_id=self.stage_id)
            Clock.schedule_once(
                lambda dt: self._show_tasks(tasks)
            )
        except Exception as error:
            error_text = str(error)
            Clock.schedule_once(
                lambda dt: self._show_error(error_text)
            )

    def _show_tasks(self, tasks):
        self.tasks_list.clear_widgets()

        if not tasks:
            self.message.text = "Задач пока нет"
            return

        self.message.text = f"Количество задач: {len(tasks)}"

        for task in tasks:
            task_id = task.get("id")
            title = task.get("title") or "Без названия"
            description = task.get("description") or "Без описания"

            status = task.get("status") or "new"
            priority = task.get("priority") or "medium"
            due_date = task.get("due_date") or "Не указан"

            assignee = task.get("assignee")
            if isinstance(assignee, dict):
                assignee_name = (
                    assignee.get("full_name")
                    or assignee.get("username")
                    or f"ID {assignee.get('id', '?')}"
                )
            else:
                assignee_name = (
                    task.get("assignee_name")
                    or (
                        f"ID {task.get('assignee_id')}"
                        if task.get("assignee_id") is not None
                        else "Не назначен"
                    )
                )

            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=230,
                padding=10,
                spacing=5
            )

            title_label = Label(
                text=f"#{task_id} — {title}",
                bold=True,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=35
            )
            title_label.bind(
                size=lambda widget, value:
                setattr(widget, "text_size", value)
            )
            card.add_widget(title_label)

            card.add_widget(Label(
                text=f"Статус: {self.status_names.get(status, status)}",
                halign="left",
                size_hint_y=None,
                height=25
            ))

            card.add_widget(Label(
                text=f"Приоритет: {self.priority_names.get(priority, priority)}",
                halign="left",
                size_hint_y=None,
                height=25
            ))

            card.add_widget(Label(
                text=f"Исполнитель: {assignee_name}",
                halign="left",
                size_hint_y=None,
                height=25
            ))

            card.add_widget(Label(
                text=f"Срок: {due_date}",
                halign="left",
                size_hint_y=None,
                height=25
            ))

            description_label = Label(
                text=description,
                halign="left",
                valign="top",
                size_hint_y=None,
                height=40
            )
            description_label.bind(
                size=lambda widget, value:
                setattr(widget, "text_size", value)
            )
            card.add_widget(description_label)

            buttons = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=38,
                spacing=5
            )

            status_btn = Button(text="Сменить статус")
            status_btn.bind(
                on_press=lambda instance, item=task:
                self.change_task_status(item)
            )

            edit_btn = Button(text="Изменить")
            edit_btn.bind(
                on_press=lambda instance, item=task:
                self.open_edit_task(item)
            )

            delete_btn = Button(text="Удалить")
            delete_btn.bind(
                on_press=lambda instance, item=task:
                self.confirm_delete_task(item)
            )

            buttons.add_widget(status_btn)
            buttons.add_widget(edit_btn)
            buttons.add_widget(delete_btn)
            card.add_widget(buttons)

            self.tasks_list.add_widget(card)

    def _show_error(self, message):
        self.message.text = "Ошибка загрузки задач"
        self.show_message("Ошибка", message)

    def show_message(self, title, text):
        content = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10
        )

        content.add_widget(Label(
            text=text,
            halign="center",
            valign="middle"
        ))

        close_btn = Button(
            text="Закрыть",
            size_hint_y=None,
            height=42
        )
        content.add_widget(close_btn)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.88, 0.42)
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def change_task_status(self, task):
        task_id = task.get("id")

        if task_id is None:
            self.show_message(
                "Ошибка",
                "У задачи отсутствует ID."
            )
            return

        current_status = task.get("status") or "new"

        status_order = [
            "new",
            "in_progress",
            "completed"
        ]

        try:
            index = status_order.index(current_status)
        except ValueError:
            index = 0

        new_status = status_order[
            (index + 1) % len(status_order)
            ]

        self.message.text = "Изменение статуса..."

        Thread(
            target=self._update_status_request,
            args=(task_id, new_status),
            daemon=True
        ).start()

    def _update_status_request(self, task_id, status):
        try:
            api.update_task(task_id, status=status)
            Clock.schedule_once(
                lambda dt: self._status_updated(status)
            )
        except Exception as error:
            error_text = str(error)
            Clock.schedule_once(
                lambda dt: self._operation_error(error_text)
            )

    def _status_updated(self, status):
        self.message.text = (
            f"Статус изменён: {self.status_names.get(status, status)}"
        )
        Thread(
            target=self._fetch_tasks,
            daemon=True
        ).start()

    def open_create_task(self, instance):
        self.open_task_form()

    def open_edit_task(self, task):
        self.open_task_form(task)

    def open_task_form(self, task=None):
        is_edit = task is not None

        layout = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=7
        )

        title_input = TextInput(
            hint_text="Название задачи",
            text=task.get("title", "") if is_edit else "",
            multiline=False,
            size_hint_y=None,
            height=42
        )

        description_input = TextInput(
            hint_text="Описание",
            text=task.get("description") or "" if is_edit else "",
            multiline=True,
            size_hint_y=None,
            height=75
        )

        assignee_spinner = Spinner(
            text="Загрузка исполнителей...",
            values=(),
            size_hint_y=None,
            height=42
        )

        current_priority = (
            self.priority_names.get(
                task.get("priority", "medium"), "Средний"
            ) if is_edit else "Средний"
        )

        priority_spinner = Spinner(
            text=current_priority,
            values=("Низкий", "Средний", "Высокий"),
            size_hint_y=None,
            height=42
        )

        current_status = (
            self.status_names.get(
                task.get("status", "new"), "Новая"
            ) if is_edit else "Новая"
        )

        status_spinner = Spinner(
            text=current_status,
            values=(
                "Новая",
                "В работе",
                "Завершена"
            ),
            size_hint_y=None,
            height=42
        )

        due_date_input = TextInput(
            hint_text="Срок ГГГГ-ММ-ДД (необязательно)",
            text=str(task.get("due_date") or "") if is_edit else "",
            multiline=False,
            size_hint_y=None,
            height=42
        )

        message = Label(
            text="",
            size_hint_y=None,
            height=42
        )

        save_btn = Button(
            text="Сохранить изменения" if is_edit else "Создать задачу",
            size_hint_y=None,
            height=44
        )

        cancel_btn = Button(
            text="Отмена",
            size_hint_y=None,
            height=40
        )

        for widget in (
            title_input,
            description_input,
            assignee_spinner,
            priority_spinner,
            status_spinner,
            due_date_input,
            message,
            save_btn,
            cancel_btn
        ):
            layout.add_widget(widget)

        popup = Popup(
            title="Редактирование задачи" if is_edit else "Создание задачи",
            content=layout,
            size_hint=(0.93, 0.95),
            auto_dismiss=False
        )

        current_assignee_id = (
            task.get("assignee_id") if is_edit else None
        )

        def save_task(_instance):
            title = title_input.text.strip()
            description = description_input.text.strip()
            due_date = due_date_input.text.strip()

            if not title:
                message.text = "Введите название задачи"
                return

            if due_date:
                try:
                    from datetime import date
                    date.fromisoformat(due_date)
                except ValueError:
                    message.text = "Дата: ГГГГ-ММ-ДД"
                    return

            assignee_id = self.assignee_ids.get(
                assignee_spinner.text
            )

            priorities = self.priority_values
            statuses = self.status_values

            save_btn.disabled = True
            message.text = "Сохранение..."

            if is_edit:
                Thread(
                    target=self._edit_task_request,
                    args=(
                        task.get("id"),
                        title,
                        description,
                        assignee_id,
                        priorities[priority_spinner.text],
                        statuses[status_spinner.text],
                        due_date or None,
                        popup,
                        save_btn,
                        message
                    ),
                    daemon=True
                ).start()
            else:
                app = App.get_running_app()
                created_by = self._extract_user_id(
                    getattr(app, "current_user", None)
                )
                creator_username = getattr(
                    app, "current_username", ""
                )

                if created_by is None and not creator_username:
                    save_btn.disabled = False
                    message.text = "Войдите в приложение снова"
                    return

                Thread(
                    target=self._create_task_request,
                    args=(
                        title,
                        description,
                        created_by,
                        creator_username,
                        assignee_id,
                        priorities[priority_spinner.text],
                        statuses[status_spinner.text],
                        due_date or None,
                        popup,
                        save_btn,
                        message
                    ),
                    daemon=True
                ).start()

        save_btn.bind(on_press=save_task)
        cancel_btn.bind(on_press=lambda *_: popup.dismiss())

        self.assignee_ids = {"Без исполнителя": None}
        assignee_spinner.values = ("Без исполнителя",)
        assignee_spinner.text = "Без исполнителя"

        popup.open()

        Thread(
            target=self._fetch_assignees,
            args=(assignee_spinner, message, current_assignee_id),
            daemon=True
        ).start()

    @staticmethod
    def _extract_user_id(user):
        if not isinstance(user, dict):
            return None

        if isinstance(user.get("user"), dict):
            user = user["user"]

        value = user.get("id", user.get("user_id"))

        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    def _fetch_assignees(
        self, spinner, message, selected_assignee_id=None
    ):
        try:
            users = api.get_users()
            Clock.schedule_once(
                lambda dt: self._show_assignees(
                    users, spinner, selected_assignee_id
                )
            )
        except Exception as error:
            error_text = str(error)
            Clock.schedule_once(
                lambda dt: self._assignees_error(
                    error_text, spinner, message
                )
            )

    def _show_assignees(
        self, users, spinner, selected_assignee_id=None
    ):
        self.assignee_ids = {"Без исполнителя": None}
        options = ["Без исполнителя"]
        selected_option = "Без исполнителя"

        for user in users:
            user_id = user.get("id")

            if user_id is None:
                continue

            name = (
                user.get("full_name")
                or user.get("username")
                or f"Пользователь {user_id}"
            )

            option = f"{user_id} — {name}"
            self.assignee_ids[option] = user_id
            options.append(option)

            if str(user_id) == str(selected_assignee_id):
                selected_option = option

        spinner.values = options
        spinner.text = selected_option

    def _assignees_error(self, error, spinner, message):
        spinner.values = ("Без исполнителя",)
        spinner.text = "Без исполнителя"
        message.text = f"Ошибка загрузки исполнителей: {error}"

    def _create_task_request(
        self, title, description, created_by, creator_username,
        assignee_id, priority, status, due_date, popup, save_btn, message
    ):
        try:
            if created_by is None:
                users = api.get_users()

                for user in users:
                    if (
                        str(user.get("username", "")).casefold()
                        == creator_username.casefold()
                    ):
                        created_by = user.get("id")
                        break

                if created_by is None:
                    raise APIError(
                        "Не удалось определить ID текущего пользователя."
                    )

            api.create_task(
                title=title,
                created_by=created_by,
                description=description,
                stage_id=self.stage_id,
                assignee_id=assignee_id,
                priority=priority,
                status=status,
                due_date=due_date
            )

            Clock.schedule_once(
                lambda dt: self._task_saved(popup, "Задача создана")
            )

        except Exception as error:
            error_text = str(error)
            Clock.schedule_once(
                lambda dt: self._form_error(
                    error_text, save_btn, message
                )
            )

    def _edit_task_request(
        self, task_id, title, description, assignee_id,
        priority, status, due_date, popup, save_btn, message
    ):
        try:
            if task_id is None:
                raise APIError("У задачи отсутствует ID.")

            api.update_task(
                task_id,
                title=title,
                description=description or None,
                assignee_id=assignee_id,
                priority=priority,
                status=status,
                due_date=due_date
            )

            Clock.schedule_once(
                lambda dt: self._task_saved(
                    popup, "Изменения сохранены"
                )
            )

        except Exception as error:
            error_text = str(error)
            Clock.schedule_once(
                lambda dt: self._form_error(
                    error_text, save_btn, message
                )
            )

    def _task_saved(self, popup, text):
        popup.dismiss()
        self.message.text = text
        Thread(
            target=self._fetch_tasks,
            daemon=True
        ).start()

    def _form_error(self, error, save_btn, message):
        save_btn.disabled = False
        message.text = f"Ошибка: {error}"

    def confirm_delete_task(self, task):
        task_id = task.get("id")

        if task_id is None:
            self.show_message(
                "Ошибка",
                "У задачи отсутствует ID."
            )
            return

        layout = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10
        )

        layout.add_widget(Label(
            text=f"Удалить задачу «{task.get('title', 'Без названия')}»?"
        ))

        buttons = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=45
        )

        confirm_btn = Button(text="Удалить")
        cancel_btn = Button(text="Отмена")

        buttons.add_widget(confirm_btn)
        buttons.add_widget(cancel_btn)
        layout.add_widget(buttons)

        popup = Popup(
            title="Подтверждение удаления",
            content=layout,
            size_hint=(0.88, 0.35),
            auto_dismiss=False
        )

        confirm_btn.bind(
            on_press=lambda *_: self._start_delete_task(
                task_id, popup, confirm_btn
            )
        )
        cancel_btn.bind(on_press=popup.dismiss)

        popup.open()

    def _start_delete_task(self, task_id, popup, button):
        button.disabled = True
        button.text = "Удаление..."

        Thread(
            target=self._delete_task_request,
            args=(task_id, popup),
            daemon=True
        ).start()

    def _delete_task_request(self, task_id, popup):
        try:
            api.delete_task(task_id)
            Clock.schedule_once(
                lambda dt: self._task_deleted(popup)
            )
        except Exception as error:
            error_text = str(error)
            Clock.schedule_once(
                lambda dt: self._delete_error(error_text, popup)
            )

    def _task_deleted(self, popup):
        popup.dismiss()
        self.message.text = "Задача удалена"
        Thread(
            target=self._fetch_tasks,
            daemon=True
        ).start()

    def _delete_error(self, error, popup):
        popup.dismiss()
        self.show_message(
            "Ошибка удаления",
            error
        )

    def _operation_error(self, error):
        self.message.text = "Не удалось выполнить действие"
        self.show_message("Ошибка", error)

    def go_back(self, instance):
        self.manager.current = "ProjectDetails"



class Stroybat(App):
    def build(self):
        manager = ScreenManager()

        manager.add_widget(vhod(name="vhod"))
        manager.add_widget(RegistrWindow(name="RegistrWindow"))
        manager.add_widget(First_Window(name="First_Window"))
        manager.add_widget(Projects(name="Projects"))
        manager.add_widget(Calculator(name="Calculator"))
        manager.add_widget(CreateProject(name="CreateProject"))
        manager.add_widget(ProjectDetails(name="ProjectDetails"))
        manager.add_widget(StageTasks(name="StageTasks"))
        return manager


Stroybat().run()
