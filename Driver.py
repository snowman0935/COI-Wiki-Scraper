from audioop import mul
from os.path import exists
import parsing
import wget
import xml.etree.ElementTree as ET
import os
import json
import multiprocessing


def get_machine_names():
    url = "https://wiki.captain-of-industry.com/index.php?title=Special:CargoExport&tables=recipes%2C&&fields=recipes._pageName%2C&&group+by=recipes._pageName&order+by=%60cargo__recipes%60.%60_pageName%60&limit=500&format=csv"
    print('Getting Machine Names')

    if exists("machines.csv"):
        os.remove("machines.csv")
    file = wget.download(url, "machines.csv")

    file = open("machines.csv","r")
    df = file.read()
    df = df.replace(' ','_')
    df = df.replace('"','')
    df = df[10:]
    df = df.replace('Designations\n','')
    file.close()

    file = open("machines.csv","w")
    file.write(df)
    file.close()

    return "machines.csv"

#get_machine_names()

def get_machine_data(name):
    xml_url = "https://wiki.captain-of-industry.com/Special:Export/"+name
    xml_file = wget.download(xml_url, name + ".xml")
    tree = ET.parse(xml_file)
    
    root = tree.getroot()
    
    data = root.find('.//{*}text').text
    data = data.replace('| ','')
    data = data.replace('{','')
    data = data.replace('}','')
    data = data.replace('<!-- not a typo -->','')
    data = data.replace('#expr: ','')
    data = data.replace('+','')
    data = data.replace('instant','-1')
    data = data.replace('Instant','-1')

    os.remove(name + ".xml")

    file = open("./Machines/"+name + ".txt","w")
    file.write(data)
    file.close()

    return 0

def save_json(obj,name):
    file = open("./Machines/"+name+".json", "w")
    file.write(obj)
    file.close()
    return 0

#get_machine_data("Air_Separator")

#info = parsing.parser("./Machines/Assembly_(Robotic).txt")


#save_json(info[0][0].toJSON(),"Assembly_(Robotic)")

""" def get_all_machine_data():
    file = open("machines.csv","r")
    line = file.readline()
    count = 0
    info = []
    while True:
        line = file.readline()[:-1]
        if (line == ""):
            break
        print("Getting:"+line)
        get_machine_data(line)
        print("Parsing:",line)
        info = parsing.parser("./Machines/"+line+".txt")
        #print("Saving JSON:",line)
        #save_json(info[0][count].toJSON(),line)
        #count+=1
        #os.remove("./Machines/"+line+".txt")
    
    for obj in parsing.Buildings:
        save_json(obj.toJSON(),obj.name) """


def get_and_save(name):
    print("Getting:"+name)
    get_machine_data(name)

    print("Parsing:",name)
    info = parsing.parser("./Machines/"+name+".txt")

    print("Saving JSON:",name)
    save_json(info.toJSON(),name)

    os.remove("./Machines/"+name+".txt")

    return info


def get_all_machine_data():
    pool = multiprocessing.Pool(processes=6)
    names = []
    machines = get_machine_names() 
    with open(machines,"r") as file:
        for line in file:
            names.append(line[:-1])   
    #print(names)
    print("Starting Extraction")    
    infos = pool.map(get_and_save,names)

   
        
#get_and_save("Anaerobic_Digester")
#get_and_save("Power_Generator")

get_all_machine_data()