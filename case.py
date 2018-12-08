from fractions import Fraction as fr
import server
#вывести сюда все константы из условия
appear = {'Tzmin' : fr(1,3), 'Tzmax' : fr(2,3)}
process = {'Tzmin' : fr(1,1), 'Tzmax' : fr(6,1)}
def main():
    now = server.generate_programm()
    while server.time <=3600:
        pass
    print(now)


if __name__ == '__main__':
    main()
