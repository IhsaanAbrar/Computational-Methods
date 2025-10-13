#!/usr/bin/env python
# coding: utf-8

# In[5]:


import sympy as sp
from sympy.interactive import printing
from IPython.display import display

printing.init_printing(use_latex=True)

x = sp.symbols('x')
f = sp.Function('f')(x)

# Define and display the differential equation
diffeq = sp.Eq(sp.diff(f, x, 2) - 5*f, 10)
display(diffeq)

# Solve and display the result
solution = sp.dsolve(diffeq, f)
display(solution)


# In[ ]:




