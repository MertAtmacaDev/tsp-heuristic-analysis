import numpy

def parse_tsp(filename):
    coords = []
    reading_header = True
    with open(filename) as file:
        for row in file:
            if row.startswith("EOF"):
                break

            if row.startswith("NODE_COORD_SECTION"):
                reading_header = False
                continue
            
            if reading_header == True:
                if row.startswith("DIMENSION"):
                    pieces = row.split(":")
                    dimension = int(pieces[1].strip())

                if row.startswith("EDGE_WEIGHT_TYPE"):
                    pieces = row.split(":")
                    edge_weight_type = pieces[1].strip()
            else:
                pieces = row.split()
                coords.append((int(pieces[1]), int(pieces[2])))
    return coords
            
        
def distance_calc(coords):
    distance = numpy.zeros((len(coords),len(coords)))

    for i in range(len(coords)):
        # exploiting symmetry to cut distance matrix calculations in half
        for j in range(i+1, len(coords)):
            x1, y1 = coords[i]
            x2, y2 = coords[j]
            euclid_calc = numpy.sqrt((x2 - x1)**2 + (y2-y1)**2)
            distance[i][j] = euclid_calc
            distance[j][i] = euclid_calc

    return distance



if __name__ == "__main__":
    coords = parse_tsp("eil51.tsp")
    print(distance_calc(coords)[0][1])