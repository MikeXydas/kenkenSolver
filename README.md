


# Ken Ken CSP solver

## Introduction

Ken Ken is an arithmetic and logic puzzle (https://en.wikipedia.org/wiki/KenKen). It is a simple Constraint Satisfaction Problem aiming to solve it using algorithms like **BT, BT+MRV, FC, FC+MRV and MAC, min_confilcts** provided by aimacode (https://github.com/aimacode/aima-python/blob/master/csp.py).

## Prerequisites

* Python3.6
* numpy

In `kenKen.py` I have 5 hardcoded problems. They are of increasing complexity and consequently need more time to be solved (For some cases like the simple BT solving a hard problem is not possible).

## Representing the CSP

* **Variables**: The points (x, y) representing a point in the grid and the cliques named 0, 1, 2, 3...
* **Domains**: 
    * For the point variables: {1, 2, 3, ..., n} where n is the dimensions of the puzzle
    * For the clique variables: The values that satisfy the clique constraint. For example, for a clique of size 3 with constraint +4 and puzzle dimensions 4 the domain would be {(1, 1, 2), (1, 2, 1), (2, 1, 1)}.
* **Neighbors**: 
    * Point neighbors: The points of the same row and column
    * Clique neighbors: The points that the clique contains
* **Constraints**:
    * Point with point: Check for their values to be different
    * Point with clique: We find which index in the clique the point has. (1st, 2nd ...) and we check if the value of the point equals with any domain value of the clique in that index.


## Conclusions

First column dimensions, first row algorithm used

![](https://lh3.googleusercontent.com/dpBSX_hqHvk9HtysDwVcodd9N0aVwg1cBCLunL0yxpFa2CLxY7hHpjvE85zVufZ6t1zR1VBoPzM)

![enter image description here](https://lh3.googleusercontent.com/9ISu4YnZpZGynT4P52f9ktDrqTtv_JeM7TdRtBxgaEpsQ2FvDIen6tNPw_qALFHzBM0zQzG8jEA)

From the above tables, we conclude that MAC is the one that will have a consistent fast time against all the other algorithms. Although due to a bigger overhead in small dimensions will not be the fastest (dims < 7).

Considering the min_conflicts algorithm, we will not be able to have a result since it exhausts max_steps really fast without finding any value that satisfies the constraints. This is explained by the high complexity of the puzzle.
