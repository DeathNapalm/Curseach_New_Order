
import server
from fractions import Fraction as fr
def main():
    test_generator_expo()


def test_generator_expo():
    # appear = {'Tzmin' : fr(1,3), 'Tzmax' : fr(2,3)}
    # process = {'Tzmin' : fr(1,1), 'Tzmax' : fr(6,1)}

    lambd = 2
    delta_time = 1/3
    testing_subject = server.generate_programm(lambd, delta_time)
    testing_server = server.Server()

    while(True):
        #rv = testing_subject()
        try:
            rv = next(testing_subject)
        except StopIteration :
            print('stop')
            break
        server.generate_timings(testing_server, rv)
        print(*rv, sep='\t')
    testing_server.its_showtime()


def test_generator_linear():
    appear = {'Tzmin' : 1/3, 'Tzmax' : 2/3}
    process = {'Tzmin' : 1, 'Tzmax' : 6}
    testing_subject = server.generate_programm_linear(appear, process)
    while(True):
        #rv = testing_subject()
        try:
            print(*next(testing_subject), sep='\t')
        except StopIteration :
            print('stop')
            break


if __name__ == '__main__':
    main()
    #test_generator_expo()
    #test_generator_linear()
