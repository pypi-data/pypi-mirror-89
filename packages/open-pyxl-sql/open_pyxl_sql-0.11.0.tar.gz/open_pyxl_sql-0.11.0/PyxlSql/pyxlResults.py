# ---------------------------------------------------------------------------------------------------------------
# PyxlSQL project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini@gmail.com
# ---------------------------------------------------------------------------------------------------------------

from typing import Optional
import re
from PyxlSql.pyxlErrors import PyxlSqlError, PyxlSqlInternalError, PyxlSqlColumnError
from PyxlSql.pyxlAbstracts import Result, Index


class AddResult(Result):
    """Result with __add__"""

    def __init__(self):
        super().__init__()

    def __add__(self, other):
        list_a = self.get_all_env()
        list_b = other.get_all_env()
        if len(list_a) == 1 and len(list_b) == 1:
            a = EnvResult(to_copy=list_a[0])
            a.add_after(list_b[0])
            return a
        ab = [a + b for a in list_a for b in list_b]
        return GroupResult(all_env=ab)


class EnvResult(AddResult):
    """Results of FROM : a list if Index"""

    def __init__(self,
                 row: Optional[int] = None, sheet_arg=None,  # first method to initialize: with row and sheet_arg
                 to_copy: Optional[Result] = None,           # second method to initialize: with 1 EnvResult to copy
                 ):
        super().__init__()
        self.index_list: list[Index] = []
        self.sheet_to_row = {}
        self.signature = "EnvResult"
        if row and sheet_arg:
            self.add_index(Index(row, sheet_arg))
        if to_copy:
            list_of_indexes = to_copy.get_index_list()
            for index in list_of_indexes:
                self.add_index(index)

    def get_index_list(self):
        return self.index_list

    def add_index(self, item: Index):
        self.index_list.append(item)
        self.sheet_to_row[item.sheet_arg.get_sheet_name()] = item.row
        self.signature += item.signature

    def get_row(self, sheet) -> Optional[int]:
        sheet_name = sheet.get_sheet_name()
        if sheet_name in self.sheet_to_row:
            return self.sheet_to_row[sheet_name]
        raise ValueError

    def add_after(self, follower: Result):
        for item in follower.get_index_list():
            self.add_index(item)

    def get_all_env(self):
        return [self]

    def evaluate_expr(self, expr):
        return [expr.evaluate(self)]

    def get_field_value(self, field_arg):
        name, sheet = field_arg.find_name_and_sheet()
        try:
            dst_row = self.get_row(sheet)
        except ValueError:
            raise PyxlSqlInternalError("Sheet not found")

        if dst_row == -1:
            # in this case, this is a JOIN, and the value is NOT available
            return None
        assert isinstance(dst_row, int)
        return sheet.get_val(dst_row, name)

    def set_all_values(self, alias_table, eval_values):
        for var_name in alias_table.keys():
            full_name, field_arg = alias_table[var_name]
            value = self.get_field_value(field_arg)
            eval_values[full_name] = value if value else 0 if var_name[0] == '#' else ""
        return eval_values


class GroupResult(AddResult):
    """Results from a GROUP BY"""

    def __init__(self,
                 first: Optional[EnvResult] = None,           # first way to initialize: with only 1 item
                 all_env: Optional[list[EnvResult]] = None):
        super().__init__()
        self.outputs: list[Result] = []
        self.signature = "GroupResult"

        not first or self.append(first)
        if all_env:
            for env in all_env:
                self.append(env)

    def append(self, inputs: Result):
        self.outputs.append(inputs)
        self.signature += inputs.signature + " OR "

    def evaluate_expr(self, expr):
        return [item.evaluate_expr(expr)[0] for item in self.outputs]

    def get_all_env(self):
        return self.outputs

    def get_row(self, sheet):
        row_0 = self.outputs[0].get_row(sheet)
        if all(ele.get_row(sheet) == row_0 for ele in self.outputs[1:]):
            return row_0
        raise PyxlSqlError("UPDATE + GROUP BY", f"not all indexes for {sheet.get_sheet_name()} are identical")


class ValueResult(AddResult):
    """ Results from INTO
        for 1 database row, all values & formats set for each field
    """

    def __init__(self):
        super(ValueResult, self).__init__()
        self.values = {}
        self.fields = {}
        self.delayed = {}
        self.signature = "ValueResult"

    def set_value(self, field_arg, value):
        field_name = field_arg.get_full_name()
        self.values[field_name] = value
        self.fields[field_name] = field_arg

    def set_delayed(self, field_arg, value):
        field_name = field_arg.get_full_name()
        self.delayed[field_name] = value

    def get_field_value(self, field_arg):
        field_name = field_arg.get_full_name()
        if field_name not in self.values:
            raise PyxlSqlColumnError(field_name, "SET")    # TODO: improved error MSG, give a name to the ValueResult!
        return self.values[field_name]

    def execute_set(self, field_arg, dst_sheet, field_name, dst_row: int):
        full_field_name = field_arg.get_full_name()
        if full_field_name in self.values:
            new_value = self.get_field_value(field_arg)
        elif full_field_name in self.delayed:
            old_value = self.delayed[full_field_name]
            f = rf'\g<1>{str(dst_row)}\2'
            new_value = re.sub(r'([A-Z]{1,2})2((?!\w))', f, old_value)
        else:
            return  # There is no value assigned to this field

        dst_sheet.set_value(dst_row, field_name, new_value)

    def set_all_values(self, alias_table, eval_values):
        for var_name in alias_table.keys():
            full_name, _field = alias_table[var_name]
            val = self.values[full_name]
            eval_values[full_name] = val if val else 0 if var_name[0] == '#' else ""
        return eval_values
