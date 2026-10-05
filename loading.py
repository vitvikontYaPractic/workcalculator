from kivy.clock import mainthread
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from database.models import *
from logs.debug_log import *
import datetime
import math


class Box(MDBoxLayout):
    drop_btn = ObjectProperty()
    menu_bt = ObjectProperty()
    label_product = ObjectProperty()
    label_info = ObjectProperty()
    enter_text = ObjectProperty()
    label_widget1 = ObjectProperty()
    label_widget2 = ObjectProperty()
    label_widget3 = ObjectProperty()
    label_widget4 = ObjectProperty()
    label_widget5 = ObjectProperty()
    label_widget6 = ObjectProperty()
    label_widget7 = ObjectProperty()
    table = ObjectProperty()
    widget_search = ObjectProperty()
    dialog = None

    def __init__(self, **kwargs):
        super(Box, self).__init__(**kwargs)
        # Инициализация аргументов
        self.numb = None
        self.menu_call = None
        self.menu_toolbar = None
        calendar_day = datetime.datetime.today()
        get_day = calendar_day.strftime('%d.%m.%y')
        get_time = calendar_day.strftime('%H:%M')
        self.stamp = "{}, {}".format(get_day, get_time)
        self.product = None
        self.menu_dr_ls = None

    @logger.catch
    def bar_menu(self, instance):
        # Меню в топике
        self.menu_toolbar = [
            {
                "viewclass": "OneLineIconListItem",
                "text": "{}".format(name_msg),
                "on_release": lambda x="{}".format(msg): self.menu_bar_callback(x),
            } for name_msg, msg in zip(["Допуски", "О приложении"], ["Info", "About"])
        ]
        self.menu_call = MDDropdownMenu(
            items=self.menu_toolbar,
            width_mult=4
        )
        self.menu_call.caller = instance
        self.menu_call.open()

    @logger.catch
    def delete_row(self, *args):
        # Удаление выделенных (отмеченных галочкой) записей из БД
        data_table = None
        for child in self.table.children:
            if isinstance(child, MDDataTable):
                data_table = child
                break

        if not data_table:
            self.enter_text.text = "Откройте Журнал или Поиск"
            return

        checked_rows = data_table.get_row_checks()

        if not checked_rows:
            self.enter_text.text = "Выберите строки (галочки)"
            return

        deleted_count = 0
        for row in checked_rows:
            number = row[0]
            deleted_count += Product.delete().where(Product.number == number).execute()

        self.enter_text.text = f"Удалено: {deleted_count}"

        # Обновляем таблицу — показываем журнал
        self.tables_data()


    @logger.catch
    def menu_bar_callback(self, instance):
        # Справочная информация в виде всплывающего окна
        word = """
        _____________________________
        Изделие  |   Max   |   Min   
        _____________________________
        ДУО          |  1400   |  1300 
        _____________________________
        Опорный |  1620   |  1460  
        _____________________________
        Чер вал   |  1210   |  1090  
        _____________________________
        Раб вал   |   840    |   760   
        _____________________________
        ВВ 4-5      |  1100   |  900     
        _____________________________
        """
        if not self.dialog and instance == "Info":
            self.dialog = MDDialog(
                title="Справка.",
                text=word,
                buttons=[
                    MDFlatButton(
                        text="Назад",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                ],
            )

        elif not self.dialog and instance == "About":
            self.dialog = MDDialog(
                title="О приложении.",
                text="Work Calculator ver. 0.0.38",
                buttons=[
                    MDFlatButton(
                        text="Назад",
                        text_color=self.theme_cls.primary_color,
                        on_press=self.close_dialog,
                    ),
                ],
            )

        self.dialog.open()

    @logger.catch
    @mainthread
    def search_base(self):
        # Отображение искомого изделия в виде таблицы
        try:
            self.table.clear_widgets()
            self.numb = self.widget_search.text
        except ValueError:
            self.widget_search.text = "Для поиска введите номер изделия"

        data_table = MDDataTable(
            size_hint=(1, None),
            height=dp(500),
            use_pagination=True,
            check=True,
            column_data=[
                ("No", dp(20)),
                ("Изделие", dp(20)),
                ("Диам нач", dp(20)),
                ("Диам кон", dp(20)),
                ("Глубина", dp(20)),
                ("Длина", dp(20)),
                ("Дата", dp(30)),
            ],
            row_data=[
                (
                    i.number,
                    i.product,
                    i.diameter_first,
                    i.diameter_last,
                    i.height,
                    i.length,
                    i.created.strftime('%Y/%m/%d | %H:%M')
                ) for i in Product.select().where(Product.number == self.numb)
            ]
        )

        self.table.add_widget(data_table)

    @logger.catch
    @mainthread
    def tables_data(self):
        # Отображение данных из базы данных в виде таблицы
        self.table.clear_widgets()
        data_table = MDDataTable(
            size_hint=(1, None),
            height=dp(500),
            use_pagination=True,
            check=True,
            column_data=[
                ("No", dp(20)),
                ("Изделие", dp(20)),
                ("Диам нач", dp(20)),
                ("Диам кон", dp(20)),
                ("Глубина", dp(20)),
                ("Длина", dp(20)),
                ("Дата", dp(30)),
            ],
            row_data=[
                (
                    i.number,
                    i.product,
                    i.diameter_first,
                    i.diameter_last,
                    i.height,
                    i.length,
                    i.created.strftime('%Y/%m/%d | %H:%M')
                ) for i in Product.select()
            ]
        )

        self.table.add_widget(data_table)

    @logger.catch
    def show_dialog(self):
        # Предварительный просмотр данных
        txt = self.get_info()
        if not self.dialog:
            self.dialog = MDDialog(
                title="Информация о изделии.",
                text=txt,
                buttons=[
                    MDFlatButton(
                        text="Назад",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                    MDRectangleFlatButton(
                        text="Сохранить",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.save_create_tables,
                        on_press=self.close_dialog
                    ),
                ],
            )

        self.dialog.open()

    @logger.catch
    def close_dialog(self, instance):
        # Закрыть всплывающее окно
        self.dialog.dismiss()
        self.dialog = None

    @logger.catch
    def get_info(self):
        # Собираем водимые значения для предварительного просмотра
        lst_word = [
            f"Дата: {self.stamp}",
            f"Изделие:  {self.product}",
            f"№ {self.label_widget1.text}",
            f"Начальный диаметр: {self.label_widget4.text}",
            f"Конечный диаметр: {self.label_widget5.text}",
            f"Глубина врезки: {self.label_widget6.text}",
            f"Обработанная длина: {self.label_widget7.text}",
        ]
        return "\n".join(lst_word)

    @logger.catch
    def backspace(self):
        # Обнуляет значения в строке для ввода данных
        self.enter_text.text = ''

    @logger.catch
    def drop_menu(self):
        # Всплывающее меню для выбора изделия
        lst_names = [
            "Рабочий вал",
            "Черновой вал",
            "ДУО",
            "Опорный вал",
            "ВВ 2-3кл",
            "ВВ 4-5кл",
            "Окалина-ломатель"
        ]
        lst = ["РВ", "ЧВ", "ДУО", "ОВ", "ВВ 2-3", "ВВ 4-5", "ВО"]
        self.menu_dr_ls = [
            {
                "viewclass": "OneLineIconListItem",
                "text": "{}".format(name_product),
                "on_release": lambda x="{}".format(product): self.menu_callback(x),
            } for name_product, product in zip(lst_names, lst)
        ]
        MDDropdownMenu(
            items=self.menu_dr_ls,
            width_mult=4,
            caller=self.ids.button_menu
        ).open()

    @logger.catch
    def menu_callback(self, text_item):
        # Функция для выбора из всплывающего меню изделия
        self.product = '{}'.format(text_item)
        self.label_product.text = self.product

    @logger.catch
    def numer_product(self) -> None:
        # номер изделия
        self.label_widget1.text = self.enter_text.text

    @logger.catch
    def text_Pn(self):
        # параметр: начальный периметр
        self.label_widget2.text = self.enter_text.text

    @logger.catch
    def text_Pc(self):
        # параметр: периметр после обработки
        self.label_widget3.text = self.enter_text.text

    @logger.catch
    def text_Dn(self):
        # параметр: начальный диаметр
        diameter_first = float(int(self.label_widget2.text) / math.pi)
        self.label_widget4.text = str(round(diameter_first, 1))

    @logger.catch
    def text_Dc(self):
        # параметр: диаметр после обработки
        diameter_last = float(int(self.label_widget3.text) / math.pi)
        self.label_widget5.text = str(round(diameter_last, 1))

    @logger.catch
    def text_height(self):
        # параметр: глубина врезки
        diameter_first = float(self.label_widget4.text)
        diameter_last = float(self.label_widget5.text)
        depth = (diameter_first - diameter_last) * 0.5
        self.label_widget6.text = str(round(depth, 1))

    @logger.catch
    def length(self):
        # параметр: длина обработки изделия
        self.label_widget7.text = self.enter_text.text

    @logger.catch
    def clear_text(self):
        # обнуление окон
        self.enter_text.text = ''
        self.label_product.text = '-'
        # self.label_info.text = 'Пусто'  # нет id label_info в .kv
        self.label_widget1.text = '0'
        self.label_widget2.text = '0'
        self.label_widget3.text = '0'
        self.label_widget4.text = '0'
        self.label_widget5.text = '0'
        self.label_widget6.text = '0'
        self.label_widget7.text = '0'

    @logger.catch
    def save_create_tables(self, *args):
        # локальное сохранение в текст файл
        Product(
            brigade=4,
            number=self.label_widget1.text,
            product=self.label_product.text,
            diameter_first=self.label_widget4.text,
            diameter_last=self.label_widget5.text,
            height=self.label_widget6.text,
            length=self.label_widget7.text
        ).save()

        self.enter_text.text = "Сохранили в базу"
        self.dialog = None

    @logger.catch
    def clear_database(self):
        # Диалог подтверждения очистки всей БД
        if not self.dialog:
            self.dialog = MDDialog(
                title="Очистить базу?",
                text="Все записи будут удалены безвозвратно!",
                buttons=[
                    MDFlatButton(
                        text="Отмена",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_dialog,
                    ),
                    MDRectangleFlatButton(
                        text="Удалить всё",
                        text_color=(1, 0, 0, 1),
                        on_release=self._confirm_clear_database,
                    ),
                ],
            )
        self.dialog.open()

    @logger.catch
    def _confirm_clear_database(self, instance):
        # Подтверждённая очистка БД
        count = Product.delete().execute()
        self.table.clear_widgets()
        self.enter_text.text = f"База очищена ({count})"
        self.close_dialog(instance)

    @logger.catch
    def closed(self, instance):
        # завершить работу приложения
        quit()
