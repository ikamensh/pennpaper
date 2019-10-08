import os
from pennpaper import Metric, plot_group, plot


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
    plot_group([m, m2], tmpdir, "bla3")
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
    plot(m, tmpdir, "bla3")
    files_after = len(os.listdir(tmpdir))

    assert files_after > files_before
