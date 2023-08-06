# py-to-zip


py-to-zip is a Python library for distributing Python files. It creates a 
zip file and a command file from your python code. The result is a zip file 
that includes the source python files and a file that can be 
double-clicked in order to run the main python file. The receiving computer 
should have Python installed and in PATH, but it is not necessary for the receiver 
to open a python IDE or a command line window.  

py-to-zip runs in Python 3+ and only in Windows. The receiving computer can 
have all Python versions if your source code supports them.

## Instructions
You need to make a settings.ini file like this:


```ini
[settings]
main_file=main.py
# The main file that would be run with the cmd file
name=name of project
# You can leave empty, default value is the name of your main file without extension
glob_pattern=*.py,data/*.png,data/**/*.txt
# The glob patterns for all the files to add the zip, separated by commas. 
# Use ** only if using python 3.5 and higher. make sure that it includes your 
# main file as well. 
glob_recursive=1 
# Optional. Set the recursive variable for the glob function,
# this is only for python 3.5+. If python version is lower, ignores this value.
cmd_file=command.bat
# The name of command file,(like run.cmd or play.bat)
# By default it will be <main_file>.cmd
python_exe=py
# The python command that is to be run on receiving computer (py,python,python3,...)
```
**Important:** The main file must be found by glob using the pattern glob_pattern.

To create zip from ini using command line:
```
czip {your ini file}
# or
CZip.bat {your ini file}
# for example:
czip settings.ini
```
And the py-to-zip creates the zip that includes source and command file 
automatically in the current folder.

### Access from python
To access the py-to-zip from a python file:
```python
from py_to_zip.py_to_zip import by_config

# create ini parameters in python code

by_config(
    dict(main_file="py_to_zip.py", 
         name="py-to-zip", 
         glob_pattern="*.py,data\\**\\*.txt",
         glob_recursive=True, 
         cmd_file="czip.bat", 
         python_exe="py",
         )
)
```
And the py-to-zip creates the zip that includes source and command file 
automatically in the current folder, without additional command line commands.

## Installation

To install with pip - type in terminal:
```
(python -m) pip install py_to_zip
```
## Additional options
Additional options when calling from Python file:
```python
from py_to_zip.py_to_zip import Zip
z= Zip(
         main_file = "py_to_zip.py",  
         name = "py-to-zip", 
         glob_pattern = "*.py,data\\**\\*.txt",
         glob_recursive = True,  
         cmd_file = "czip.bat",  
         python_exe = "py",
         with_print = True or False,
        # if set to False,py-to-zip will not print anything.
        # this can be used also in INI file
)

#to do the same as before you can use the command:
z.create_zip()
#but you can also acsess
z._find_names() #to find names of file with glob
z._create_cmd() #to create the cmd script
### or alternatively
from py_to_zip.py_to_zip import _parse_cmd_argev 
_parse_cmd_argev(["file.ini"])#exactly likce czip {your ini file}
```

## Author

matan h

## License

This project is licensed under the MIT License.

## created by

This library was created and uploaded using [libtool](https://github.com/matan-h/libtool)
