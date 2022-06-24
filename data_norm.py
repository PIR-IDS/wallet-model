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
                new_liste_row.append(['-'])
            else:
                norm = (row[0])**2 + (row[1])**2 + (row[2])**2
                new_liste_row.append([norm])
        else:
            new_liste_row = []
        new_liste.append(new_liste_row)
    #
    pathlib.Path(path).mkdir(parents=True, exist_ok=True) 
    with open(str(path)+"/"+str(file_name) , 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in new_liste:
            writer.writerows(row)
    print(new_liste)
    print( "ok")

data_norm("output/custom_train/wallet" ,data_in_list("./train/wallet", "output_wallet_test1.txt"), "custom_output_wallet_norm_test1.txt")
