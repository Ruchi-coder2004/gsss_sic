import tax_level2

tax_percentage = 0
def tax_cal():
    if tax_level2.annual_gross_salary >=0 and tax_level2.annual_gross_salary <= 300000:
        tax_percentage = 0
    elif tax_level2.annual_gross_salary >=300001 and tax_level2.annual_gross_salary <= 600000:
        tax_percentage = (tax_level2.annual_gross_salary/100)*5
    elif tax_level2.annual_gross_salary >=600001 and tax_level2.annual_gross_salary <= 900000:
        tax_percentage = (tax_level2.annual_gross_salary/100)*10
    elif tax_level2.annual_gross_salary >=900001 and tax_level2.annual_gross_salary <= 1200000:
        tax_percentage = (tax_level2.annual_gross_salary/100)*15
    elif tax_level2.annual_gross_salary >=1200001 and tax_level2.annual_gross_salary <= 1500000:
        tax_percentage = (tax_level2.annual_gross_salary/100)*20
    else:
        tax_percentage = (tax_level2.annual_gross_salary/100)*30

apply_section_rebate = input('Do you have 87A Rebate(say yes or no): ')
if apply_section_rebate == 'yes' and tax_percentage <= 700000:
    tax_percentage = 0
else:
    tax_cal()

health_and_education_cess = (tax_percentage/100)*4
tax_amount = health_and_education_cess + tax_percentage

print('Total tax to be payed: ',tax_percentage)
print('Health and education cess: ',health_and_education_cess)
