import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

original_df = pd.read_csv('initial_dataset.csv')
anonymized_df = pd.read_csv('generalized_dataset.csv')

ordered_ages = ["30-20" ,"40-30", "50-40","60-50","70-60"]
anonymized_df['age'] = pd.Categorical(anonymized_df['age'], categories=ordered_ages, ordered=True)



plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
sns.boxplot(x='age', y='salary', data=original_df)
plt.title('Initial distribution of salary by age')
plt.xlabel('Age')
plt.ylabel('Salary')
plt.xticks(rotation=45)
plt.grid(True)

plt.subplot(1, 2, 2)
sns.boxplot(x='age', y='salary', data=anonymized_df)
plt.title('Generalized distribution of salary by age')
plt.xlabel('Age')
plt.ylabel('Salary')
plt.xticks(rotation=45)
plt.grid(True)


plt.tight_layout()
plt.show()
