#! /usr/bin/python3

##--------------------------------------------------------------------\
#   multi_glods_python
#   './multi_glods_python/src/main_test_graph.py'
#   Test function/example for using the multiglods optimizer. To match
#       the format of the other optimizers in the AntennaCAT suite, this
#       file directly replaces multiglods_test.py from the main branch
#       of multi_glods_python. Format updates are for integration in
#       the AntennaCAT GUI.
#       This has been modified from the original to include message 
#       passing back to the parent class or testbench, rather than printing
#       error messages directly from the 'multiglods' class. 

#       This version builds from 'main_test.py' to include a 
#       matplotlib plot of particle location
#
#   Author(s): Jonathan Lundquist, Lauren Linkous 
#   Last update: June 28, 2024
##--------------------------------------------------------------------\



import numpy as np
import time
import matplotlib.pyplot as plt

import sys
# multiGLODS functions
try: # for outside func calls, program calls
    sys.path.insert(0, './multi_glods_python/src/')
    from multi_glods import multi_glods

except:# for local, unit testing
    from multi_glods import multi_glods


# OBJECTIVE FUNCTION SELECTION
#import one_dim_x_test.configs_F as func_configs     # single objective, 1D input
#import himmelblau.configs_F as func_configs         # single objective, 2D input
import lundquist_3_var.configs_F as func_configs     # multi objective function



class TestGraph():
    def __init__(self):
        self.ctr = 0
        
        # Constant variables
        TOL = 10 ** -6      # Convergence Tolerance (This is a radius 
                                # based tolerance, not target based tolerance)
        MAXIT = 10000        # Maximum allowed iterations  

        # Objective function dependent variables
        LB = func_configs.LB[0]              # Lower boundaries, [[0.21, 0, 0.1]]
        UB = func_configs.UB[0]              # Upper boundaries, [[1, 1, 0.5]]
        IN_VARS = func_configs.IN_VARS      # Number of input variables (x-values)   
        OUT_VARS = func_configs.OUT_VARS     # Number of output variables (y-values)
        TARGETS = func_configs.TARGETS       # Target values for output

        # Objective function dependent variables
        func_F = func_configs.OBJECTIVE_FUNC  # objective function
        constr_F = func_configs.CONSTR_FUNC   # constraint function


        # optimizer specific vars
        BP = 0.5            # Beta Par
        GP = 1              # Gamma Par
        SF = 2              # Search Frequency

        # optimizer setting values
        parent = None                 # Optional parent class for optimizer
                                        # (Used for passing debug messages or
                                        # other information that will appear 
                                        # in GUI panels)

        self.best_eval = 1

        self.suppress_output = True   # Suppress the console output of multiglods



        detailedWarnings = False      # Optional boolean for detailed feedback
                                        # (Independent of suppress output. 
                                        #  Includes error messages and warnings)

        self.allow_update = True      # Allow objective call to update state 
                                # (Can be set on each iteration to allow 
                                # for when control flow can be returned 
                                # to multiglods)   


        # instantiation of multiglods optimizer 
        self.optimizer = multi_glods(IN_VARS, LB, UB, TARGETS, TOL, MAXIT,
                        func_F=func_F, constr_func=constr_F,
                        BP=BP, GP=GP, SF=SF,
                        parent=parent, detailedWarnings=detailedWarnings)


        # Matplotlib setup
        self.targets = TARGETS
        self.fig = plt.figure(figsize=(10, 5))#(figsize=(14, 7))
        # position
        self.ax1 = self.fig.add_subplot(121, projection='3d')
        self.ax1.set_title("Search Locations, Iteration: " + str(self.ctr))
        self.ax1.set_xlabel('x_1')
        self.ax1.set_ylabel('x_2')
        self.ax1.set_zlabel('x_3')
        self.scatter1 = None
        # fitness
        self.ax2 = self.fig.add_subplot(122, projection='3d')
        self.ax2.set_title("Fitness Relation to Target")
        self.ax2.set_xlabel('x_1')
        self.ax2.set_ylabel('x_2')
        self.ax2.set_zlabel('x_3')
        self.scatter2 = None
        # plotting dims
        self.in_vals = IN_VARS
        self.out_vals = OUT_VARS


    def debug_message_printout(self, txt):
        if txt is None:
            return
        # sets the string as it gets it
        curTime = time.strftime("%H:%M:%S", time.localtime())
        msg = "[" + str(curTime) +"] " + str(txt)
        print(msg)


    def update_plot(self, x_coords, y_coords, targets, last_iter, showTarget=True, clearAx=True):
        
        # check if any points. first call might not have anythign set yet.
        if len(x_coords) < 1:
            return 


        if clearAx == True:
            self.ax1.clear() #use this to git rid of the 'ant tunnel' trails
            self.ax2.clear()

        # MOVEMENT PLOT
        if np.shape(x_coords)[1]==1: # 1 dim function
            x_plot_coords = np.array(x_coords[:,0])*0.0
            title_txt = "Search Locations, Step: " + str(self.ctr) + ", Objective Iter: " + str(last_iter)
            self.ax1.set_title(title_txt)
            self.ax1.set_xlabel("$x_1$")
            self.ax1.set_ylabel("filler coords")
            self.ax1.set_zlabel("filler coords")
            self.scatter = self.ax1.scatter(x_coords, x_plot_coords, edgecolors='b')   
        
        elif np.shape(x_coords)[1] == 2: #2-dim func
            title_txt = "Search Locations, Step: " + str(self.ctr) + ", Objective Iter: " + str(last_iter)
            self.ax1.set_title(title_txt)
            self.ax1.set_xlabel("$x_1$")
            self.ax1.set_ylabel("$x_2$")
            self.ax1.set_zlabel("filler coords")
            self.scatter = self.ax1.scatter(x_coords[:,0], x_coords[:,1], edgecolors='b')

        elif np.shape(x_coords)[1] == 3: #3-dim func
            title_txt = "Search Locations, Step: " + str(self.ctr) + ", Objective Iter: " + str(last_iter)
            self.ax1.set_title(title_txt)
            self.ax1.set_xlabel("$x_1$")
            self.ax1.set_ylabel("$x_2$")
            self.ax1.set_zlabel("$x_3$")
            self.scatter = self.ax1.scatter(x_coords[:,0], x_coords[:,1], x_coords[:,2], edgecolors='b')


        # FITNESS PLOT
        if np.shape(y_coords)[1] == 1: #1-dim obj func
            y_plot_filler = np.array(y_coords[:,0])*0.0
            self.ax2.set_title("Global Best Fitness Relation to Target")
            self.ax2.set_xlabel("$F_{1}(x_1,x_2)$")
            self.ax2.set_ylabel("filler coords")
            self.ax2.set_zlabel("filler coords")
            self.scatter = self.ax2.scatter(y_coords, y_plot_filler,  marker='o', s=40, facecolor="none", edgecolors="k")

        elif np.shape(y_coords)[1] == 2: #2-dim obj func
            self.ax2.set_title("Global Best Fitness Relation to Target")
            self.ax2.set_xlabel("$F_{1}(x_1,x_2)$")
            self.ax2.set_ylabel("$F_{2}(x_1,x_2)$")
            self.ax2.set_zlabel("filler coords")
            self.scatter = self.ax2.scatter(y_coords[:,0], y_coords[:,1], marker='o', s=40, facecolor="none", edgecolors="k")

        elif np.shape(y_coords)[1] == 3: #3-dim obj fun
            self.ax2.set_title("Global Best Fitness Relation to Target")
            self.ax2.set_xlabel("$F_{1}(x_1,x_2)$")
            self.ax2.set_ylabel("$F_{2}(x_1,x_2)$")
            self.ax2.set_zlabel("$F_{3}(x_1,x_2)$")
            self.scatter = self.ax2.scatter(y_coords[:,0], y_coords[:,1], y_coords[:,2], marker='o', s=40, facecolor="none", edgecolors="k")


        if showTarget == True: # plot the target point
            if len(targets) == 1:
                self.scatter = self.ax2.scatter(targets[0], 0, marker='*', edgecolors='r')
            if len(targets) == 2:
                self.scatter = self.ax2.scatter(targets[0], targets[1], marker='*', edgecolors='r')
            elif len(targets) == 3:
                self.scatter = self.ax2.scatter(targets[0], targets[1], targets[2], marker='*', edgecolors='r')


        plt.pause(0.0001)  # Pause to update the plot
        if self.ctr == 0:
            time.sleep(3)
            
        self.ctr = self.ctr + 1



    def run(self):

        # sometimes multiGLODS doesn't call the objective function, so only print out when it does
        last_iter = 0
        while not self.optimizer.complete():

            # step through optimizer processing
            self.optimizer.step(self.suppress_output)

            # call the objective function, control 
            # when it is allowed to update and return 
            # control to optimizer
            self.optimizer.call_objective(self.allow_update)
            iter, eval = self.optimizer.get_convergence_data()
            if (eval < self.best_eval) and (eval != 0):
                self.best_eval = eval
            if iter > last_iter:
                last_iter = iter
                if self.suppress_output:
                    if iter%100 == 0: #print out every 100th iteration update
                        print("************************************************")
                        print("Objective Function Iterations: " + str (iter))
                        print("Best Eval: " + str(self.best_eval))

            x_coords = np.array(self.optimizer.get_search_locations()).T
            y_coords = np.array(self.optimizer.get_fitness_values()).T
            self.update_plot(x_coords, y_coords, self.targets, last_iter, showTarget=True, clearAx=True) #update matplot

        print("************************************************")
        print("Objective Function Iterations: " + str (iter))
        print("Best Eval: " + str(self.best_eval))
        print("Optimized Solution")
        print(self.optimizer.get_optimized_soln())
        print("Optimized Outputs")
        print(self.optimizer.get_optimized_outs())

        time.sleep(15) #keep the window open for 15 seconds before ending program

if __name__ == "__main__":
    tg = TestGraph()
    tg.run()
