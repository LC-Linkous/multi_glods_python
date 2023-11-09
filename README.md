# multi_glods_python
Python translation of MATLAB MultiGLODS 0.1 (with random search method only)

## Translation of MultiGLODS to Python
The original MultiGLODS 0.1 was is written in MATLAB by Dr. Ana Luise Custódio and 
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
