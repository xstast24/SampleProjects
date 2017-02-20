<?php
# Projekt IPP
# CLS: xstast24
# Filip Stastny

params::get_params();
params::check_params();

$input = fileHandling::read_input_file(params::$input_file);
fileHandling::check_output_file(params::$output_file);

# cut starting whitespaces and first 'class' word, remove ending '{;' and whitespaces, so we got same formatted result for each class when split by '}; class'
$input = preg_replace('/(\s*)class(\s+)/', '', $input, 1);
$input = preg_replace('/};(\s*)$/', '', $input, 1);
$split_classes = preg_split('/};(\s*)class(\s+)/', $input);
# save each class to a separate object with its content string
$array = array();
foreach($split_classes as $current_class){
    array_push($array, $class = new classData($current_class));
}

# load each class data from its content string
foreach($array as $item){
    classData::parse_class_content($item, $array);
    classData::get_class_kind($item);
}
classData::get_class_children($array);


# write to output XML file
$writer = new XMLWriter();
$writer->openUri(params::$output_file);
$writer->startDocument('1.0','utf-8');
$writer->setIndent(true);
$writer->setIndentString(str_repeat(' ', params::$pretty_xml));

# details of one class
if(params::$details_class){
    $class_found = false;
    foreach($array as $item){
        if(params::$details_class == $item->name) $class_found = true;
    }

    if($class_found){
        # print class details
        # TODO
    }
    else{
        # class not found, output is just XML header
        exit(0);
    }
}

# print details of all classes
if(params::$details_set){
    $writer->startElement('model');
    # TODO
    $writer->endElement();
}
# print inheritance tree
else{
    $writer->startElement('model');
    foreach($array as $class){
        if(count($class->children) > 0 and $class->already_print == false){
            $writer->startElement('class');
            $writer->writeAttribute('name', $class->name);
            $writer->writeAttribute('kind', $class->kind);
            print_children($class);
            $writer->endElement();
        }
    }
    $writer->endElement();
}

# script finished successfully
exit(0);

# class to save each variable into object
class variable{
    public
        $name = '',
        $type = NULL,
        $is_pointer = false,
        $privacy = NULL;
}

# class to save each method into object
class method{
    public
        $name = '',
        $type = NULL,
        $privacy = NULL;
}

# enum of C++ types for regex purposis and output xml formatting
class type{
    static public
        $bool = 'bool',
        $void = 'void',
        $char = 'char',
        $unsigned_char = 'unsigned char',
        $signed_char = 'signed char',
        $int = 'int',
        $unsigned_int = 'unsigned int',
        $signed_int = 'signed int',
        $short_int = 'short int',
        $unsigned_short_int = 'unsigned short int',
        $signed_short_int = 'signed short int',
        $long_int = 'long int',
        $signed_long_int = 'signed long int',
        $unsigned_long_int = 'unsigned long int',
        $float = 'float',
        $double = 'double',
        $long_double = 'long double',
        $wchar_t = 'wchar_t';
    static public $reg_types = array(
        'rbool' => 'bool',
        'rvoid' => 'void',
        'rchar' => 'char',
        'runsigned_char' => 'unsigned\s+char',
        'rsigned_char' => 'signed\s+char',
        'rint' => 'int',
        'runsigned_int' => 'unsigned\s+int',
        'rsigned_int' => 'signed\s+int',
        'rshort_int' => 'short\s+int',
        'runsigned_short_int' => 'unsigned\s+short\s+int',
        'rsigned_short_int' => 'signed\s+short\s+int',
        'rlong_int' => 'long\s+int',
        'rsigned_long_int' => 'signed\s+long\s+int',
        'runsigned_long_int' => 'unsigned\s+long\s+int',
        'rfloat' => 'float',
        'rdouble' => 'double',
        'rlong_double' => 'long\s+double',
        'rwchar_t' => 'wchar_t');
}

# each class is represented by this object, everything related to a class is stored here
class classData{
    public
        $class_content = NULL,

        $name = '',
        $kind = '',
        $match = '',
        $parents = array(),
        $children = array(),

        # arrays of class variables' objects
        $default_variables = array(),
        $public_variables = array(),
        $protected_variables = array(),
        $private_variables = array(),

        # arrays of class methods' objects
        $default_methods = array(),
        $public_methods = array(),
        $protected_methods = array(),
        $private_methods = array(),

        # class areas with different access kept as strings
        $default_string = '',
        $public_string = '',
        $protected_string = '',
        $private_string = '',

        $already_print = false;

    function __construct($class_content){
        $this->class_content = $class_content;
    }

    # get class kind - abstract/concrete
    # argument is instance of classData
    public static function get_class_kind($class){
        $matches = array();
        if(preg_match('/virtual\s+(.*)\s*=\s*0;/', $class->class_content, $matches)){
            $class->kind = 'abstract';
            $class->match = $matches[1];
            $class->match = preg_replace('/\(/', '', $class->match);
            $class->match = preg_replace('/\)/', '', $class->match);
            $class->match = preg_replace('/\s+/', '', $class->match);
        }
        else $class->kind = 'concrete';

        $abstract = false;
        $match = '';
        if(count($class->parents) > 0) {
            foreach ($class->parents as $parent) {
                $tmp = preg_replace('/\(/', '', $class->class_content);
                $tmp = preg_replace('/\)/', '', $tmp);
                $tmp = preg_replace('/\s+/', '', $tmp);
                if ($parent->kind == 'abstract' and preg_match("/$parent->match/", $tmp) == false){
                    $abstract = true;
                    $match = $parent->match;
                }
            }
        }

        if($abstract){
            $class->kind = 'abstract';
            $class->match = $match;
        }
    }

    # get all children of class
    # argument is array of instances of classData
    public static function get_class_children($array){
        foreach($array as $item){
            if(count($item->parents) > 0){
                foreach($item->parents as $parent){
                    foreach($array as $item2){
                        if($item2->name == $parent->name) array_push($item2->children, $item);
                    }
                }
            }
        }
    }

    # load all class variables and save to array
    # argument is instance of classData
    public static function get_class_variables($class){
        $matches = array();
        $match_found = true;
        $tmp_string = $class->default_string;
        # get default variables
        foreach(type::$reg_types as $type){
            while($match_found){
                $pattern = "/$type".'\s+(*{0,1})(\w+);/';
                $match_found = false;
                if(preg_match($pattern, $tmp_string, $matches)){
                    $variable = new variable();
                    $variable->name = $matches[2];
                    $variable->type = preg_replace('\s+', ' ', $type);
                    if($matches[1]) $variable->is_pointer = true;
                    array_push($class->default_variables, $variable);
                    $tmp_string = preg_replace($pattern, '', $tmp_string, 1);
                    $match_found = true;
                    $matches = array();
                }
            }
        }

        # get public variables
        $tmp_string = $class->public_string;
        foreach(type::$reg_types as $type){
            while($match_found){
                $pattern = "/$type".'\s+(*{0,1})(\w+);/';
                $match_found = false;
                if(preg_match($pattern, $tmp_string, $matches)){
                    $variable = new variable();
                    $variable->name = $matches[2];
                    $variable->type = preg_replace('\s+', ' ', $type);
                    if($matches[1]) $variable->is_pointer = true;
                    array_push($class->public_variables, $variable);
                    $tmp_string = preg_replace($pattern, '', $tmp_string, 1);
                    $match_found = true;
                    $matches = array();
                }
            }
        }

        # get protected variables
        $tmp_string = $class->protected_string;
        foreach(type::$reg_types as $type){
            while($match_found){
                $pattern = "/$type".'\s+(*{0,1})(\w+);/';
                $match_found = false;
                if(preg_match($pattern, $tmp_string, $matches)){
                    $variable = new variable();
                    $variable->name = $matches[2];
                    $variable->type = preg_replace('\s+', ' ', $type);
                    if($matches[1]) $variable->is_pointer = true;
                    array_push($class->protected_variables, $variable);
                    $tmp_string = preg_replace($pattern, '', $tmp_string, 1);
                    $match_found = true;
                    $matches = array();
                }
            }
        }

        # get private variables
        $tmp_string = $class->private_string;
        foreach(type::$reg_types as $type){
            while($match_found){
                $pattern = "/$type".'\s+(*{0,1})(\w+);/';
                $match_found = false;
                if(preg_match($pattern, $tmp_string, $matches)){
                    $variable = new variable();
                    $variable->name = $matches[2];
                    $variable->type = preg_replace('\s+', ' ', $type);
                    if($matches[1]) $variable->is_pointer = true;
                    array_push($class->private_variables, $variable);
                    $tmp_string = preg_replace($pattern, '', $tmp_string, 1);
                    $match_found = true;
                    $matches = array();
                }
            }
        }

    }

    # TODO
    # argument is instance of classData
    public static function get_class_methods($class){
        # TODO
    }

    # this function parses input file and gets all data for current class and saves them to its obejct instance
    # argument $class is instance of classData, $array is array of instances of classData
    public static function parse_class_content($class, $array){
        $matches = array(); # tmp variable to store regex match results
        $tmp_content = $class->class_content; # tmp variable to store class sting content

        # get class name
        preg_match('/^(\w+)/', $tmp_content, $matches);
        $class->name = $matches[0];
        $tmp_content = preg_replace('/^(\w+)(\s*)/', '', $tmp_content, 1);

        # get class parents (classes it inherits from)
        if(preg_match('/^:/', $tmp_content)){
            $tmp_content = preg_replace('/^:(\s*)/', '', $tmp_content, 1);
            $matches = array();
            $i = 0;
            while(preg_match('/^(public|protected|private){0,1}(\s*)(\w+)(\s*),/', $tmp_content, $matches)){
                $class->parents[$i] = $matches[3];
                $tmp_content = preg_replace('/^(\w*)(\s*)(\w+)(\s*),(\s*)/', '', $tmp_content, 1);
                $matches = array();
                $i = $i + 1;
            }
            preg_match('/^(\w*)(\s*)(\w+)(\s*){/', $tmp_content, $matches);
            $class->parents[$i] = $matches[3];
            $tmp_content = preg_replace('/^(\w*)(\s*)(\w+)(\s*){(\s*)/', '', $tmp_content, 1);
        }
        else $tmp_content = preg_replace('/^{(\s*)/', '', $tmp_content, 1); # the class does not inherit

        # get parent classes' objects
        $tmp_parents = $class->parents;
        $class->parents = array();
        foreach($tmp_parents as $parent){
            $parent_found = false;
            $i = 0;
            while(!$parent_found and ($i < count($array))){
                if($array[$i]->name == $parent){
                    $parent_found = true;
                    array_push($class->parents, $array[$i]);
                }
                $i = $i + 1;
            }
        }

        # class body is empty -> no variables, no methods
        $default_string = '';
        $public_string = '';
        $protected_string = '';
        $private_string = '';
        if($tmp_content != ''){
            #get class properties
            #match default vars, save them
            $matches = array();
            if(preg_match('/^(.+)(;\s+public:\s*|;\s+protected:\s*|;\s+private:\s*|;\s*$)/', $tmp_content, $matches)) {
                $default_string = $matches[0];
                $default_string = preg_replace('/(\s+public:\s*|\s+protected:\s*|\s+private:\s*|\s*$)/', '', $default_string, 1);
            }

            #match public vars, save them
            $matches = array();
            if(preg_match('/\s*public:\s*(.+)(;\s+protected:\s*|;\s+private:\s*|;\s*$)/', $tmp_content, $matches)){
                $public_string = $matches[0];
                $public_string = preg_replace('/\s*public:\s*/', '', $public_string, 1);
                $public_string = preg_replace('/(\s+protected:\s*|\s+private:\s*|\s*$)/', '', $public_string, 1);
            }

            #match protected vars, save them
            $matches = array();
            if(preg_match('/\s*protected:\s*(.+)(;\s+public:\s*|;\s+private:\s*|;\s*$)/', $tmp_content, $matches)){
                $protected_string = $matches[0];
                $protected_string = preg_replace('/\s*protected:\s*/', '', $protected_string, 1);
                $protected_string = preg_replace('/(\s+public:\s*|\s+private:\s*|\s*$)/', '', $protected_string, 1);
            }

            #match private vars, save them
            $matches = array();
            if(preg_match('/\s*private:\s*(.+)(;\s+public:\s*|;\s+protected:\s*|;\s*$)/', $tmp_content, $matches)){
                $private_string = $matches[0];
                $private_string = preg_replace('/\s*private:\s*/', '', $private_string, 1);
                $private_string = preg_replace('/(\s+public:\s*|\s+protected:\s*|\s*$)/', '', $private_string, 1);
            }
        }
        $class->default_string = $default_string;
        $class->public_string = $public_string;
        $class->protected_string = $protected_string;
        $class->private_string = $private_string;
    }
}

# this class serves purposes of opening input and output files and checking if everything is allright
class fileHandling{
    # read all content from input file as string
    # argument is filename/filepath
    static function read_input_file($file){
        $input = @file_get_contents($file);
        if($input == false) printError("Zdrojovy soubor '$file' nelze cist.", 2);
        return $input;
    }

    # open output file for writing
    # argument is filename/filepath
    static function check_output_file($file){
        $output = @fopen($file, "w");
        if($output == false) printError("Zdrojovy soubor '$file' nelze otevrit.", 2);
        fclose($output);
    }
}

# this class stores all arguments passed to this script, as it is completely static, there is no need to create any instances
class params{
    static $params_count = NULL;
    static  # script parameters stored in variables
        $help = NULL,
        $input_file = NULL,
        $output_file = NULL,
        $details_set = NULL,
        $details_class = NULL,
        $pretty_xml = NULL,
        $search_xpath = NULL;

    # gets needed parameters from script's arguments
    static function get_params(){
        global $argv;
        $params = $argv;
        #remove script name from parameters, then check and save all parameters
        unset($params[0]);
        self::$params_count = count($params);
        foreach($params as $param){
            if($param == '--help'){
                if(self::$help){
                    printError('Chybne zadane argumenty skriptu, vicenasobny argument: '.$param, 1);
                }
                self::$help = true;
            }
            elseif(substr($param, 0, 8) == '--input='){
                if(self::$input_file){
                    printError('Chybne zadane argumenty skriptu, vicenasobny argument: '.$param, 1);
                }
                if(strlen($param) < 9) printError('Chybne zadane argumenty skriptu, neplatne zadany parametr --input=', 1);
                self::$input_file = substr($param, 8);
            }
            elseif(substr($param, 0, 9) == '--output='){
                if(self::$output_file){
                    printError('Chybne zadane argumenty skriptu, vicenasobny argument: '.$param, 1);
                }
                if(strlen($param) < 10) printError('Chybne zadane argumenty skriptu, neplatne zadany parametr --output=', 1);
                self::$output_file = substr($param, 9);
            }
            elseif(substr($param, 0, 9) == '--details'){
                if(self::$details_set){
                    printError('Chybne zadane argumenty skriptu, vicenasobny argument: '.$param, 1);
                }
                self::$details_set = true;
                if(strlen($param) == 10 or strlen($param) == 9) self::$details_class = false;
                else self::$details_class = substr($param, 10);
            }
            elseif(substr($param, 0, 12) == '--pretty-xml') {
                if(self::$pretty_xml){
                    printError('Chybne zadane argumenty skriptu, vicenasobny argument: '.$param, 1);
                }
                if(strlen($param) == 12 or strlen($param) == 13) self::$pretty_xml = 4;
                else self::$pretty_xml = (int)substr($param, 13);
            }
            elseif(substr($param, 0, 8) == '--search'){
                if(self::$search_xpath){
                    printError('Chybne zadane argumenty skriptu, vicenasobny argument: '.$param, 1);
                }
                if(strlen($param) < 10) printError('Chybne zadane argumenty skriptu, neplatne zadany parametr --search=XPATH', 1);
                self::$search_xpath = substr($param, 9);
                # TODO
                printError('Funkcionalita parametru --search=xpath neni implementovana. Pro vice informaci prosim nahlednete do dokumentace.', 125);
            }
            else{
                printError('Chybny argument skriptu: '.$param, 1);
            }
        }
    }

    # checks if script's arguments are correct
    static function check_params(){
        # print help
        if(self::$help){
            if(self::$params_count == 1) printHelp();
            else printError('Chybne zadane argumenty skriptu, kombinace parametru --help.', 1);
        }

        # number of parameters
        if(self::$params_count > 5){
            printError("Neplatny pocet argumentu skriptu.", 1);
        }

        # set default values to skript parameters if missing
        if(self::$input_file == NULL) self::$input_file = 'php://stdin';
        if(self::$output_file == NULL) self::$output_file = 'php://stdout';
        if(self::$details_set == NULL){self::$details_set = false; self::$details_class = false;}
        if(self::$pretty_xml == NULL) self::$pretty_xml = 4;
        if(self::$search_xpath == NULL) self::$search_xpath = false;
    }
}

/* Print children of class object in argument, recursively. */
function print_children($item){
    global $writer;
    if(count($item->children) > 0){
        foreach($item->children as $child){
            $child->already_print = true;
            $writer->startElement('class');
            $writer->writeAttribute('name', $child->name);
            $writer->writeAttribute('kind', $child->kind);
            print_children($child);
            $writer->endElement();
        }
    }
}

/* Print help message and exit the script. */
function printHelp(){
    fprintf(STDOUT, 'Tento skript pracuje s parametry:
--help Viz společné zadání všech úloh https://wis.fit.vutbr.cz/FIT/st/course-files-st.php/course/IPP-IT/projects/2015-2016/Zadani/proj2016.pdf
--input=file Vstupní textový soubor file, který obsahuje popis tříd jazyka C++ podle popsaných
omezení. Předpokládejte kódování ASCII. Chybí-li tento parametr, je uvažován standardní
vstup.
--output=file Výstupní soubor file ve formátu XML v kódování UTF-8. Není-li tento
parametr zadán, bude výstup vypsán na standardní výstup.
--pretty-xml=k Výstupní XML bude formátováno tak, že každé nové zanoření bude odsazeno
o k mezer oproti předchozímu. Není-li k zadáno, uvažujte k = 4. Pokud tento parametr není
zadán, je formátování výstupního XML volné (doporučujeme mít na každém řádku maximálně
jeden element).
--details=class Místo stromu dědičností mezi třídami se na výstup vypisují údaje o členech
třídy se jménem class. Formát je popsán výše. Pokud argument class není zadán, vypisují se
detaily o všech třídách v daném souboru, kde kořenem XML souboru je model. Pokud class
neexistuje, bude na výstup vypsána pouze XML hlavička.'."\n");
    exit(0);
}

/* Print error message with error code and exit the script. */
function printError($message, $code) {
    fprintf(STDERR, "ERROR: $message\nCODE: $code\n");
    exit($code);
}