# MUO.io
just some fun with python syntax

this is fizzbuzz (checking input type):
```python
from muoio import Piper
pipe = (Piper()
    [lambda x:isinstance(x,int) : (lambda x:(x,""))]
    [lambda x:x[0]%3!=0 :: lambda x:(x[0],x[1]+"fizz")]
    [lambda x:x[0]%5!=0 :: lambda x:(x[0],x[1]+"buzz")]
)
print list(pipe.run.run([
    1,None, None
    2,3,4,
    None,5,6,
    None, None, 7,
    8,9,10
]))

```

`Piper()[condition:branch_if_true:branch_if_false]`