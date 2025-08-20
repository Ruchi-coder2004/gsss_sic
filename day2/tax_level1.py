print('Enter your basic details: ')
employee_name = input('Enter your name: ')
employee_id = int(input('Enter your ID: '))
employee_basic_salary = float(input('Enter your salary: '))
employee_special_allowance = float(input('Enter your Special Monthly Allowance: '))
employee_bonus_percentage = int(input('Enter you Annual Bonus as percentage of gross salary: '))

gross_monthly_salary = employee_basic_salary + employee_special_allowance 
employee_bonus = gross_monthly_salary * employee_bonus_percentage /100
annual_gross_salary = (gross_monthly_salary * 12) + employee_bonus
print('\n\nThe employee Details is as follows: ')
print('Employee Name: ',employee_name,'\nEmployee ID: ',employee_id)
print('Employee Gross Monthly salary: ',gross_monthly_salary)
print('Employee Anuual Gross salary: ',annual_gross_salary)


