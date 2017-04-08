# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: To formulate this as a CSP, we define the variables to be the regions like boxes on the board.
   The domain of each variable is the set of numbers like {1,2,3,4,5,6,7,8,9}.
   The solution of this problem requires naked twins to be removed from every other box within the same row and column.
   Constraint propagation is about propagating constraint of removing the naked twins from one variable onto other variables.
   A solution is therefore a set of values for the variables that satisfies all constraints.
   We are iteratively applying removing: from each boxes, for each peers, already founded naked twins;
   as long as we won't be able to apply this removing (then we now that no more naked_twins from peers can be removed)

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: To formulate this as a CSP, we define the variables to be the regions like boxes on the board.
   The domain of each variable is the set of numbers like {1,2,3,4,5,6,7,8,9}.
   The solution requires distinct number in the boxes within the same row, column and diagonal.
   Constraint propagation is about propagating constraints like elimination and only_choice from one variable onto other variables (states of the board).
   A solution is therefore a set of values for the variables that satisfies all constraints.
   Iterate eliminate() and only_choice(). If after an iteration of both functions, the sudoku remains the same, return the sudoku.
   At the same time elimination() has been extended for diagonal peers.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

