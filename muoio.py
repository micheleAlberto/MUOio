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


class Piper(Pipe):
  def __call__(self, gen):
    return self.chain_in(gen)
  def __getitem__(self, arg):
    if isinstance(arg, slice):
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

    