# ---------------------------------------------------------------------------------------------------------------
# PyxlSQL project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini@gmail.com
# ---------------------------------------------------------------------------------------------------------------

import re
import string
from typing import Optional
from PyxlSql.pyxlErrors import PyxlSqlParseError, PyxlSqlExecutionError, PyxlSqlInternalError
from PyxlSql.pyxlSheets import NamedWS
from PyxlSql.pyxlAbstracts import Statement, Arg, Result


# -------------------------------------------------------------------------------------------------------------
# Actual Arg
# -------------------------------------------------------------------------------------------------------------


class ErrorArg(Arg):
    name = "ERROR"

    def __init__(self):
        super().__init__(None, "*ERROR*")


class CstArg(Arg):
    name = "CST"

    def __init__(self, command: Statement, spec: str):
        super().__init__(command, spec)

    def get_constant(self):
        return self.specification

    def verify_fields(self, not_in_src=False, not_in_dst=False):
        return


class SheetArg(Arg):
    name = "SHEET"

    def __init__(self, command: Statement, specification: str, sheet: NamedWS):
        super().__init__(command, specification)
        if command is None:
            self.sheet_number: int = -1  # will be asserted afterwards
        else:
            self.sheet_number: int = command.build_sheet_number()
        self.named_sheet: NamedWS = sheet
        self.sheet_name: str = sheet.title
        self.alias = None

    def add_alias(self, alias):
        self.alias = alias

    def get_sheet(self) -> NamedWS:
        return self.named_sheet

    def get_sheet_name(self) -> str:
        return self.specification

    def set_sheet_number(self, sheet_number: int):
        assert self.sheet_number == -1
        self.sheet_number = sheet_number

    def get_column_range(self):
        return self.named_sheet.get_column_range()

    def get_start_of_range(self):
        return self.named_sheet.get_start_of_range()

    def get_val(self, row: int, field: str):
        return self.get_sheet().get_val(row, field)

    # def set_value(self, row: int, field: str, value, number_format=None) -> None:
    #     return self.get_sheet().set_value(row, field, value, number_format)

    def get_columns(self):
        return self.get_sheet().columns


class FieldArg(Arg):
    name = "Field"

    def __init__(self, command: Statement, field_descriptor: str):
        super().__init__(command, field_descriptor)
        # Format of the Field name may be:
        #       'field name' only, if no ambiguity
        #       '(@|#)N{field name}', if there is an ambiguity, or
        #       '(@|#)alias{field name},
        self.field_descriptor = field_descriptor        # The initial string BEFORE parsing
        self.my_sheet_arg: Optional[SheetArg] = None
        self.field_name = field_descriptor
        self.full_name = None

    @staticmethod
    def normalise(name: str):
        """returns a name usable for a variable, and unique"""
        res = ""
        for c in name:
            res += c if c in string.ascii_letters + string.digits + '_' else '_' + hex(ord(c)) + '_'
        return res

    def get_full_name(self):
        if self.full_name is None:
            field_name, sheet_arg = self.find_name_and_sheet()
            loc_type = "Number_" if self.field_descriptor[0] == '#' else 'String_'
            if sheet_arg is None:
                raise PyxlSqlInternalError('get_full_name(None)')
            self.full_name = loc_type + self.normalise(sheet_arg.get_sheet_name()+'__F__'+field_name)
        return self.full_name

    def find_name_and_sheet(self, not_in_src=False, not_in_dst=False):  # Str, NamedWS
        """returns self.field_name, self.sheet after parsing the field descriptor"""
        return self.field_name, self.my_sheet_arg

    def verify_fields(self, not_in_src=False, not_in_dst=False):
        """sets self.field_name, self.sheet after parsing the field descriptor"""
        if self.my_sheet_arg:
            return

        assert not (not_in_src and not_in_dst)

        tt = re.match(r'[@#](\d+){([^}]+)}', self.field_descriptor)
        if tt:
            self.field_name = tt.group(2)
            sheet_nb = int(tt.group(1))
            if sheet_nb == 0:
                self.my_sheet_arg = self.command.dst_sheet_arg
            elif sheet_nb > len(self.command.source_sheets):
                raise PyxlSqlParseError(f"sheet number too high '{sheet_nb}'", self.field_descriptor)
            else:
                self.my_sheet_arg = self.command.source_sheets[sheet_nb - 1]

            if not isinstance(self.my_sheet_arg, SheetArg):
                raise PyxlSqlParseError(f'illegal sheet number {sheet_nb}', self.field_descriptor)

            if self.field_name not in self.my_sheet_arg.get_columns():
                raise PyxlSqlParseError(f"Illegal field name '{self.field_descriptor}'",
                                        self.my_sheet_arg.get_sheet_name())
            return

        tt = re.match(r'[@#](\w+){([^}]+)}', self.field_descriptor)
        if tt:
            self.field_name = tt.group(2)
            sheet_alias = tt.group(1)
            self.my_sheet_arg = self.command.sheet_from_alias(sheet_alias, not_in_src=not_in_src, not_in_dst=not_in_dst)

            if not isinstance(self.my_sheet_arg, SheetArg):
                raise PyxlSqlParseError(f"illegal sheet alias '{sheet_alias}'", self.field_descriptor)

            if self.field_name not in self.my_sheet_arg.get_columns():
                raise PyxlSqlParseError(f"Illegal field name '{self.field_descriptor}'",
                                        self.my_sheet_arg.get_sheet_name())
            return

        self.field_name = self.field_descriptor  # The only remaining solution
        all_sheets = [] if not_in_dst else [self.command.dst_sheet_arg]
        all_sheets += [] if not_in_src else self.command.source_sheets

        for sheet_arg in all_sheets:
            s = sheet_arg.get_sheet()
            if self.field_name in s.columns:
                if self.my_sheet_arg:
                    raise PyxlSqlParseError(f"Ambiguous field name '{self.field_descriptor}'",
                                            f" between '{s.title}' and '{self.get_sheet_name()}'")
                self.my_sheet_arg = sheet_arg
        if self.my_sheet_arg is None:
            raise PyxlSqlParseError(f"Illegal field name '{self.field_descriptor}'", "")
        return

    def evaluate(self, inputs: Result):
        return inputs.get_field_value(self)

    def get_constant(self):
        return self.field_name

    def get_sheet_name(self):
        return self.my_sheet_arg.get_sheet_name()


class ExprArg(Arg):
    name = "Expr"

    def __init__(self, command: Statement, expr: str):
        super().__init__(command, expr)

        self.alias_table = {}
        self.eval_values = {}
        self.expression = expr
        self.build_aliases()

        self.compiled = compile(self.expression, '<string>', 'eval')
        # TODO: trap compile errors

    def verify_fields(self, not_in_src=False, not_in_dst=False):
        return  # already done in build_aliases
        # expr_vars = re.findall(r'([#@]\d*{[\w\s_-]*})', self.expression)
        # for var in expr_vars:
        #     field = FieldArg(self.command, var)
        #     field.verify_fields(not_in_src, not_in_dst)

    # def set_eval_values(self, row_nb: int, alias_table, eval_values, header: str):
    #     for v in alias_table:
    #         column_name = v[3:-1]
    #         if v[1] != header:
    #             continue
    #         val = self.get_val(row_nb, column_name) if row_nb != -1 else None  # None for failing JOINs
    #
    #         var_name = alias_table[v]
    #         eval_values[var_name] = val or (0 if v[0] == '#' else "")
    #
    #     return eval_values

    def rename_vars(self):
        """Renames all the column names contained in the expression by a variable name
        the column name must be enclosed by @n{} of #n{}, where n is the sheet index, i.e.
        0 for the destination
        1 etc for the source sheets, in increasing order
        @ for strings
        # for numbers
        It is preferable to 'type' the variables, because the conventions for 'empty cell'
        for excel: empty is 0 or ""
        when for python, empty is None, and None cannot be part of expressions with strings or numbers

        also removes the heading ':= '
        """
        if self.expression[0:3] == ":= ":
            self.expression = self.expression[3:]

        expr_vars = re.findall(r'([@#]\w+{[^}]+})', self.expression)

        for field_name in expr_vars:
            if field_name in self.alias_table:
                continue  # because the same variable can occur 2 times in the same expression

            field_arg = FieldArg(self.command, field_name)
            field_arg.verify_fields()
            alias = field_arg.get_full_name()

            self.expression = self.expression.replace(field_name, alias)
            self.alias_table[field_name] = alias, field_arg
            self.eval_values[alias] = None

    def build_aliases(self):
        #  {Variable names} are fields in the excel sheet, so do not follow the Python naming convention
        #  So we create an Alias for each variable, 'Int_0123' etc.
        #  The Alias replaces {Variable name} inside the expression
        #  A dictionary is also built, it will be used for the execution of the clause
        #  The dictionary is populated with variable values for each line

        self.rename_vars()

        # verify no remaining fields
        variables = re.findall(r'{([^}]*)}', self.expression)
        if variables:
            msg = " unknowns = "
            for v in variables:
                msg += v + ', '
            raise PyxlSqlParseError("unknown variable in expression", msg)
            # TODO: build a test case

    def evaluate(self, inputs: Result):
        """Evaluates self.compiled in the environment of inputs"""
        for f in self.eval_values.keys():
            self.eval_values[f] = None
        self.eval_values = inputs.set_all_values(self.alias_table, self.eval_values)

        for k, v in self.command.dst_wb.imported.items():
            # here, we get the modules that were imported dynamically
            # this list can change over execution, and the eval_values is different for each clause
            self.eval_values[k] = v
        try:
            value = eval(self.compiled, None, self.eval_values)
            return value
        except NameError as err:
            raise PyxlSqlExecutionError(f"Evaluating Python expression '{self.expression}'", str(err))
        except TypeError as err:
            raise PyxlSqlExecutionError(f"Type error evaluating Python expression '{self.expression}'", str(err))

    def find_name_and_sheet(self, not_in_src=False):
        return None, None


class AggregateExprArg(ExprArg):
    name = "Aggregate Expr"

    def __init__(self, command: Statement, expr: str):
        super().__init__(command, expr)

    def build_aliases(self):
        """Builds the list of variable names for the expression,
        replacing each @$0 etc by a variable name"""

        if self.expression[0:3] == "$= ":
            self.expression = self.expression[3:]
        else:
            raise PyxlSqlParseError("Reduce expression must start with '$= '", self.expression)

        expr_vars = re.findall(r'([#@]\$\d*)', self.expression)

        for v in expr_vars:
            if v in self.alias_table:
                continue  # because the same variable can occur 2 times in the same expression
            loc_type = "_Number_" if v[0] == '#' else '_String_'
            alias = 'sheet_aggregate_' + loc_type
            self.expression = self.expression.replace(v, alias)
            self.alias_table[v] = alias
            self.eval_values[alias] = None

    def set_aggregate_values(self, results_list: list):
        for v in self.alias_table:
            var_name = self.alias_table[v]
            self.eval_values[var_name] = results_list or (0 if v[0] == '#' else "")

    def eval_reduce(self, results_list: list):
        self.set_aggregate_values(results_list)

        for k, v in self.command.dst_wb.imported.items():
            # here, we get the modules that were imported dynamically
            # this list can change over execution, and the eval_values is different for each clause
            self.eval_values[k] = v

        try:
            value = eval(self.compiled, None, self.eval_values)
        except NameError as err:
            raise PyxlSqlExecutionError(f"Name not defined in evaluating Python '{self.expression}'", str(err))

        for v in self.eval_values.keys():
            self.eval_values[v] = None
        return value


class FormulaArg(Arg):
    name = "Formula"

    def __init__(self, command: Statement, formula: str):
        super().__init__(command, formula)
        self.formula = formula

    def evaluate(self, _inputs: Result):
        return self.formula

    def verify_fields(self, not_in_src=False, not_in_dst=False):
        expr_vars = re.findall(r'([#@]\d*{[\w\s_-]*})', self.formula)
        for var in expr_vars:
            raise PyxlSqlParseError(f"field name {var}", "Excel expression")

    def find_name_and_sheet(self, not_in_src=False):
        return None, None  # FIXME: To be verified
