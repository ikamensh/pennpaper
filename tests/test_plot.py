import os
from pennpaper import Metric, plot_group, plot

import pytest

def test_empty_no_plot(tmpdir):
    files_before = len(os.listdir(tmpdir))

    m = Metric('empty')
    plot(m, folder=tmpdir)

    assert len(os.listdir(tmpdir)) == files_before

def test_all_empty_no_plot(tmpdir):
    files_before = len(os.listdir(tmpdir))

    m1 = Metric('empty')
    m2 = Metric('empty2')

    plot_group([m1, m2], folder=tmpdir)

    assert len(os.listdir(tmpdir)) == files_before

def test_some_empty_plots(tmpdir):
    files_before = len(os.listdir(tmpdir))

    m1 = Metric('empty')
    m2 = Metric('empty2')
    m2.add_record(1,1)

    plot_group([m1, m2], folder=tmpdir)

    assert len(os.listdir(tmpdir)) > files_before

def test_plot_group(tmpdir):
    m = Metric('x', 'y')
    m.add_ys(1, [1, 2, 3])
    m.add_record(2, 4)
    m.add_record(2, 4)
    m.add_record(2, 4)
    m.add_ys(4, [5, 6, 12])

    m2 = Metric('x', 'y')
    m2.add_ys(1, [4, 3, 5])
    m2.add_record(2, 5)
    m2.add_record(2, 9)
    m2.add_record(2, 9)
    m2.add_ys(4, [5, 6, -1])

    files_before = len(os.listdir(tmpdir))
    plot_group([m, m2], folder=tmpdir, name="bla3")
    files_after = len(os.listdir(tmpdir))

    assert files_after > files_before

def test_ezplot(tmpdir):
    m = Metric('x', 'y')
    m.add_ys(1, [1, 2, 3])
    m.add_record(2, 4)
    m.add_record(2, 4)
    m.add_record(2, 4)
    m.add_ys(4, [5, 6, 12])

    files_before = len(os.listdir(tmpdir))
    plot(m, folder=tmpdir, name="bla3")
    files_after = len(os.listdir(tmpdir))

    assert files_after > files_before
