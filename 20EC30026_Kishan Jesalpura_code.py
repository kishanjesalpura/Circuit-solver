import sympy as sym
from sympy.functions import transpose
import math
import sys

''' This is a programme in which you will give you:
        currents in branches
        voltages at nodes.
    This is done form:
        input given in file about branch data with start node, end node, Voltage source and current source accross the branch.
        it also has values of resistances, Inductors and Capacitors.

'''

s=sym.sympify("s")

class Node():

    ''' 
    class for the nodes in the circuit
    (bevare the node should be a part of circuit)
    '''

    def __init__(self, node_no, incoming_twigs , outgoing_twigs , incoming_links , outgoing_links ):
        self.node_no = node_no
        self.incoming_twigs = incoming_twigs
        self.incoming_links = incoming_links
        self.outgoing_twigs = outgoing_twigs
        self.outgoing_links = outgoing_links

    def __str__(self):
        return(f"node_no = {self.node_no}\n incoming_twigs = {self.incoming_twigs}\n outgoing_twigs = {self.outgoing_twigs}\n incoming_links = {self.incoming_links}\n outgoing_links = {self.outgoing_links}\n")

class Branch():

    '''
    class for the branches in the circuit
    (Bevare the node should be a part of circuit too)
    '''

    def __init__(self, branch_name, start_node, end_node, R = 0, L = 0, C = 0, Vg = 0, Ig = 0):
        self.branch_name = branch_name
        self.start_node = start_node
        self.end_node = end_node
        self.R = R
        self.L = L
        self.C = C
        self.Vg = sym.simplify(str(Vg))
        self.Ig = sym.simplify(str(Ig))

    def impedance(self):
        self.impedance = self.R+self.L*s
        if self.C!=0:
            self.impedance += 1/s/self.C
        return self.impedance
''' input file format is
        below are the parameters taken in order in one line.
        1. branch/node (first charachter of any of both) (for this version only branches are compatible.)
        2. start node for branch
        3. end node of branch
        4. Vg
        5. Ig
        6. R
        7. L
        8. C
        (every value should be space seperated. Compulsory plz... ;) )
'''

class Circuit():

    ''' 
    class that stores the circuit in the form of nodes and branches
    '''

    def __init__(self, nodes = [], twigs = None, links = None):
        self.nodes = []
        self.twigs = []
        self.links = []

    def circuit_read(self, circuit):
        # Reading the input file
        with open(circuit, "r") as circuit:

            # Loop to seperte the nodes and branches and store them in nodes and branches list.
            data = circuit.readline()
            c=0
            while data!='':
                l = []
                for x in data.split(' '):
                    if x != '':
                        l.append(x)
                if l[0] == 't':
                    twig = Branch(c+1, None, None, float(l[5]), float(l[6]), float(l[7]), sym.sympify(l[3]), sym.sympify(l[4]))
                    self.twigs.append(twig)
                    s_node = float(l[1])
                    e_node = float(l[2])
                    for y in self.nodes:
                        if y.node_no == s_node:
                            y.outgoing_twigs.append(twig)
                            twig.start_node = y
                            s_node = None 
                        elif y.node_no == e_node:
                            y.incoming_twigs.append(twig)
                            twig.end_node = y
                            e_node = None

                    if s_node is not None:
                        new_node = Node(s_node, [], [twig], [], [])
                        self.nodes.append(new_node)
                        twig.start_node = new_node
                    if e_node is not None:
                        new_node = Node(e_node,[twig],[],[],[])
                        self.nodes.append(new_node)
                        twig.end_node = new_node

                elif l[0] == 'l':
                    link = Branch(c+1, None, None, float(l[5]), float(l[6]), float(l[7]), sym.sympify(l[3]), sym.sympify(l[4]))
                    self.links.append(link)
                    s_node = float(l[1])
                    e_node = float(l[2])
                    for z in self.nodes:
                        y=z
                        if y.node_no == s_node:
                            y.outgoing_links.append(link)
                            link.start_node = y
                            s_node = None 
                        elif y.node_no == e_node:
                            y.incoming_links.append(link)
                            link.end_node = y
                            e_node = None

                    if s_node is not None:
                        new_node = Node(s_node, [], [], [], [link])
                        self.nodes.append(new_node)
                        link.start_node = new_node
                    if e_node is not None:
                        new_node = Node(e_node, [], [], [link], [])
                        self.nodes.append(new_node)
                        link.end_node = new_node

                data = circuit.readline()
                c+=1

class Solver():

    '''
    class to keep the tactics and ways to solve the circuits
    its made as a class so as others can import this in other file and solve equations.
    '''

    def __init__(self, circuit):
        self.circuit = circuit

    def loop_finder(self, link, current_node = None, last_branch = None, loop = [], sign = []):
        if current_node is None:
            current_node = link.start_node
        for x in current_node.incoming_twigs:
            if x.start_node is link.end_node:
                loop.append(x)
                sign.append(1)
                return True
            if x is last_branch:
                continue
        for x in current_node.outgoing_twigs:
            if x.end_node is link.end_node:
                loop.append(x)
                sign.append(-1)
                return True
            if x is last_branch:
                continue

        #if len(current_node.incoming_twigs+current_node.outgoing_twigs) == 1:
        #    print(current_node.node_no)
        #    return False

        for x in current_node.outgoing_twigs:
            if x == last_branch:
                continue

            elif self.loop_finder(link, x.end_node, x, loop, sign):
                loop.append(x)
                sign.append(-1)
                return True
        for x in current_node.incoming_twigs:
            if x == last_branch:
                continue

            elif self.loop_finder(link, x.start_node, x, loop, sign):
                loop.append(x)
                sign.append(1)
                return True


    def loop_matrix_maker(self):
        a = []
        a_sign = []
        order = []
        counter = 0
        for y in self.circuit.twigs:
            order.append(y)
            counter+=1
        for y in self.circuit.links:
            l = []
            l_sign = []
            print(self.loop_finder(y, y.start_node, loop = l, sign = l_sign))
            l.append(y)
            l_sign.append(1)
            a.append(l)
            a_sign.append(l_sign)
            order.append(y)
        print(a,a_sign)
        mat = []
        for x in range(len(a)):
            l = []
            for y in order:
                for z in range(len(a[x])):
                    if a[x][z] is y:
                        l.append(a_sign[x][z])
                        break
                else:
                    l.append(0)
            mat.append(l)
        mat = sym.Matrix(mat)
        self.loop_matrix = mat
        self.counter = counter
        self.order = order
        print(f"loop_matrix = {self.loop_matrix}")

    def cutset_maker(self):
        a = self.loop_matrix[:,:self.counter]
        a = -a.transpose()
        m,n=a.shape
        b=sym.eye(m,dtype=int)
        c=b.row_join(a)
        self.cutset_matrix = sym.Matrix(c)
        print(f"cutset_matrix = {self.cutset_matrix}")

    def vg_ig_maker(self):
        vg=[]
        ig=[]
        for x in self.order:
            vg.append([x.Vg])
        for x in self.order:
            ig.append([x.Ig])
        self.Vg_mat = sym.Matrix(vg)
        self.Ig_mat = sym.Matrix(ig)
        print(f"Vg_mat = {self.Vg_mat}")
        print(f"Ig_mat = {self.Ig_mat}")

    def impedance_matrix(self):
        self.impedance_mat = sym.eye(len(self.order))
        self.conductance_mat = sym.eye(len(self.order))

        for x in range(len(self.order)):
            a = self.order[x].impedance()
            self.impedance_mat[x,x] = a
            self.conductance_mat[x,x] = 1/a

    def simplify_mat(self, mat):
        for x in range(len(mat)):
            mat[x] = sym.simplify(str(mat[x]))

    def solve(self):
        zf=self.loop_matrix*self.impedance_mat*transpose(self.loop_matrix)
        zf_inv = zf.inv()
        yf = self.cutset_matrix*self.conductance_mat*transpose(self.cutset_matrix)
        yf_inv = yf.inv()
        Igl = self.Ig_mat[self.counter:,:]
        Vgt = self.Vg_mat[0:self.counter,:]
        Es = self.loop_matrix*(self.Vg_mat+self.impedance_mat*transpose(self.loop_matrix)*Igl-self.impedance_mat*self.Ig_mat)
        Il = zf_inv*Es
        self.simplify_mat(Il)
        Js = self.cutset_matrix*(self.Ig_mat-self.conductance_mat*self.Vg_mat+self.conductance_mat*transpose(self.cutset_matrix)*Vgt)
        Vt = yf_inv*Js
        self.simplify_mat(Vt)
        Vs = transpose(self.cutset_matrix)*Vt-transpose(self.cutset_matrix)*Vgt+self.Vg_mat
        self.simplify_mat(Vs)
        Is = transpose(self.loop_matrix)*Il+self.Ig_mat-transpose(self.loop_matrix)*Igl
        self.simplify_mat(Is)
        with open("vs.txt", "w") as f:
            print(Vs.tolist(), file = f)
        with open("is.txt", "w") as f:
            print(Is.tolist(), file = f)
        t = sym.sympify("t")
        v = sym.inverse_laplace_transform(Vs, s, t)
        print(v)
        i = sym.inverse_laplace_transform(Is, s, t)
        print(i)


c=Circuit()
c.circuit_read("input.txt")
sol=Solver(c)
sol.loop_matrix_maker()
sol.cutset_maker()
sol.vg_ig_maker()
sol.impedance_matrix()
sol.solve()
