### Dpp Project
Implementing a k-anonymization and l-diverse algorithm using the Samarati approach 
# Dasaset generator
In the dataset_generator.py we use the library "Faker" to generate an artificial dataset with these columns:
- first name
- last name
- gender
- age
- zipcode
- education
- role
- salary
# l-diversity.py
We define the categorical and numerical quasi identifiers and functions to generalize them.
After generating the artificial dataset we apply the generalization to it and we check if the generalized dataset respects the concepts of k-anonymity and l-diversity. If it does we try to generalize further until k-anonymity and l-diversity are not possible 
# JSON files
JSON files are used to map the generalization tree used for the different levels of generalization
## How To Run
Clone the repository
'''
git clone  https://github.com/AaronKromer/progetto_data.git
cd progetto_data
'''
# Install dependencies
Make sure you have python installed. Install the required packages using pip
''' 
pip install -r requirements.txt
'''
# Run the generalization with anonymization and diversity check
''' 
python l-diversity.py 
'''
# Requirements 
- Python 3
- Faker library
- Pandas
