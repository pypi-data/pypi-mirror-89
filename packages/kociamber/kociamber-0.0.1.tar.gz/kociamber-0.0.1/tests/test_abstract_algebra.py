from abstract_algebra import say_hello


def test_abstract_algebra_no_params():
    assert say_hello() == "Hello, World!"


def test_abstract_algebra_with_param():
    assert say_hello("Everyone") == "Hello, Everyone!"
