from muoio import Piper
import pytest


elems = [1, 2, 3, 4, 5, None, 6, 7, None]


def test_filter_out_none():
    assert list(Piper()[::].run(elems)) == [x for x in elems if x is not None]


def test_transform_none():
    intended = [x if x is not None else "muoio" for x in elems]
    use = Piper()[::"muoio"]
    assert list(use.run(elems)) == intended


def test_transform2_none():
    intended = [x if x is not None else "muoio" for x in elems]
    use = Piper()[::lambda x:"muoio"]
    assert list(use.run(elems)) == intended


def test_transform_not_none():
    def transform(x): return x+2
    intended = map(transform, [e for e in elems if e is not None])
    use = Piper()[:transform:]
    assert list(use.run(elems)) == list(intended)


def test_transform_if():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]

    def transform(x): return x+2

    def condition(x): return x < 6
    intended = map(transform, filter(condition, numbers))
    use = Piper()[condition:transform:]
    assert list(use.run(numbers)) == list(intended)


def test_transform_rails():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]

    def transform(x): return x+2

    def condition(x): return x < 6

    def negative_transform(x): return "faulty {}".format(x)
    intended = [transform(x) if condition(
        x) else negative_transform(x) for x in numbers]
    use = Piper()[condition:transform:negative_transform]
    assert list(use.run(numbers)) == list(intended)


def test_transform_if_keeping_none():
    numbers = [1, 2, 3, 4, None, 5, 6, 7, 8]

    def transform(x): return x+2
    intended = [transform(x) if x is not None else x for x in numbers]
    use = Piper()[:transform:lambda x: None]
    assert list(use.run(numbers)) == list(intended)


def test_transform_if_even_odds_are_none():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]

    def transform(x): return x+2

    def condition(x): return x % 2 == 0
    intended = [transform(x) if condition(x) else None for x in numbers]
    use = Piper()[condition:transform:lambda x: None]
    assert list(use.run(numbers)) == list(intended)


def test_transform_if_even():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]

    def transform(x): return x+2

    def condition(x): return x % 2 == 0
    intended = [transform(x) for x in numbers if condition(x)]
    use = Piper()[condition:transform:]
    assert list(use.run(numbers)) == list(intended)
