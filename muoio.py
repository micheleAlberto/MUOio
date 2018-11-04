class Pipe(object):
  def __init__(self, eager=None):
    self.eager = eager
    def first_computation():
      for e in self.eager:
        yield e
    self.computation=first_computation
  def chain_in(self,next_function):
    current_computation = self.computation
    def new_computation():
      for e in next_function(current_computation()):
        yield e
    self.computation = new_computation
    return self
  def chain(self, function):
    current_computation = self.computation
    self.computation = lambda : map(function,current_computation())
    return self
  def run(self,eager):
    self.eager = eager
    for x in self.computation():
      yield x

def identity(x):
  return x

def not_none(x):
  return x is not None

from collections import defaultdict

class Piper(Pipe):


  def __call__(self, gen):
    return self.chain_in(gen)

  def __getitem__(self, arg):
    if isinstance(arg, tuple):
      matchers = defaultdict(list)
      for case in arg:
        if isinstance(case, slice):
          matchers[
            case.start # match on this type
          ].append((
            case.stop, # if this condition(x) is true or condition is None
            case.step  # using this transformation if callable or this value
          ))
      def func(x):
        key = type(x) if x is not None else None
        if key not in matchers:
          key = None
        M = matchers[key]
        for (condition, transform) in M:
          if (condition is None) or( callable(condition) and condition(x)):
            if callable(transform):
              return transform(x)
            else:
              return transform
        return None
      return self.chain(func)
    elif isinstance(arg, slice):
      condition = (
          arg.start          if callable(arg.start) else (
          not_none
      ))
      yes_transform = (
          arg.stop            if callable(arg.stop) else (
          (lambda x : arg.stop) if arg.stop is not None else (
          identity
      ))) 
      no_transform = (
          arg.step            if callable(arg.step) else (
          (lambda x : arg.step) if arg.step is not None else (
          None
      )))
      def gen(xs):
        for x in xs:
          if condition(x):
            yield yes_transform(x)
          elif no_transform is not None:
            yield no_transform(x)
      return self.chain_in(gen)


# P
#   [
#     Ta :: fa,
#     Tb :: fb,
#     Tc :condition: fc,
#     : f_star
#   ]

#   [ 
#     # matching types and mapping with functions
#     str   :: lambda x : (int(a),[a]),
#     list  :: lambda x : (len(a),[]),

#     # matching types and mapping to values
#     tuple :: (0,["tuppy"])

#     # matching types and conditionally mapping
#     float : lambda x: x>0 : lambda x : (int(-a),[]),
#     float :: lambda x : (int(a),[]),

#     int   : lambda x: x>0 : lambda x : (-a,[]),
#     int   :: lambda x : (a,[]),

#     # explicit removal of dicts from the pipeline
#     dict :: None,
    
#     # default matcher
#     :: (0,[])
#   ]
  
#   [
#     int : lambda x: x==1 : 1
#     # recursive case, yield back
#     int, :: lambda x,block=None : x * block(x-1)
#   ]