from dataset_generator import dataGeneration
import pandas as pd
import json , math
import itertools
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

gerirachi=[ 'age', 'zip code', 'education', 'role']

def numerical_generalization(ds ,attr,lv):
    if attr=="zip code":
        for data in ds:
            data[attr]=str(data[attr])
            data[attr] = data[attr][:-(ZIPCODE_GENERALIZATION-lv+1)] + "*"*(ZIPCODE_GENERALIZATION-lv+1)
    elif attr=="age":
        n= ((AGE_GENERALIZATION/3)*(4-lv))
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
            if lv != 4 and attr == "gender":
                data[attr]=gen[-1][data[attr]]
            continue


def ei_generalization(ds ,attr):
    for data in ds:
        data[attr]="****"
    return 0

def apply_generalization(ds ,lvs):
    for attr in ds[0].keys():
        if attr not in names:
            raise Exception("attr not in names list")
        if attr in numerical:
            numerical_generalization(ds ,attr,lvs[attr])
        elif attr in categorical:
            categorical_generalization(ds ,attr,lvs[attr])
        elif attr in ei:
            ei_generalization(ds ,attr)
        elif attr in sens:
            continue
        else:
            raise Exception("attr not in any list")
        
    return 0

# function to check if the dataset is k-anonymous
def check_k_anonymity(ds, quasi_identifiers, k):
    df = pd.DataFrame(ds)
    # group the dataset by quasi identifiers and return the size
    group_sizes = df.groupby(quasi_identifiers).size()
    anon = group_sizes >= k
    return all(anon)

def check_l_diversity(ds, quasi_identifiers, sensitive_attr,l):
    df = pd.DataFrame(ds)
    groups = df.groupby(quasi_identifiers)
    # check the diversity
    for name, group in groups:
        if group[sensitive_attr].nunique() < l:
            return False
    return True

# data generation
initial_ds = dataGeneration()

lvs={"age":1, "role":1, "education":1, "zip code":1, "gender":1} 
iterKeys = itertools.cycle(lvs.keys())
valid_ds = initial_ds.copy()
valid_lv = lvs
while True:
    ds = dataGeneration()
    apply_generalization(ds,lvs)
    
    satisfies_k_anonymity = check_k_anonymity(ds, ['gender', 'age', 'zip code', 'role', 'education'], K)
    satisfies_l_diversity = check_l_diversity(ds, ['gender', 'age', 'zip code', 'role', 'education'], 'salary', L)
    
    if satisfies_k_anonymity and satisfies_l_diversity:

        valid_ds = ds
        valid_lvs = lvs.copy()

        attr = next(iterKeys)
        lvs[attr] += 1
    else:
        print(f"Dataset with lvs={valid_lvs} doesn't satisfies k-anonymity and l-diversity")
        break

print("Initial dataset:")
print(pd.DataFrame(initial_ds))

print(f"Generalized dataset at this level {valid_lvs}:")
print(pd.DataFrame(valid_ds))



# # Print the dataset and the results
# print(pd.DataFrame(ds))
# print(f"Does the dataset satisfy the k-anonymity for k={K}? {satisfies_k_anonymity}")
# print(f"Does the dataset satisfy the l-diversity for l={L}? {satisfies_l_diversity}")
