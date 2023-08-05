import numpy as np
from unittest import TestCase

from diffprivlib.mechanisms import Exponential
from diffprivlib.utils import global_seed


class TestExponential(TestCase):
    def setup_method(self, method):
        if method.__name__ .endswith("prob"):
            global_seed(314159)

        self.mech = Exponential

    def teardown_method(self, method):
        del self.mech

    def test_class(self):
        from diffprivlib.mechanisms import DPMechanism
        self.assertTrue(issubclass(Exponential, DPMechanism))

    def test_inf_epsilon(self):
        utility = [1, 0, 0, 0, 0]
        mech = self.mech(epsilon=float("inf"), utility=utility, sensitivity=1)

        for i in range(1000):
            self.assertEqual(mech.randomise(), 0)

    def test_zero_sensitivity(self):
        utility = [1, 0, 0, 0, 0]
        mech = self.mech(epsilon=1, utility=utility, sensitivity=0)

        for i in range(1000):
            self.assertEqual(mech.randomise(), 0)

    def test_nonzero_delta(self):
        utility = [1, 0, 0, 0, 0]
        mech = self.mech(epsilon=1, utility=utility, sensitivity=1)
        mech.delta = 0.1

        with self.assertRaises(ValueError):
            mech.randomise()

    def test_empty_utility(self):
        with self.assertRaises(ValueError):
            self.mech(epsilon=1, utility=[], sensitivity=1)

    def test_neg_sensitivity(self):
        with self.assertRaises(ValueError):
            self.mech(epsilon=1, utility=[1], sensitivity=-1)

    def test_wrong_input_types(self):
        with self.assertRaises(TypeError):
            self.mech(epsilon=1j, utility=[1], sensitivity=1)

        with self.assertRaises(TypeError):
            self.mech(epsilon="1", utility=[1], sensitivity=1)

        with self.assertRaises(TypeError):
            self.mech(epsilon=1, utility=[1j], sensitivity=1)

        with self.assertRaises(TypeError):
            self.mech(epsilon=1, utility=["1"], sensitivity=1)

        with self.assertRaises(TypeError):
            self.mech(epsilon=1, utility=[1], sensitivity=1j)

        with self.assertRaises(TypeError):
            self.mech(epsilon=1, utility=[1], sensitivity="1")

        with self.assertRaises(TypeError):
            self.mech(epsilon=1, utility=(1), sensitivity=1)

        with self.assertRaises(TypeError):
            self.mech(epsilon=1, utility=[1], sensitivity=1, measure=(1))

        with self.assertRaises(TypeError):
            self.mech(epsilon=1, utility=[1], sensitivity=1, measure=[1j])

        with self.assertRaises(TypeError):
            self.mech(epsilon=1, utility=[1], sensitivity=1, candidates=(1))

    def test_wrong_arg_length(self):
        with self.assertRaises(ValueError):
            self.mech(epsilon=1, utility=[1, 2], sensitivity=1, candidates=[1, 2, 3])

        with self.assertRaises(ValueError):
            self.mech(epsilon=1, utility=[1, 2], sensitivity=1, candidates=[1])

        with self.assertRaises(ValueError):
            self.mech(epsilon=1, utility=[1, 2], sensitivity=1, measure=[1, 2, 3])

        with self.assertRaises(ValueError):
            self.mech(epsilon=1, utility=[1, 2], sensitivity=1, measure=[1])

    def test_non_none_input(self):
        mech = self.mech(epsilon=1, sensitivity=1, utility=[0, 1])

        with self.assertRaises(ValueError):
            mech.randomise(1)

    def test_correct_output_domain(self):
        mech = self.mech(epsilon=1, utility=[1, 0, 0, 0, 0], sensitivity=1)
        runs = 100

        for i in range(runs):
            self.assertTrue(0 <= mech.randomise() < 5)

        candidates = ["A", "B", "C", "D", "F"]
        mech = self.mech(epsilon=1, utility=[1, 0, 0, 0, 0], sensitivity=1, candidates=candidates)

        for i in range(runs):
            self.assertIn(mech.randomise(), candidates)

    def test_non_uniform_measure(self):
        measure = [1, 2, 1, 1]
        utility = [1, 1, 0, 0]
        runs = 20000
        mech = self.mech(epsilon=2 * np.log(2), utility=utility, measure=measure, sensitivity=1)
        count = [0] * 4

        for i in range(runs):
            count[mech.randomise()] += 1

        self.assertAlmostEqual(count[1] / count[0], 2, delta=0.1)

    def test_zero_measure(self):
        measure = [1, 1, 0]
        utility = [1, 1, 1]
        runs = 10000
        mech = self.mech(epsilon=1, utility=utility, measure=measure, sensitivity=1)
        count = [0] * 3

        for i in range(runs):
            count[mech.randomise()] += 1

        self.assertEqual(count[2], 0)
        self.assertAlmostEqual(count[0], count[1], delta=runs*0.03)

    def test_inf_utility_measure(self):
        list_with_inf = [1, 0, float("inf")]

        self.assertRaises(ValueError, self.mech, epsilon=1, utility=list_with_inf, sensitivity=1)
        self.assertRaises(ValueError, self.mech, epsilon=1, utility=[1] * 3, measure=list_with_inf, sensitivity=1)

        self.assertRaises(ValueError, self.mech, epsilon=1, utility=[-l for l in list_with_inf], sensitivity=1)
        self.assertRaises(ValueError, self.mech, epsilon=1, utility=[1] * 3, measure=[-l for l in list_with_inf],
                          sensitivity=1)

    def test_distrib_prob(self):
        epsilon = 2 * np.log(2)
        runs = 20000
        mech = self.mech(epsilon=epsilon, utility=[2, 1, 0], sensitivity=1)
        count = [0, 0, 0]

        for i in range(runs):
            count[mech.randomise()] += 1

        # print("A: %d, B: %d, C: %d" % (count[0], count[1], count[2]))
        # print("%f, %f" % (count[0] / count[1], count[1] / count[2]))

        self.assertLessEqual(count[0] / runs, np.exp(epsilon) * count[2] / runs + 0.05)
        # self.assertAlmostEqual(count[0] / count[1], count[1] / count[2], delta=0.2)

    def test_repr(self):
        repr_ = repr(self.mech(epsilon=1, utility=[1], sensitivity=1))
        self.assertIn(".Exponential(", repr_)

    def test_bias(self):
        self.assertRaises(NotImplementedError, self.mech(epsilon=1, utility=[1], sensitivity=1).bias, 0)

    def test_variance(self):
        self.assertRaises(NotImplementedError, self.mech(epsilon=1, utility=[1], sensitivity=1).variance, 0)
