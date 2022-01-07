# Circuit-solver
## This is a basic circuit solver which will take in the graph of the circuit in the form of a tree and its branches and will give you the currents and voltages accross each branch and node in laplace domain.

 -  I made the solver which will also give the inverse laplace transform to you.
 -  It will print the cutset matrix, branch matrix, Vg matrix, and Ig matrix.
 -  Format for the input file is:
    1. All the elements in a line should be space separated.
    2. One line corresponds to one branch.
    3. Before entering the values in the input.txt file. Make a tree and separate the twigs and the links with their values of Vg and Ig and R,L,C.
    4. Now, once tree is found and made.
    5. Enter the data in the file in following order.
        1. First enter t or l for twig or link.
        2. Then enter the starting node.
        3. Then enter the ending node.(direction of branch is from start node to end node)
        4. Enter Vg(in V) (please only keep variable s only in the expression of Vg expand sqareroots and pi to their original float values.)
        5. Enter Ig(in A) (variable should be only s and expand pi and sqrt(2) to its original value.)
        6. Then enter value of R in Ohm
        7. Then the value of L in henry(you can use the exponential notation 1e-6).
        8. Then the value of C in farad(you can use the exponential notation 1e-6).
        9. All the above values should be space separated and new branch starts from new line.
 - The output matrices will have the same order of twigs and links as given in input
    1. For eample:
    2. If you enter twig 1, then link 1, then twig 2 then the output will show the twig1, then twig 2 then link1.
    3. If you enter the branches according to the names given by you then the predicted order for the matrix will be given out.
    4. Let’s say graph has twigs(1,2,6,7,8) and links(3,4,5,9).
    5. And if all entries according to the name then the output will also have (1,2,3,7,8,3,4,5,9).
 - The programme will find the loop matrix and the branch matrix.
 - Then it will print all the matrices.
 - And finally it will print the inverse laplace transforms of the Vs and Is.
 - It will store the Vs and Is in  vs.txt and is.txt files respectively.
 - The programme could not run for bigger circuits but for smaller circuits is showing exact results.
