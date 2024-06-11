from dataset_generator import dataGeneration
import pandas as pd
import json , math , argparse
import itertools
# variable initialization
LV=1
AGE_GENERALIZATION=15
ZIPCODE_GENERALIZATION=3

# list of attributes
names = ['first name', 'last name', 'gender', 'age', 'zip code', 'role', 'education', 'salary']
numerical =  ['age', 'zip code' ]
categorical =  ['gender', 'role', 'education']
ei =  ['first name', 'last name']
sens =  ['salary']

# function to parse the program options
def programOptions():
    parser = argparse.ArgumentParser()
    parser.add_argument("--k_anoniminity","-k", required=False, default=3)
    parser.add_argument("--l_diversity", "-l",  required=False, default=3)
    parser.add_argument("--num" , "-n" , required=False, default=1000)
    return parser

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

# function to apply the generalization function to the correct quasi identifier 
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

# function to check if the dataset is l-diverse
def check_l_diversity(ds, quasi_identifiers, sensitive_attr,l):
    df = pd.DataFrame(ds)
    groups = df.groupby(quasi_identifiers)
    # check the diversity
    for name, group in groups:
        if group[sensitive_attr].nunique() < l:
            return False
    return True

if __name__ == '__main__':
    # parse the program options
    args = programOptions().parse_args()
    print(f"argument: {args}")
    k=int(args.k_anoniminity)
    l=int(args.l_diversity)
    num=int(args.num)
    
    # data generation
    initial_ds = dataGeneration(num)

    # generalization levels
    lvs={"age":1, "role":1, "education":1, "zip code":1, "gender":1} 
    iterKeys = itertools.cycle(lvs.keys())
    valid_ds = initial_ds.copy()
    valid_lv = lvs
    # generalization loop
    while True:
        ds = dataGeneration()
        apply_generalization(ds,lvs)
        
        satisfies_k_anonymity = check_k_anonymity(ds, ['gender', 'age', 'zip code', 'role', 'education'], k)
        satisfies_l_diversity = check_l_diversity(ds, ['gender', 'age', 'zip code', 'role', 'education'], 'salary', l)
        
        # keep the dataset if it satisfies k-anonymity and l-diversity
        if satisfies_k_anonymity and satisfies_l_diversity:

            valid_ds = ds
            valid_lvs = lvs.copy()

            attr = next(iterKeys)
            lvs[attr] += 1
        # if the dataset doesn't satisfy k-anonymity and l-diversity, break the loop
        else:
            print(f"Dataset with lvs={valid_lvs} doesn't satisfies k-anonymity and l-diversity")
            
            # Print if the dataset couldn't satisfy the k-anonymity and l-diversity with lv = 1
            if all(value == 1 for value in valid_lvs.values()):
                print(f"k={k} and l={l} are not satisfied even with the maximum level of generalization")
            break

    print("Initial dataset:")
    print(pd.DataFrame(initial_ds))

    print(f"Generalized dataset at this level {valid_lvs}:")
    print(pd.DataFrame(valid_ds))

