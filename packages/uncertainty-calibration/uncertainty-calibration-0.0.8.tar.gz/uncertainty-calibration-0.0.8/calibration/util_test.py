import unittest
from parameterized import parameterized
from utils import *
from utils import _get_ce
import numpy as np


import collections


def multiset_equal(list1, list2):
    return collections.Counter(list1) == collections.Counter(list2)


def list_to_tuple(l):
    if not isinstance(l, list):
        return l
    return tuple(list_to_tuple(x) for x in l)


class TestUtilMethods(unittest.TestCase):

    def test_split(self):
        self.assertEqual(split([1, 3, 2, 4], parts=2), [[1, 3], [2, 4]])
        self.assertEqual(split([1], parts=1), [[1]])
        self.assertEqual(split([2, 3], parts=1), [[2, 3]])
        self.assertEqual(split([2, 3], parts=2), [[2], [3]])
        self.assertEqual(split([1, 2, 3], parts=1), [[1, 2, 3]])
        self.assertEqual(split([1, 2, 3], parts=2), [[1, 2], [3]])
        self.assertEqual(split([1, 2, 3], parts=3), [[1], [2], [3]])

    def test_get_1_equal_bin(self):
        probs = [0.3, 0.5, 0.2, 0.3, 0.5, 0.7]
        bins = get_equal_bins(probs, num_bins=1)
        self.assertEqual(bins, [1.0])

    def test_get_2_equal_bins(self):
        probs = [0.3, 0.5, 0.2, 0.3, 0.5, 0.7]
        bins = get_equal_bins(probs, num_bins=2)
        self.assertEqual(bins, [0.4, 1.0])

    def test_get_3_equal_bins(self):
        probs = [0.3, 0.5, 0.2, 0.3, 0.5, 0.7]
        bins = get_equal_bins(probs, num_bins=3)
        self.assertEqual(bins, [0.3, 0.5, 1.0])

    def test_get_3_equal_bins_lots_of_1s(self):
        probs = [0.3, 0.5, 1.0, 1.0, 1.0, 1.0]
        bins = get_equal_bins(probs, num_bins=3)
        self.assertEqual(bins, [0.75, 1.0])

    def test_get_3_equal_bins_uneven_sizes(self):
        probs = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        bins = np.array(get_equal_bins(probs, num_bins=3))
        self.assertTrue(np.allclose(bins, np.array([0.55, 0.85, 1.0])))

    def test_get_1_equal_prob_bins(self):
        probs = [0.3, 0.5, 0.2, 0.3, 0.5, 0.7]
        bins = get_equal_prob_bins(probs, num_bins=1)
        self.assertEqual(bins, [1.0])

    def test_get_2_equal_prob_bins(self):
        probs = [0.3, 0.5, 0.2, 0.3, 0.5, 0.7]
        bins = get_equal_prob_bins(probs, num_bins=2)
        self.assertEqual(bins, [0.5, 1.0])

    def test_get_discrete_bins(self):
        probs = [0.3, 0.5, 0.2, 0.3, 0.5, 0.7]
        bins = get_discrete_bins(probs)
        self.assertEqual(bins, [0.25, 0.4, 0.6, 1.0])

    def test_enough_duplicates(self):
        probs = np.array([0.1, 0.3, 0.5])
        self.assertFalse(enough_duplicates(probs))
        probs = np.array([0.1, 0.1, 0.5])
        self.assertFalse(enough_duplicates(probs))
        probs = np.array([0.1, 0.1, 0.1, 0.1, 0.6, 0.6, 0.6, 0.6, 0.6])
        self.assertTrue(enough_duplicates(probs))

    def test_get_bin(self):
        bins = [0.2, 0.5, 1.0]
        self.assertEqual(get_bin(0.0, bins), 0)
        self.assertEqual(get_bin(0.19, bins), 0)
        self.assertEqual(get_bin(0.21, bins), 1)
        self.assertEqual(get_bin(0.49, bins), 1)
        self.assertEqual(get_bin(0.51, bins), 2)
        self.assertEqual(get_bin(1.0, bins), 2)

    def test_get_bin_size_1(self):
        bins = [1.0]
        self.assertEqual(get_bin(0.0, bins), 0)
        self.assertEqual(get_bin(0.5, bins), 0)
        self.assertEqual(get_bin(1.0, bins), 0)

    def test_bin(self):
        data = [(0.3, 1.0), (0.5, 0.0), (0.2, 1.0), (0.3, 0.0), (0.5, 1.0), (0.7, 0.0)]
        bins = [0.4, 1.0]
        binned_data = tuple(np.array(bin(data, bins)).tolist())
        self.assertTrue(multiset_equal(
            list_to_tuple(binned_data[0]), ((0.3, 1.0), (0.2, 1.0), (0.3, 0.0))))
        self.assertTrue(multiset_equal(
            list_to_tuple(binned_data[1]), ((0.5, 1.0), (0.5, 0.0), (0.7, 0.0))))

    @parameterized.expand([
        [[(0.3, 0.5)], -0.2],
        [[(0.5, 0.3)], 0.2],
        [[(0.3, 0.5), (0.8, 0.4)], 0.1],
        [[(0.3, 0.5), (0.8, 0.4), (0.4, 0.0)], 0.2]
    ])
    def test_difference_mean(self, data, true_value):
        self.assertAlmostEqual(difference_mean(data), true_value)


    @parameterized.expand([
        [[[(0.3, 0.5)]], [1.0]],
        [[[(0.3, 0.5)], [(0.4, 0.7)]], [0.5, 0.5]],
        [[[(0.3, 0.5)], [(0.4, 0.7)], [(0.0, 1.0), (0.6, 0.0)]], [0.25, 0.25, 0.5]],
    ])
    def test_get_bin_probs(self, binned_data, probs):
        self.assertAlmostEqual(get_bin_probs(binned_data), probs)

    @parameterized.expand([
        [[[(0.3, 1.0)]], 1, 0.7],
        [[[(0.3, 0.0)]], 1, 0.3],
        [[[(0.3, 1.0)]], 2, 0.7],
        [[[(0.3, 1.0)], [(0.6, 0.0)]], 1, 0.65],
        [[[(0.3, 1.0)], [(0.6, 0.0), (0.6, 1.0)]], 1, 0.3],
        [[[(0.3, 1.0)], [(0.6, 0.0)]], 2, 0.6519202405],
    ])
    def test_plugin_ce(self, binned_data, power, true_ce):
        self.assertAlmostEqual(plugin_ce(binned_data, power), true_ce)

    @parameterized.expand([
        [1, 4/9*0.25+5/9*0.2],
        [2, (4/9*(0.25**2)+5/9*(0.2**2))**(1/2.0)],
        [3, (4/9*(0.25**3)+5/9*(0.2**3))**(1/3.0)],
    ])
    def test_get_binary_ce(self, p, true_ce):
        probs = [0.5, 0.5, 0.5, 0.6, 0.5, 0.6, 0.6, 0.6, 0.6]
        labels = [0, 1, 0, 1, 0, 1, 1, 1, 0]
        pred_ce = _get_ce(probs, labels, p, debias=False, num_bins=None,
            binning_scheme=get_discrete_bins)
        self.assertAlmostEqual(pred_ce, true_ce)
        wrapper_ce = get_calibration_error(probs, labels, p=p, debias=False)
        self.assertAlmostEqual(pred_ce, wrapper_ce)
        pred_ce = _get_ce(probs, labels, p, debias=True, num_bins=None,
            binning_scheme=get_discrete_bins)
        self.assertLess(pred_ce, true_ce)

    @parameterized.expand([
        [1, 4/9*0.25+5/9*0.2],
        [2, (4/9*(0.25**2)+5/9*(0.2**2))**(1/2.0)],
        [3, (4/9*(0.25**3)+5/9*(0.2**3))**(1/3.0)],
    ])
    def test_get_two_label_ce(self, p, true_ce):
        # Same as the previous test, except probs is now multi-dimensional.
        pt6 = [0.4, 0.6]
        pt5 = [0.5, 0.5]
        probs = [pt5, pt5, pt5, pt6, pt5, pt6, pt6, pt6, pt6]
        labels = [0, 1, 0, 1, 0, 1, 1, 1, 0]
        pred_ce = _get_ce(probs, labels, p, debias=False, num_bins=None,
            binning_scheme=get_discrete_bins)
        self.assertAlmostEqual(pred_ce, true_ce)
        # Check that the wrapper calls _get_ce with the right options.
        wrapper_ce = get_calibration_error(probs, labels, p=p, debias=False)
        self.assertAlmostEqual(pred_ce, wrapper_ce)
        # For the 2 label case, marginal calibration and top-label calibration should be the same.
        top_label_ce = get_calibration_error(probs, labels, p=p, debias=False, mode='top-label')
        self.assertAlmostEqual(top_label_ce, pred_ce)
        debiased_top_label_ce = get_calibration_error(probs, labels, p=p, debias=True, mode='top-label')
        self.assertLess(debiased_top_label_ce, pred_ce)
        debiased_pred_ce = _get_ce(probs, labels, p, debias=True, num_bins=None,
            binning_scheme=get_discrete_bins)
        self.assertLess(debiased_pred_ce, true_ce)

    @parameterized.expand([
        [1, 4/42.0*0.1 + 6/42.0*(5/6.0-0.6) + 8/42.0*0.1 + 4/42.0*0.05 + 6/42.0*(0.3-1/6.0),
         6/14.0*(5/6.0-0.6) + 4/14.0*0.05 + 4/14.0*0.1],
        [2, (4/42.0*0.1**2 + 6/42.0*(5/6.0-0.6)**2 + 8/42.0*0.1**2 +
             4/42.0*0.05**2 + 6/42.0*(0.3-1/6.0)**2)**(1/2.0),
         (6/14.0*(5/6.0-0.6)**2 + 4/14.0*0.05**2 + 4/14.0*0.1**2)**(1/2.0)],
        [3, (4/42.0*0.1**3 + 6/42.0*(5/6.0-0.6)**3 + 8/42.0*0.1**3 +
             4/42.0*0.05**3 + 6/42.0*(0.3-1/6.0)**3)**(1/3.0),
         (6/14.0*(5/6.0-0.6)**3 + 4/14.0*0.05**3 + 4/14.0*0.1**3)**(1/3.0)]
    ])
    def test_get_three_label_ce(self, p, true_marginal_ce, true_top_ce):
        # Same as the previous test, except probs is now multi-dimensional.
        l0 = [0.6, 0.3, 0.1]
        l1 = [0.1, 0.8, 0.1]
        l2 = [0.1, 0.0, 0.9]
        probs = np.array([l0, l0, l0, l0, l0, l0, l1, l1, l1, l1, l2, l2, l2, l2])
        labels = np.array([ 0,  0,  0,  0,  0,  1,  1,  1,  1,  2,  2,  2,  2,  2])
        perm = np.random.permutation(len(labels))
        probs, labels = probs[perm], labels[perm]
        pred_ce = _get_ce(probs, labels, p, debias=False, num_bins=None,
            binning_scheme=get_discrete_bins)
        self.assertAlmostEqual(pred_ce, true_marginal_ce)
        # Check that the wrapper calls _get_ce with the right options.
        wrapper_ce = get_calibration_error(probs, labels, p=p, debias=False)
        self.assertAlmostEqual(pred_ce, wrapper_ce)
        top_label_ce = get_calibration_error(probs, labels, p=p, debias=False, mode='top-label')
        self.assertAlmostEqual(top_label_ce, true_top_ce)
        debiased_top_label_ce = get_calibration_error(probs, labels, p=p, debias=True, mode='top-label')
        self.assertLess(debiased_top_label_ce, true_top_ce)
        debiased_pred_ce = _get_ce(probs, labels, p, debias=True, num_bins=None,
            binning_scheme=get_discrete_bins)
        self.assertLess(debiased_pred_ce, true_marginal_ce)


    @parameterized.expand([
        [1, 0.5*(2/3.0-0.6) + 0.5*(1-2.75/3)],
        [2, (0.5*(2/3.0-0.6)**2 + 0.5*(1-2.75/3)**2)**(1/2.0)],
        [3, (0.5*(2/3.0-0.6)**3 + 0.5*(1-2.75/3)**3)**(1/3.0)],
    ])
    def test_three_label_top_ce_lower_bound(self, p, true_top_ce):
        # Same as the previous test, except probs is now multi-dimensional.
        probs = np.array([[0.8, 0.1, 0.1],
                           [0.6, 0.2, 0.2],
                           [0.0, 0.9, 0.1],
                           [0.0, 1.0, 0.0],
                           [0.3, 0.3, 0.4],
                           [0.2, 0.0, 0.85]])
        labels = np.array([0, 0, 1, 1, 0, 2])
        perm = np.random.permutation(len(labels))
        probs, labels = probs[perm], labels[perm]
        top_label_ce = lower_bound_scaling_ce(probs, labels, p=p, debias=False, num_bins=2,
                                              binning_scheme=get_equal_bins, mode='top-label')
        self.assertAlmostEqual(top_label_ce, true_top_ce)
        debiased_top_label_ce = lower_bound_scaling_ce(probs, labels, p=p, debias=True, num_bins=2,
                                              binning_scheme=get_equal_bins, mode='top-label')
        self.assertLess(debiased_top_label_ce, true_top_ce)

    def test_ece(self):
        probs = np.array([[0.8, 0.1, 0.1],
                           [0.6, 0.2, 0.2],
                           [0.0, 0.9, 0.1],
                           [0.0, 1.0, 0.0],
                           [0.3, 0.3, 0.4],
                           [0.2, 0.0, 0.85]])
        labels = np.array([0, 0, 1, 1, 0, 2])
        perm = np.random.permutation(len(labels))
        probs, labels = probs[perm], labels[perm]
        true_ece = 4/6.0 * (1 - (0.8+0.85+0.9+1.0)/4)
        pred_ece = get_ece(probs, labels, num_bins=3)
        self.assertAlmostEqual(pred_ece, true_ece)

    def test_missing_classes_ece(self):
        pred_ece = get_ece([[0.9,0.1], [0.8,0.2]], [0,0])
        true_ece = 0.15
        self.assertAlmostEqual(pred_ece, true_ece)

if __name__ == '__main__':
    unittest.main()
