import pandas as pd
import random
from faker import Faker

fake = Faker(locale='en_US')
Faker.seed(10)
random.seed(10)

roles = {"manager":{"age":"40-60", "salary":"120000-180000"}, "human resources":{"age":"20-50", "salary":"30000-50000"}, "developer":{"age":"22-45", "salary":"80000-100000"}, "cleaner":{"age":"20-60", "salary":"20000-25000"}, "security":{"age":"30-50", "salary":"40000-60000"}, "technical support":{"age":"25-55", "salary":"40000-60000"}, "IT":{"age":"20-45", "salary":"45000-70000"}}
numOfEmployees = 50
employee_list = []
num_woman=0
num_man=0

for i in range(int(numOfEmployees)):
    #choose random number 0 or 1: 0 for female name and 1 for male name
    if random.randint(0,1)==0:
        first_name = fake.first_name_female()
        num_woman += 1
    else:
        first_name = fake.first_name_male()
        num_man += 1
        
    last_name = fake.last_name()
    #detroit has zip codes from 48127 to 48288
    zip_code = random.randint(48127,48288)
    #select role based on roles list with the following weights
    role = random.choices(list(roles.keys()), weights = [10, 10, 30, 10, 10, 15, 15]) 

    lower_age = int(roles[role[0]]["age"].split("-")[0])
    higher_age = int(roles[role[0]]["age"].split("-")[1])
    age = random.randint(lower_age, higher_age)
    
    lower_salary = int(roles[role[0]]["salary"].split("-")[0])
    higher_salary = int(roles[role[0]]["salary"].split("-")[1])
    salary = random.randint(lower_salary, higher_salary)
    
    #add all elements to the list
    employee_list.append({"first name": first_name, "last name": last_name, "zip code": zip_code, "role": role[0], "age": age, "salary": salary})
    
print(num_man)
print(num_woman)

#list conversion to pandas dataframe
df = pd.DataFrame(employee_list)
print(df)
