import csv
import re

from datetime import datetime
from eurobonus_categories import payee_to_labels, label_to_categories, list_invalid_payees

other_expenses_string="Other Expenses"

#date_pattern = '^\d{4}-\d{2}-\d{2}'
date_pattern = '/^\d{4}\/\d{2}\/\d{2}'
#valid_csv_line_pattern = '^\d{4}-\d{2}-\d{2},.+,[\d]+\.[\d]+,.+,(.+)?'
#valid_csv_line_pattern = '^\d{4}\/\d{2}\/\d{2},\d{4}\/\d{2}\/\d{2},["0-a\*. ]+,["0-a ]+,(["0-a ]+)?,[\d]+,[0-9",]'
#valid_csv_line_pattern = '^\d{4}\/\d{2}\/\d{2},\d{4}\/\d{2}\/\d{2},[0-9A-Za-z \*"\.]+,["0-a ]+,(["0-a ]+)?,[\d]+,[0-9",]'

alphanumeric_word_with_special_chars_regex='[a-zA-Z0-9 -_äöåÄÖÅ"\*\.]+'
date_regex='\d{4}\/\d{2}\/\d{2}'
#valid_csv_line_pattern = '^\d{4}\/\d{2}\/\d{2},\d{4}\/\d{2}\/\d{2},[a-zA-Z0-9 _äöåÄÖÅ"\*\.]+,[\-"0-a ]+,([\-"0-a ]+)?,[\d]+,[\-0-9",]'
valid_csv_line_pattern = '^{},{},{},{},([\-"0-a ]+)?,[\d]+,[\-0-9",]'.format(date_regex, date_regex, alphanumeric_word_with_special_chars_regex, alphanumeric_word_with_special_chars_regex)


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

    #print("No payee found for |{}|".format(payee))

    return other_expenses_string, ""

def replace_commas_with_dots(value: str):
    return value.replace(",", ".")

def replace_slashes_with_dashes(string: str):
    return string.replace("/", "-")

def get_date_object_from_string(date: str):
    return datetime.strptime(date, '%Y-%m-%d').date()

def is_date_between_period(date, start, end):
    return date >= start and date <= end

def is_current_data_vacation_date(date: datetime):
    vacation_periods = [ 
        { "from": "2023-06-25", "to": "2023-07-02" },
        { "from": "2023-04-14", "to": "2023-04-19" }
    ]
    
    for period in vacation_periods:
        if is_date_between_period(date, get_date_object_from_string(period["from"]), get_date_object_from_string(period["to"])):
            return True
    return False

list_of_csv_files = [
#    "invoices/may-2022-eurobonus.csv",
#    "invoices/jun-2022-eurobonus.csv",
#    "invoices/jul-2022-eurobonus.csv",
#    "invoices/aug-2022-eurobonus.csv",
#    "invoices/sep-2022-eurobonus.csv"
		"eurobonus-all-transactions-2023_01-01_10-31.csv",
    "eurobonus-all-transactions-2022_12.csv"
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
        #       print("full line |{}|".format(row_full_line))
				#				print("Excluding row {}".format(row))
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

        if category == other_expenses_string:
            date_object = datetime.strptime(date, '%Y-%m-%d').date()
            
            if is_current_data_vacation_date(date_object):
                category = "Vacation"
                subcategory = "Travel"

        print("{},{},{},{},{}".format(date,payee,amount,category,subcategory))


