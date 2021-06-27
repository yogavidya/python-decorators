from datetime import datetime
from typing import Callable
"""
  Annotated experiments on decorators.
  Beware: using with no arguments, as in @dec a decorator that expects arguments,
    as in @dec(args), breaks your code. The correct syntax if you want to pass
    no arguments to such a decorator is @dec().
  practical use of decorators can be, for example, for timing, logging, error check, type check...
  See example1() for an implementation of chained decorators with or without arguments.
  See example2() for a practical example of a function call log implemented via decorators.
"""



def example1():
  """Three chained decorators:
    * format result into a string (no arguments)
    * execute n times (one argument) 
    * add documentation (one argument with default)
  """
  def doc_dec(doc='no document'):
    def doc_dec(f): # wrapper 1: arguments from enclosing dec, receives function
      def doc_dec_wrapper(*args, **kwargs): # wrapper 2: receives function args
        return f(*args, **kwargs)
      doc_dec_wrapper.__doc__ = doc
      return doc_dec_wrapper
    return doc_dec

  def outer_dec(n): # used with arguments: receives arguments
    def outer_dec(f): # wrapper 1: arguments from enclosing dec, receives function
      def outer_dec_wrapper(*args, **kwargs): # wrapper 2: receives function args
        result = []
        for _ in range(n):
          result.append(f(*args, **kwargs))
        return 'outer_dec ' + str(result)
      return outer_dec_wrapper
    return outer_dec
        
        
  def inner_dec(f): # used with no arguments, receives the function
    def inner_wrapper(*args, **kwargs):
      return 'inner_dec: "' + str(f(*args, **kwargs) + '"')
    return inner_wrapper


  @doc_dec('My function documentation')
  @outer_dec(2)
  @inner_dec
  def my_f(n):
    return(f'my_f = {n}')

  print(f'Docstring for my_f: {my_f.__doc__}')
  print(my_f(42))

def example2():
  def log_decorator(logfilename='functions.log'):
    def open_file_and_run(f: Callable):
      logfile = open(logfilename,'a')
      def log_execution(*args, **kwargs):
        time_start = datetime.now()
        try:
          exception = False
          result = f(*args, **kwargs)
        except Exception as exc:
          exception = True
          result = exc
        finally:
          time_end = datetime.now()
          logfile.write(
            f'''\n{str(time_start)}
              function call: {f.__module__}.{f.__name__}
              args: {args}
              kwargs: {kwargs}
              end time: {str(time_end)}
              elapsed: {str(time_end - time_start)}
              ''')
          if exception:
            logfile.write(
              f'''\tRAISED EXCEPTION
                  \tof type {type(result)}
                  \targs: {repr(result.args)}
                  ''')
          else:
            logfile.write(f'function returned: {type(result)}, value: {repr(result)}\n')
          if exception:
            raise result
          return result
      return log_execution
    return open_file_and_run
    
  @log_decorator()
  def target_fn():
    return 42

  @log_decorator()
  def target_fn_except(a, b):
    return a / b
  
  print(target_fn())
  print(target_fn_except(1,1))
  print(target_fn_except(1,0))
  
example1()
example2()