
import csv
import pathlib
import os

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

    
def rotation_1( liste):
    # rotation of -pi/2 rad : x becomes -y ,y becomes x , z stay z 
    new_list= list()
    for i in range(len(liste)):
        new_list_row= list()
        if len(liste[i]) != 0:
            if  liste[i][0] == '-':
                for n in range(3):
                    new_list_row.append('-')
            elif len( liste[i] ) == 0:
                new_list_row = []

            else: 
                new_list_row.append( (-1)*liste[i][1] )
                new_list_row.append( liste[i][0])
                new_list_row.append(liste[i][2])
        new_list.append(new_list_row)
    return new_list

def rotation_2( liste):
    #rotation of pi rad : x becomes -x , y becomes, -y , z stay z 
    r =  rotation_1( liste)
    return rotation_1( r)

def rotation_3( liste):
    #rotation of 3pi/2 rad 
    r =  rotation_2(liste)
    return rotation_1( r)


def rotation_4( liste):
    #z becomes -z, x stays x , y becomes -y
    new_list= list()
    for i in range(len(liste)):
        new_list_row= list()
        if len(liste[i]) != 0:
            if  liste[i][0] == '-':
                for n in range(3):
                    new_list_row.append('-')
            elif len( liste[i] ) == 0:
                new_list_row = []

            else: 
                new_list_row.append( liste[i][0] )
                new_list_row.append( (-1)*liste[i][1] )
                new_list_row.append( (-1)*liste[i][2] )
        new_list.append(new_list_row)
    return new_list

def rotation_5( liste):
    # rotation of pi/2 rad while the module in upside down 
    r = rotation_4( liste)
    return rotation_1( r)

def rotation_6( liste):
    r = rotation_5( liste)
    return rotation_1( r)

def rotation_7( liste):
    r = rotation_6( liste)
    return rotation_1(r) 

def create_file_for_rotation(path, liste, file_name ):
    #creation of a file with the new data corresponding with the 7 rotations
    pathlib.Path(path ).mkdir(parents=True, exist_ok=True) 
    with open(str(path)+"/"+str(file_name) , 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerows(rotation_1(rotation_3(liste)))
        writer.writerows(rotation_1(liste))
        writer.writerows(rotation_2(liste))
        writer.writerows(rotation_3(liste))
        writer.writerows(rotation_4(liste))
        writer.writerows(rotation_5(liste))
        writer.writerows(rotation_6(liste))
        writer.writerows(rotation_7(liste))


#pathlib.Path("output/custom_train").mkdir(parents=True, exist_ok=True)
#create_file_for_rotation("output/custom_train/wallet/custom_output_wallet_test1.txt", data_in_list("train/wallet", "output_wallet_test1.txt"))
