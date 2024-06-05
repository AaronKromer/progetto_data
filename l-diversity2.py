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
            a=0
            #print(f"era di questo attr:{attr}")



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
ds = dataGeneration()
# debug print
print("dataframe prima della anonimizzazione")
print(pd.DataFrame(ds))

# initial generalization
lv = 1
satisfies_k_anonymity = False
satisfies_l_diversity = False

# apply generalization
while not (satisfies_k_anonymity and satisfies_l_diversity):
    ds = dataGeneration()  # retry generation
    apply_generalization(ds, lv)
    
    # check k-anonimity and l-diversity
    satisfies_k_anonymity = check_k_anonymity(ds, ['gender', 'age', 'zip code', 'role', 'education'], K)
    satisfies_l_diversity = check_l_diversity(ds, ['gender', 'age', 'zip code', 'role', 'education'], 'salary', L)
    
    # increase generalization level
    if not (satisfies_k_anonymity and satisfies_l_diversity):
        lv += 1
        if lv > max(ZIPCODE_GENERALIZATION, AGE_GENERALIZATION):
            raise Exception("Impossible to satisfy k-anonymity and l-diversity with the given generalization levels")

# Print the dataset and the results
print(pd.DataFrame(ds))
print(f"Does the dataset satisfy the k-anonymity for k={K}? {satisfies_k_anonymity}")
print(f"Does the dataset satisfy the l-diversity for l={L}? {satisfies_l_diversity}")
