import sqlalchemy as db
from tabulate import tabulate

engine = db.create_engine("mysql+pymysql://root:root@localhost:3306/ecommerce")
conn = engine.connect()


print("  Question 1: Aggregates for Age > 50 & Grade 3")


query1 = db.text('''
    SELECT 
        Status,
        COUNT(*) AS total_patients,
        ROUND(AVG(`Tumor Size`), 2) AS avg_tumor_size,
        ROUND(AVG(`Survival Months`), 2) AS avg_survival_months
    FROM breast_cancer
    WHERE Age > 50 
      AND Grade LIKE '%3%'
    GROUP BY Status;
''')

exe1 = conn.execute(query1)
headers1 = ['Status', 'Total Patients', 'Avg Tumor Size', 'Avg Survival Months']
results1 = exe1.fetchall()
print(tabulate(results1, headers=headers1, tablefmt='grid'))

print("  Question 2: Patient Categorization by Age Group")


query2 = db.text('''
    SELECT 
        CASE 
            WHEN Age < 40 THEN 'Young (<40)'
            WHEN Age BETWEEN 40 AND 60 THEN 'Middle-Aged (40-60)'
            ELSE 'Senior (>60)'
        END AS age_group,
        COUNT(*) AS total_patients,
        ROUND(AVG(`Survival Months`), 2) AS avg_survival_months
    FROM breast_cancer
    GROUP BY age_group;
''')

exe2 = conn.execute(query2)
headers2 = ['Age Group', 'Total Patients', 'Avg Survival Months']
results2 = exe2.fetchall()

print(tabulate(results2, headers=headers2, tablefmt='grid'))
print(" Question 3: Race vs Average Survival & Tumor Size")
query3 = db.text('''
    SELECT 
        Race, 
        ROUND(AVG(`Survival Months`), 2) AS avg_survival, 
        ROUND(AVG(`Tumor Size`), 2) AS avg_tumor_size 
    FROM breast_cancer 
    GROUP BY Race 
    ORDER BY avg_survival DESC;
''')

exe3 = conn.execute(query3)
headers3 = ['Race', 'Avg Survival Months', 'Avg Tumor Size']
results3 = exe3.fetchall()
print(tabulate(results3, headers=headers3, tablefmt='grid'))
conn.close()