import numpy

coords = []
flag = True
with  open("eil51.tsp") as file:
    for row in file:
        if row.startswith("EOF"):
            break

        print(row.strip())

        if row.startswith("NODE_COORD_SECTION"):
            flag = False
            continue
        
        if flag == True:
            if row.startswith("DIMENSION"):
                pieces = row.split(":")
                dimension = int(pieces[1].strip())

            if row.startswith("EDGE_WEIGHT_TYPE"):
                pieces = row.split(":")
                edge_weight_type = pieces[1].strip()
        else:
            pieces = row.split()
            coords.append((int(pieces[1]), int(pieces[2])))
            
        
def distance_calc(coords):
    distance = numpy.zeros((len(coords),len(coords)))

    for i in range(len(coords)):

        for j in range(i+1, len(coords)):
            x1, y1 = coords[i]
            x2, y2 = coords[j]
            euclid_calc = numpy.sqrt((x2 - x1)**2 + (y2-y1)**2)
            distance[i][j] = euclid_calc
            distance[j][i] = euclid_calc

    return distance

print(distance_calc(coords)[0][1])