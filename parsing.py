import lezc

Buildings = []
Recipies = []
meta_vars = ["Name","Tier", "Image", "Description", "Recipe", "Workers", "Electricity", "Maintenance", "MaintenanceII", "MaintenanceIII",  
                "ResearchSpeed", "Footprint", "Research", "Cargo", "Storage", "BoostByUnity", "Designation", "Variants"]


def add_meta(file, line):
    temp_count = 0
    temp_meta = {}
    words = line.split()
    flag = 0
    while temp_count < 50 and not (temp_count-1 > flag and words == []):
        if(words == []):
            continue
        
        elif(words[0] == "Recipe" or words[0] == "recipe"):
            
            temp_ios = [[]]
            temp_line = file.readline()
            if(temp_line.split()[0] == "Machine"):
                temp_line = file.readline()
            words = temp_line.split()
            
            while(words != [] and temp_count <25):
                
                if(words[0][:5] == "Input"):
                    temp_name = ''.join(words[2:])
                    temp_line = file.readline()
                    words = temp_line.split()
                    temp_qty = words[-1]

                    temp_io = lezc.io(temp_name, temp_qty)
                    temp_ios[0].append(temp_io)
                    
                    temp_count += 1
                    temp_line = file.readline()
                    words = temp_line.split()
            temp_meta["Recipe"] = lezc.recipe(temp_ios)
            flag = temp_count
            
        elif(words[0] in meta_vars):
            temp_meta[words[0]] = ''.join(words[2:])
            
        temp_count += 1

        temp_line = file.readline()
        words = temp_line.split()
    
    temp_meta_obj = lezc.meta(temp_meta)

    Buildings.append(lezc.building(temp_meta["Name"],temp_meta_obj))

    return temp_count

def add_recipies(file):
    rcps = []
    temp_line = file.readline()
    temp_count = 0
    words = temp_line.split()
    

    while(temp_count <300):
        if(words != []):
            if(words[0] == "Navbox/Machines"):
                break
            if((words[0] == "recipe" or words[0] == "Recipe") and words[1] == "define"):
                temp_ios = [[],[]]
                temp_count2 = 0
                while(temp_count2<22):
                    temp_line = file.readline()
                    words = temp_line.split()
                    if(words == []):
                        break

                    if(words[0][:5] == "Input"):
                        temp_name = ''.join(words[2:])

                        temp_line = file.readline()
                        words = temp_line.split()

                        if (words[-1] == '?'):
                            words[-1] = -1
                        temp_quantity = words[-1]
                        temp_ios[0].append(lezc.io(temp_name, temp_quantity))

                        temp_count2 += 1

                    elif(words[0][:6] == "Output"):
                        if(words[0][7:] == "Unit"):
                            continue
                        temp_name = ''.join(words[2:])

                        temp_line = file.readline()
                        words = temp_line.split()

                        if (words[-1] == '?'):
                            words[-1] = -1
                        temp_quantity = words[-1]

                        temp_ios[1].append(lezc.io(temp_name, temp_quantity))

                        temp_count2 += 1

                    elif(words[0] == "Time"):
                        temp_ios.append(words[-1])

                    temp_count2 += 1
            
                rcps.append(lezc.recipe(temp_ios))
                Recipies.append(rcps[-1])

                temp_count += temp_count2

            temp_line = file.readline()
            words = temp_line.split()
            temp_count += 1

        else:
            temp_line = file.readline()
            words = temp_line.split()
            temp_count += 1

    return rcps


def parser(df):
    file = open(df,"r")
    print("File opened")
    count = 0
    while count <50:
        line = file.readline()
        if(line[:4] == "Name"):
            count = add_meta(file, line)
            print("Machine Data Added")
        
        elif(line == "== Recipes ==\n" or line == "==Recipes==\n" or line == "== Recipes==\n" or line == "==Recipes ==\n"):
            print("Adding Recipes")
            rcps = add_recipies(file)
            print("Recipes Added")
            Buildings[0].add_recipies(rcps)
            file.close()
            break
        count += 1

    return (Buildings.pop())