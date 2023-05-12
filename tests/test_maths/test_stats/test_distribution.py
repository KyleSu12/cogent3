#!/usr/bin/env python
"""Tests of statistical probability distribution integrals.

Currently using tests against calculations in R, spreadsheets being unreliable.
"""

from unittest import TestCase, main

from numpy.testing import assert_allclose, assert_almost_equal

from cogent3.maths.stats.distribution import (
    bdtr,
    bdtrc,
    bdtri,
    binomial_exact,
    fdtri,
    fprob,
    gdtr,
    gdtrc,
    gdtri,
    pdtr,
    pdtrc,
    pdtri,
    poisson_exact,
    poisson_high,
    poisson_low,
    probability_points,
    stdtr,
    stdtri,
    theoretical_quantiles,
    tprob,
    zprob,
)


class DistributionsTests(TestCase):
    """Tests of particular statistical distributions."""

    def setUp(self):
        self.values = [0, 0.01, 0.1, 0.5, 1, 2, 5, 10, 20, 30, 50, 200]
        self.negvalues = [-i for i in self.values]
        self.df = [1, 10, 100]

    def test_zprob(self):
        """zprob should match twice the z_high probability for abs(z)"""

        probs = [
            2 * i
            for i in [
                5.000000e-01,
                4.960106e-01,
                4.601722e-01,
                3.085375e-01,
                1.586553e-01,
                2.275013e-02,
                2.866516e-07,
                7.619853e-24,
                2.753624e-89,
                4.906714e-198,
                0.000000e00,
                0.000000e00,
            ]
        ]

        for z, p in zip(self.values, probs):
            assert_allclose(zprob(z), p, rtol=1e-6)
        for z, p in zip(self.negvalues, probs):
            assert_allclose(zprob(z), p, rtol=1e-6)

    def test_tprob(self):
        """tprob should match twice the t_high probability for abs(t)"""

        probs = {
            1: [
                2 * i
                for i in [
                    0.500000000,
                    0.496817007,
                    0.468274483,
                    0.352416382,
                    0.250000000,
                    0.147583618,
                    0.062832958,
                    0.031725517,
                    0.015902251,
                    0.010606402,
                    0.006365349,
                    0.001591536,
                ]
            ],
            10: [
                2 * i
                for i in [
                    5.000000e-01,
                    4.961090e-01,
                    4.611604e-01,
                    3.139468e-01,
                    1.704466e-01,
                    3.669402e-02,
                    2.686668e-04,
                    7.947766e-07,
                    1.073031e-09,
                    1.980896e-11,
                    1.237155e-13,
                    1.200254e-19,
                ]
            ],
            100: [
                2 * i
                for i in [
                    5.000000e-01,
                    4.960206e-01,
                    4.602723e-01,
                    3.090868e-01,
                    1.598621e-01,
                    2.410609e-02,
                    1.225087e-06,
                    4.950844e-17,
                    4.997134e-37,
                    4.190166e-52,
                    7.236082e-73,
                    2.774197e-132,
                ]
            ],
        }
        for df in self.df:
            for x, p in zip(self.values, probs[df]):
                assert_almost_equal(tprob(x, df), p, decimal=4)

    def test_poisson_low(self):
        """Lower tail of poisson should match R for integer successes"""
        # WARNING: Results only guaranteed for integer successes: floating
        # point _should_ yield reasonable values, but R rounds to int.
        expected = {
            (0, 0): 1,
            (0, 0.75): 0.4723666,
            (0, 1): 0.3678794,
            (0, 5): 0.006737947,
            (0, 113.7): 4.175586e-50,
            (2, 0): 1,
            (2, 3): 0.4231901,
            (2, 17.8): 3.296636e-06,
            (17, 29.6): 0.008753318,
            (180, 0): 1,
            (180, 137.4): 0.999784,
            (180, 318): 2.436995e-17,
            (180, 1024): 8.266457e-233,
        }
        for key, value in list(expected.items()):
            assert_allclose(poisson_low(*key), value, rtol=1e-6)

    def test_poisson_high(self):
        """Upper tail of poisson should match R for integer successes"""
        # WARNING: Results only guaranteed for integer successes: floating
        # point _should_ yield reasonable values, but R rounds to int.
        expected = {
            (0, 0): 0,
            (0, 0.75): 0.5276334,
            (0, 1): 0.6321206,
            (0, 5): 0.993262,
            (0, 113.7): 1,
            (2, 0): 0,
            (2, 3): 0.5768099,
            (2, 17.8): 0.9999967,
            (17, 29.6): 0.9912467,
            (180, 0): 0,
            (180, 137.4): 0.0002159856,
            (180, 318): 1,
            (180, 1024): 1,
        }
        for key, value in list(expected.items()):
            assert_allclose(poisson_high(*key), value)

    def test_poisson_exact(self):
        """Poisson exact should match expected values from R"""
        expected = {
            (0, 0): 1,
            (0, 0.75): 0.4723666,
            (0, 1): 0.3678794,
            (0, 5): 0.006737947,
            (0, 113.7): 4.175586e-50,
            (2, 0): 0,
            (2, 3): 0.2240418,
            (2, 17.8): 2.946919e-06,
            (17, 29.6): 0.004034353,
            (180, 0): 0,
            (180, 137.4): 7.287501e-05,
            (180, 318): 1.067247e-17,
            (180, 1024): 6.815085e-233,
        }
        for key, value in list(expected.items()):
            assert_allclose(poisson_exact(*key), value, rtol=1e-6)

    def test_binomial_series(self):
        """binomial_exact should match values from R on a whole series"""
        expected = list(
            map(
                float,
                "0.0282475249 0.1210608210 0.2334744405 0.2668279320 0.2001209490 0.1029193452 0.0367569090 0.0090016920 0.0014467005 0.0001377810 0.0000059049".split(),
            )
        )

        for i in range(len(expected)):
            assert_allclose(binomial_exact(i, 10, 0.3), expected[i])

    def test_binomial_exact(self):
        """binomial_exact should match values from R for integer successes"""
        expected = {
            (0, 1, 0.5): 0.5,
            (1, 1, 0.5): 0.5,
            (1, 1, 0.0000001): 1e-07,
            (1, 1, 0.9999999): 0.9999999,
            (3, 5, 0.75): 0.2636719,
            (0, 60, 0.5): 8.673617e-19,
            (129, 130, 0.5): 9.550892e-38,
            (299, 300, 0.099): 1.338965e-298,
            (9, 27, 0.0003): 9.175389e-26,
            (1032, 2050, 0.5): 0.01679804,
        }
        for key, value in list(expected.items()):
            assert_almost_equal(binomial_exact(*key), value, 1e-4)

    def test_binomial_exact_floats(self):
        """binomial_exact should be within limits for floating point numbers"""
        expected = {
            (18.3, 100, 0.2): (0.09089812, 0.09807429),
            (2.7, 1050, 0.006): (0.03615498, 0.07623827),
            (2.7, 1050, 0.06): (1.365299e-25, 3.044327e-24),
            (2, 100.5, 0.6): (7.303533e-37, 1.789727e-36),
            (10, 100.5, 0.5): (7.578011e-18, 1.365543e-17),
            (0.2, 60, 0.5): (8.673617e-19, 5.20417e-17),
            (0.5, 5, 0.3): (0.16807, 0.36015),
        }

        for key, value in list(expected.items()):
            min_val, max_val = value
            assert min_val < binomial_exact(*key) < max_val
            # assert_almost_equal(binomial_exact(*key), value, 1e-4)

    def test_binomial_exact_errors(self):
        """binomial_exact should raise errors on invalid input"""
        self.assertRaises(ValueError, binomial_exact, 10.2, 5, 0.33)
        self.assertRaises(ValueError, binomial_exact, -2, 5, 0.33)
        self.assertRaises(ValueError, binomial_exact, 10, 50, -2)
        self.assertRaises(ValueError, binomial_exact, 10, 50, 3)

    def test_fprob(self):
        """fprob should return twice the tail on a particular side"""
        error = 1e-4
        # right-hand side
        assert_allclose(fprob(10, 10, 1.2), 0.7788, rtol=error)
        # left-hand side
        assert_allclose(fprob(10, 10, 1.2, side="left"), 1.2212, rtol=error)
        self.assertRaises(ValueError, fprob, 10, 10, -3)
        self.assertRaises(ValueError, fprob, 10, 10, 1, "non_valid_side")

    def test_stdtr(self):
        """stdtr should match cephes results"""
        t = [-10, -3.1, -0.5, -0.01, 0, 1, 0.5, 10]
        k = [2, 10, 100]
        exp = [
            0.00492622851166,
            7.94776587798e-07,
            4.9508444923e-17,
            0.0451003650651,
            0.00562532860804,
            0.00125696358826,
            0.333333333333,
            0.313946802871,
            0.309086782915,
            0.496464554479,
            0.496108987495,
            0.496020605117,
            0.5,
            0.5,
            0.5,
            0.788675134595,
            0.829553433849,
            0.840137922108,
            0.666666666667,
            0.686053197129,
            0.690913217085,
            0.995073771488,
            0.999999205223,
            1.0,
        ]
        index = 0
        for i in t:
            for j in k:
                assert_allclose(stdtr(j, i), exp[index])
                index += 1

    def test_bdtr(self):
        """bdtr should match cephes results"""
        k_s = [0, 1, 2, 3, 5]
        n_s = [5, 10, 1000]
        p_s = [1e-10, 0.1, 0.5, 0.9, 0.999999]
        exp = [
            0.9999999995,
            0.59049,
            0.03125,
            1e-05,
            1.00000000014e-30,
            0.999999999,
            0.3486784401,
            0.0009765625,
            1e-10,
            1.00000000029e-60,
            0.9999999,
            1.74787125172e-46,
            9.33263618503e-302,
            0.0,
            0.0,
            1.0,
            0.91854,
            0.1875,
            0.00046,
            4.99999600058e-24,
            1.0,
            0.7360989291,
            0.0107421875,
            9.1e-09,
            9.99999100259e-54,
            1.0,
            1.9595578811e-44,
            9.34196882121e-299,
            0.0,
            0.0,
            1.0,
            0.99144,
            0.5,
            0.00856,
            9.99998500087e-18,
            1.0,
            0.9298091736,
            0.0546875,
            3.736e-07,
            4.49999200104e-47,
            1.0,
            1.09744951737e-42,
            4.67099374325e-296,
            0.0,
            0.0,
            1.0,
            0.99954,
            0.8125,
            0.08146,
            9.99998000059e-12,
            1.0,
            0.9872048016,
            0.171875,
            9.1216e-06,
            1.19999685024e-40,
            1.0,
            4.09381247279e-41,
            1.5554471507e-293,
            0.0,
            0.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            0.9998530974,
            0.623046875,
            0.0016349374,
            2.51998950038e-28,
            1.0,
            2.55654569306e-38,
            7.7385053063e-289,
            0.0,
            0.0,
        ]
        index = 0
        for k in k_s:
            for n in n_s:
                for p in p_s:
                    assert_allclose(bdtr(k, n, p), exp[index])
                    index += 1

    def test_bdtrc(self):
        """bdtrc should give same results as cephes"""
        k_s = [0, 1, 2, 3, 5]
        n_s = [5, 10, 1000]
        p_s = [1e-10, 0.1, 0.5, 0.9, 0.999999]

        exp = [
            4.999999999e-10,
            0.40951,
            0.96875,
            0.99999,
            1.0,
            9.9999999955e-10,
            0.6513215599,
            0.9990234375,
            0.9999999999,
            1.0,
            9.9999995005e-08,
            1.0,
            1.0,
            1.0,
            1.0,
            9.999999998e-20,
            0.08146,
            0.8125,
            0.99954,
            1.0,
            4.4999999976e-19,
            0.2639010709,
            0.9892578125,
            0.9999999909,
            1.0,
            4.99499966766e-15,
            1.0,
            1.0,
            1.0,
            1.0,
            9.9999999985e-30,
            0.00856,
            0.5,
            0.99144,
            1.0,
            1.19999999937e-28,
            0.0701908264,
            0.9453125,
            0.9999996264,
            1.0,
            1.66166987575e-22,
            1.0,
            1.0,
            1.0,
            1.0,
            4.9999999996e-40,
            0.00046,
            0.1875,
            0.91854,
            0.99999999999,
            2.09999999899e-38,
            0.0127951984,
            0.828125,
            0.9999908784,
            1.0,
            4.14171214499e-30,
            1.0,
            1.0,
            1.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            2.09999999928e-58,
            0.0001469026,
            0.376953125,
            0.9983650626,
            1.0,
            1.36817318242e-45,
            1.0,
            1.0,
            1.0,
            1.0,
        ]
        index = 0
        for k in k_s:
            for n in n_s:
                for p in p_s:
                    assert_allclose(bdtrc(k, n, p), exp[index])
                    index += 1

    def test_pdtr(self):
        """pdtr should match cephes results"""
        k_s = [0, 1, 2, 5, 10]
        m_s = [1e-9, 0.1, 0.5, 1, 2, 31]
        exp = [
            0.999999999,
            0.904837418036,
            0.606530659713,
            0.367879441171,
            0.135335283237,
            3.44247710847e-14,
            1.0,
            0.99532115984,
            0.909795989569,
            0.735758882343,
            0.40600584971,
            1.10159267471e-12,
            1.0,
            0.99984534693,
            0.985612322033,
            0.919698602929,
            0.676676416183,
            1.76426951809e-11,
            1.0,
            0.999999998725,
            0.999985835063,
            0.999405815182,
            0.983436391519,
            9.72616712615e-09,
            1.0,
            1.0,
            0.999999999992,
            0.999999989952,
            0.999991691776,
            1.12519146046e-05,
        ]
        index = 0
        for k in k_s:
            for m in m_s:
                assert_allclose(pdtr(k, m), exp[index])
                index += 1

    def test_pdtrc(self):
        """pdtrc should match cephes results"""
        k_s = [0, 1, 2, 5, 10]
        m_s = [1e-9, 0.1, 0.5, 1, 2, 31]
        exp = [
            9.999999995e-10,
            0.095162581964,
            0.393469340287,
            0.632120558829,
            0.864664716763,
            1.0,
            4.99999999667e-19,
            0.00467884016044,
            0.090204010431,
            0.264241117657,
            0.59399415029,
            0.999999999999,
            1.66666666542e-28,
            0.000154653070265,
            0.014387677967,
            0.0803013970714,
            0.323323583817,
            0.999999999982,
            1.3888888877e-57,
            1.27489869223e-09,
            1.41649373223e-05,
            0.000594184817582,
            0.0165636084806,
            0.999999990274,
            2.50521083625e-107,
            2.28584493079e-19,
            7.74084073923e-12,
            1.00477663757e-08,
            8.30822436848e-06,
            0.999988748085,
        ]
        index = 0
        for k in k_s:
            for m in m_s:
                assert_allclose(pdtrc(k, m), exp[index])
                index += 1

    def test_gdtr(self):
        """gdtr should match cephes results"""
        a_s = [1, 2, 10, 1000]
        b_s = a_s
        x_s = [0, 0.01, 0.5, 10, 521.4]
        exp = [
            0.0,
            0.00995016625083,
            0.393469340287,
            0.99995460007,
            1.0,
            0.0,
            4.96679133403e-05,
            0.090204010431,
            0.999500600773,
            1.0,
            0.0,
            2.7307942837e-27,
            1.70967002935e-10,
            0.542070285528,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            2.78154480191e-77,
            0.0,
            0.0198013266932,
            0.632120558829,
            0.999999997939,
            1.0,
            0.0,
            0.00019735322711,
            0.264241117657,
            0.999999956716,
            1.0,
            0.0,
            2.77103020131e-24,
            1.11425478339e-07,
            0.995004587692,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.91070640569,
            0.0,
            0.095162581964,
            0.993262053001,
            1.0,
            1.0,
            0.0,
            0.00467884016044,
            0.959572318005,
            1.0,
            1.0,
            0.0,
            2.51634780677e-17,
            0.0318280573062,
            1.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.99995460007,
            1.0,
            1.0,
            1.0,
            0.0,
            0.999500600773,
            1.0,
            1.0,
            1.0,
            0.0,
            0.542070285528,
            1.0,
            1.0,
            1.0,
            0.0,
            0.0,
            3.29827279707e-86,
            1.0,
            1.0,
        ]
        index = 0
        for a in a_s:
            for b in b_s:
                for x in x_s:
                    assert_allclose(gdtr(a, b, x), exp[index])
                    index += 1

    def test_gdtrc(self):
        """gdtrc should match cephes results"""
        a_s = [1, 2, 10, 1000]
        b_s = a_s
        x_s = [0, 0.01, 0.5, 10, 521.4]
        exp = [
            1.0,
            0.990049833749,
            0.606530659713,
            4.53999297625e-05,
            3.62123855523e-227,
            1.0,
            0.999950332087,
            0.909795989569,
            0.000499399227387,
            1.89173502125e-224,
            1.0,
            1.0,
            0.999999999829,
            0.457929714472,
            2.89188102723e-208,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            0.980198673307,
            0.367879441171,
            2.06115362244e-09,
            0.0,
            1.0,
            0.999802646773,
            0.735758882343,
            4.32842260712e-08,
            0.0,
            1.0,
            1.0,
            0.999999888575,
            0.00499541230831,
            0.0,
            1.0,
            1.0,
            1.0,
            1.0,
            0.0892935943104,
            1.0,
            0.904837418036,
            0.00673794699909,
            3.72007597602e-44,
            0.0,
            1.0,
            0.99532115984,
            0.0404276819945,
            3.75727673578e-42,
            0.0,
            1.0,
            1.0,
            0.968171942694,
            1.12534739608e-31,
            0.0,
            1.0,
            1.0,
            1.0,
            1.0,
            0.0,
            1.0,
            4.53999297625e-05,
            7.12457640674e-218,
            0.0,
            0.0,
            1.0,
            0.000499399227387,
            3.56941277978e-215,
            0.0,
            0.0,
            1.0,
            0.457929714472,
            3.90479663912e-199,
            0.0,
            0.0,
            1.0,
            1.0,
            1.0,
            0.0,
            0.0,
        ]
        index = 0
        for a in a_s:
            for b in b_s:
                for x in x_s:
                    assert_allclose(gdtrc(a, b, x), exp[index])
                    index += 1

    def test_stdtri(self):
        """stdtri should match cephes results"""
        k_s = [1, 2, 5, 10, 100]
        p_s = [1e-50, 1e-9, 0.02, 0.5, 0.8, 0.99]
        exp = [
            -3.18309886184e49,
            -318309886.184,
            -15.8945448441,
            8.1775627727e-17,
            1.37638192049,
            31.8205159538,
            -7.07106781216e24,
            -22360.6797414,
            -4.84873221444,
            7.48293180888e-17,
            1.06066017178,
            6.96455671876,
            -15683925591.1,
            -98.9372246484,
            -2.75650852191,
            6.976003623e-17,
            0.919543780236,
            3.36492999891,
            -256452.571877,
            -20.1446977667,
            -2.35931462368,
            6.80574793291e-17,
            0.879057828551,
            2.76376945745,
            -28.9584072963,
            -6.59893982023,
            -2.08088390123,
            6.6546053747e-17,
            0.845230424487,
            2.3642173659,
        ]
        index = 0
        for k in k_s:
            for p in p_s:
                assert_allclose(stdtri(k, p), exp[index], rtol=1e-6, atol=1e-6)
                index += 1

    def test_pdtri(self):
        """pdtri should match cephes results"""
        k_s = [1, 2, 5, 10, 100]
        p_s = [1e-50, 1e-9, 0.02, 0.5, 0.8, 0.99]
        exp = [
            119.924420375,
            23.9397278656,
            5.83392170192,
            1.67834699002,
            0.824388309033,
            0.148554740253,
            124.094307191,
            26.6722865587,
            7.51660387561,
            2.67406031372,
            1.53504420264,
            0.436045165078,
            134.901981814,
            33.6746016741,
            12.0269783451,
            5.67016118871,
            3.90366383933,
            1.7852844853,
            150.2138305,
            43.627975401,
            18.8297496417,
            10.6685224038,
            8.15701989758,
            4.77124616939,
            332.371212972,
            173.368244558,
            122.695978128,
            100.666862949,
            92.4593447729,
            79.0999186597,
        ]
        index = 0
        for k in k_s:
            for p in p_s:
                assert_allclose(pdtri(k, p), exp[index])
                index += 1

    def test_bdtri(self):
        """bdtri should match cephes results"""
        k_s = [0, 1, 2, 3]
        n_s = [5, 10, 1000]
        p_s = [1e-10, 0.1, 0.5, 0.9, 0.999999]
        exp = [
            0.99,
            0.36904265552,
            0.129449436704,
            0.020851637639,
            2.00000080006e-07,
            0.9,
            0.205671765276,
            0.0669670084632,
            0.0104807417938,
            1.00000045003e-07,
            0.0227627790442,
            0.00229993617745,
            0.000692907009547,
            0.000105354965434,
            1.00000049953e-09,
            0.997884361719,
            0.58389037462,
            0.313810170456,
            0.112234958546,
            0.000316327821398,
            0.939678616058,
            0.336847723307,
            0.162262728195,
            0.0545286199977,
            0.00014913049349,
            0.0260030189545,
            0.0038841043984,
            0.00167777786542,
            0.000531936197341,
            1.415587631e-06,
            0.999784533318,
            0.753363546712,
            0.5,
            0.246636453288,
            0.00465241636163,
            0.964779035441,
            0.449603888674,
            0.258574723285,
            0.11582527803,
            0.00203463563411,
            0.0287538329681,
            0.00531348536403,
            0.00267315927217,
            0.00110256069953,
            1.82723947076e-05,
            0.999996837712,
            0.887765041454,
            0.686189829544,
            0.41610962538,
            0.0212382182007,
            0.981054188003,
            0.551730832384,
            0.355099967912,
            0.187562296647,
            0.00839131408953,
            0.0312483560212,
            0.00666849533707,
            0.00367082709364,
            0.00174586632568,
            7.10965576424e-05,
        ]
        index = 0
        for k in k_s:
            for n in n_s:
                for p in p_s:
                    assert_allclose(bdtri(k, n, p), exp[index])
                    index += 1

    def test_gdtri(self):
        """gdtri should match cephes results"""
        k_s = [1, 2, 4, 10, 100]
        n_s = k_s
        p_s = [1e-9, 0.02, 0.5, 0.8, 0.99]
        exp = [
            1.0000000005e-09,
            0.0202027073175,
            0.69314718056,
            1.60943791243,
            4.60517018599,
            4.47220262303e-05,
            0.214699095008,
            1.67834699002,
            2.994308347,
            6.63835206799,
            0.0124777531242,
            1.01623845904,
            3.67206074885,
            5.51504571515,
            10.0451175148,
            0.602134838869,
            4.61834927756,
            9.66871461471,
            12.5187528198,
            18.7831173933,
            51.1433022288,
            80.5501391278,
            99.6668649193,
            108.304391619,
            124.722561491,
            5.0000000025e-10,
            0.0101013536588,
            0.34657359028,
            0.804718956217,
            2.30258509299,
            2.23610131152e-05,
            0.107349547504,
            0.839173495008,
            1.4971541735,
            3.319176034,
            0.00623887656209,
            0.50811922952,
            1.83603037443,
            2.75752285758,
            5.02255875742,
            0.301067419435,
            2.30917463878,
            4.83435730736,
            6.25937640991,
            9.39155869666,
            25.5716511144,
            40.2750695639,
            49.8334324597,
            54.1521958095,
            62.3612807454,
            2.50000000125e-10,
            0.00505067682938,
            0.17328679514,
            0.402359478109,
            1.1512925465,
            1.11805065576e-05,
            0.053674773752,
            0.419586747504,
            0.748577086751,
            1.659588017,
            0.00311943828105,
            0.25405961476,
            0.918015187213,
            1.37876142879,
            2.51127937871,
            0.150533709717,
            1.15458731939,
            2.41717865368,
            3.12968820495,
            4.69577934833,
            12.7858255572,
            20.1375347819,
            24.9167162298,
            27.0760979048,
            31.1806403727,
            1.0000000005e-10,
            0.00202027073175,
            0.069314718056,
            0.160943791243,
            0.460517018599,
            4.47220262303e-06,
            0.0214699095008,
            0.167834699002,
            0.2994308347,
            0.663835206799,
            0.00124777531242,
            0.101623845904,
            0.367206074885,
            0.551504571515,
            1.00451175148,
            0.0602134838869,
            0.461834927756,
            0.966871461471,
            1.25187528198,
            1.87831173933,
            5.11433022288,
            8.05501391278,
            9.96668649193,
            10.8304391619,
            12.4722561491,
            1.0000000005e-11,
            0.000202027073175,
            0.0069314718056,
            0.0160943791243,
            0.0460517018599,
            4.47220262303e-07,
            0.00214699095008,
            0.0167834699002,
            0.02994308347,
            0.0663835206799,
            0.000124777531242,
            0.0101623845904,
            0.0367206074885,
            0.0551504571515,
            0.100451175148,
            0.00602134838869,
            0.0461834927756,
            0.0966871461471,
            0.125187528198,
            0.187831173933,
            0.511433022288,
            0.805501391278,
            0.996668649193,
            1.08304391619,
            1.24722561491,
        ]
        index = 0
        for k in k_s:
            for n in n_s:
                for p in p_s:
                    assert_allclose(gdtri(k, n, p), exp[index], rtol=1e-6)
                    index += 1

    def test_fdtri(self):
        """fdtri should match cephes results"""
        k_s = [1, 2, 4, 10, 100]
        n_s = k_s
        p_s = [1e-50, 1e-9, 0.02, 0.5, 0.8, 0.99]
        exp = [
            0.0,
            2.46740096071e-18,
            0.000987610197427,
            1.0,
            9.472135955,
            4052.18069548,
            0.0,
            1.99999988687e-18,
            0.000800320128051,
            0.666666666667,
            3.55555555556,
            98.5025125628,
            0.0,
            1.77777767722e-18,
            0.000711321880645,
            0.548632170413,
            2.35072147881,
            21.1976895844,
            0.0,
            1.65119668161e-18,
            0.000660638708985,
            0.489736921158,
            1.88288794493,
            10.0442892734,
            0.0,
            1.57866975531e-18,
            0.000631602221127,
            0.458262714634,
            1.66429288986,
            6.89530103058,
            0.0,
            9.99999973218e-10,
            0.0206164098292,
            1.5,
            12.0,
            4999.5,
            0.0,
            9.99999972718e-10,
            0.0204081632653,
            1.0,
            4.0,
            99.0,
            0.0,
            9.99999972468e-10,
            0.0203050891044,
            0.828427124746,
            2.472135955,
            18.0,
            0.0,
            9.99999972318e-10,
            0.0202435772829,
            0.743491774985,
            1.89864830731,
            7.55943215755,
            0.0,
            9.99999972228e-10,
            0.0202067893611,
            0.697973989501,
            1.63562099482,
            4.82390980716,
            0.0,
            1.29104998825e-05,
            0.0712270257663,
            1.82271484235,
            13.6443218387,
            5624.58332963,
            0.0,
            1.58118880931e-05,
            0.082357834815,
            1.20710678119,
            4.2360679775,
            99.2493718553,
            0.0,
            1.82578627816e-05,
            0.0917479893415,
            1.0,
            2.48261291932,
            15.9770248526,
            0.0,
            2.04128031324e-05,
            0.0999726146531,
            0.898817134423,
            1.82861100515,
            5.99433866163,
            0.0,
            2.21407117017e-05,
            0.106518545067,
            0.844891468084,
            1.5273126184,
            3.5126840636,
            0.0,
            0.00213897888638,
            0.130917099116,
            2.04191262042,
            14.7718897826,
            6055.8467074,
            0.0,
            0.00322083313175,
            0.168531162323,
            1.34500479177,
            4.38216390487,
            99.3991959745,
            0.0,
            0.00448830777955,
            0.207656634378,
            1.11257336081,
            2.45957986729,
            14.5459008033,
            0.0,
            0.00608578074458,
            0.251574092492,
            1.0,
            1.73159473193,
            4.84914680208,
            0.0,
            0.00800159033308,
            0.298648905106,
            0.940477156977,
            1.38089597558,
            2.50331112688,
            0.0,
            3.09672866088e-11,
            0.178906118636,
            2.18215440197,
            15.4973240414,
            6334.110036,
            0.0,
            5.2776234633e-11,
            0.2457526061,
            1.43271814572,
            4.47142755584,
            99.4891628084,
            0.0,
            0.0659164713677,
            0.326585865322,
            1.18358397235,
            2.43020291912,
            13.5769915067,
            0.0,
            0.119865858243,
            0.442669184276,
            1.06329004653,
            1.63265061785,
            4.01371941549,
            0.0,
            0.289673110482,
            0.661509869668,
            1.0,
            1.1839371445,
            1.59766912303,
        ]
        index = 0
        for k in k_s:
            for n in n_s:
                for p in p_s:
                    assert_allclose(fdtri(k, n, p), exp[index])
                    index += 1

    def test_probability_points(self):
        """generates evenly spaced probabilities"""
        expect = (
            0.1190476190476190,
            0.3095238095238095,
            0.5000000000000000,
            0.6904761904761905,
            0.8809523809523809,
        )
        got = probability_points(5)
        assert_almost_equal(got, expect)
        expect = (
            0.04545454545454546,
            0.13636363636363635,
            0.22727272727272727,
            0.31818181818181818,
            0.40909090909090912,
            0.50000000000000000,
            0.59090909090909094,
            0.68181818181818177,
            0.77272727272727271,
            0.86363636363636365,
            0.95454545454545459,
        )
        got = probability_points(11)
        assert_almost_equal(got, expect)

    def test_theoretical_quantiles(self):
        """correctly produce theoretical quantiles"""
        expect = probability_points(4)
        got = theoretical_quantiles(4, dist="uniform")
        assert_almost_equal(got, expect)
        expect = (
            -1.049131397963971,
            -0.299306910465667,
            0.299306910465667,
            1.049131397963971,
        )
        probability_points(4)
        got = theoretical_quantiles(len(expect), dist="normal")
        assert_almost_equal(got, expect)

        # for gamma with shape 2, scale 1/3
        expect = [
            3.833845224364122,
            1.922822334309249,
            0.9636761737854768,
            0.3181293892593747,
        ]
        got = theoretical_quantiles(4, "chisq", 2)
        assert_almost_equal(got, expect)

        expect = (
            -1.2064470985524887,
            -0.3203979544794824,
            0.3203979544794824,
            1.2064470985524887,
        )
        got = theoretical_quantiles(4, "t", 4)
        assert_almost_equal(got, expect)


if __name__ == "__main__":
    main()
