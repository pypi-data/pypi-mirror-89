import glob
import itertools
import os
import shutil
import sys
import zipfile
import difflib
import configparser


class ListOfTypeError(TypeError):
    pass


class Zip:
    def __init__(self,
                 main_file: str,
                 name="by file",
                 glob_pattern: str = "*",
                 glob_recursive=False,
                 cmd_file="by name or by file (with file extension)",
                 python_exe="py",
                 with_print=True):
        """
        :param main_file: the main file would be run with the cmd file
        :param name: you can leave empty, default value is the name of your main file without extension

        :param glob_pattern:the glob patterns for search the files to the zip
        the glob patterns split by comma (example:*.py,*.ini,data/*)
        :param glob_recursive:set the recursive for the glob function,this is only to python 3.5+

        :param cmd_file:the name of cmd,(like run.cmd or play.bat),in default it will be name of file
        :param python_exe:the python name who can access from the command-line.
        """

        self.main_file = main_file

        self.glob = glob_pattern
        self.glob_recursive = glob_recursive

        self.python_exe = python_exe

        if with_print == "0" or with_print == "1":
            with_print = int(with_print)

        self.with_print = with_print
        if name == "by file":
            self.main_name = os.path.splitext(main_file)[0]
        else:
            self.main_name = name
        ##################################
        if cmd_file == "by name or by file (with file extension)":
            self.cmd_file = self.main_name + ".cmd"
        else:
            self.cmd_file = cmd_file

    def _create_cmd(self):
        """create the cmd file"""
        cmd = f"""@echo off\n{self.python_exe} \"{self.main_name}-src\\{self.main_file}\" @echo off"""

        with open(self.cmd_file, "w") as cmd_file_io:
            cmd_file_io.write(cmd)
        if self.with_print:
            print("done create command file")

    def create_zip(self):
        """create zip with glob and raise FileNotFoundError if the main_file not found in glob"""
        self._create_cmd()
        if os.path.exists(self.main_name):
            shutil.rmtree(self.main_name)

        if os.path.exists(self.main_name + ".zip"):
            os.remove(self.main_name + ".zip")

        names = self._find_names()
        names = list(itertools.chain.from_iterable(names))
        if self.main_file not in names:
            raise FileNotFoundError("the main_file \"{}\" not not found in glob list".format(self.main_file))

        with zipfile.ZipFile(self.main_name + ".zip", "w") as zip_ref:
            for file in names:
                zip_ref.write(file, self.main_name + "-src\\" + file)
            zip_ref.write(self.cmd_file)
            os.remove(self.cmd_file)
        if self.with_print:
            print("done create zip from files and folders:", ",".join(names))

    def _find_names(self):
        """
        :return: list of file using glob
        """
        globs = self.glob.split(",")
        if len(globs) > 0:
            # ############################ find files name

            files_list = []
            for g in globs:
                if sys.version_info[0] >= 3 and sys.version_info[1] >= 5:
                    # if python version is above or equal to 3.5 (for glob recursive )
                    files_list.append(glob.glob(g, recursive=self.glob_recursive))
                else:
                    files_list.append(glob.glob(g))
            # ########################### files filter
            return files_list


def by_config(config_dict):
    """
    auto create zip,if there was unexpected keyword it try to find the similar word to keyword.
    :param config_dict: dictionary of values for the Zip class
    """

    try:
        Zip(**config_dict).create_zip()
    except TypeError as type_error:

        if "__init__() got an unexpected keyword argument" in str(type_error):
            pattern = "Zip got an unexpected keyword argument \"{}\". "
            real_values = "main_file,name,glob_pattern,glob_recursive,cmd_file,python_exe,with_print".split(",")
            error_list = []
            for key in config_dict.keys():
                if key not in real_values:
                    d = difflib.get_close_matches(key, real_values)
                    if d:
                        s = TypeError((pattern + "Did you mean \"{}\"?").format(key, d[0]))
                    else:
                        s = TypeError(pattern.format(key))
                    error_list.append(s)
                    # print("append",s)

            raise ListOfTypeError(error_list)
        else:
            raise type_error


def _parse_cmd_argev(args):
    """this is for cmd command"""
    if not args:
        raise TypeError("you need to type the filename after the command")
    conf = configparser.ConfigParser()
    conf.read(args[0])
    by_config(dict(conf.items('settings')))


if __name__ == '__main__':
    z = Zip(main_file="py_to_zip.py",  # the main file would be run with the cmd file
            name="py-to-zip",  # the name of project,in default("by file") it will be name of file
            glob_pattern="*.py,data\\**\\*.txt",  # the glob patterns for search the files to the zip
            glob_recursive=True,  # set the recursive for the glob function,this is only to python 3.5+
            cmd_file="czip.bat",  # the name of cmd file,(like run.cmd or play.bat),in default it will be name of file
            python_exe="py")  # the python.exe name who can access from the command-line.
