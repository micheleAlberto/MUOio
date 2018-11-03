from muoio import Piper
import pytest


def test_fizzbuzz0():
    v = list((Piper())
    .run([1,2,3,4,5]))
    assert v == [1,2,3,4,5]

def test_fizzbuzz1():
    v = list((Piper()
        [lambda x:isinstance(x,int) ::]
    )
    .run([1,2,None, 3,4, None,5]))
    assert v == [1,2,3,4,5]

def test_fizzbuzz2():
    v = list((Piper()
        [lambda x:isinstance(x,int) : (lambda x:(x,""))]
    )
    .run([1,2,None, 3,4, None,5]))
    assert v == [(i,"") for i in [1,2,3,4,5]]

def test_fizzbuzz3():
    v = list((Piper()
        [lambda x:isinstance(x,int) : (lambda x:(x,""))]
        [lambda x:x[0]%3!=0 :: lambda x:(x[0],x[1]+"fizz")]
        [lambda x:x[0]%5!=0 :: lambda x:(x[0],x[1]+"buzz")]
    )
    .run([1,2,None, 3,4, None,5]))
    print(v)
    for observed, expected in zip(v, [1,2,3,4,5]):
        assert observed[0] == expected
        if expected%3 == 0: assert "fizz" in observed[1]
        if expected%5 == 0: assert "buzz" in observed[1]
    
