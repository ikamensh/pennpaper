from ilya_ezplot.processing.running_avg import apply_running_average
from ilya_ezplot.processing.momentum import apply_momentum


import random
import pytest

@pytest.fixture(params=[apply_running_average, apply_momentum])
def smoothen_func(request):
    yield request.param

def test_same_length(smoothen_func):
    for i in range(10):
        x = [random.random() for i in range(random.randint(10,100))]
        s = smoothen_func(x, smoothen=random.random()*0.99 + 1e-3)
        assert len(x) == len(s)



@pytest.mark.parametrize("k_smoothen", [1e-2, 0.5, 0.99])
def test_is_smoother_second_derivative(smoothen_func, k_smoothen):
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
def test_is_smoother_first_derivative(smoothen_func, k_smoothen):
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
def test_within_bounds(smoothen_func, k_smoothen):
    x = [random.random() for i in range(100)]

    s = smoothen_func(x, smoothen=k_smoothen)
    if len(x) != len(s):
        pytest.skip("precondition not met.")

    assert min(x) <= min(s) <= max(s) <= max(x)

