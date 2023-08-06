"""
.. module:: test_reader
   :synopsis: Unit tests for reader module
"""

import pytest

import pandas as pd
import numpy as np
import numpy.testing as nt

from nutsflow import Collect, Sort
from nutsml import ReadNumpy, ReadImage, ReadLabelDirs, ReadPandas


def test_ReadLabelDirs():
    read = ReadLabelDirs('tests/data/labeldirs', '*.txt')
    samples = read >> Sort()
    assert samples == [('tests/data/labeldirs/0/test0.txt', '0'),
                       ('tests/data/labeldirs/1/test1.txt', '1'),
                       ('tests/data/labeldirs/1/test11.txt', '1')]

    read = ReadLabelDirs('tests/data/labeldirs', '*.txt', '')
    samples = read >> Sort()
    assert samples == [('tests/data/labeldirs/0/test0.txt', '0'),
                       ('tests/data/labeldirs/1/test1.txt', '1'),
                       ('tests/data/labeldirs/1/test11.txt', '1'),
                       ('tests/data/labeldirs/_2/test2.txt', '_2')]


def test_ReadNumpy():
    arr0 = np.load('tests/data/img_arrays/nut_color.gif.npy')
    arr1 = np.load('tests/data/img_arrays/nut_grayscale.gif.npy')
    samples = [('nut_color', 1), ('nut_grayscale', 2)]

    filepath = 'tests/data/img_arrays/*.gif.npy'
    np_samples = samples >> ReadNumpy(0, filepath) >> Collect()
    nt.assert_equal(np_samples[0][0], arr0)
    nt.assert_equal(np_samples[1][0], arr1)
    assert np_samples[0][1] == 1
    assert np_samples[1][1] == 2

    pathfunc = lambda s: 'tests/data/img_arrays/{0}.gif.npy'.format(*s)
    np_samples = samples >> ReadNumpy(0, pathfunc) >> Collect()
    nt.assert_equal(np_samples[0][0], arr0)
    nt.assert_equal(np_samples[1][0], arr1)

    samples = [('label', 'tests/data/img_arrays/nut_color.gif.npy')]
    np_samples = samples >> ReadImage(1) >> Collect()
    nt.assert_equal(np_samples[0][1], arr0)


def test_ReadImage():
    arr0 = np.load('tests/data/img_arrays/nut_color.gif.npy')
    arr1 = np.load('tests/data/img_arrays/nut_grayscale.gif.npy')
    samples = [('nut_color', 1), ('nut_grayscale', 2)]

    imagepath = 'tests/data/img_formats/*.gif'
    img_samples = samples >> ReadImage(0, imagepath) >> Collect()
    nt.assert_equal(img_samples[0][0], arr0)
    nt.assert_equal(img_samples[1][0], arr1)
    assert img_samples[0][1] == 1
    assert img_samples[1][1] == 2

    pathfunc = lambda sample: 'tests/data/img_formats/{0}.gif'.format(*sample)
    img_samples = samples >> ReadImage(0, pathfunc) >> Collect()
    nt.assert_equal(img_samples[0][0], arr0)
    nt.assert_equal(img_samples[1][0], arr1)

    samples = [('label', 'tests/data/img_formats/nut_color.gif')]
    img_samples = samples >> ReadImage(1, as_grey=False) >> Collect()
    assert img_samples[0][1].shape == (213, 320, 3)
    img_samples = samples >> ReadImage(1, as_grey=True) >> Collect()
    assert img_samples[0][1].shape == (213, 320)

    samples = ['tests/data/img_formats/nut_color.gif']
    img_samples = samples >> ReadImage(None, as_grey=False) >> Collect()
    assert img_samples[0][0].shape == (213, 320, 3)

    samples = ['tests/data/img_formats/nut_color.gif']
    img_samples = samples >> ReadImage(None, dtype=float) >> Collect()
    assert img_samples[0][0].dtype == float


def test_ReadPandas_isnull():
    assert not ReadPandas.isnull(1.0)
    assert not ReadPandas.isnull(0)
    assert ReadPandas.isnull(None)
    assert ReadPandas.isnull(np.NaN)


def test_ReadPandas_pkl():
    # create pickle version of table from CSV table
    df = pd.read_csv('tests/data/pandas_table.csv')
    df.to_pickle('tests/data/pandas_table.pkl')

    for ext in ['.pkl', '.csv', '.tsv', '.xlsx']:
        filepath = 'tests/data/pandas_table' + ext
        samples = ReadPandas(filepath, dropnan=True) >> Collect()
        nt.assert_equal(samples, [[1, 4], [3, 6]])

        samples = ReadPandas(filepath, dropnan=False) >> Collect()
        nt.assert_equal(samples, [[1, 4], [2, np.NaN], [3, 6]])

        samples = ReadPandas(filepath, replacenan=None) >> Collect()
        nt.assert_equal(samples, [[1, 4], [2, None], [3, 6]])

        samples = ReadPandas(filepath, columns=['col1', 'col2']) >> Collect()
        nt.assert_equal(samples, [[1, 4], [3, 6]])

        samples = ReadPandas(filepath, columns=['col1']) >> Collect()
        nt.assert_equal(samples, [[1], [2], [3]])

        samples = ReadPandas(filepath, columns=['col2']) >> Collect()
        nt.assert_equal(samples, [[4], [6]])

        samples = ReadPandas(filepath,
                             columns=['col2'], replacenan='NA') >> Collect()
        nt.assert_equal(samples, [[4], ['NA'], [6]])

        samples = ReadPandas(filepath,
                             rows='col1 > 1', replacenan=0) >> Collect()
        nt.assert_equal(samples, [[2, 0], [3, 6]])

        samples = ReadPandas(filepath,
                             rows='col1 < 3', columns=['col1']) >> Collect()
        nt.assert_equal(samples, [[1], [2]])
