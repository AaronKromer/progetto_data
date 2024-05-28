import pandas as pd
import random
from faker import Faker

fake = Faker(locale='en_US')
Faker.seed(10)
random.seed(10)

roles = {
    "Manager":{
        "age":"40-60", 
        "salary":"120000-130000",
        "education":{
            "Doctorate":20, 
            "Masters":40, 
            "Bachelors":30,
            "High School Graduate":10
        }
    }, 
    "Human Resources":{
        "age":"20-50",
        "salary":"30000-40000", 
        "education":{
            "Doctorate":3, 
            "Masters":20, 
            "Bachelors":30,
            "High School Graduate":47
        }
    }, 
    "Developer":{
        "age":"22-45", 
        "salary":"80000-90000",
        "education":{
            "Doctorate":20, 
            "Masters":40, 
            "Bachelors":25,
            "High School Graduate":15
        }
    }, 
    "Cleaner":{
        "age":"20-60", 
        "salary":"18000-22000",
        "education":{
            "Doctorate":2, 
            "Masters":3, 
            "Bachelors":5,
            "High School Graduate":90
        }
    }, 
    "Security":{
        "age":"30-50", 
        "salary":"40000-50000",
        "education":{
            "Doctorate":5, 
            "Masters":5, 
            "Bachelors":10,
            "High School Graduate":80
        }
    }, 
    "Technical Support":{
        "age":"25-55", 
        "salary":"40000-50000",
        "education":{
            "Doctorate":10, 
            "Masters":30, 
            "Bachelors":30,
            "High School Graduate":30
        }
    }, 
    "IT":{
        "age":"20-45", 
        "salary":"45000-55000",
        "education":{
            "Doctorate":10, 
            "Masters":30, 
            "Bachelors":30,
            "High School Graduate":30
        }
    }
}
numOfEmployees = 50
employee_list = []
num_woman=0
num_man=0

for i in range(int(numOfEmployees)):
    #choose random number 0 or 1: 0 for female name and 1 for male name
    if random.randint(0,1)==0:
        first_name = fake.first_name_female()
        num_woman += 1
        gender="F"
    else:
        first_name = fake.first_name_male()
        num_man += 1
        gender="M"
        
    last_name = fake.last_name()
    #detroit has zip codes from 48127 to 48288
    zip_code = random.randint(48127,48288)
    #select role based on roles list with the following weights
    role = random.choices(list(roles.keys()), weights = [10, 10, 30, 10, 10, 15, 15]) 
    education= random.choices(list(roles[role[0]]["education"].keys()), weights = list(roles[role[0]]["education"].values()))

    lower_age = int(roles[role[0]]["age"].split("-")[0])
    higher_age = int(roles[role[0]]["age"].split("-")[1])
    age = random.randint(lower_age, higher_age)
    
    lower_salary = int(roles[role[0]]["salary"].split("-")[0])
    higher_salary = int(roles[role[0]]["salary"].split("-")[1])
    salary = random.randint(lower_salary, higher_salary)
    seniority=age-20
    #add all elements to the list
    employee_list.append({"first name": first_name, "last name": last_name, "gender":gender,"age": age,  "zip code": zip_code, "education": education[0] ,"role": role[0],  "salary":round((salary+(seniority*500)) / 100) * 100})
    

#list conversion to pandas dataframe
df = pd.DataFrame(employee_list)
print(df)
