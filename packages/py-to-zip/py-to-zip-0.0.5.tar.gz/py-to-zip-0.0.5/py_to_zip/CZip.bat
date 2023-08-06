@echo off
python -c "from py_to_zip.py_to_zip import _parse_cmd_argev;_parse_cmd_argev('%*'.split())"
@echo on