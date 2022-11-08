import json
from functools import reduce

class io:
    def __init__(self, name, qty):
        self.name = name
        if (type(qty) == float) or (type(qty) == int):
            self.qty = float(qty)
        
        else:
            if len(qty.split('*')) == 1:
                self.qty = float(qty)
            else:
                self.qty = reduce((lambda x,y: x*y),map(float,qty.split('*')))

class recipe:
    def __init__(self,ios):
        self.inputs = ios[0]
        self.outputs = [] if len(ios)<2 else ios[1]
        self.time = 0 if len(ios)<3 else int(ios[2])

class meta:
    def __init__(self, meta_dic):
        self.Tier = 0 if "Tier" not in meta_dic else meta_dic["Tier"]
        self.Image = 0 if "Image" not in meta_dic else meta_dic["Image"]
        self.Description = 0 if "Description" not in meta_dic else meta_dic["Description"]
        self.Recipe = [] if "Recipe" not in meta_dic else meta_dic["Recipe"]
        self.Workers = 0 if "Workers" not in meta_dic else (0 if meta_dic["Workers"] in ["None","none"] else int(meta_dic["Workers"]))
        self.Electricity = 0 if "Electricity" not in meta_dic else meta_dic["Electricity"]
        self.Maintenance = 0 if "Maintenance" not in meta_dic else (0 if meta_dic["Maintenance"] == "None" else int(float((meta_dic["Maintenance"]))))
        self.ResearchSpeed = 0 if "ResearchSpeed" not in meta_dic else meta_dic["ResearchSpeed"]
        self.Footprint = 0 if "Footprint" not in meta_dic else meta_dic["Footprint"]
        self.Research = 0 if "Research" not in meta_dic else meta_dic["Research"]
        self.Cargo = 0 if "Cargo" not in meta_dic else meta_dic["Cargo"]
        self.Storage = 0 if "Storage" not in meta_dic else meta_dic["Storage"]
        self.BoostByUnity = 0 if "BoostByUnity" not in meta_dic else meta_dic["BoostByUnity"]
        self.Designation = 0 if "Designation" not in meta_dic else meta_dic["Designation"]
        self.Variants = 0 if "Variants" not in meta_dic else meta_dic["Variants"]
        self.MaintenanceII = 0 if "MaintenanceII" not in meta_dic else meta_dic["MaintenanceII"] 
        self.MaintenanceIII = 0 if "MaintenanceIII" not in meta_dic else meta_dic["MaintenanceIII"] 

class building:
    def __init__(self, name, meta):
        self.name = name
        self.meta = meta
    
    def add_recipies(self, recipies):
        self.recipies = recipies

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)