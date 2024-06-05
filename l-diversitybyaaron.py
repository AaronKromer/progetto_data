from dataset_generator import dataGeneration
import pandas as pd
import json , math
K=3
L=3
LV=1
AGE_GENERALIZATION=15
ZIPCODE_GENERALIZATION=3

names = ['first name', 'last name', 'gender', 'age', 'zip code', 'role', 'education', 'salary']
numerical =  ['age', 'zip code' ]
categorical =  ['gender', 'role', 'education']
ei =  ['first name', 'last name']
sens =  ['salary']

def numerical_generalization(ds ,attr,lv):
    if attr=="zip code":
        for data in ds:
            data[attr]=str(data[attr])
            data[attr] = data[attr][:-(ZIPCODE_GENERALIZATION-lv+1)] + "*"*(ZIPCODE_GENERALIZATION-lv+1)
    elif attr=="age":
        n=AGE_GENERALIZATION/lv
        for data in ds:
            upperage=int(math.ceil((data[attr]+0.1) / n) * n) #per eliminare i numeri tipo 35 che venivano 35-35
            lowerage=int(math.floor((data[attr]) / n) * n)
            data[attr] =f"{upperage}-{lowerage}"

def categorical_generalization(ds ,attr,lv):
    with open(f"{attr}.json", 'r') as file:
        gen = json.load(file)
    for data in ds:
        try:
            data[attr]=gen[-lv][data[attr]]
        except:
            print(f"era di questo attr:{attr}")



def ei_generalization(ds ,attr,lv):
    for data in ds:
        data[attr]="****"
    return 0

def apply_generalization(ds ,lv):
    for attr in ds[0].keys():
        if attr not in names:
            raise Exception("attr not in names list")
        if attr in numerical:
            numerical_generalization(ds ,attr,lv)
        elif attr in categorical:
            categorical_generalization(ds ,attr,lv)
        elif attr in ei:
            ei_generalization(ds ,attr,lv)
        elif attr in sens:
            continue
        else:
            raise Exception("attr not in any list")
        
    return 0



ds = dataGeneration()
done=True
print(pd.DataFrame(ds))
lv=4
while(done):
    apply_generalization(ds ,lv)
    done=False
print(pd.DataFrame(ds))
