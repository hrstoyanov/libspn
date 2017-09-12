#!/usr/bin/env python3

# ------------------------------------------------------------------------
# Copyright (C) 2016-2017 Andrzej Pronobis - All Rights Reserved
#
# This file is part of LibSPN. Unauthorized use or copying of this file,
# via any medium is strictly prohibited. Proprietary and confidential.
# ------------------------------------------------------------------------

import unittest
import tensorflow as tf
import numpy as np
from context import libspn as spn


class TestNodesProducts(unittest.TestCase):

    def tearDown(self):
        tf.reset_default_graph()

    def test_compute_value(self):
        """Calculating value of Products"""

        def test(inputs, num_prods, feed, output):
            with self.subTest(inputs=inputs, num_prods=num_prods, feed=feed):
                n = spn.Products(*inputs, num_prods=num_prods)
                op = n.get_value(spn.InferenceType.MARGINAL)
                op_log = n.get_log_value(spn.InferenceType.MARGINAL)
                op_mpe = n.get_value(spn.InferenceType.MPE)
                op_log_mpe = n.get_log_value(spn.InferenceType.MPE)
                with tf.Session() as sess:
                    out = sess.run(op, feed_dict=feed)
                    out_log = sess.run(tf.exp(op_log), feed_dict=feed)
                    out_mpe = sess.run(op_mpe, feed_dict=feed)
                    out_log_mpe = sess.run(tf.exp(op_log_mpe), feed_dict=feed)
                np.testing.assert_array_almost_equal(
                    out,
                    np.array(output, dtype=spn.conf.dtype.as_numpy_dtype()))
                np.testing.assert_array_almost_equal(
                    out_log,
                    np.array(output, dtype=spn.conf.dtype.as_numpy_dtype()))
                np.testing.assert_array_almost_equal(
                    out_mpe,
                    np.array(output, dtype=spn.conf.dtype.as_numpy_dtype()))
                np.testing.assert_array_almost_equal(
                    out_log_mpe,
                    np.array(output, dtype=spn.conf.dtype.as_numpy_dtype()))

        # Create inputs
        v1 = spn.ContVars(num_vars=3)
        v2 = spn.ContVars(num_vars=1)

        # Single Product node
        num_prods = 1

        # Multiple inputs, multi-element batch
        test([v1, v2],
             num_prods,
             {v1: [[0.1, 0.2, 0.3],
                   [0.4, 0.5, 0.6]],
              v2: [[0.7],
                   [0.8]]},
             [[0.1 * 0.2 * 0.3 * 0.7],
              [0.4 * 0.5 * 0.6 * 0.8]])
        test([(v1, [0, 2]), (v2, [0])],
             num_prods,
             {v1: [[0.1, 0.2, 0.3],
                   [0.4, 0.5, 0.6]],
              v2: [[0.7],
                   [0.8]]},
             [[0.1 * 0.3 * 0.7],
              [0.4 * 0.6 * 0.8]])

        # Single input with 1 value, multi-element batch
        test([v2],
             num_prods,
             {v2: [[0.1],
                   [0.2]]},
             [[0.1],
              [0.2]])
        test([(v1, [1])],
             num_prods,
             {v1: [[0.01, 0.1, 0.03],
                   [0.02, 0.2, 0.04]]},
             [[0.1],
              [0.2]])

        # Multiple inputs, single-element batch
        test([v1, v2],
             num_prods,
             {v1: [[0.1, 0.2, 0.3]],
              v2: [[0.7]]},
             [[0.1 * 0.2 * 0.3 * 0.7]])
        test([(v1, [0, 2]), (v2, [0])],
             num_prods,
             {v1: [[0.1, 0.2, 0.3]],
              v2: [[0.7]]},
             [[0.1 * 0.3 * 0.7]])

        # Single input with 1 value, single-element batch
        test([v2],
             num_prods,
             {v2: [[0.1]]},
             [[0.1]])
        test([(v1, [1])],
             num_prods,
             {v1: [[0.01, 0.1, 0.03]]},
             [[0.1]])

        # Multiple Product nodes
        num_prods = 2

        # Multiple inputs, multi-element batch
        test([v1, v2, v1, v2],
             num_prods,
             {v1: [[0.1, 0.2, 0.3],
                   [0.4, 0.5, 0.6]],
              v2: [[0.7],
                   [0.8]]},
             [[(0.1 * 0.2 * 0.3 * 0.7), (0.1 * 0.2 * 0.3 * 0.7)],
              [(0.4 * 0.5 * 0.6 * 0.8), (0.4 * 0.5 * 0.6 * 0.8)]])
        test([(v1, [0, 2]), (v2, [0]), (v1, [0, 2]), (v2, [0])],
             num_prods,
             {v1: [[0.1, 0.2, 0.3],
                   [0.4, 0.5, 0.6]],
              v2: [[0.7],
                   [0.8]]},
             [[(0.1 * 0.3 * 0.7), (0.1 * 0.3 * 0.7)],
              [(0.4 * 0.6 * 0.8), (0.4 * 0.6 * 0.8)]])

        # Single input with 1 value, multi-element batch
        test([v2, v2],
             num_prods,
             {v2: [[0.1],
                   [0.2]]},
             [[0.1, 0.1],
              [0.2, 0.2]])
        test([(v1, [1]), (v1, [1])],
             num_prods,
             {v1: [[0.01, 0.1, 0.03],
                   [0.02, 0.2, 0.04]]},
             [[0.1, 0.1],
              [0.2, 0.2]])

        # Multiple inputs, single-element batch
        test([v1, v2, v1, v2],
             num_prods,
             {v1: [[0.1, 0.2, 0.3]],
              v2: [[0.7]]},
             [[(0.1 * 0.2 * 0.3 * 0.7), (0.1 * 0.2 * 0.3 * 0.7)]])
        test([(v1, [0, 2]), (v2, [0]), (v1, [0, 2]), (v2, [0])],
             num_prods,
             {v1: [[0.1, 0.2, 0.3]],
              v2: [[0.7]]},
             [[(0.1 * 0.3 * 0.7), (0.1 * 0.3 * 0.7)]])

        # Single input with 1 value, single-element batch
        test([v2, v2],
             num_prods,
             {v2: [[0.1]]},
             [[0.1, 0.1]])
        test([(v1, [1]), (v1, [1])],
             num_prods,
             {v1: [[0.01, 0.1, 0.03]]},
             [[0.1, 0.1]])

    def test_comput_scope(self):
        """Calculating scope of Products"""
        # Create graph
        v12 = spn.IVs(num_vars=2, num_vals=4, name="V12")
        v34 = spn.ContVars(num_vars=2, name="V34")
        s1 = spn.Sum((v12, [0, 1, 2, 3]), name="S1")
        s1.generate_ivs()
        s2 = spn.Sum((v12, [4, 5, 6, 7]), name="S2")
        ps1 = spn.Products((v12, [0, 7]), (v12, [3, 4]), v34, num_prods=3,
                           name="Ps1")
        n1 = spn.Concat(s1, s2, (ps1, [2]), name="N1")
        n2 = spn.Concat((ps1, [0]), (ps1, [1]), name="N2")
        s3 = spn.Sum(ps1, name="S3")
        s3.generate_ivs()
        ps2 = spn.Products((n1, [0, 1]), (n1, 2), (n2, 0), n2, (n2, 1), s3,
                           num_prods=4, name="Ps2")
        s4 = spn.Sum((ps2, 0), n2, name="S4")
        s5 = spn.Sum(ps2, name="S5")
        s6 = spn.Sum((ps2, [1, 3]), name="S6")
        s6.generate_ivs()
        ps3 = spn.Products(s4, (n1, 2), name="Ps3")
        ps4 = spn.Products(s4, s5, s6, s4, s5, s6, num_prods=2, name="Ps4")
        # Test
        self.assertListEqual(v12.get_scope(),
                             [spn.Scope(v12, 0), spn.Scope(v12, 0),
                              spn.Scope(v12, 0), spn.Scope(v12, 0),
                              spn.Scope(v12, 1), spn.Scope(v12, 1),
                              spn.Scope(v12, 1), spn.Scope(v12, 1)])
        self.assertListEqual(v34.get_scope(),
                             [spn.Scope(v34, 0), spn.Scope(v34, 1)])
        self.assertListEqual(s1.get_scope(),
                             [spn.Scope(v12, 0) | spn.Scope(s1.ivs.node, 0)])
        self.assertListEqual(s2.get_scope(),
                             [spn.Scope(v12, 1)])
        self.assertListEqual(ps1.get_scope(),
                             [spn.Scope(v12, 0) | spn.Scope(v12, 1),
                              spn.Scope(v12, 0) | spn.Scope(v12, 1),
                              spn.Scope(v34, 0) | spn.Scope(v34, 1)])
        self.assertListEqual(n1.get_scope(),
                             [spn.Scope(v12, 0) | spn.Scope(s1.ivs.node, 0),
                              spn.Scope(v12, 1),
                              spn.Scope(v34, 0) | spn.Scope(v34, 1)])
        self.assertListEqual(n2.get_scope(),
                             [spn.Scope(v12, 0) | spn.Scope(v12, 1),
                              spn.Scope(v12, 0) | spn.Scope(v12, 1)])
        self.assertListEqual(s3.get_scope(),
                             [spn.Scope(v12, 0) | spn.Scope(v12, 1) |
                              spn.Scope(v34, 0) | spn.Scope(v34, 1) |
                              spn.Scope(s3.ivs.node, 0)])
        self.assertListEqual(ps2.get_scope(),
                             [spn.Scope(v12, 0) | spn.Scope(v12, 1) |
                              spn.Scope(s1.ivs.node, 0),
                              spn.Scope(v12, 0) | spn.Scope(v12, 1) |
                              spn.Scope(v34, 0) | spn.Scope(v34, 1),
                              spn.Scope(v12, 0) | spn.Scope(v12, 1),
                              spn.Scope(v12, 0) | spn.Scope(v12, 1) |
                              spn.Scope(v34, 0) | spn.Scope(v34, 1) |
                              spn.Scope(s3.ivs.node, 0)])
        self.assertListEqual(s4.get_scope(),
                             [spn.Scope(v12, 0) | spn.Scope(v12, 1) |
                              spn.Scope(s1.ivs.node, 0)])
        self.assertListEqual(s5.get_scope(),
                             [spn.Scope(v12, 0) | spn.Scope(v12, 1) |
                              spn.Scope(s1.ivs.node, 0) | spn.Scope(v34, 0) |
                              spn.Scope(v34, 1) | spn.Scope(s3.ivs.node, 0)])
        self.assertListEqual(s6.get_scope(),
                             [spn.Scope(v12, 0) | spn.Scope(v12, 1) |
                              spn.Scope(v34, 0) | spn.Scope(v34, 1) |
                              spn.Scope(s3.ivs.node, 0) |
                              spn.Scope(s6.ivs.node, 0)])
        self.assertListEqual(ps3.get_scope(),
                             [spn.Scope(v12, 0) | spn.Scope(v12, 1) |
                              spn.Scope(s1.ivs.node, 0) |
                              spn.Scope(v34, 0) | spn.Scope(v34, 1)])
        self.assertListEqual(ps4.get_scope(),
                             [spn.Scope(v12, 0) | spn.Scope(v12, 1) |
                              spn.Scope(v34, 0) | spn.Scope(v34, 1) |
                              spn.Scope(s1.ivs.node, 0) |
                              spn.Scope(s3.ivs.node, 0) |
                              spn.Scope(s6.ivs.node, 0),
                              spn.Scope(v12, 0) | spn.Scope(v12, 1) |
                              spn.Scope(v34, 0) | spn.Scope(v34, 1) |
                              spn.Scope(s1.ivs.node, 0) |
                              spn.Scope(s3.ivs.node, 0) |
                              spn.Scope(s6.ivs.node, 0)])

    def test_compute_valid(self):
        """Calculating validity of Products"""
        v12 = spn.IVs(num_vars=2, num_vals=3)
        v345 = spn.IVs(num_vars=3, num_vals=3)
        v678 = spn.ContVars(num_vars=3)
        v910 = spn.ContVars(num_vars=2)
        p1 = spn.Products((v12, 0), (v12, 4), (v12, 0), (v12, 5),
                          (v12, 1), (v12, 4), (v12, 1), (v12, 5), num_prods=4)
        p2 = spn.Products((v12, 3), (v345, 0), (v12, 3), (v345, 1), (v12, 3), (v345, 2),
                          (v12, 5), (v345, 0), (v12, 5), (v345, 1), (v12, 5), (v345, 2),
                          num_prods=6)
        p3 = spn.Products((v345, 0), (v345, 3), (v345, 6), (v345, 0), (v345, 3),
                          (v345, 7), (v345, 0), (v345, 3), (v345, 8), (v345, 0),
                          (v345, 4), (v345, 6), (v345, 0), (v345, 4), (v345, 7),
                          (v345, 0), (v345, 4), (v345, 8), (v345, 0), (v345, 5),
                          (v345, 6), (v345, 0), (v345, 5), (v345, 7), (v345, 0),
                          (v345, 5), (v345, 8), (v345, 1), (v345, 3), (v345, 6),
                          (v345, 1), (v345, 3), (v345, 7), (v345, 1), (v345, 3),
                          (v345, 8), (v345, 1), (v345, 4), (v345, 6), (v345, 1),
                          (v345, 4), (v345, 7), (v345, 1), (v345, 4), (v345, 8),
                          (v345, 1), (v345, 5), (v345, 6), (v345, 1), (v345, 5),
                          (v345, 7), (v345, 1), (v345, 5), (v345, 8), (v345, 2),
                          (v345, 3), (v345, 6), (v345, 2), (v345, 3), (v345, 7),
                          (v345, 2), (v345, 3), (v345, 8), (v345, 2), (v345, 4),
                          (v345, 6), (v345, 2), (v345, 4), (v345, 7), (v345, 2),
                          (v345, 4), (v345, 8), (v345, 2), (v345, 5), (v345, 6),
                          (v345, 2), (v345, 5), (v345, 7), (v345, 2), (v345, 5),
                          (v345, 8), num_prods=27)
        p4 = spn.Products((v345, 6), (v678, 0), (v345, 6), (v678, 1),
                          (v345, 8), (v678, 0), (v345, 8), (v678, 1), num_prods=4)
        p5 = spn.Products((v678, 1), (v910, 0), (v678, 1), (v910, 1), num_prods=2)
        p6_1 = spn.Products((v678, 0), (v910, 0), (v678, 0), (v910, 1),
                            (v678, 1), (v910, 0), (v678, 1), (v910, 1),
                            (v678, 2), (v910, 0), (v678, 2), (v910, 1), num_prods=6)
        p6_2 = spn.Products((v678, 0), (v910, 0), (v678, 1), (v910, 0),
                            (v678, 1), (v910, 1), (v678, 2), (v910, 0), num_prods=4)
        p7_1 = spn.Products((v678, [0, 1, 2]))
        p7_2 = spn.Products(v678)
        p8_1 = spn.Products((v910, [0]), (v910, [1]))
        p8_2 = spn.Products(v910, num_prods=2)
        self.assertTrue(p1.is_valid())
        self.assertTrue(p2.is_valid())
        self.assertTrue(p3.is_valid())
        self.assertTrue(p4.is_valid())
        self.assertTrue(p5.is_valid())
        self.assertTrue(p6_1.is_valid())
        self.assertTrue(p6_2.is_valid())
        self.assertTrue(p7_1.is_valid())
        self.assertTrue(p7_2.is_valid())
        self.assertTrue(p8_1.is_valid())
        self.assertTrue(p8_2.is_valid())
        p9 = spn.Products((v12, 0), (v12, 1), (v12, 0), (v12, 2),
                          (v12, 1), (v12, 1), (v12, 1), (v12, 2), num_prods=4)
        p10 = spn.Products((v12, 3), (v345, 0), (v345, 0),
                           (v12, 3), (v345, 0), (v345, 1),
                           (v12, 3), (v345, 0), (v345, 2),
                           (v12, 4), (v345, 0), (v345, 0),
                           (v12, 4), (v345, 0), (v345, 1),
                           (v12, 4), (v345, 0), (v345, 2),
                           (v12, 5), (v345, 0), (v345, 0),
                           (v12, 5), (v345, 0), (v345, 1),
                           (v12, 5), (v345, 0), (v345, 2), num_prods=9)
        p11_1 = spn.Products((v345, 3), (v678, 0), (v678, 0),
                             (v345, 5), (v678, 0), (v678, 0), num_prods=2)
        p11_2 = spn.Products((v345, 3), (v678, 0), (v678, 0),
                             (v345, 5), (v678, 0), (v678, 0), num_prods=3)
        p12 = spn.Products((v910, 1), (v910, 1), num_prods=1)
        p13_1 = spn.Products((v910, 0), (v910, 0), (v910, 0), (v910, 1),
                             (v910, 1), (v910, 0), (v910, 1), (v910, 1), num_prods=4)
        p13_2 = spn.Products((v910, 0), (v910, 0), (v910, 0), (v910, 1),
                             (v910, 1), (v910, 0), (v910, 1), (v910, 1), num_prods=1)
        self.assertFalse(p9.is_valid())
        self.assertFalse(p10.is_valid())
        self.assertFalse(p11_1.is_valid())
        self.assertFalse(p11_2.is_valid())
        self.assertFalse(p12.is_valid())
        self.assertFalse(p13_1.is_valid())
        self.assertFalse(p13_2.is_valid())

    def test_compute_mpe_path(self):
        v12 = spn.IVs(num_vars=2, num_vals=4)
        v34 = spn.ContVars(num_vars=2)
        v5 = spn.ContVars(num_vars=1)
        p = spn.Products((v12, [0, 5]), v5, v34, (v12, [3]), num_prods=2)
        counts = tf.placeholder(tf.float32, shape=(None, 2))
        op = p._compute_mpe_path(tf.identity(counts),
                                 v12.get_value(),
                                 v5.get_value(),
                                 v34.get_value(),
                                 v12.get_value())
        feed = [[11, 12],
                [21, 22],
                [31, 32]]
        with tf.Session() as sess:
            out = sess.run(op, feed_dict={counts: feed})
        np.testing.assert_array_almost_equal(
            out[0], np.array([[11., 0., 0., 0., 0., 11., 0., 0.],
                              [21., 0., 0., 0., 0., 21., 0., 0.],
                              [31., 0., 0., 0., 0., 31., 0., 0.]],
                             dtype=np.float32))
        np.testing.assert_array_almost_equal(
            out[1], np.array([[11.],
                              [21.],
                              [31.]],
                             dtype=np.float32))
        np.testing.assert_array_almost_equal(
            out[2], np.array([[12., 12.],
                              [22., 22.],
                              [32., 32.]],
                             dtype=np.float32))

        np.testing.assert_array_almost_equal(
            out[3], np.array([[0., 0., 0., 12., 0., 0., 0., 0.],
                              [0., 0., 0., 22., 0., 0., 0., 0.],
                              [0., 0., 0., 32., 0., 0., 0., 0.]],
                             dtype=np.float32))


if __name__ == '__main__':
    unittest.main()
