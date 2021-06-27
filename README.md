# python-decorators
## Python: chained decorators with arguments and a practical example of logging function calls with a decorator.

Annotated experiments on decorators.

Beware: using with no arguments (as in `@dec`) a decorator that expects arguments (as in `@dec(args)`), 
breaks your code. The correct syntax if you want to pass no arguments to such a decorator is `@dec()`.

practical use of decorators can be, for example, for timing, logging, error check, type check...

See `example1` for an implementation of chained decorators with or without arguments.

See `example2` for a practical example of a function call log implemented via decorators.
