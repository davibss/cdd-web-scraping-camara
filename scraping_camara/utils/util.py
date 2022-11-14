def string_cleaner(raw_text):
    return raw_text.replace('\n', '').strip()

def get_number_from_text(raw_text):
    return int(string_cleaner(raw_text).split(' ')[0])

def bill_parser(raw_salary):
    cleaned_salary = string_cleaner(raw_salary.replace('R$',''))
    return float(cleaned_salary.replace('.', '').replace(',', '.'))