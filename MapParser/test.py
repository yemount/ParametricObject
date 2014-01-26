import xml.etree.ElementTree as ET
from shapely.geometry import *
import random
import math

nodes = {}
buildings = []
streets = []
inflation = 1000
minHeight = 10
minType0Height = 15
minType1Height = 15
maxHeight = 30
pyramidAreaThres = 0.1
streetDistThres = 0.01

class Building:
    def __init__(self, points):
        polygon = Polygon(points)
        self.center = polygon.centroid
        self.points = [[point[0] - self.center.x, point[1] - self.center.y] for point in points]
        self.area = polygon.area
        self.d = max([Point(p[0], p[1]).distance(self.center) for p in points])
        self.height = max(min(random.expovariate(2.0/(minHeight+maxHeight)), maxHeight), minHeight)#minHeight + random.random() * (maxHeight - minHeight)
        if self.area < pyramidAreaThres:
            # btype 0 => pyramid
            self.btype = 0
            self.height = max(self.height, 10)
        elif len(self.points) > 25:
            # btype 1 => cylinder roof
            self.btype = 1
            self.height = max(self.height, 10)
        elif self.d * self.d / self.area < 1:
           # btype 2 => platform roof
           if random.random() < 0.8:
                self.btype = 2
           else:
                self.btype = 4
        else:
            # btype 3 => pointy roof
            self.btype = 3

    def writeToFile(self, out):
        line = '['
        for point in self.points[:-1]:
            line += '[' + str(point[0])+ ', ' + str(point[1]) + '], '
        line += '[' + str(self.points[-1][0]) + ', ' + str(self.points[-1][1]) + ']];\n'
        out.write(line)

class Street:
    def __init__(self, points):
        cX = 0
        cY = 0
        for p in points:
            cX += p[0]
            cY += p[1]
        self.center = Point(cX/len(points), cY/len(points))
        self.points = [[point[0] - self.center.x, point[1] - self.center.y] for point in points]
        self.numInts = 0
        self.simplify()

    def writeToFile(self, out):
        line = '['
        for point in self.points[:-1]:
            line += '[' + str(point[0])+ ', ' + str(point[1]) + '], '
        line += '[' + str(self.points[-1][0]) + ', ' + str(self.points[-1][1]) + ']];\n'
        out.write(line)

    def dist(self, other):
        l1 = LineString([[p[0]+self.center.x, p[1]+self.center.y] for p in self.points])
        l2 = LineString([[p[0]+other.center.x, p[1]+other.center.y] for p in other.points])
        return l1.distance(l2)

    def simplify(self):
        p1 = [0, 0]
        p2 = [0, 0]
        for _p1 in self.points:
            for _p2 in self.points:
                if math.pow(_p1[0]-_p2[0], 2) + math.pow(_p1[1]-_p2[1], 2) > math.pow(p1[0]-p2[0], 2) + math.pow(p1[1]-p2[1], 2):
                    p1 = _p1
                    p2 = _p2
        self.points = [p1, p2] 

    def extrude(self):
        self.points = [self.points[0], self.points[1], [self.points[1][0]-0.1, self.points[1][1]-0.1], [self.points[0][0]-0.1, self.points[0][1]-0.1]]

def getCoord(nodeId, _root):
    n = _root.find("./node[@id='" + nodeId + "']")
    if n is not None:
        return [float(n.get("lat")) * inflation, float(n.get("lon")) * inflation]
    else:
        return [0, 0]

def getCenter(building):
    cX = 0
    cY = 0
    for node in building:
        cX += nodes[node][0]
        cY += nodes[node][1]
    cX /= len(building)
    cY /= len(building)
    return [cX, cY]

def getGlobalCenter(buildings):
    cX = 0
    cY = 0
    for building in buildings:
        cX += building.center.x
        cY += building.center.y
    pc = Point(cX/len(buildings), cY/len(buildings))
    pd = None
    dist = -1
    for building in buildings:
        if building.center.distance(pc) > dist:
            dist = building.center.distance(pc)
            pd = building.center
    return (pc, pd)

def writeToFile(out, inflation):
#    for k, v in nodes.iteritems():
#        out.write(k + ' = [' + str(v[0]*inflation) + ', ' + str(v[1]*inflation) + '];\n')

    # write buildings
    for i in range(len(buildings)):
        out.write('building' + str(i) + ' = ')
        buildings[i].writeToFile(out)
    line = 'buildings = ['
    for i in range(len(buildings)-1):
        line += 'building' + str(i) + ', '
    line += 'building' + str(len(buildings)-1) + '];\n'
    out.write(line)

    # write streets
    for i in range(len(streets)):
        out.write('street' + str(i) + ' = ')
        streets[i].writeToFile(out)
    line = 'streets = ['
    for i in range(len(streets)-1):
        line += 'street' + str(i) + ', '
    line += 'street' + str(len(streets)-1) + '];\n'
    out.write(line)

    # write street centers
    line = 'streetTrans = ['
    for i in range(len(streets)-1):
        line += '[' + str(streets[i].center.x) + ', ' + str(streets[i].center.y) + '], '
    line += '[' + str(streets[-1].center.x) + ', ' + str(streets[-1].center.y) + ']];\n'
    out.write(line)
    
    # write building centers
    line = 'buildingTrans = ['
    for i in range(len(buildings)-1):
        line += '[' + str(buildings[i].center.x) + ', ' + str(buildings[i].center.y) + '], '
    line += '[' + str(buildings[-1].center.x) + ', ' + str(buildings[-1].center.y) + ']];\n'
    out.write(line)

    # write types
    line = 'types = ['
    for i in range(len(buildings)-1):
        line += str(buildings[i].btype) + ', '
    line += str(buildings[-1].btype) + '];\n';
    out.write(line)

    # write diameters
    line = 'diameters = ['
    for i in range(len(buildings)-1):
        line += str(buildings[i].d) + ', '
    line += str(buildings[-1].d) + '];\n'
    out.write(line)

    # write heights
    line = 'heights = ['
    for i in range(len(buildings)-1):
        line += str(buildings[i].height) + ', '
    line += str(buildings[-1].height) + '];\n'
    out.write(line)

def getRefPoints(way):
    points = []
    for node in way.findall("./nd"):
        nodeId = node.get("ref")
        points.append(getCoord(nodeId, root))
    return points   
        
tree = ET.parse('cmumap.osm')
root = tree.getroot()
print 'parsing map...'

# parse buildings and streets
for way in root.iter('way'):
    if len(way.findall("./*[@k='highway'][@v='secondary']")) > 0 or len(way.findall("./*[@k='highway'][@v='residential']")) > 0 or len(way.findall("./*[@k='highway'][@v='tertiary']")) > 0 :
        points = getRefPoints(way)
        streets.append(Street(points))
    elif len(way.findall("./*[@k='building'][@v='yes']")) > 0:
        points = getRefPoints(way)
        buildings.append(Building(points))

# remove floating streets
for street in streets:
    intersecting = False
    for street1 in streets:
        if (street1 != street) and (street.dist(street1) < streetDistThres):
            street.numInts += 1

pc, pd = getGlobalCenter(buildings)

streets = [street for street in streets if street.numInts > 0]
streets = [street for street in streets if street.center.distance(pc) < pd.distance(pc) * 0.7]
for street in streets:
    street.extrude()

out = open('out', 'w')
print 'parsing DONE '
print 'exporting with inflation rate... ' + str(inflation)
writeToFile(out, inflation)
out.write('gcenter = [' + str(pc.x) + ', ' + str(pc.y) + '];')
out.close()
print 'DONE'
