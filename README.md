# multi_glods_python
Python translation of MATLAB MultiGLODS 0.1 (with random search method only)

## Translation of MultiGLODS to Python
The original MultiGLODS 0.1 is written in MATLAB by Dr. Ana Luise Custódio and 
J. F. A. Madeira at the Nova School of Science and Technology and at ISEL and IDMEC-IST, Lisbon
respectively.  Please use the following references and complementary material:

A. L. Custódio and J. F. A. Madeira, MultiGLODS: Global and Local Multiobjective 
Optimization using Direct Search, Journal of Global Optimization, 72 (2018), 323 - 345 PDF

This Python project, moves MultiGLODS to a state based design so that the objective function calls
are de-embedded from loops and could be executed as callbacks with minor modification. The translation
to Python allows the algorithm to be run without using MATLAB licensed software and allows for interoperability
with AntennaCAT software written by Lauren Linkous at VCU. Much of the code is a direct translation and 
as such is GPL 3.0 like MultiGLODS before it. Please include the license with any derivative work, and 
please be sure to credit the original creators. 

Due to the translation the majority of code is written in the proceedural style characteristic of most
MATLAB code; however, it has been wrapped in a class in multi_glods.py with an example use case in 
multiglods_test.py.  Some configuration options (including certain search methods, and starting configurations)
were not translated due to the MATLAB libraries these were implemented in (Pull requests with the functionality 
returned would be appreciated if anyone has interests and time).

This is not an actively maintained project and is provided with no waranty, may not be stable under all conditions
or work as expected against all functions. 

Requires Python 3.6 or later.
