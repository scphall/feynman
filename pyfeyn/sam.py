from pyfeyn.user import *
from math import cos
from math import sin
from math import atan
import pyx

processOptions()

proton_quark_sep = 0.3
proton_radius = 0.5

SCircle = CircleMark(0.05)


class Penguin(object):
    def __init__(self, x, y, r, l1=1, l2=None,
                 Propagator1=Fermion,
                 Propagator2=Fermion):
        if l2 == None: l2 = l1
        self._x = x
        self._y = y
        self._r = r
        self.p1 = DecoratedPoint(x-r-l1, y)
        self.p2 = DecoratedPoint(x+r+l2, y)
        self.v1 = Vertex(x-r, y, mark=SCircle)
        self.v2 = Vertex(x+r, y, mark=SCircle)
        self.l1 = Propagator1(self.v1, self.v2).bend(r)
        self.l2 = Propagator2(self.v2, self.v1).bend(r)
        self.f1 = Fermion(self.p1, self.v1)
        self.f2 = Fermion(self.v2, self.p2)
        self.p3 = None
        self.p4 = None
        self.l3 = None
        return
    def addRadiation(self, x, y, theta=None, Propagator=Fermion):
        if theta is None: theta = atan((y-self._y)/(x-self._x))
        self.p3 = Vertex(self._x + self._r*cos(theta),
                         self._y + self._r*sin(theta), mark=SCircle)
        self.p4 = Vertex(x, y)
        self.l3 = Propagator(self.p3, self.p4)
        return self


class Pair(object):
    def __init__(self, x, y, deltax=1, deltay=1):
        self._x = x
        self._y = y
        self.p1 = Vertex(x, y, mark=SCircle)
        self.p2 = Vertex(x+deltax, y+deltay)
        self.p3 = Vertex(x+deltax, y-deltay)
        self.l1 = Fermion(self.p2, self.p1)
        self.l1 = Fermion(self.p1, self.p3)
        return


class Tree(object):
    def __init__(self, x1, y1, x2, y2, d=None, Propagator=Vector):
        self.i1 = Vertex(x1, y1)
        self.i2 = Vertex(x1, y2)
        self.o1 = Vertex(x2, y1)
        self.o2 = Vertex(x2, y2)
        if d is None:
            d = (x2 - x1) / 3.
        self.v1 = Vertex(x1 + d, (y1 + y2)/2., mark=SCircle)
        self.v2 = Vertex(x2 - d, (y1 + y2)/2., mark=SCircle)
        self.l1 = Fermion(self.i1, self.v1)
        self.l2 = Fermion(self.v1, self.i2)
        self.l3 = Fermion(self.o1, self.v2)
        self.l4 = Fermion(self.v2, self.o2)
        self.l5 = Propagator(self.v1, self.v2)


class Box(object):
    def __init__(self, x1, y1, x2, y2, PropagatorLR=Fermion, PropagatorUD=Fermion):
        self.v1 = Vertex(x1, y1, mark=SCircle)
        self.v2 = Vertex(x1, y2, mark=SCircle)
        self.v3 = Vertex(x2, y1, mark=SCircle)
        self.v4 = Vertex(x2, y2, mark=SCircle)
        self.l1 = PropagatorLR(self.v1, self.v2)
        self.l2 = PropagatorLR(self.v3, self.v4)
        self.l3 = PropagatorUD(self.v1, self.v3)
        self.l4 = PropagatorUD(self.v2, self.v4)


def penguinSchematic(x, y, ygap=0):
    point1 = Vertex(x, y+ygap)
    point2 = Vertex(x, y+2-1*ygap)
    point3 = Vertex(point1, [1, 0], mark=SCircle)
    point4 = Vertex(point2, [1, 0], mark=SCircle)
    point5 = Vertex(point1, [2.5, 0], mark=SCircle)
    point6 = Vertex(point2, [2.5, 0], mark=SCircle)
    point7 = Vertex(point1, [3.5, 0])
    point8 = Vertex(point2, [3.5, 0])
    line1 = Fermion(point1, point3)
    line2 = Fermion(point3, point5)
    line3 = Fermion(point5, point7)
    line4 = Fermion(point2, point4)
    line5 = Fermion(point4, point6)
    line6 = Fermion(point6, point8)
    bline1 = Vector(point3, point4)
    bline2 = Vector(point5, point6)

def boxSchematic(x, y, ygap=0):
    point1 = Vertex(x, y+ygap)
    point2 = Vertex(x, y+2-1*ygap)
    point3 = Vertex(point1, [1, 0], mark=SCircle)
    point5 = Vertex(point1, [2.5, 0], mark=SCircle)
    point7 = Vertex(point1, [3.5, 0])
    point8 = Vertex(point2, [3.5, 0])
    point9 = Vertex(point2, [1.75, 0], mark=SCircle)
    point10 = Vertex(point9, [0, -0.75-ygap/2], mark=SCircle)
    line1 = Fermion(point1, point3)
    line2 = Vector(point3, point5)
    line3 = Fermion(point5, point7)
    line4 = Fermion(point2, point9)
    line5 = Fermion(point9, point8)
    line6 = Fermion(point5, point3)
    line6.bend(line6.length() / 2)
    Fermion(point9, point10)


def schematics():
    fd = FeynDiagram()
    iwidth = 3.5
    idelta = 0.2
    ygap = 0.2
    tree = Tree(0, 0, iwidth, 2, d=1, Propagator=Vector)
    penguinSchematic(tree.o1.getX() + idelta, tree.o1.getY(), ygap)
    boxSchematic(tree.o1.getX() + idelta*2 + 3.5, tree.o1.getY(), ygap)
    fd.draw("schematics.pdf")
    return


def b2dsphi():
    fd = FeynDiagram()
    iwidth = 3.5
    tree = Tree(0, 0, iwidth, 2, d=1, Propagator=Vector)
    tree.i1.addLabel("b", displace=0.2, angle=180)
    tree.i2.addLabel("u", displace=0.2, angle=180)
    tree.v1.addLabel("$V_{ub}$", displace=0.5, angle=50)
    tree.v2.addLabel("$V_{cs}$", displace=0.5, angle=130)
    tree.l1.anti().addArrow()
    tree.l2.anti().addArrow()
    r = distance(tree.v2, tree.o1)
    deltax = distance(tree.o1, tree.v2, 'x')
    deltay = distance(tree.o1, tree.v2, 'y')
    o1 = Vertex(tree.o1.getX() + deltax, tree.o1.getY() - deltay)
    o2 = Vertex(tree.o1.getX() + deltax, tree.o2.getY() + deltay)
    o3 = Vertex(o1, [0, distance(o1, o2, 'y')/4.])
    o4 = Vertex(o3, [0, distance(o1, o2, 'y')/2.])
    v3 = Vertex(tree.v2.getX() + distance(tree.v2, o1, 'x')/2,
                tree.v2.getY(), mark=SCircle)
    oline1 = Fermion(tree.v2, o1).anti().addArrow()
    oline2 = Fermion(tree.v2, o2).addArrow()
    oline3 = Fermion(v3, o3).addArrow()
    oline4 = Fermion(v3, o4).anti().addArrow()
    o1.addLabel("s", displace=0.2)
    o2.addLabel("c", displace=0.2)
    o3.addLabel("s", displace=0.2)
    o4.addLabel("s", displace=0.2)
    fd.draw("b2dsphi.pdf")
    return


def b2kpipimumu():
    fd = FeynDiagram()
    i1 = Vertex(0, 0, mark=SCircle)
    i2 = Vertex(0, 3.5, mark=SCircle)
    o1 = Vertex(5.5, 0, mark=SCircle)
    o2 = Vertex(5.5, 0.5, mark=SCircle)
    o3 = Vertex(5.5, 1.5, mark=SCircle)
    o4 = Vertex(5.5, 2.0, mark=SCircle)
    o5 = Vertex(5.5, 3.0, mark=SCircle)
    o6 = Vertex(5.5, 3.5, mark=SCircle)
    o7 = Vertex(5.5, 4.5, mark=SCircle)
    o8 = Vertex(5.5, 5.5, mark=SCircle)
    g1 = Vertex(3.5, (o2.getY()+o3.getY())/2., mark=SCircle)
    g2 = Vertex(3.5, (o4.getY()+o5.getY())/2., mark=SCircle)
    g3 = Vertex(4.5, (o7.getY()+o8.getY())/2., mark=SCircle)
    peng = Penguin(2.75, 3.5, 0.5, l1=2.25, Propagator1=Vector)
    peng.addRadiation(g3.getX(), g3.getY(), Propagator=Vector)

    fd.draw("b2kpipimumu.pdf")
    return



b2kpipimumu()
#schematics()
#b2dsphi()

#p = Penguin(0, 0, 1, typeUpper=Vector)
#p.addRadiation(3, 3)
#Tree(0, 0, 5, 5)






