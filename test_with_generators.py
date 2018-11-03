from muoio import Pipe
import pytest

class PipeAdd(Pipe):
  def __add__(self, f):
    return self.chain_in(f)
  
def test_pipe_with_adds():
    for e in (PipeAdd() 
    + (lambda x: (xe + 3 for xe in x) )
    + (lambda xe : xe )
    + (lambda x: (xe / 2 for xe in x if xe % 5 ==3))
    + (lambda xe : xe )        
    ).run(range(30)): print(e)
  
class PipeCall(Pipe):
  def __call__(self, f):
    return self.chain_in(f)
def test_pipe_with_calls():  
    for e in (PipeCall() 
    (lambda x: (xe + 3 for xe in x) )
    (lambda xe : xe )
    (lambda x: (xe / 2 for xe in x if xe % 5 ==3))
    (lambda xe : xe )        
    ).run(range(30)): print(e)