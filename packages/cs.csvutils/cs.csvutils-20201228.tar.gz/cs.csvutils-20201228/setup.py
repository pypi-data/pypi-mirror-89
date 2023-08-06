#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.csvutils',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20201228',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'CSV file related facilities',
  long_description =
    ('Utility functions for CSV files.\n'    
 '\n'    
 '*Latest release 20201228*:\n'    
 'Python 3 csv_reader new a generator.\n'    
 '\n'    
 'In python 2 the stdlib CSV reader reads 8 bit byte data and returns str '    
 'objects;\n'    
 'these need to be decoded into unicode objects.\n'    
 'In python 3 the stdlib CSV reader reads an open text file and returns str\n'    
 'objects (== unicode).\n'    
 'So we provide `csv_reader()` generators to yield rows containing unicode.\n'    
 '\n'    
 '## Function `csv_import(fp, class_name=None, column_names=None, '    
 'computed=None, preprocess=None, mixin=None, **kw)`\n'    
 '\n'    
 'Read CSV data where the first row contains column headers.\n'    
 'Returns a row namedtuple factory and an iterable of instances.\n'    
 '\n'    
 'Parameters:\n'    
 '* `fp`: a file object containing CSV data, or the name of such a file\n'    
 '* `class_name`: optional class name for the namedtuple subclass\n'    
 '  used for the row data.\n'    
 '* `column_names`: optional iterable of column headings; if\n'    
 '  provided then the file is not expected to have internal column\n'    
 '  headings\n'    
 '* `computed`: optional keyword parameter providing a mapping\n'    
 '  of str to functions of `self`; these strings are available\n'    
 '  via __getitem__\n'    
 '* `preprocess`: optional keyword parameter providing a callable\n'    
 '  to modify CSV rows before they are converted into the namedtuple.\n'    
 '  It receives a context object and the data row. It may return\n'    
 '  the row (possibly modified), or None to drop the row.\n'    
 '* `mixin`: an optional mixin class for the generated namedtuple subclass\n'    
 '  to provide extra methods or properties\n'    
 '\n'    
 'All other keyword parameters are passed to csv_reader(). This\n'    
 'is a very thin shim around `cs.mappings.named_column_tuples`.\n'    
 '\n'    
 'Examples:\n'    
 '\n'    
 "      >>> cls, rows = csv_import(['a, b', '1,2', '3,4'], "    
 "class_name='Example_AB')\n"    
 '      >>> cls     #doctest: +ELLIPSIS\n'    
 '      <function named_row_tuple.<locals>.factory at ...>\n'    
 '      >>> list(rows)\n'    
 "      [Example_AB(a='1', b='2'), Example_AB(a='3', b='4')]\n"    
 '\n'    
 "      >>> cls, rows = csv_import(['1,2', '3,4'], class_name='Example_DEFG', "    
 "column_names=['D E', 'F G '])\n"    
 '      >>> list(rows)\n'    
 "      [Example_DEFG(d_e='1', f_g='2'), Example_DEFG(d_e='3', f_g='4')]\n"    
 '\n'    
 '## Function `csv_reader(arg, *a, **kw)`\n'    
 '\n'    
 'Read the file `fp` using csv.reader.\n'    
 '`fp` may also be a filename.\n'    
 'Yield the rows.\n'    
 '\n'    
 'Warning: _ignores_ the `encoding` and `errors` parameters\n'    
 'because `fp` should already be decoded.\n'    
 '\n'    
 "## Function `csv_writerow(csvw, row, encoding='utf-8')`\n"    
 '\n'    
 'Write the supplied row as strings encoded with the supplied `encoding`,\n'    
 "default 'utf-8'.\n"    
 '\n'    
 '## Function `xl_import(workbook, sheet_name=None, skip_rows=0, **kw)`\n'    
 '\n'    
 'Read the named `sheet_name` from the Excel XLSX file named\n'    
 '`filename` as for `csv_import`.\n'    
 'Returns a row namedtuple factory and an iterable of instances.\n'    
 '\n'    
 'Parameters:\n'    
 '* `workbook`: Excel work book from which to load the sheet; if\n'    
 '  this is a str then the work book is obtained from\n'    
 '  openpyxl.load_workbook()\n'    
 '* `sheet_name`: optional name of the work book sheet\n'    
 '  whose data should be imported;\n'    
 '  the default (`None`) selects the active worksheet\n'    
 '\n'    
 'Other keyword parameters are as for cs.mappings.named_column_tuples.\n'    
 '\n'    
 'NOTE: this function requires the `openpyxl` module to be available.\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20201228*:\n'    
 'Python 3 csv_reader new a generator.\n'    
 '\n'    
 '*Release 20191118*:\n'    
 'xl_import: make sheet_name parameter optional with useful default\n'    
 '\n'    
 '*Release 20190103*:\n'    
 'Documentation updates.\n'    
 '\n'    
 '*Release 20180720*:\n'    
 'csv_import and xl_import function to load spreadsheet exports via '    
 'cs.mappings.named_column_tuples.\n'    
 '\n'    
 '*Release 20170608*:\n'    
 'Recode using new simpler cs.sharedfile.SharedAppendLines.\n'    
 '\n'    
 '*Release 20160828*:\n'    
 '* Update metadata with "install_requires" instead of "requires".\n'    
 '* Python 2 and 3 portability fixes.\n'    
 '* Assorted minor improvements.\n'    
 '\n'    
 '*Release 20150116*:\n'    
 'Initial PyPI release.'),
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  install_requires = ['cs.deco', 'cs.logutils', 'cs.mappings', 'cs.pfx'],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.csvutils'],
)
