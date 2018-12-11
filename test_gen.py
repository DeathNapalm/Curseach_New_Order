import unittest
import cs
from fractions import Fraction as fr

class TestGenMethods(unittest.TestCase):

    def test_generator(self):
        appear = {'Tzmin' : fr(1,3), 'Tzmax' : fr(2,3)}
        process = {'Tzmin' : fr(1,1), 'Tzmax' : fr(6,1)}

        testing_subject = cs.generate_programm(appear, process)
        while():
            print(testing_subject())


if __name__ == '__main__':
    unittest.main()
