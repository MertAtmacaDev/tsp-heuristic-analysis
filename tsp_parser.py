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
            
        
        