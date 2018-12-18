import toga
from toga.style.pack import Pack, ROW, CENTER, COLUMN, RIGHT
from main import main as mn


class Graze(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)

        self.table = toga.Table(['Название параметра', 'Значение'], style=Pack(
                direction=COLUMN,
                height=400,
                width=300,
                alignment=RIGHT,
                padding = 5
        ))

        box = toga.Box(
            children=[
                toga.Box(
                    children=[
                        toga.Button('Линейный метод', on_press=self.load_page_linear, style=Pack(width=300, padding_left=5)),
                        toga.Button('Экспоненциальный метод', on_press=self.load_page_expo, style=Pack(width=300, padding_left=5)),


                    ],
                    style=Pack(
                        direction=ROW,
                        alignment=CENTER,
                        padding=5,
                        # height=4200,
                        flex=1
                    )
                ),
                self.table,
                # toga.Label('Hello world')

            ],
            style=Pack(
                direction=COLUMN,
                # height=2200,
                flex=1,
                padding_top=10
            )
        )

        self.main_window.content = box

        # Show the main window
        self.main_window.show()

    def load_page_expo(self, logick = 1):
        self.table.data.clear()
        values = mn(logick)
        i = 0
        # for k, v in values.items():
        #     self.table.data.insert(i, str(k), str(v))
        #     i += 1
        for key in sorted(values):
            self.table.data.insert(i, str(key), str(values[key]))
            i += 1

    def load_page_linear(self, logick = 0):
        self.table.data.clear()
        values = mn(logick)
        i = 0
        # for k, v in values.items():
        #     self.table.data.insert(i, str(k), str(v))
        #     i += 1
        for key in sorted(values):
            self.table.data.insert(i, str(key), str(values[key]))
            i += 1


def main():
    return Graze('Сurseach', 'org.pybee.graze')


if __name__ == '__main__':
    main().main_loop()
