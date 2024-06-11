import pandas as pd
import random
from faker import Faker
import os
NUM=10000

def dataGeneration(num=NUM):
    fake = Faker(locale='en_US')
    Faker.seed(10)
    random.seed(10)

    roles = {
        "Manager":{
            "age":"40-68", 
            "salary":"50000-60000",
            "education":{
                "Doctorate":20, 
                "Masters":40, 
                "Bachelors":30,
                "High School Graduate":10
            }
        }, 
        "Team Leader":{
            "age":"35-62", 
            "salary":"45000-55000",
            "education":{
                "Doctorate":10, 
                "Masters":20, 
                "Bachelors":40,
                "High School Graduate":30
            }
        },
        "Project Manager":{
            "age":"40-64", 
            "salary":"40000-50000",
            "education":{
                "Doctorate":20, 
                "Masters":40, 
                "Bachelors":30,
                "High School Graduate":10
            }
        },
        "Accountant":{ 
            "age":"23-64", 
            "salary":"35000-40000",
            "education":{
                "Doctorate":2, 
                "Masters":20, 
                "Bachelors":40,
                "High School Graduate":40
            }
        },
        "Finance Analyst":{
            "age":"30-60", 
            "salary":"35000-40000",
            "education":{
                "Doctorate":5, 
                "Masters":30, 
                "Bachelors":30,
                "High School Graduate":35
            }
        },
        "Human Resource Recruiter":{
            "age":"22-60", 
            "salary":"25000-30000",
            "education":{
                "Doctorate":2, 
                "Masters":20, 
                "Bachelors":40,
                "High School Graduate":38
            }
        },
        "Training and Development Specialist":{
            "age":"23-60", 
            "salary":"27000-30000",
            "education":{
                "Doctorate":2, 
                "Masters":23, 
                "Bachelors":40,
                "High School Graduate":35
            }
        },
        "Compensation and Benefits Specialist":{
            "age":"24-50", 
            "salary":"30000-33000",
            "education":{
                "Doctorate":2, 
                "Masters":20, 
                "Bachelors":40,
                "High School Graduate":38
            }
        },
        "Sales Representative":{   
            "age":"24-55", 
            "salary":"30000-33000",
            "education":{
                "Doctorate":2, 
                "Masters":20, 
                "Bachelors":20,
                "High School Graduate":58
            }
        },
        "Customer Service Representative":{
            "age":"22-55", 
            "salary":"30000-33000",
            "education":{
                "Doctorate":2, 
                "Masters":15, 
                "Bachelors":15,
                "High School Graduate":68
            }
        },
        "Marketing Specialist":{
            "age":"23-60", 
            "salary":"30000-33000",
            "education":{
                "Doctorate":2, 
                "Masters":30, 
                "Bachelors":30,
                "High School Graduate":38
            }
        },
        "Sales Support Specialist":{
            "age":"22-50", 
            "salary":"30000-33000",
            "education":{
                "Doctorate":5, 
                "Masters":30, 
                "Bachelors":30,
                "High School Graduate":35
            }
        },
        "IT Specialist":{
            "age":"24-63", 
            "salary":"33000-35000",
            "education":{
                "Doctorate":5, 
                "Masters":20, 
                "Bachelors":30,
                "High School Graduate":45
            }
        },
        "Data Analyst":{
            "age":"24-63", 
            "salary":"35000-40000",
            "education":{
                "Doctorate":15, 
                "Masters":50, 
                "Bachelors":30,
                "High School Graduate":5
            }
        },
        "Software Engineer":{
            "age":"24-63", 
            "salary":"30000-40000",
            "education":{
                "Doctorate":10, 
                "Masters":60, 
                "Bachelors":20,
                "High School Graduate":10
            }
        },
        "Administrative Assistant":{
            "age":"22-40", 
            "salary":"33000-35000",
            "education":{
                "Doctorate":5, 
                "Masters":40, 
                "Bachelors":30,
                "High School Graduate":25
            }
        },
        "Executive Assistant":{
            "age":"22-40", 
            "salary":"33000-35000",
            "education":{
                "Doctorate":5, 
                "Masters":40, 
                "Bachelors":30,
                "High School Graduate":25
            }
        },
        "Legal Consultant":{
            "age":"25-68", 
            "salary":"40000-45000",
            "education":{
                "Doctorate":10, 
                "Masters":70, 
                "Bachelors":20,
                "High School Graduate":0
            }
        }
    }
        
    numOfEmployees = num
    employee_list = []
    num_woman=0
    num_man=0
    zip_code_list=range(48127 ,48289)
    #zip_code_list=[16121, 16124, 16125, 16126, 16127, 16128, 16129, 16131, 16132, 16133, 16134, 16135, 16136, 16137, 16138, 16139, 16140, 16141, 16142, 16143, 16144, 16145, 16146, 16147, 16148, 16149]

    for i in range(int(numOfEmployees)):
        #choose random number 0 or 1: 0 for female name and 1 for male name
        if random.randint(0,1)==0:
            first_name = fake.first_name_female()
            num_woman += 1
            gender="Female"
        else:
            first_name = fake.first_name_male()
            num_man += 1
            gender="Male"
            
        last_name = fake.last_name()
        #detroit has zip codes from 48127 to 48288
        # zip_code = random.randint(48127,48288)
        zip_code = random.choice(zip_code_list)
        #select role based on roles list with the following weights
        role = random.choices(list(roles.keys()), weights = [10, 10, 30, 10, 10, 15, 15, 10, 10, 10, 10, 10, 10, 10, 10, 10,10,10]) 
        education= random.choices(list(roles[role[0]]["education"].keys()), weights = list(roles[role[0]]["education"].values()))

        lower_age = int(roles[role[0]]["age"].split("-")[0])
        higher_age = int(roles[role[0]]["age"].split("-")[1])
        age = random.randint(lower_age, higher_age)
        # salary = roles[role[0]]["salary"]
        
        lower_salary = int(roles[role[0]]["salary"].split("-")[0])
        higher_salary = int(roles[role[0]]["salary"].split("-")[1])
        salary = random.randint(lower_salary, higher_salary)
        seniority=age-20
        # add all elements to the list
        employee_list.append({"first name":first_name,"last name":last_name,"gender":gender,"age": age,  "zip code": zip_code, "education": education[0] ,"role": role[0],  "salary":round((salary+(seniority*350)) / 1000) * 1000})
    

    df = pd.DataFrame(employee_list)
    return employee_list
    # csv_filename = 'employee_dataset.csv'
    # df.to_csv(csv_filename, index=False)
    
    # data_filename = 'employee_data.data'
    # os.rename(csv_filename, data_filename)


dataGeneration()
    #list conversion to pandas dataframe
# df = pd.DataFrame(employee_list)
    # return(df)



