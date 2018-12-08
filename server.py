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

#абсолютная вероятность - относительную умножить на лямбда
from random import expovariate, uniform
# lambd_a = 1/2
# delta_time = 1/3
class Server():
    """сервер представляет из себя структуру, которая приниманет время паявления программы и создает таймлайн
    , в котором отображены все события связанные с исполнением этих программ"""
    def __init__(self):
        self.programm_number = 1
        global time
        time = 0
        self.log = []
        self.isworking = False
        self.buffer = 0
        self.programstart = 0
        self.programend = 0
        self.statystics = {'P0': 0, 'P1': 0, 'P2' : 0, 'P3': 0, 'P4': 0, 'Q': 0,  'S': 0,'Potk': 0,
                           'Nprog': 0, 'Tprog': 0, 'Nbuf': 0, 'Tbuf':0}

    def take_program(self, program_itself):
        """
        принимает время через которое приходит следующая программа и  решает что с ней делать
        если буфер пустой и сервер не работает, то отмечает начало и конец исполнения Программы
        если сервер занят то отправляет программу в буфер
        если в буфере больше 3х программ то программа покидает сервер необработанной
        """
        self.statystics['Q'] += 1
        #TODO добавить вариант простоя сервера
        #time = time + program_appear_time
        if self.isworking:
            if program_itself.appear_time > self.programmend:
                self.close_program()
                self.debuffer_program()
            self.buffer_programm(program_itself)
        else:
            self.isworking = True
            self.programstart = program_itself.appear_time
            self.progrmand  = program_itself.process_time#+ generate_process_time
            #self.log.append((time,))



    def buffer_programm(self,  program):
        if len(self.buffer)>=3:
            self.log.append((time,'програма покинула сервер необработанной'))
            self.statystics['Potk']+=1
        else:
            self.buffer+=1
            self.log.append((time,'в буфере теперь {} программ'.format(self.buffer)))

    def debuffer_program(self):
        """Убирает программу из буфера, уменьшает буфер на 1 записывает в статистику
            когда из буфера была убрана программа    """
        pass


    def its_showtime(self):
        print(self.statystics)

class Program():
    """программа , которая создается генератором и обрабатывается сервером имеет в себе характеристики:
    глобальное время появления, время, необходимое на исполнение время, появления в ВС( по идее время создания,
    программы приходят на сервер мгновенно, и время покидания сервера)"""

    def __init__(self, appear_time, process_time):
        self.appear_time = appear_time
        self.process_time = process_time
        self.input_time = appear_time
        self.output_time = 0

def generate_programm(lambd, delta_time):
    """генерирует программу, состоящую из времени начала, времени обработки . ито и то генератор.
    оба времени генерируются экспоненциальным распределением. """
    global time
    time  = 0

    while time<3600:
        appear_time = expovariate(lambd)
        #appear_time = (appear['Tzmax']-appear['Tzmin'])*appear_time + appear['Tzmin']
        appear_time = time + appear_time

        time = appear_time

        process_time = expovariate(delta_time)
        #process_time = ((process['Tzmax']-process['Tzmin'])*process_time + process['Tzmin'])
        if appear_time>=3600: break
        yield Program(appear_time, process_time)


def generate_programm_linear(appear, process):
    """генерирует программу, состоящую из времени начала, времени обработки . ито и то генератор.
    оба времени генерируются экспоненциальным распределением. """
    time = 0

    while time<3600:
        #appear_time = expovariate(lambd_a)
        #appear_time = (appear['Tzmax']-appear['Tzmin'])*appear_time + appear['Tzmin']
        appear_time = uniform(appear['Tzmin'], appear['Tzmax'])
        appear_time = time + appear_time
        time = appear_time

        process_time = uniform(process['Tzmin'], process['Tzmax'])
        #process_time = ((process['Tzmax']-process['Tzmin'])*process_time + process['Tzmin'])
        #if
        yield Program(appear_time, process_time)



# def generate_timings(server_instance, program):
#     """создавать время начала и время окончания программы, вызывать take_program от каждого из времён"""
#     server_instance.take_program(program[0])
#     server_instance.statystics['Q']+=1
#     server_instance.take_program(program[0]+program[1])
