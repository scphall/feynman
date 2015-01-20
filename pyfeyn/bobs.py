from pyfeyn.user import *
import pyx

processOptions()
fd = FeynDiagram()

proton_quark_sep = 0.3
proton_radius = 0.5

SCircle = CircleMark(0.05)

def draw_proton_and_legs(x, y, r):
    delta = r/2.
    pi1 = Point(x-2*r, y+delta)
    pi2 = Point(x-2*r, y)
    pi3 = Point(x-2*r, y-delta)
    po1 = Point(x, y+delta)
    po2 = Point(x, y)
    po3 = Point(x, y-delta)
    Fermion(pi1, po1)
    Fermion(pi2, po2)
    Fermion(pi3, po3)
    Circle(x, y, radius=r)
    return Point(x, y)

def branch(point, deltax, deltay, label1="", label2="", mark1=None, mark2=None):
    point1 = Vertex(point.getX() + deltax, point.getY() + deltay, mark=mark1)
    point2 = Vertex(point.getX() + deltax, point.getY() - deltay, mark=mark2)
    f1 = Fermion(point1, point).addLabel(label1, displace=0.15)
    f2 = Fermion(point, point2).addLabel(label2, displace=0.17)
    return f1, f2


class Penguin(object):
    def __init__(self, x, y, r, l1=1, l2=None):
        if l2 == None: l2 = l1
        self.p1 = DecoratedPoint(x-r-l1, y)
        self.p2 = DecoratedPoint(x+r+l2, y)
        self.v1 = DecoratedPoint(x-r, y)
        self.v2 = DecoratedPoint(x+r, y)
        self.l1 = Fermion(self.v1, self.v2).bend(r)
        self.l2 = Fermion(self.v2, self.v1).bend(r)
        self.f1 = Fermion(self.p1, self.v1)
        self.f2 = Fermion(self.v2, self.p2)
        return


def Robyn():
    r = 0.4
    xi = 0
    deltax = 1
    p1 = [xi, 2]
    p2 = [xi, 0]
    v1 = [xi + deltax, (p1[1] + p2[1])/2]
    v2 = [v1[0] + deltax, v1[1]]
    pp1 = draw_proton_and_legs(p1[0], p1[1], r)
    pp2 = draw_proton_and_legs(p2[0], p2[1], r)
    pv1 = Vertex(*v1, mark=SCircle)
    pv2 = Vertex(*v2, mark=SCircle)
    Fermion(pp1, pv1)
    Fermion(pp2, pv1)
    Fermion(pv1, pv2)
    ttbar_hi, ttbar_lo = branch(pv2, 1, 1,
                                label1=r'$\tilde t$',
                                label2=r'$\tilde{\bar t}$',
                                mark1=SCircle, mark2=SCircle)
    c1, chi1 = branch(ttbar_hi.p1, 1, 0.5)
    chi2, c2 = branch(ttbar_lo.p2, 1, 0.5)
    c1.p1.addLabel(r'\Pqc', displace=0.15)
    chi1.p2.addLabel(r'$\tilde\chi_0$', displace=0.15)
    c2.p2.addLabel(r'\Paqc', displace=0.15)
    chi2.p1.addLabel(r'$\tilde{\bar\chi}_{0}$', displace=0.15)
    chi1.addStyle(pyx.style.linestyle.dashed)
    chi2.addStyle(pyx.style.linestyle.dashed)
    glu = Gluon(midpoint(pp1, pv1), Point(pv2.getX(), p1[1]+0.2)).set3D()
    Vertex(glu.p1.getX(), glu.p1.getY(), mark=SCircle)
    Vertex(glu.p2.getX(), glu.p2.getY()).addLabel("$g$", displace=0.15)
    #l1 = Label("Robyn is a fool", x=1.5, y=3)
    fd.draw("bobbyn.pdf")

#
#penguin(0, v10, 1)
#fd.draw("test.pdf")

Robyn()
