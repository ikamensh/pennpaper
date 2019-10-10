from pennpaper.plot.plot import smoothen_func

import random
import pytest




def test_same_length():
    for i in range(100):
        x = [random.random() for i in range(random.randint(10,100))]
        k_smoothen = random.random()*0.99 + 1e-3
        s = smoothen_func(x, smoothen=k_smoothen)
        assert len(x) == len(s), f"failed on {i}th iteration for {k_smoothen} and {x}"



@pytest.mark.parametrize("k_smoothen", [1e-2, 0.5, 0.99])
def test_is_smoother_second_derivative(k_smoothen):
    x = [random.random() for i in range(100)]
    s = smoothen_func(x, smoothen=k_smoothen)

    if len(x) != len(s):
        pytest.skip("precondition not met.")

    def differences( a ):
        result = []
        for i in range(len(a)-1):
            result.append(abs(a[i+1] - a[i]))
        return result

    ddx, dds = sum(differences(differences(x))), sum(differences(differences(s)))
    assert ddx > dds


@pytest.mark.parametrize("k_smoothen", [1e-2, 0.5, 0.99])
def test_is_smoother_first_derivative(k_smoothen):
    x = [random.random() for i in range(100)]
    s = smoothen_func(x, smoothen=k_smoothen)

    if len(x) != len(s):
        pytest.skip("precondition not met.")

    def differences( a ):
        result = []
        for i in range(len(a)-1):
            result.append(abs(a[i+1] - a[i]))
        return result

    dx, ds = sum(differences(x)), sum(differences(s))
    assert dx > ds




@pytest.mark.parametrize("k_smoothen", [1e-2, 0.5, 0.99])
def test_within_bounds(k_smoothen):
    x = [random.random() for i in range(100)]

    s = smoothen_func(x, smoothen=k_smoothen)
    if len(x) != len(s):
        pytest.skip("precondition not met.")

    assert min(x) <= min(s) <= max(s) <= max(x)


@pytest.mark.parametrize("k_smoothen", [0.15, 0.5, 0.8])
def test_bondary_effect_is_minor(k_smoothen):
    x1 = list(range(100)) + [-50]
    s1 = smoothen_func(x1, smoothen=k_smoothen)

    sum1 = sum(s1)

    x2 = list(range(99)) + [-50] + [99]
    s2 = smoothen_func(x2, smoothen=k_smoothen)

    sum2 = sum(s2)

    assert abs(sum2 - sum1) / (sum1 + sum2) < 0.02



