# multi_glods_antennaCAT

Python-based MultiGLODS optimizer compatable with the [AntennaCAT](https://github.com/LC-Linkous/AntennaCalculationAutotuningTool) optimizer suite.  This has been forked & modified from [multi_glods_python](https://github.com/jonathan46000/multi_glods_python) by [jonathan46000](https://github.com/jonathan46000).  Now featuring AntennaCAT hooks for GUI integration and user input handling.

The [multi_glods_python](https://github.com/jonathan46000/multi_glods_python) by [jonathan46000](https://github.com/jonathan46000), is a Python translation of MATLAB MultiGLODS 0.1 (with random search method only). Please see the []() and []() sections for more information about the translation of the code and the original publication.


# IN PROGRESS!! Currently undergoing a major reformat for paths, comments, and documentation.
For consistency across optimizers, files have been pulled from other files in LC-Linkous's optimizer 
collection for AntennaCAT. This project does not currently work due to all of the path breakage 
but a backup was needed during the restructure


## Table of Contents
* [MultiGLODS](#multiglods)
* [Translation of MultiGLODS to Python](#)
* [Requirements](#requirements)
* [Implementation](#implementation)
    * [Constraint Handling](#constraint-handling)
    * [Internal Objective Function Examples](#internal-objective-function-examples)
* [Example Implementations](#example-implementations)
    * [Basic Example](#basic-example)
    * [Realtime Graph](#realtime-graph)
* [References](#references)
* [Publications and Integration](#publications-and-integration)
* [Licensing](#licensing)  



## MultiGLODS


The Multiobjective Optimization Global and Local Optimization using Direct Search (MultiGLODS) [1] is an algorith created by Dr. Ana Luise Custódio (Nova School of Science and Technology, Lisbon) and J. F. A. Madeira (ISEL and IDMEC-IST, Lisbon). It is a derivative-free optimizizer generalized for calculating the Pareto fronts of multiobjective multimodal derivative-free optimization problems. It builds off their GLODS algorithm in [2]. 

Some key points of this algorithm are:

* "The proposed algorithm alternates between initializing new searches, using a multistart strategy, and exploring promising subregions, resorting to directional direct search. Components of the objective function are not aggregated and new points are accepted using the concept of Pareto dominance. The initialized searches are not all conducted until the end, merging when they start to be close to each other. The convergence of the method is analyzed under the common assumptions of directional direct search. Numerical experiments show its ability to generate approximations to the different Pareto fronts of a given problem." [1]

* "Points sufficiently close to each other are compared and only nondominated points will remain active. In the end of the optimization process, the set of all active points will define the approximations to the Pareto fronts of the problem (local and global)." [1]



## Translation of MultiGLODS to Python
From the [multi_glods_python README:](https://github.com/jonathan46000/multi_glods_python/blob/main/README.md)

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
multiglods_test.py

## Requirements

This project requires numpy and matplotlib. The original multi_glods_python does not require matplotlib or its dependencies.

Use 'pip install -r requirements.txt' to install the following dependencies:

```python
contourpy==1.2.1
cycler==0.12.1
fonttools==4.51.0
importlib_resources==6.4.0
kiwisolver==1.4.5
matplotlib==3.8.4
numpy==1.26.4
packaging==24.0
pillow==10.3.0
pyparsing==3.1.2
python-dateutil==2.9.0.post0
six==1.16.0
zipp==3.18.1

```


## Implementation

### Constraint Handling
Users must create their own constraint function for their problems, if there are constraints beyond the problem bounds.  This is then passed into the constructor. If the default constraint function is used, it always returns true (which means there are no constraints).


### Internal Objective Function Examples

There are three functions included in the repository:
1) Himmelblau's function, which takes 2 inputs and has 1 output
2) A multi-objective function with 3 inputs and 2 outputs (see lundquist_3_var)
3) A single-objective function with 1 input and 1 output (see one_dim_x_test)

Each function has four files in a directory:
   1) configs_F.py - contains imports for the objective function and constraints, CONSTANT assignments for functions and labeling, boundary ranges, the number of input variables, the number of output values, and the target values for the output
   2) constr_F.py - contains a function with the problem constraints, both for the function and for error handling in the case of under/overflow. 
   3) func_F.py - contains a function with the objective function.
   4) graph.py - contains a script to graph the function for visualization.



<p align="center">
        <img src="https://github.com/LC-Linkous/bayesian_optimization_python/blob/main/media/himmelblau_plots.png" alt="Himmelblau function" height="250">
</p>
   <p align="center">Plotted Himmelblau Function with 3D Plot on the Left, and a 2D Contour on the Right</p>

```math
f(x, y) = (x^2 + y - 11)^2 + (x + y^2 - 7)^2
```

| Global Minima | Boundary | Constraints |
|----------|----------|----------|
| f(3, 2) = 0                 | $-5 \leq x,y \leq 5$  |   | 
| f(-2.805118, 3.121212) = 0  | $-5 \leq x,y \leq 5$  |   | 
| f(-3.779310, -3.283186) = 0 | $-5 \leq x,y \leq 5$  |   | 
| f(3.584428, -1.848126) = 0  | $-5 \leq x,y \leq 5$   |   | 




<p align="center">
        <img src="https://github.com/LC-Linkous/bayesian_optimization_python/blob/main/media/lundquist_3var_plots.png" alt="Function Feasible Decision Space and Objective Space with Pareto Front" height="200">
</p>
   <p align="center">Plotted Multi-Objective Function Feasible Decision Space and Objective Space with Pareto Front</p>

```math
\text{minimize}: 
\begin{cases}
f_{1}(\mathbf{x}) = (x_1-0.5)^2 + (x_2-0.1)^2 \\
f_{2}(\mathbf{x}) = (x_3-0.2)^4
\end{cases}
```

| Num. Input Variables| Boundary | Constraints |
|----------|----------|----------|
| 3      | $0.21\leq x_1\leq 1$ <br> $0\leq x_2\leq 1$ <br> $0.1 \leq x_3\leq 0.5$  | $x_3\gt \frac{x_1}{2}$ or $x_3\lt 0.1$| 



<p align="center">
        <img src="https://github.com/LC-Linkous/bayesian_optimization_python/blob/main/media/1D_test_plots.png" alt="Function Feasible Decision Space and Objective Space with Pareto Front" height="200">
</p>
   <p align="center">Plotted Single Input, Single-objective Function Feasible Decision Space and Objective Space with Pareto Front</p>

```math
f(\mathbf{x}) = sin(5 * x^3) + cos(5 * x) * (1 - tanh(x^2))
```

## Example Implementations

### Basic Example
main_test.py provides a sample use case of the optimizer with tunable parameters.

### Realtime Graph

<p align="center">
        <img src="https://github.com/LC-Linkous/bayesian_optimization_python/blob/main/media/surrogate_model_progress.gif" alt="gif of surrogate model development through iterations" height="325">
</p>
<p align="center">Bayesian Optimization with a Gaussian Proccess Using Himmelblau. Left to Right: Objective function ground truth, areas of interest to the optimizer, and surrogate model development process.</p>

<br>
<br>
<p align="center">
        <img src="https://github.com/LC-Linkous/bayesian_optimization_python/blob/main/media/surrogate_model_1X.gif" alt="gif of surrogate model development through iterations" height="325">
</p>
<p align="center">Bayesian Optimization with a Gaussian Proccess Using Single Input, Single Objective Function. Left, Gaussian Process Regression Model. Right: Aquisition Function.</p>

<br>
<br>

<p align="center">
        <img src="https://github.com/LC-Linkous/bayesian_optimization_python/blob/main/media/surrogate_model_multi_obj.gif" alt="gif of surrogate model development through iterations" height="325">
</p>
<p align="center">Bayesian Optimization with a Gaussian Proccess Using Multi-Objective Function. Left, Objective Function Output and Sampling. Right, Surrogate Model GP Mean Fitting and Sample Points.</p>

<br>
<br>

main_test_graph.py provides an example using a parent class, and the self.suppress_output and detailedWarnings flags to control error messages that are passed back to the parent class to be printed with a timestamp. Additionally, a realtime graph shows particle locations at every step.

The figure above shows a low-resolution version of the optimization for example. In this first figure, the Far left plot is the objective ground truth function with sample locations in red. The center plot is the expected improvement, which highlights areas of interest to the optimizer. The far right plot is the current shape of the surrogate model, with sampled points from the ground truth in red. The other two graphs present a similar process for different dimensions of objective functions.


NOTE: if you close the graph as the code is running, the code will continue to run, but the graph will not re-open.



## References

[1] A. L. Custódio and J. F. A. Madeira, “MultiGLODS: global and local multiobjective optimization using direct search,” Journal of Global Optimization, vol. 72, no. 2, pp. 323–345, Feb. 2018, doi: https://doi.org/10.1007/s10898-018-0618-1.

[2] A. L. Custódio and J. F. A. Madeira, “GLODS: Global and Local Optimization using Direct Search,” Journal of Global Optimization, vol. 62, no. 1, pp. 1–28, Aug. 2014, doi: https://doi.org/10.1007/s10898-014-0224-9.



## Publications and Integration
This software works as a stand-alone implementation, and as one of the optimizers integrated into AntennaCAT. Publications featuring the code as part of AntennaCAT will be added as they become public.

When citing the algorithm itself, please refer to the original publication for MultiGLODS by the original authors:

A. L. Custódio and J. F. A. Madeira, MultiGLODS: Global and Local Multiobjective 
Optimization using Direct Search, Journal of Global Optimization, 72 (2018), 323 - 345 PDF




## Licensing

Unlike other optimizers in the AntennaCAT suite, which were released under GPL-2.0, this work is licensed
under GPL-3.0 per the license used by the original authors of the MultiGLODS algorithm. 


