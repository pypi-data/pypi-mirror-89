from py_to_zip.py_to_zip import by_config

__title__ = 'py_to_zip'
__description__ = 'libtool is a library for creating a zip with command file from python files.'
__url__ = 'https://github.com/matan-h/czip'
__version__ = '0.0.5'
__author__ = 'matan h'
__author_email__ = 'matan.honig2@gmail.com'
__license__ = 'MIT'
if __name__ == "__main__":
    # you can add ini Directly to function
    by_config(
        dict(main_file="py_to_zip.py",
             name="py-to-zip",
             glob_pattern="*.py,*.bat,*.txt",
             cmd_file="CZip.bat",
             python_exe="py")
    )
