import csv
import re

from datetime import datetime
from eurobonus_categories import payee_to_labels, label_to_categories, list_invalid_payees

#date_pattern = '^\d{4}-\d{2}-\d{2}'
date_pattern = '/^\d{4}\/\d{2}\/\d{2}'
#valid_csv_line_pattern = '^\d{4}-\d{2}-\d{2},.+,[\d]+\.[\d]+,.+,(.+)?'
valid_csv_line_pattern = '^\d{4}\/\d{2}\/\d{2},\d{4}\/\d{2}\/\d{2},["0-a ]+,["0-a ]+,(["0-a ]+)?,[\d]+,[0-9",]'
#valid_csv_line_pattern = '^\d{4}\/\d{2}\/\d{2},\d{1}'
invoice_payment_pattern = 'BETALT BG DATUM'
current_year = datetime.now().year

def get_category_from_payee(payee: str):
    payee_to_labels_dict = payee_to_labels()
    for payee_pattern in payee_to_labels_dict.keys():
        payee_matched = re.search(payee_pattern, payee)
        
        if payee_matched:
            label = payee_to_labels_dict[payee_pattern]
            category = label_to_categories()[label]
            return category[0], category[1]

    return "Other Expenses", ""

def replace_commas_with_dots(value: str):
    return value.replace(",", ".")

def replace_slashes_with_dashes(string: str):
    return string.replace("/", "-")

list_of_csv_files = [
    "invoices/jun-2022-eurobonus.csv",
    "invoices/jul-2022-eurobonus.csv",
    "invoices/aug-2022-eurobonus.csv",
    "invoices/sep-2022-eurobonus.csv"
]
rows = []

for csv_file in list_of_csv_files:
				file = open(csv_file)
				csvreader = csv.reader(file)
				header = next(csvreader)

				for row in csvreader:
						row_full_line = ','.join(row)
						is_valid_line = re.match(valid_csv_line_pattern, row_full_line)
						if not is_valid_line:
				#        print("full line |{}|".format(row_full_line))
								print("Excluding row {}".format(row))
								continue
						else:
								rows.append(row)
#								print("Matched the regex {}".format(row))

				file.close()

# ['04-30', '05-05', 'ÅRSAVGIFT', '', '', '', '1,495.00']
# transforming into
# 2022-05-26,IZ *FABRIQUE STOCK,-1200.00,Food,Groceries
for row in rows:
    date = replace_slashes_with_dashes(row[0])
    payee = row[2]


    is_payee_invalid = False

    for invalid_payee_pattern in list_invalid_payees():
        is_payee_invalid = re.match(invalid_payee_pattern, payee)

        if is_payee_invalid:
            continue

    if not is_payee_invalid:
        amount = replace_commas_with_dots(row[6])
        category, subcategory = get_category_from_payee(payee)

        print("{},{},{},{},{}".format(date,payee,amount,category,subcategory))


