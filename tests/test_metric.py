from ilya_ezplot import Metric


def test_unique():
    m1 = Metric("x", "y")
    m2 = Metric("x", "y")

    assert m1 is not m2
    assert not m1 == m2


def test_summ_valid():
    m1 = Metric("x", "y")
    m1.add_many(x=2, ys=[3])
    m1.add_many(x=3, ys=[3])

    m2 = Metric("x", "y")
    m2.add_many(x=2, ys=[15])
    m2.add_many(x=3, ys=[10])

    m3 = m1 + m2

    assert len(m3.data.keys()) == 2


def test_summ_3():
    m1 = Metric("x", "y")
    m1.add_many(x=2, ys=[3, 4, 5])
    m1.add_many(x=3, ys=[20, 4, 5])

    m2 = Metric("x", "y")
    m2.add_many(x=2, ys=[15])
    m2.add_many(x=3, ys=[20])

    m3 = Metric("x", "y")
    m3.add_many(x=2, ys=[15])
    m3.add_many(x=3, ys=[20])


    m4 = sum([m1, m2, m3])

    assert 2 in m4.data.keys()


def test_summ_many():
    import random

    metrics = [Metric('x', 'y') for x in range(10)]
    for m in metrics:
        for i in range(50):
            m.add_record(x=random.random(), y=random.random())
        m.sort()

    m11 = sum(metrics)

    assert 50 <= len(m11.data)  <= 500
    assert len( list(m11.data.values())[0] ) == 10


def test_samples():
    m1 = Metric("x", "y")
    m1.add_many(x=2, ys=[3])
    m1.add_many(x=3, ys=[3])

    m2 = Metric("x", "y")
    m2.add_many(x=2, ys=[15,14])
    m2.add_many(x=3, ys=[10,12])


    assert m1.samples == 1
    assert m2.samples == 2

def test_original_metrics_intact():
    m1 = Metric("x", "y")
    m1.add_many(x=2, ys=[3])
    m1.add_many(x=3, ys=[3])

    m2 = Metric("x", "y")
    m2.add_many(x=2, ys=[15])
    m2.add_many(x=3, ys=[10])

    m3 = m1 + m2

    assert m1.samples == 1
    assert m2.samples == 1
    assert m3.samples == 2


def test_summ_many_originals_intact():
    import random

    metrics = [Metric('x', 'y') for x in range(10)]
    for m in metrics:
        for i in range(50):
            m.add_record(x=random.random(), y=random.random())
        m.sort()

    m11 = sum(metrics)

    m1 = metrics[0]
    assert m1.samples == 1