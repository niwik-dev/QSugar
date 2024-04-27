"""
The framework mainly uses decorator syntax to implement dynamic proxies.

And the submodules are described below:
    - `count`
        * proxy setter methods in the style of the Fluent api
        * implement the `self` property to get the control handle proxy
        * simplify the naming and calling of some attributes

    - `bind`
        * proxy setter methods to accommodate reactive programming

    - `dsl`
        * implement the child and children properties to meet the most basic nested DSL requirements

More modules are coming...
Any good ideas? Welcome to contact me!

"""
from .base import Batch, Def
from .bind import Bind
from .dsl import DSL

