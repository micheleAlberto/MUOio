from muoio import Piper
import pytest

def test_match_int():
    class TA(int): pass
    class TB(int): pass
    class TC(int): pass
    sequence = [TA(0), TB(0), TC(0),0 ,None]
    p = (Piper()
        [
            int :: lambda x : x + 1,
            TA :: lambda x : x + 2,
            TB :: lambda x : x + 3,
            TC :: lambda x : x + 4,
            int :: lambda x : x + 5,
        ]
    )
    sequence = [
        TA(0), TB(0), TC(0),0 ,"lol"]
    expected_output = [
        2, 3, 4, 1, None
    ]
    observed = list(p.run(sequence))
    assert observed == expected_output

def test_match_int_with_condition():
    class TA(int): pass
    class TB(int): pass
    class TC(int): pass
    sequence = [TA(0), TB(0), TC(0),0 ,None]
    p = (Piper()
        [
            int : lambda x : x > 4 : 100,
            TA :: lambda x : x + 2,
            TB :: lambda x : x + 3,
            TC :: lambda x : x + 4,
            int :: lambda x : - 100,
        ]
    )
    sequence = [
        TA(0), TB(0), TC(0),
        2 , 9 , "lol", None ]
    expected_output = [
        2, 3, 4, 
        -100, 100 , None, None
    ]
    observed = list(p.run(sequence))
    assert observed == expected_output

def test_match_int_with_condition_and_default():
    class TA(int): pass
    class TB(int): pass
    class TC(int): pass
    p = (Piper()
        [
            int : lambda x : x > 4 : 100,
            TA :: lambda x : x + 2,
            TB :: lambda x : x + 3,
            TC :: lambda x : x + 4,
            int :: lambda x : - 100,
            str :: 42,
            : lambda x : hasattr(x,"__add__") : 64,
            ::314
        ]
    )
    sequence, expected_output = zip(*[
        (TA(0),     2),
        (TB(0),     3),
        (TC(0),     4),
        (2 ,        -100),
        (9 ,        100),
        ("lol",     42),
        (None,      314),
        (3.7,       64)
    ])
    sequence = list(sequence)
    expected_output = list(expected_output)
    observed = list(p.run(sequence))
    assert observed == expected_output

def test_match_int_with_default():
    class TA(int): pass
    class TB(int): pass
    class TC(int): pass
    sequence = [TA(0), TB(0), TC(0),0 ,None]
    p = (Piper()
        [
            int :: lambda x : x + 1,
            TA :: lambda x : x + 2,
            TB :: lambda x : x + 3,
            TC :: lambda x : x + 4,
            int :: lambda x : x + 5,
            ::lambda x : str(x)
        ]
    )
    sequence = [
        TA(0), TB(0), TC(0),0 ,"lol",3.3]
    expected_output = [
        2, 3, 4, 1, "lol", "3.3"
    ]
    observed = list(p.run(sequence))
    assert observed == expected_output

def test_match_int2():
    class TA(int): pass
    class TB(int): pass
    class TC(int): pass
    sequence = [TA(0), TB(0), TC(0),0 ,None]
    p = (Piper()
        [
            int :: lambda x : x + 1,
            TA :: lambda x : x + 2,
            TB :: lambda x : x + 3,
            TC :: lambda x : x + 4,
            int :: lambda x : x + 5,
        ][::]
    )
    sequence = [
        TA(0), TB(0), TC(0),0 ,"lol"]
    expected_output = [
        2, 3, 4, 1
    ]
    observed = list(p.run(sequence))
    assert observed == expected_output

def test_match_int3():
    class TA(int): pass
    class TB(int): pass
    class TC(int): pass
    sequence = [TA(0), TB(0), TC(0),0 ,None]
    p = (Piper()
        [
            int :: lambda x : x + 1,
            TA :: lambda x : x + 2,
            TB :: lambda x : x + 3,
            TC :: lambda x : x + 4,
            int :: lambda x : x + 5,
        ][::str]
    )
    sequence = [
        TA(0), TB(0), TC(0),0 ,"lol"]
    expected_output = [
        2, 3, 4, 1, str(None)
    ]
    observed = list(p.run(sequence))
    assert observed == expected_output




def main():
    pytest.main()

if __name__ == '__main__':
    main()