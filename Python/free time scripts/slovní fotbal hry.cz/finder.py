import sys
import re


# PATH TO DESIRED DICTIONARY
source_dict_name = "open_office_grammar_dict"


with open(source_dict_name, 'r', encoding='utf-8') as f_source_dict:
    source_dict = f_source_dict.readlines()

# remove whitespaces if necessary
source_dict = [word.strip() for word in source_dict]

print("velikost slovniku v kb: ", sys.getsizeof(source_dict))
print("pocet slov: ", len(source_dict))

# begin cycle - input letters, get results (input only letters, connected or separated by whitespaces)
print("\nzadejte pismena (jako celek, nebo oddelena mezerami)")
letters = input()
while letters != 'exit' and letters != '':
    letters = letters.strip().replace(' ', '')  # remove whitespaces between letters

    regex = r"\b"
    for letter in set(letters):  # only unique letters, letter count is then added
        regex += "(?!([^" + letter + "\W]*" + letter + "){" + str(letters.count(letter) + 1) + "})"

    unique_letters = ''.join(set(letters))
    regex += ("[" + unique_letters + "]+" + r"\b")  # complete regex without duplicite letters
    # 'noha' regex = r"(?!([^n\W]*n){2})(?!([^o\W]*o){2})(?!([^h\W]*h){2})(?!([^a\W]*a){2})[noha]+"
    # 'noohaaa' regex = r"(?!([^n\W]*n){2})(?!([^o\W]*o){3})(?!([^h\W]*h){2})(?!([^a\W]*a){4})[noha]+"
    # matching in the middle of string regex = r"\b(?!([^n\W]*n){2})(?!([^o\W]*o){3})(?!([^h\W]*h){2})(?!([^a\W]*a){4})[noha]+\b"

    matched = [word for word in source_dict if re.fullmatch(regex, word)]

    print("nalezeno shod: ", len(matched))
    for word in sorted(matched, key=len):
        print(word.upper())

    print("\nzadejte pismena (jako celek, nebo oddelena mezerami)")
    letters = input()
