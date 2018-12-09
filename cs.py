"""Задание №14.
Вычислительная система (ВС) состоит из сервера, обрабатывающего программы.
Программы поступают случайным образом, распределенные по линейному закону:
Tzmin=1/3 сек, Tzmax=2/3 сек.
Время обработки одной программы сервером – случайная величина, распределенная по линейному закону:
Tsmin=1 сек, Tsmax=6 сек.
Если сервер занят, обрабатывает программу, то поступающая следующая программа отправляется в буфер.
Число программ в буфере – случайная величина и ограничено (не более 3-х).
Если поступила следующая программа, а в буфере содержится уже 3 три программы, то программа покидает ВС не обработанной.
Разработать программу, моделирующую работу ВС и найти ее характеристики за время работы 1 час. Характеристики ВС:
P0 – вероятность того, что ВС не загружена,
P1 – вероятность того, что сервер обрабатывает одну программу и буфер пуст,
P2 – вероятность того, что в буфере находится 1-на программа,
P3 – вероятность того, что в буфере находится 2-ве программы,
P4 – вероятность того, что в буфере находится 3-ри программы,
Q – относительная пропускная способность ВС – средняя доля программ, обработанных ВС,
S – абсолютная пропускная способность – среднее число программ, обработанных в единицу времени,
Pотк – вероятность отказа, т.е. того, что программа будет не обработанной,
Nпрог.- среднее число программ в ВС,
Tпрог – среднее время нахождения программы в ВС,
Nбуф.- среднее число программ в буфере,
Tбуф – среднее время нахождения программы в буфере.
Найти характеристики ВС, если программы поступают случайным образом,
распределенные по экспоненциальному закону с частотой λ=2 1/сек,
а среднее время обработки программы каждым сервером составляет tобр= 3 сек (закон распределения -экспоненциальный)."""

# абсолютная вероятность - относительную умножить на лямбда
from pprint import pprint as pp

from random import expovariate, uniform


class Server:
    """сервер представляет из себя структуру, которая приниманет время паявления программы и создает таймлайн
    , в котором отображены все события связанные с исполнением этих программ"""
    def __init__(self):
        self.programm_number = 1
        server_time = 0
        self.isworking = False
        self.buffer = []
        self.programstart = 0
        self.program_end = 0
        self.program = 0
        self.statystics = {'P0': [0, 0], 'P1': [0, 0], 'P2': [0, 0], 'P3': [0, 0], 'P4': [0, 0], 'Potk': 0,
                           'Q': 0,  'S': 0,
                           'Nprog': 0, 'Tprog': 0,
                           'Nbuf': 0, 'Tbuf': 0}

    def take_program(self, program_itself):
        """
        принимает время через которое приходит следующая программа и  решает что с ней делать
        если буфер пустой и сервер не работает, то отмечает начало и конец исполнения Программы
        если сервер занят то отправляет программу в буфер
        если в буфере больше 3х программ то программа покидает сервер необработанной
        """

        # сервер простаивает до появления нулевой программы
        if not self.statystics['Q']:
            self.statystics['P0'][0] = program_itself.appear_time
            program_itself.cs_enter = program_itself.appear_time

        self.statystics['Q'] += 1
        if self.isworking:
            if program_itself.appear_time >= self.program_end:
                self.program.cs_exit = self.program_end
                self.close_program()
                self.isworking = False
                if len(self.buffer):
                    self.debuffer_program()
                else:
                    # простой сервера
                    pass
            self.buffer_program(program_itself)
        else:
            self.statystics['P1'][0] += program_itself.appear_time - self.statystics['P0'][1]
            self.isworking = True
            self.program = program_itself
            self.programstart = program_itself.appear_time
            self.program_end = program_itself.appear_time + program_itself.process_time
            # self.log.append((time,))

    def buffer_program(self,  program):
        """Кладет программу в буффер, если буффер переполнен, программа выбрасывается"""
        if len(self.buffer) >= 3:
            self.statystics['Potk'] += 1
            program.cs_exit = program.appear_time
            self.throw_program(program)
        else:
            self.buffer.append(program)
            program.buffer_enter = program.appear_time

    def debuffer_program(self):
        """Убирает программу из буфера, уменьшает буфер на 1 записывает в статистику
            когда из буфера была убрана программа"""
        if len(self.buffer) == 0:
            self.statystics['P1'][1] = self.program_end
            self.isworking = False
        else:
            self.isworking = False
            program = self.buffer.pop()
            program.buffer_exit = self.time
            self.take_program(program)

    def close_program(self):
        """Программа выходит из системы после выполнения на сервере"""
        self.programstart = 0
        self.time = self.program_end
        self.program_end = 0
        self.throw_program(self.program)
        self.program = 0

    def throw_program(self, program):
        """ Программа покидает вычислительную систему , неважно по какой причине"""
        self.statystics['Tprog'] += program.cs_exit - program.cs_enter
        self.statystics['Tbuf'] += program.buffer_exit - program.buffer_enter



    def its_showtime(self):
        """
            приводит стаистику в нужный вид: высчитвает среднее значение, вероятности,
             добавляет значок процента, округляет до 4 знаков после запятой, и так далее
        """
        self.statystics['Potk'] = round(self.statystics['Potk'] / self.statystics['Q'], 4)
        self.statystics['P0'] = round(self.statystics['P0'][0] / 3600, 4)
        self.statystics['P1'] = round(self.statystics['P1'][0] / 3600, 4)
        self.statystics['P2'] = round(self.statystics['P2'][0] / 3600, 4)
        self.statystics['P3'] = round(self.statystics['P3'][0] / 3600, 4)
        self.statystics['Tbuf'] = round(self.statystics['Tbuf'], 4)
        self.statystics['Tprog'] = round(self.statystics['Tprog'], 4)
        self.statystics['Q'] = 1 - self.statystics['Potk']
        self.statystics['S'] =self.statystics['Q'] * 2
        pp(self.statystics)


class Program:
    """программа , которая создается генератором и обрабатывается сервером имеет в себе характеристики:
    глобальное время появления, время, необходимое на исполнение время, появления в ВС( по идее время создания,
    программы приходят на сервер мгновенно, и время покидания сервера)"""

    def __init__(self, appear_time, process_time):
        self.appear_time = appear_time
        self.process_time = process_time
        self.cs_enter = self.appear_time
        self.cs_exit = 0
        self.input_time = appear_time
        self.output_time = 0
        self.buffer_enter = 0
        self.buffer_exit = 0

    # def __repr__(self):
    #     return str(self.appear_time) + '\t' + str(self.process_time)


def generate_program_expo(lambd, delta_time):
    """генерирует программу, состоящую из времени начала, времени обработки . ито и то генератор.
    оба времени генерируются экспоненциальным распределением. """
    # global time
    time = 0

    while time < 3600:
        appear_time = expovariate(lambd)
        # appear_time = (appear['Tzmax']-appear['Tzmin'])*appear_time + appear['Tzmin']
        appear_time = time + appear_time

        time = appear_time

        process_time = expovariate(delta_time)
        # process_time = ((process['Tzmax']-process['Tzmin'])*process_time + process['Tzmin'])
        if appear_time >= 3600:
            break
        yield Program(appear_time, process_time)


def generate_program_linear(appear, process):
    """генерирует программу, состоящую из времени начала, времени обработки . ито и то генератор.
    оба времени генерируются экспоненциальным распределением. """
    # global time
    time = 0

    while time < 3600:
        # appear_time = expovariate(lambd_a)
        # appear_time = (appear['Tzmax']-appear['Tzmin'])*appear_time + appear['Tzmin']
        appear_time = uniform(appear['Tzmin'], appear['Tzmax'])
        appear_time = time + appear_time
        time = appear_time

        process_time = uniform(process['Tzmin'], process['Tzmax'])
        # process_time = ((process['Tzmax']-process['Tzmin'])*process_time + process['Tzmin'])
        # if
        yield Program(appear_time, process_time)
