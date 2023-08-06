# Dirio - Python Independent Class Process
[![PyPi Version](https://img.shields.io/pypi/v/dirio)](https://github.com/manahter/dirio)
[![Python Version](https://img.shields.io/pypi/pyversions/dirio)](https://github.com/manahter/dirio)
[![Dirio](https://img.shields.io/github/license/manahter/dirio)](https://github.com/manahter/dirio/blob/main/LICENSE)
![GitHub last commit](https://img.shields.io/github/last-commit/manahter/dirio)
[![PyPi Downloads](https://img.shields.io/pypi/dm/dirio)](https://github.com/manahter/dirio)

The class in your main file becomes the client. 
Another working Class is created in parallel. 
When the client calls the method, the Class in the other file does the job.
The class in the main file gets the reply to the method.

## Features
* Inherit Class independently from running script.
* Uses serialization method with JSON
* You do not wait in classes like Socket

## Cons
* Since it is JSON based, it supports; dict, list, tuple, int, str, float, bool, type (None). 
  Does not support serialize of other types (like object etc)

## Install
```buildoutcfg
pip3 install dirio
```
or
```buildoutcfg
pip install dirio
```


## Usage

```python
# Import module
from dirio import Dirio


# Inherit class
# args mut be tuple. Don't forget to put a comma -> args=(xx, )
try_cls = Dirio(target=TryClass, args=("arg1",), kwargs={"key1": "val1"})
# PARAMETERS:
#   target      : class : Target Class
#   args        : tuple : Arguments for Target Class
#   kwargs      : dict  : Keyword Arguments for Target Class
#   tempdir     : str   : Temporary directory path. If it is empty, system temp path is used.
#   keeperiod   : float : !!! Not activated. Do not use.
#   looperiod   : float : Independent Class renewal frequency. 
#                         Default: .05
#                         Smaller value, more CPU
#                         Bigger  value, delayed processing
#   worker      : bool  : You don't use. The class itself uses



# Standard, Call your method, 
# First time return value is None
try_cls.yourmethod("arg1", key="value")
#-> Returned: None

# In the next call, the return value is that of the previous one.
try_cls.yourmethod("arg1", key="value")
#-> Returned: "result_of_previous_call_returned"

# If you want to return the value of the method you are calling;
# Notice; dr_code=True used
call_code = try_cls.yourmethod("arg1", key="value", dr_code=True)
#-> call_code -> 12

# Give the result of call code 12
try_cls.yourmethod("arg1", key="value", dr_code=call_code)
#-> Returned: None

# After a short while. Call it directly from the dr_code
try_cls.dr_code(dr_code=call_code)
#-> Returned: "result_of_previous_call_returned"

# If None, the method operation is not yet run or finished.
# We can call again and again
try_cls.yourmethod("arg1", key="value", dr_code=call_code)
#-> Returned: "result_of_previous_call_returned"

# We can wait as long as we want the answer to arrive
# dr_wait=3.4 -> Wait 3.4 second
try_cls.yourmethod("arg1", key="value", dr_wait=3.4)
#-> Returned: "result_of_previous_call_returned"
# if the operation is not over
#-> Returned: None

# Wait until the reply comes
# dr_wait=-1 -> until the operation is over
try_cls.yourmethod("arg1", key="value", dr_wait=-1)
#-> Returned: "result_of_previous_call_returned"

# Terminate the Dirio Process. 
# Make sure to use this at the end of the script.
try_cls.dr_terminate()

# When the result of the code returns, run the function.
# Function must take a parameter named 'result'. The return value is put in this parameter.
try_cls.dr_bind(code=call_code, func=your_func, args=("arg1", ), kwargs={"key1": "val1"})
# -> Calling:  your_func(arg1, key1="val1", result="dr_result_value")

# If we check it in the cycle, it will get faster results.
# Sometimes need to check if there is event. Binds work this way.
try_cls.dr_binds_check()

# Is active, control
try_cls.dr_isactive()
```

NOTE : Sorry, my English is poor. I use translation.