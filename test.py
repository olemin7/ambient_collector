import pytest


def fun(x):
    return x*x

def test_fun():
    assert fun(5)==10

