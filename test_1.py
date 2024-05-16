#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-


import pytest

sku_info = ["H7148", "H7148_618A"]


@pytest.fixture(params=sku_info, ids=['1', '2'])
def sku_name(request):
    return request.param


def test_data(sku_name):
    print(f"fun={sku_name}")


if __name__ == '__main__':
    pytest.main(['-vs'])
