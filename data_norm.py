import csv
import pathlib
import os
import math


def data_in_list(folder, file_to_read):
    f= open(folder + "/" + file_to_read, "r")
    lines = csv.reader(f)
    list_coord = list()
    for row in lines:
        list_row = list()
        for coord in row:
            if coord == '-':
                list_row.append('-')
            else:
                list_row.append(int(coord))
        list_coord.append(list_row)
    return list_coord
    


def data_norm(path, liste, file_name ):
    new_liste = list()
    for row in liste:
        new_liste_row = list()
        if len(row)!= 0:
            if row[0] == '-' :
                new_liste_row.append([])
                new_liste_row.append([])
                new_liste_row.append(['-','-'])
            else:
                norm = (row[0])**2 + (row[1])**2 + (row[2])**2
                norm2 = (row[3])**2 + (row[4])**2 + (row[5])**2
                new_liste_row.append( [norm, norm2] )
        else:
            new_liste_row = []
        new_liste.append(new_liste_row)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True) 
    with open(str(path)+"/"+str(file_name) , 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in new_liste:
            writer.writerows(row)

