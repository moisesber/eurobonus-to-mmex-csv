import csv
import re

from datetime import datetime
from eurobonus_categories import payee_to_labels, label_to_categories

mm_day_pattern = '^((1[0-2])|(0[1-9]))-[0-3][0-9]'
invoice_payment_pattern = 'BETALT BG DATUM'
current_year = datetime.now().year

def get_category_from_payee(payee: str):
    payee_to_labels_dict = payee_to_labels()
    for payee_pattern in payee_to_labels_dict.keys():
        #payee_matched = re.match(payee_pattern, payee)
        payee_matched = re.search(payee_pattern, payee)
        
        if payee_matched:
            label = payee_to_labels_dict[payee_pattern]
            category = label_to_categories()[label]
            return category[0], category[1]

    return "Other Expenses", ""

def clear_commas_from_values(value: str):
    return value.replace(",", "")

file = open("april-2022-eurobonus.csv")
csvreader = csv.reader(file)
header = next(csvreader)
rows = []
for row in csvreader:
    starts_with_date = re.match(mm_day_pattern, row[0])
    invoice_payment = re.match(invoice_payment_pattern, row[2])

    if starts_with_date and not invoice_payment:
        rows.append(row)
    else:
        print("Excluding row {}".format(row))

file.close()

# ['04-30', '05-05', 'ÅRSAVGIFT', '', '', '', '1,495.00']
# transforming into
# 2022-05-26,IZ *FABRIQUE STOCK,-1200.00,Food,Groceries
for row in rows:
    date = "{}-{}".format(current_year, row[0])
    payee = row[2]
    amount = clear_commas_from_values(row[6])
    category, subcategory = get_category_from_payee(payee)

    print("{},{},{},{},{}".format(date,payee,amount,category,subcategory))

#print(rows)

