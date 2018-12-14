import cs


def main(gen_type):
    appear = {'Tzmin': 1 / 3, 'Tzmax': 2 / 3}
    process = {'Tzmin': 1, 'Tzmax': 6}
    lambd = 2
    delta_time = 1 / 3

    if gen_type:
        testing_generator = cs.generate_program_expo(lambd, delta_time)
    else:
        testing_generator = cs.generate_program_linear(appear, process)
    testing_server = cs.Server()

    while True:
        try:
            rv = next(testing_generator)
            # print(rv.appear_time)
        except StopIteration:
            break
        testing_server.take_program(rv)

    testing_server.its_showtime()


if __name__ == '__main__':
    main(0)
