from pyfeyn.user import *

processOptions()
fd = FeynDiagram()

boxgap = 0.8
Edge = 0.1
Textheight = 0.5

def makebox(x, y, texts, width=5., edge=Edge, textheight=Textheight):
    #edge = 0.1
    #textheight = 0.5
    height = len(texts)*textheight + 2*edge
    top = len(texts)*textheight*0.5 - textheight*0.5
    rect = Rectangle(x, y, width, height, rounding=0.3)
    for i, text in enumerate(texts):
        rect.addLabel(text, displace=top-i*textheight, angle=90)
    return rect

def getPoints(rect):
    return Point(rect.x(), rect.y()+rect.height/2.), Point(rect.x(), rect.y()-rect.height/2.)


newy = 0
coll = makebox(0, 0, ['Collisons at $40\,\mathrm{MHz}$'])


l0y = -2.5
l0 = makebox(0, -2.5, ['L0 triggers on $p_{T}$ and $E_{T}$', 'Output: $1\,\mathrm{MHz}$', '', '', ''])
muon = makebox(0, l0y-0.6, ['$\mu(\mu)$', '$400\,\mathrm{kHz}$'], width=1.5)
hadron = makebox(-1.6, l0y-0.6, ['$h$', '$490\,\mathrm{kHz}$'], width=1.5)
photon = makebox(1.6, l0y-0.6, ['$\gamma/e$', '$150\,\mathrm{kHz}$'], width=1.5)


collp0, collp1 = getPoints(coll)
l0p0, l0p1 = getPoints(l0)
deferred = makebox(1.25, -5.0, ['Defer 20\%'], width=2.5)
dp0, dp1 = getPoints(deferred)

deffered_height = abs(dp0.y() - dp1.y())

mid_of_hlt1 = l0p1.getY() - deffered_height - 2*boxgap - 0.6
hlt1 = makebox(0, mid_of_hlt1, ['HLT1', 'Output: $80\,\mathrm{kHz}$'])
hlt1p0, hlt1p1 = getPoints(hlt1)

mid_of_hlt2 = mid_of_hlt1 - 0.6 - boxgap - 0.6
hlt2 = makebox(0, mid_of_hlt2, ['HLT2', 'Output:  $5\,\mathrm{kHz}$'])
hlt2p0, hltp1 = getPoints(hlt2)


l0pl = Point(l0p1.getX()-1.25, l0p1.getY())
l0pr = Point(l0p1.getX()+1.25, l0p1.getY())
hlt1pl = Point(hlt1p0.getX()-1.25, hlt1p0.getY())
hlt1pr = Point(hlt1p0.getX()+1.25, hlt1p0.getY())
f1 = Fermion(collp1, l0p0).addArrow()
f2 = Fermion(l0pr, dp0).addArrow()
f3 = Fermion(l0pl, hlt1pl).addArrow()
f4 = Fermion(dp1, hlt1pr).addArrow()
f5 = Fermion(hlt1p1, hlt2p0).addArrow()




#coll.addLabel('Collisions at\n40 MHz', displace=0.0)
#Label('thit', x=2, y=0)
#
#l0 = Rectangle(0, -2, 3, 1, rounding=0.3)
#l0.addLabel('L0 Output 1 MHz', displace=0.0)

#in1 = Point(-4,  2)
#in2 = Point(-4, -2)
#out1 = Point(4, -2)
#out2 = Point(4,  2)
#in_vtx = Vertex(-2, 0, mark=CIRCLE)
#out_vtx = Vertex(2, 0, mark=CIRCLE)
#
#l1 = Label("Drell-Yan QCD vertex correction", x=0, y=2)
#
#fa1 = Fermion(in1, in_vtx).addArrow().addLabel(r"\Pelectron")
#fa2 = Fermion(in_vtx, in2).addArrow().addLabel(r"\Ppositron")
#fa2.addParallelArrow(size=0.1, displace=-0.06, sense=-1)
#bos = Photon(in_vtx, out_vtx).addLabel(r"\Pphoton/\PZ")
#fb1 = Fermion(out1, out_vtx).addArrow(0.2).addLabel(r"\APquark")
#fb1.addParallelArrow(size=0.1, displace=-0.06, sense=-1)
#fb2 = Fermion(out_vtx, out2).addArrow(0.8).addLabel(r"\Pquark")
#glu = Gluon(midpoint(out_vtx, out1), midpoint(out_vtx, out2)).set3D()
#glu.invert().bend(0.5).addLabel("\Pgluon", displace=0.35)
#glu.addParallelArrow(size=0.1, displace=0.2, sense=-1)

fd.draw("trigger.pdf")
