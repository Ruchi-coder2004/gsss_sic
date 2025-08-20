import tax_level3, tax_level2

net_salary = tax_level2.annual_gross_salary - tax_level3.tax_percentage

print('Annual Gross Salary: ',tax_level2.annual_gross_salary)
print('Total Tax Payable: ',tax_level3.tax_percentage)
print('Annual Net Salary: ',net_salary)