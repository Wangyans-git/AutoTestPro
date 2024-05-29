#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
import pytest


@pytest.fixture(params=[1])
def condition(request):
    return request.param


@pytest.mark.parametrize("condition", [1], indirect=True)
def test_case1(condition):
    print(condition)
    assert condition == 1
    print("Executing test case 1")


@pytest.mark.parametrize("condition", [2], indirect=True)
def test_case2(condition):
    print(condition)
    assert condition == 2
    print("Executing test case 2")


if __name__ == '__main__':
    pytest.main(["-vs"])
