# ---------------------------------------------------------------------------------------------------------------
# PyxlSQL project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini@gmail.com
# ---------------------------------------------------------------------------------------------------------------


# how to get openpyxl, pytest etc
# shell>python -m pip install --upgrade openpyxl pytest setuptools wheel tox pytest-flakes pytest-cov sphinx gitpython

# how to test: (cf tox.ini, which does everything)
# (venv) PyxlSQL> pyxlSql -f tests/Test_pyxlsql.xlsx
# (venv) PyxlSQL> pytest --cache-clear --ff
# (venv) PyxlSQL> pytest --flakes
# (venv) PyxlSQL> pytest --cov --cov-report html --cov-report term
# (venv) PyxlSQL> sphinx-build source build/html -W -b html
# or:
# (venv) PyxlSQL> tox


import argparse
import os
import re
from typing import Optional
from PyxlSql.pyxlErrors import PyxlSqlError
from PyxlSql.pyxlSheets import NamedWS, NamedWB
from PyxlSql.pyxlEngine import Statement
from PyxlSql.pyxlGrammar import Parser

# ----------------------- General behavior
# REQ 0001: PyxlSQL uses openPyxl to read excel files
# REQ 0002: PyxlSQL statements are stored 'Pyxl SQL' sheet
# REQ 0003: Sheet are described as 'sheet name' or 'filename.xlsx[sheet name]'
# TODO: remove start/trailing spaces for Command, Clause, field names, it is a common error, hard to find

# ----------------------- Cmdline arguments
# REQ 1001: --dir/-d directory: processes all excel files in the directory
# REQ 1002: --file/-f file (multiple times): process this file
# REQ 1003: --filepath/-p dir (multiple times): adds directory to path for included excel files
# REQ 1004: the directory of the file being processed is added in the filepath


# ----------------------- Commands
# REQ 2001: Command "SELECT INTO" dst_sheet "FROM" src_sheet (FIELD, WHERE)
# SELECT INTO adds a FORMULA and a FORMAT clause if the 1st data line is filled with examples, then erases this line

# REQ 2002: Command "LEFT JOIN" dst_sheet "FROM" src_sheet (FIELD, ON)
# REQ 2003: Command "RIGHT JOIN" dst_sheet "FROM" src_sheet (FIELD, ON)
# REQ 2004: Command "DELETE" dst_sheet
#           Behavior : remove a sheet, e.g. the Micro SQL sheet
# REQ 2005: Command "SAVE" filename
#           Behavior: file saved is writen with the same directory than the original file
# TODO: REQ 2006: Command "SAVE" workbook "AS" filename
# REQ 2007: Command "IMPORT" module
# REQ 2008: Command "IMPORT" module "SUBS" sub modules
#           Behavior: allows to use more features in the EXPRESSION clauses
# REQ 2009: Command "UPDATE" dst_sheet (FIELD, EXPRESSION, FORMULA, FORMAT)

# HOW TO do a multiple stages approach
# because *Excel* formulas are evaluated when the file is loaded by openPyxl
# if the values of *newly inserted* formulas are required by PyxlSQL,
# then it is necessary to reload the file
# how to do it:
#       several PyxlSQL sheets store multiple stages: "Pyxl SQL", "Pyxl SQL 2" etc
#       DELETE "Pyxl SQL"
#       RENAME "Pyxl SQL 2" AS "Pyxl SQL"
#       SAVE "initial_file_stage_2"
#       LOAD "initial_file_stage_2" will load the file with formulas computed, and execute
# TODO: REQ 2010: Command "RENAME" sheet "AS" new_name
# TODO: REQ 2011: Command "LOAD" filename: loads file, and executes it.
# TODO: REQ 2012: Command "INSERT" sheet "AS" new_field
# TODO: REQ 2013: Command "INNER JOIN" dst_sheet "FROM" src_sheet (FIELD, ON)
#       behavior: see https://www.w3schools.com/sql/sql_join_inner.asp


# ----------------------- Clauses
# REQ 3000: Clause "FIELD" dst_field "IS" src_field (WHEN)
# REQ 3001: Clause "FIELD" dst_field "IS" src_expression (WHEN)
# REQ 3002: SubClause "WHEN" dst_field "EQUALS" src_field
# TODO: REQ 3004: SubClause "WHEN" dst_expr "EQUALS" src_expr
# TODO: REQ 3003: SubClause "HAVING" s.expr name red_expr
#       where: red_expr is a reduction expression, ex
# REQ 3010: Clause "WHERE" python_expression : if expression evaluates to True, the command is executed
# REQ 3011: Clause "ON" dst_field "IS" src_field: specify the rows where the LEFT JOIN command is executed
# TODO: REQ 3012: Clause "ON" dst_expression "IS" src_expression: evaluates its arguments
# REQ 3013: Clause "EXPRESSION" field "IS" example
# REQ 3014: Clause "FORMULA" field "IS" example
# REQ 3015: Clause "FORMAT" field "IS" example
# TODO: REQ 3016: Clause "UNIQUE ID" field IS template
# TODO: REQ 3017: Clause "GROUP BY" field
#       Behavior: a clause from a SELECT INTO or JOIN xxx command, where several lines match the condition
#       lines are grouped together depending on the field
#       other fields must be aggregated with a
#       Example:
#       SELECT INTO
# TODO: REQ 3018: Clause "GROUP BY" expression(t,s)
# TODO: Trouver un moyen

# ----------------------- Error generation

# TODO: Add an error "clause without command", and a test for it
# TODO: test if clause is accepted by Cmd, and generate an error otherwise

# TODO: Validate all Sheets, and Fields before Exec
# TODO: Do the verifications in 1st pass, executions in 2nd pass
# TODO: Trap execution errors in Exec()


# ----------------------- Testing
# cf https://openpyxl.readthedocs.io/en/stable/development.html#coding-style
# DONE: run tests using pytest
# DONE: use tox to tests code for different submissions
# TODO: use the python pympler package to profile the memory usage
# DONE: Use pytest as the tests runner with pytest-cov for coverage information
# DONE: Use pytest-flakes for static code analysis.

# TODO: test case for PyxlSqlSheetError
# TODO: test case for PyxlSqlCellError
# TODO: test case for PyxlSqlExecutionError
# TODO: test case for "too much errors"

# TODO: Test case for EXPRESSION with a reference to a formula in a cell
# TODO: test case for RIGHT JOIN

# ----------------------- Bugs
# DONE: remove pytest-cov warning for PyxlSqlInternalError

# ---------------------------------------------------------------------------------------------------
# class SqlWb
# ---------------------------------------------------------------------------------------------------


class SqlWb(NamedWB):
    column_names = 'STATEMENT', 'First', 'KEY', 'Second', 'CONDITION', 'Third'
    sql_sheet_name = 'Pyxl SQL'

    def __init__(self, file_name, file_path=None):
        super().__init__(file_name, file_path=file_path)
        self.parser = Parser()
        self.parse_commands()

    def parse_commands(self):
        current_command: Optional[Statement] = None
        active_sheet: NamedWS = self.get_sheet(SqlWb.sql_sheet_name, raise_except=False)
        if active_sheet is None:
            PyxlSqlError.warning(f"file '{self.filename}' does not hold any '{SqlWb.sql_sheet_name}' sheet")
            return

        for row in active_sheet.get_row_range():
            word = active_sheet.get_val(row, self.column_names[0])
            if word is None:
                if current_command is not None and current_command.is_a_command():
                    try:
                        current_command.execute()
                    except PyxlSqlError as error:
                        error.print("Executing")
                current_command = None
                continue

            values = []
            cells = []
            for param in self.column_names[1:]:
                val = active_sheet.get_val(row, param)
                cell = active_sheet.get_cell(row, param)
                if val is None:
                    break
                values.append(val)
                cells.append(cell)

            PyxlSqlError.set_line(self.filename + ':[' + SqlWb.sql_sheet_name + ']', row, [word]+values)
            try:
                new_item = self.parser.parse(active_sheet, [word]+values, cells)
            except PyxlSqlError as current_error:
                current_error.print()
                continue

            if new_item.is_a_command():
                if current_command is not None and current_command.is_a_command():
                    current_command.execute()
                current_command = new_item

        if current_command is not None and current_command.is_a_command():
            current_command.execute()


# ------------------------------------------------------------
# Class PyxlSqlCmdLine
# ------------------------------------------------------------


class PyxlSqlCmdLine:
    def __init__(self, arguments=None):
        self.parser = argparse.ArgumentParser(description='execute PyxlSql commands in Excel files')
        self.parser.add_argument('--filepath', '-p', help="path for included files", type=str, action='append')
        self.parser.add_argument('--files', '-f', help="(multiple times): process this file",
                                 type=str, dest='files', action='append')
        self.parser.add_argument('--dir', '-d', help="process all excel files in the directory",
                                 type=str, dest='dir', action='store')

        self.parser.add_argument('--licence', help="prints the LICENCE", action='store_true')
        self.parser.add_argument('--full-help', help="prints the complete help, and exits", action='store_true')
        self.parser.add_argument('--parse-only', help="parse PyxlSql commands, verifies syntax only, and exits",
                                 action='store_true')

        self.args = self.parser.parse_args() if arguments is None else self.parser.parse_args(arguments)

        d = self.args.dir or "."
        self.dir = d if d[-1] == "/" or d[-1] == '\\' else d+"/"
        file_path = self.args.filepath or [self.dir]
        self.file_path = list(map(lambda f: f if f[-1] == "/" or f[-1] == '\\' else f+"/", file_path))
        self.files = self.args.files or list(map(lambda f: self.dir + f, os.listdir(self.dir)))

    def run(self):
        for existing_file in self.files:
            if os.path.isfile(existing_file) and re.match(r".*\.xls(x|m|)$", existing_file):
                SqlWb(existing_file, file_path=self.file_path)

    def run_first(self):
        """Used for tests with pytest"""
        for existing_file in self.files:
            if os.path.isfile(existing_file) and re.match(r".*\.xls(x|m|)$", existing_file):
                return SqlWb(existing_file, file_path=self.file_path)
        raise PyxlSqlError("No file to process", '{' + self.files[0] + '}')


if __name__ == "__main__":
    cmdline = PyxlSqlCmdLine()
    cmdline.run()
