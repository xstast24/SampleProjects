#!/usr/bin/env python3

#CSV:xstast24

import sys
import xml.etree.ElementTree as ETree
import re
sys.path.append(sys.path.pop(0))
# noinspection PyUnresolvedReferences
import csv


class TagValidator:
    """
    This class serves only to validate XML tags - valid anmes and characters.
    """
    @staticmethod
    def replace_problematic_symbols(element_name, replacement):
        """
        Replaces unwanted symbols in string with their escaped XML equivalents, eg. & -> &mp;.
        :param element_name: string to replace symbols in
        :param replacement: symbol which should replace the original invalid symbol
        """
        # replace invalid symbols
        if element_name.find(';') != -1 or element_name.find('[') != -1 or element_name.find(']') != -1 or element_name.find('\\') != -1 or element_name.find('^') != -1:
            element_name = element_name.replace(';', replacement)
            element_name = element_name.replace('[', replacement)
            element_name = element_name.replace(']', replacement)
            element_name = element_name.replace('\\', replacement)
            element_name = element_name.replace('^', replacement)

        # replace more invalid symbols
        if element_name.find('/') != -1 or element_name.find('<') != -1 or element_name.find('>') != -1 or element_name.find('=') != -1 or element_name.find('?') != -1 or element_name.find('@') != -1:
            element_name = element_name.replace('/', replacement)
            element_name = element_name.replace('<', replacement)
            element_name = element_name.replace('>', replacement)
            element_name = element_name.replace('=', replacement)
            element_name = element_name.replace('?', replacement)
            element_name = element_name.replace('@', replacement)

        # replace even more invalid symbols
        if element_name.find('{') != -1 or element_name.find('}') != -1:
            element_name = element_name.replace('{', replacement)
            element_name = element_name.replace('}', replacement)

        # replace &
        if element_name.find('&') != -1:
            element_name = element_name.replace('&', replacement)

        if element_name.find('"') != -1 or element_name.find("'") != -1:
            element_name = element_name.replace('"', replacement)
            element_name = element_name.replace("'", replacement)

        if element_name.find('<') != -1 or element_name.find('>') != -1:
            element_name = element_name.replace("<", replacement)
            element_name = element_name.replace(">", replacement)

        if element_name.find('\n') != -1 or element_name.find('\r\r') != -1 or element_name.find('\u0020') != -1:
            element_name = element_name.replace("\r\n", replacement)
            element_name = element_name.replace("\n", replacement)
            element_name = element_name.replace("\u0020", replacement)

        chars = [(0x00, 0x08), (0x0B, 0x0C), (0x0E, 0x1F), (0x7F, 0x84), (0x86, 0x9F), (0xD800, 0xDFFF), (0xFDD0, 0xFDDF), (0xFFFE, 0xFFFF)]
        ranges = ["%s-%s" % (chr(low), chr(high)) for (low, high) in chars]
        invalid_xml_chars = re.compile(u'[%s]' % u''.join(ranges))
        if invalid_xml_chars.search(element_name):
            element_name = re.sub(invalid_xml_chars, replacement, element_name)

        return element_name

    @staticmethod
    def check_valid_tag(element_name, error_message, error_code):
        """
        This method validates element's name. If not valid XML tag name, call an error function. The code execution will not continue!
        :param element_name: string to validate
        :param error_message: error message to print if invalid name
        :param error_code: error code to return if invalid name
        """
        chars = [(0x00, 0x08), (0x0B, 0x0C), (0x0E, 0x1F), (0x7F, 0x84), (0x86, 0x9F), (0xD800, 0xDFFF), (0xFDD0, 0xFDDF), (0xFFFE, 0xFFFF)]
        ranges = ["%s-%s" % (chr(low), chr(high)) for (low, high) in chars]
        invalid_xml_chars = re.compile(u'[%s]' % u''.join(ranges))
        if invalid_xml_chars.search(element_name):
            print_error(error_message, error_code)

        # check first char
        check_xml_start = re.compile(r'^(\-|\.|\d|\xb7|\u0020)')
        if check_xml_start.search(element_name[0]):
            print_error(error_message, error_code)

        # check starting with 'xml'
        check_xml_start = re.compile(r'^(x|X)(m|M)(l|L)')
        if check_xml_start.search(element_name):
            print_error(error_message, error_code)

        # check some invalid symbols
        if element_name.find(';') != -1 or element_name.find('[') != -1 or element_name.find(']') != -1 or element_name.find('\\') != -1 or element_name.find('^') != -1:
            print_error(error_message, error_code)

        # check some other invalid symbols
        if element_name.find('/') != -1 or element_name.find('<') != -1 or element_name.find('>') != -1 or element_name.find('=') != -1 or element_name.find('?') != -1:
            print_error(error_message, error_code)

        # check some more invalid symbols
        if element_name.find('@') != -1 or element_name.find('{') != -1 or element_name.find('}') != -1:
            print_error(error_message, error_code)

        # check unescaped &&&&&&&
        pos = 0
        while pos != -1:
            pos = element_name.find('&')
            if pos != -1:
                if element_name[pos:pos+3] != '&lt' and element_name[pos:pos+3] != '&gt' and element_name[pos:pos+4] != '&amp' and element_name[pos:pos+5] != '&apos' and element_name[pos:pos+5] != '&quot':
                    print_error(error_message, error_code)
                element_name = element_name.replace('&', '', 1)

        if element_name.find('"') != -1 or element_name.find("'") != -1:
            print_error(error_message, error_code)

        if element_name.find('<') != -1 or element_name.find('>') != -1:
            print_error(error_message, error_code)


class Params:
    """
    This class serves to handle input parameters and control their validity.
    """

    def __init__(self, argv):
        # remove script from parameters
        self.params = argv
        self.input = None
        self.output = None
        self.no_xml_header = None
        self.root_element = None
        self.root_element_set = None
        self.separator = None
        self.first_line_header = None
        self.first_line_header_subst = None
        self.column = None
        self.row_set = None
        self.row = None
        self.row_index = None
        self.row_index_init = None
        self.error_recovery = None
        self.missing_cols = None
        self.extra_cols = None
        self.padding = None

    @staticmethod
    def print_help():
        print("Skript pro konverzi CSV (dle RFC 4180) do XML. Kazdemu radku CSV opovida jeden dodefinovany parovy element (viz parametr -l),\n"
              "ten bude obsahovat elementy pro jednotlive sloupce (viz parametr -h). Tyto elementy pak jiz budou obsahovat textovou hodnotu dane bunky z csv zdroje.\n"
              "Problematicke znaky budou konvertovany na odpovidajici zapis v XML. Skript pracuje s temito parametry:\n"
              "--help - vypise napovedu a ukonci skript.\n"
              "--input=filename - vstupni CSV soubor, pokud parametr chybi, nacte data ze standardniho vstupu.\n"
              "--output=filename - vystupni XML soubor, pokud chybi, vypise skript data na standardni vystup.\n"
              "-n - negenerovat hlavicku skriptu.\n"
              "-r=root-element - jmeno paroveho korenoveho elementu obalujici vysledek. Pokud chybi, vysledek neni obalen kor. elementem (nevalidni XML).\n"
              "-s=separator - oddelovac bunek/sloupcu na kazdem radku CSV souboru. Vychozi oddelovac je carka ','.\n"
              "-h=subst - prvni zaznam CSV souboru slouzi jako hlavicka a podle nej se nazyvaji XML elementy.\n"
              "-c=column-element - urcuje prefix jmena XML elementu kdyz neni prvni radek CSV pouzit pro tento ucel. Vychozi nazev je 'colX', kde X je cislo bunky.\n"
              "-l=line_element - jmeno elementu, ktery v XML obaluje zvlast kazdy radek vstupniho CSV. Vychozi hodnota je 'row'.\n"
              "-i - vlozeni atributu 'index' do XML elementu 'line-element', platne pouze v kombinaci s parametrem '-l'.\n"
              "--start=n - inicializacni hodnota citace '-i', platny pouze v kombinaci s '-l' a '-i'.\n"
              "-e / --error-recovery - pri chybnem poctu sloupcu v CSV jsou chybejici sloupce nahrazeny prazdnym elementem a prebyvajici sloupce ignorovany.\n"
              "-missing-field=val - pokud CSV sloupec chybi, nahradi se hodnotou 'val'. Pouze v kombinaci s '-e'.\n"
              "--all-columns - sloupce v CSV prebyvajici jsou take vypsany do XML. Pouze v kombinaci s '-e'."
              "--padding - zarovnani idnexu u radku i sloupcu na stejny pocet cislic.")
        sys.exit(0)

    def get_params(self):
        """
        Gets all input parameters and checks if they are in valid format and there are no multiple definitions of one parameter.
        """
        del(self.params[0])
        if not len(self.params) == 0:
            for param in self.params:
                length = len(param)
                err_msg = "Chybne zadane parametry. Chybny, nekompletni, nebo vicenasobny parametr: {0}".format(param)
                if param == '--help' or param == '-help':
                    if len(self.params) == 1:
                        self.print_help()
                    else:
                        print_error("Parametr --help nelze kombinovat.", 1)
                elif param.startswith('--input='):
                    if not self.input and length > 8:
                        self.input = param[8:]
                    else:
                        print_error(err_msg, 1)
                elif param.startswith('--output='):
                    if not self.output and length > 9:
                        self.output = param[9:]
                    else:
                        print_error(err_msg, 1)
                elif param == '-n':
                    if self.no_xml_header:
                        print_error(err_msg, 1)
                    self.no_xml_header = True
                elif param.startswith('-r='):
                    if not self.root_element_set and length > 3:
                        self.root_element = param[3:]
                        self.root_element_set = True
                    else:
                        print_error(err_msg, 1)
                elif param.startswith('-s='):
                    if not self.separator and length > 3:
                        self.separator = param[3:]
                    else:
                        print_error(err_msg, 1)
                elif param.startswith('-h='):
                    if not self.first_line_header and length > 3:
                        self.first_line_header = True
                        self.first_line_header_subst = param[3:]
                    else:
                        print_error(err_msg, 1)
                elif param == '-h':
                    if not self.first_line_header:
                        self.first_line_header = True
                        self.first_line_header_subst = '-'
                    else:
                        print_error(err_msg, 1)
                elif param.startswith('-c='):
                    if not self.column and length > 3:
                        self.column = param[3:]
                    else:
                        print_error(err_msg, 1)
                elif param.startswith('-l='):
                    if not self.row_set and length > 3:
                        self.row_set = True
                        self.row = param[3:]
                    else:
                        print_error(err_msg, 1)
                elif param == '-i':
                    if not self.row_index:
                        self.row_index = True
                    else:
                        print_error(err_msg, 1)
                elif param.startswith('--start='):
                    if not self.row_index_init and length > 8:
                        self.row_index_init = param[8:]
                    else:
                        print_error(err_msg, 1)
                elif param == '-e' or param == '--error-recovery':
                    if not self.error_recovery:
                        self.error_recovery = True
                    else:
                        print_error(err_msg, 1)
                elif param.startswith('--missing-field='):
                    if not self.missing_cols and length > 16:
                        self.missing_cols = param[16:]
                    else:
                        print_error(err_msg, 1)
                elif param == '--all-columns':
                    if not self.extra_cols:
                        self.extra_cols = True
                    else:
                        print_error(err_msg, 1)
                elif param == '--padding':
                    if self.padding:
                        print_error(err_msg, 1)
                    self.padding = True
                else:
                    print_error(err_msg, 1)

    def check_params(self):
        """
        Checks if all needed parameters have been set properly, sets the default ones if needed. Checks if there are no invalid param combinations.
        """
        if self.input is None:
            self.input = sys.stdin

        if self.output is None:
            self.output = sys.stdout

        if self.root_element_set:
            TagValidator.check_valid_tag(self.root_element, "Neplatny XML nazev root elementu!", 30)

        if self.separator is None:
            self.separator = ','

        elif len(self.separator) > 1:
            if self.separator == 'TAB' or self.separator == 'tab':
                self.separator = '\t'
            else:
                print_error("Neplatny separator {0}".format(self.separator), 1)

        if self.column is None:
            self.column = 'col'
        else:
            TagValidator.check_valid_tag(self.column, "Neplatny nazev column elementu.", 30)

        if self.row_set is None:
            self.row = 'row'
        else:
            TagValidator.check_valid_tag(self.row, "Neplatny nazev line elementu.", 30)

        if self.row_index is not None and self.row_set is None:
            print_error("-i parametr muze byt pouzit pouze v kombinaci s -l=line-element.", 1)

        if self.row_index_init is not None and (self.row_set is None or self.row_index is None):
            print_error("--start=n muze byt pouzit pouze v kombinaci s -l=line_element a -i.", 1)

        if self.row_index_init is not None:
            try:
                self.row_index_init = int(self.row_index_init)
            except ValueError:
                print_error("Chybne zadany parametr --start=n, nelze konvertovat na cele cislo.", 1)

        if self.missing_cols is not None and self.error_recovery is None:
            print_error("--missing-field=val muze byt pouzito pouze v kombinaci s --error-recovery / -e.", 1)

        if self.extra_cols is not None and self.error_recovery is None:
            print_error("--all-columns muze byt pouzito pouze v kombinaci s --error-recovery / -e.", 1)


def print_error(error_message, code):
    """
    Prints given error message to stderr and exits program execution with given code.
    :param error_message: string - error description
    :param code:  int - error code according to project specification
    """
    sys.stderr.write(error_message)
    sys.exit(code)


def open_input_file(in_csv_file):
    """
    Opens input file.
    :param in_csv_file: CSV file (input), from which the csv content will be loaded
    """
    if in_csv_file != sys.stdin:
        try:
            source_file = open(in_csv_file, newline='')
            return source_file
        except IOError:
            print_error("Nelze nacist data ze vstupniho souboru.", 2)
    else:
        return in_csv_file


def open_output_file(output, no_header):
    """
    Open output file and write XML header if needed.
    :param output: output file name to open
    :param no_header: parameter which tells if there should be XML header, or not
    """
    if output != sys.stdout:
        xml_file = None
        # opening output file
        try:
            xml_file = open(output, mode='w', encoding='utf-8')
        except IOError:
            print_error("Nelze zapisovat data do vystupniho souboru.", 2)
    else:
        xml_file = output

    # write XML header
    if not no_header:
        xml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")

    return xml_file


def write_xml_elements_to_file(xml_elements, file):
    """
    Get list of ElementTree Elements, write them to the given file, if needed, wraps the elements with a root element.
    :param xml_elements: list of ElementTree Elements which will be written to the file
    :param file: opened file pointer to which xml elements will be written
    """
    # write XML to file
    if params.root_element_set:
        root = ETree.Element(params.root_element)
        for element in xml_elements:
            root.extend([element])

        root_string = ETree.tostring(root).decode()
        file.write(root_string)
    else:
        for element in xml_elements:
            element_string = ETree.tostring(element).decode()
            file.write(element_string + '\n')

# parse parameters
params = Params(sys.argv)
params.get_params()
params.check_params()

# open input file
source_csv_file = open_input_file(params.input)
# read CSV file
csv_ = []
if source_csv_file != sys.stdin:
    # create list of CSV rows (list of lists)
    for row in csv.reader(source_csv_file, delimiter=params.separator):
        csv_.append(row)

    # close source_file
    source_csv_file.close()
else:
    buffer_stdin = sys.stdin.readlines()
    for row in csv.reader(buffer_stdin, delimiter=params.separator):
        csv_.append(row)

col_names = []

# in case of empty input file
if len(csv_) == 0:
    # if given empty csv file and first line header is set, invalid - empty - xml tag would be created
    if params.first_line_header:
        print_error("Not valid file for given parameters.", 31)

    # open output file
    output_file = open_output_file(params.output, params.no_xml_header)
    if params.root_element_set:
        output_file.write("<{0}><row><col1></col1></row></{0}>".format(params.root_element))
    else:
        output_file.write("<row><col1></col1></row>")
    sys.exit(0)


header_length = len(csv_[0])
if params.first_line_header:
    for col in csv_[0]:
        col = TagValidator.replace_problematic_symbols(col, params.first_line_header_subst)
        TagValidator.check_valid_tag(col, "Neplatne jmeno elementu po zpracovani parametru -h.", 31)
        col_names.append(col)

    del(csv_[0])

# list of row elements
elements = []
# set row index if needed
if params.row_index is not None and params.row_index_init is not None:
    index = params.row_index_init
elif params.row_index is not None and params.row_index_init is None:
    index = 1
else:
    index = None

# parse csv into ElementTree Elements
first_line_length = None
i = 0
csv_len = len(csv_)  # for padding purposes
csv_index_len = len(str(csv_len))  # for padding purposes
for row in csv_:
    i += 1
    row_len = len(row)  # for padding purposes
    row_index_len = len(str(row_len))  # for padding purposes
    # make elements from rows
    if index is not None:
        if params.padding:
            index_len = len(str(index))
            pad_index = '0'*(csv_index_len - index_len) + str(index)
            new_row = ETree.Element(params.row, attrib={'index': pad_index})
        else:
            new_row = ETree.Element(params.row, attrib={'index': str(index)})

        index += 1
    else:
        new_row = ETree.Element(params.row)

    # initiate cols count according to first line
    if not first_line_length:
        if params.first_line_header:
            first_line_length = header_length
        else:
            first_line_length = len(row)

        if first_line_length < 1:
            print_error("Vstupni soubor nema platny pocet sloupcu na prvnim radku.", 32)

    # no error recovery and invalid columns -> error
    if not params.error_recovery and len(row) != first_line_length:
        print_error("Neplatny vstupni soubor, chybny pocet sloupcu v casti {0}".format(i), 32)

    cols = []
    if not params.first_line_header:  # first line headers NOT used to name cols
        col_index = 1
        for col in row:
            if params.padding:  # padding purposes
                col_index_len = len(str(col_index))
                pad_col_index = '0'*(row_index_len - col_index_len) + str(col_index)
                if params.error_recovery:
                    pad_col_index = '0'*(len(str(first_line_length)) - col_index_len) + str(col_index)
                    if params.extra_cols:
                        if len(str(first_line_length)) < row_index_len:
                            pad_col_index = '0' * (row_index_len - col_index_len) + str(col_index)
                new_col = ETree.Element(params.column + pad_col_index)
            else:
                new_col = ETree.Element(params.column + str(col_index))

            new_col.text = col
            cols.append(new_col)
            col_index += 1

        if params.error_recovery:
            # less columns than first line
            if len(row) < first_line_length:
                for item in range(first_line_length - len(row)):
                    if params.padding:  # padding purposes
                        col_index_len = len(str(col_index))
                        pad_col_index = '0' * (len(str(first_line_length)) - col_index_len) + str(col_index)
                        new_col = ETree.Element(params.column + pad_col_index)
                    else:
                        new_col = ETree.Element(params.column+str(col_index))

                    if params.missing_cols is not None:
                        new_col.text = params.missing_cols

                    cols.append(new_col)
                    col_index += 1

            # more columns than first line
            if not params.extra_cols:
                if len(row) > first_line_length:
                    for x in range(len(row) - first_line_length):
                        cols.pop()
    else:  # first line header used to name cols
        i = 0
        col_index = 1
        for col in row:
            if i >= len(col_names):
                if params.extra_cols and params.padding:
                    col_index_len = len(str(col_index))
                    pad_col_index = '0' * (row_index_len - col_index_len) + str(col_index)
                    new_col = ETree.Element(params.column+pad_col_index)
                else:
                    new_col = ETree.Element(params.column + str(col_index))
            else:
                new_col = ETree.Element(col_names[i])

            new_col.text = col
            cols.append(new_col)
            i += 1
            col_index += 1

        if params.error_recovery:
            # less columns than first line
            if len(row) < first_line_length:
                for item in range(first_line_length - len(row)):
                    if params.padding:  # padding purposes
                        col_index_len = len(str(col_index))
                        pad_col_index = '0' * (len(str(first_line_length)) - col_index_len) + str(col_index)
                        new_col = ETree.Element(params.column + pad_col_index)
                    else:
                        new_col = ETree.Element(params.column + str(col_index))

                    if params.missing_cols is not None:
                        new_col.text = params.missing_cols

                    cols.append(new_col)
                    col_index += 1

            # more columns than first line
            if not params.extra_cols:
                if len(row) > first_line_length:
                    for x in range(len(row) - first_line_length):
                        cols.pop()

    new_row.extend(cols)
    elements.append(new_row)

# open output file
output_file = open_output_file(params.output, params.no_xml_header)
# write xml to output file
write_xml_elements_to_file(elements, output_file)
