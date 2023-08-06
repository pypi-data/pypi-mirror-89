# ---------------------------------------------------------------------------------------------------------------
# PyxlSQL project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini@gmail.com
# ---------------------------------------------------------------------------------------------------------------
from typing import Optional
from PyxlSql.pyxlErrors import PyxlSqlParseError, PyxlSqlInternalError
from PyxlSql.pyxlSheets import NamedWS, NamedWB
from PyxlSql.pyxlAbstracts import Statement, Arg, Clause
from PyxlSql.pyxlEngine import Cmd,\
    FormatClause, CommentsClause, WhereClause, SetClause, UidClause, FromClause, GroupClause, HavingClause, \
    SaveCmd, DeleteCmd, UpdateCmd, SelectIntoCmd, ImportCmd, JoinClause, RightJoinClause, LeftJoinClause, \
    OrderByClause, OnClause, InnerJoinClause
from PyxlSql.pyxlArgs import ExprArg, FormulaArg, FieldArg, CstArg, ErrorArg, SheetArg, AggregateExprArg


# ---------------------------------------------------------------------------------------------------
# Parsing tools
# ---------------------------------------------------------------------------------------------------
# Parsing is represented by 2 classes: Token and Parser
#
# The parser
#       Holds the grammar
#       Selects the 1st token of the line depending on the string in the 1st column
#       if this is a clause, verifies it is compatible with the current Command
#       calls current_token.parse_statement(worksheet, self.current_cmd, values[1:], cells)
#
# A Token
#       describes each object expected by the Parser.
#       token.complies(): returns error,Arg  only of these is None.
#                   Creates the appropriate Arg
#

# ---------------------------------------------------------------------------------------------------
# Token is the elementary object managed by the grammar parser
# ---------------------------------------------------------------------------------------------------


class Token:
    """the Abstract class for all items that can be parsed by the Parser"""

    def __init__(self, sub_tokens=None, sub_clauses=None):
        self.name: str = "INTERNAL ERROR"
        self.sub_tokens: list = sub_tokens if sub_tokens is not None else []

        self.sub_clauses_names = []
        if sub_clauses is not None:
            for cl in sub_clauses:
                self.sub_clauses_names.append(cl.name)

    def accepts(self, clause_parser):
        """
        :param clause_parser: Token
        :return: True if self accepts 'clause' as a sub item
        """
        name = clause_parser.name
        for cl in self.sub_clauses_names:
            if name == cl:
                return True
        return False

    def complies(self, _workbook: NamedWB, _command: Statement, value: str):
        """ returns error, Arg"""
        raise PyxlSqlInternalError(f"abstract Token.complies({str(value)}")

    def is_a_command(self):
        raise PyxlSqlInternalError("abstract Token.is_a_command()")

    @staticmethod
    def denotes_an_expression(expr: str):
        expr = str(expr)
        return expr[0:2] == ":="

    @staticmethod
    def denotes_a_formula(expr: str):
        expr = str(expr)
        return expr[0] == "="

    @staticmethod
    def denotes_an_aggregation(expr: str):
        expr = str(expr)
        return expr[0:2] == "$="

    def parse_statement(self, worksheet: NamedWS, command: Statement, clause: Statement,  values, cells):
        raise PyxlSqlInternalError("abstract Token.parse_statement()")


class NoneToken(Token):
    """Denotes an empty itemParser"""

    def __init__(self):
        super().__init__()
        self.name = "None"


class KeywordToken(Token):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name

    def complies(self, _workbook, command: Cmd, value: str):
        if value == self.name:
            return None, CstArg(command, value)
        return f"'{self.name}' <> '{str(value)}' ", ErrorArg()


class MultiKeywordToken(Token):
    def __init__(self, *all_names):
        super().__init__()
        self.all_names = all_names
        self.descriptor = all_names[0]
        for n in all_names[1:]:
            self.descriptor += " | " + n

    def __str__(self):
        return self.descriptor

    def complies(self, _workbook, command: Cmd, value: str):
        if value in self.all_names:
            return None, CstArg(command, value)
        return f"'{self.name}' <> '{str(value)} ", ErrorArg()


class SheetToken(Token):
    """Denotes a Sheet"""

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def complies(self, workbook: NamedWB, command: Cmd, sheet_name: str):
        """return None if OK or an error"""

        if sheet_name is None:
            return f"'{self.name}' should not be None", ErrorArg()

        sheet: NamedWS = workbook.get_sheet(sheet_name, raise_except=False)

        if sheet is None:
            return f"'{self.name}' : '{str(sheet_name)}' is not known sheet", ErrorArg()
        return None, SheetArg(command, str(sheet_name), sheet)


class StringToken(Token):
    """Denotes ANY string"""

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def complies(self, _workbook, command: Cmd, string_arg: str):
        if string_arg is None:
            return f"'{self.name}' : should not be None", ErrorArg()

        string_arg = str(string_arg)
        if self.denotes_an_expression(string_arg):
            return f"'{self.name}' : {string_arg} : should not be a Python expression", ErrorArg()

        if self.denotes_a_formula(string_arg):
            return f"'{self.name}' : {string_arg} : should not be an Excel formula", ErrorArg()

        if self.denotes_an_aggregation(string_arg):
            return f"'{self.name}' : {string_arg} : should not be an aggregation", ErrorArg()

        return None, CstArg(command, string_arg)


class FieldToken(Token):
    """Denotes a Field name, existence is not mandatory"""

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def complies(self, _workbook, command: Cmd, field_name: str):
        if field_name is None:
            return f"'{self.name}' : should not be None", ErrorArg()

        field_name = str(field_name)

        if self.denotes_an_expression(field_name):
            return f"'{self.name}' : {field_name} : should not be a Python expression", ErrorArg()

        if field_name[0] == "=":
            return f"'{self.name}' : {field_name} : should not be an Excel formula", ErrorArg()

        return None, FieldArg(command, field_name)


class ValueToken(Token):
    """Any possible value """

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def complies(self, _workbook, command: Cmd, value: str):
        if value is None:
            return f"'{self.name}' : should not be None", ErrorArg()

        value = str(value)
        if self.denotes_an_expression(value):
            return None, ExprArg(command, value)

        if self.denotes_a_formula(value):
            return None, FormulaArg(command, value)

        if self.denotes_an_aggregation(value):
            return None, AggregateExprArg(command, value)

        return None, FieldArg(command, value)


# ---------------------------------------------------------------------------------------------------
# Actual implementations of Tokens
# ---------------------------------------------------------------------------------------------------


# Representation of a command/clause :
# A list of ITEMS, each one is a string or a list.
# when the ITEM is a list, it is a list of alternatives for the ITEM and its continuation
# example
# A := B C D E
#   |  B C F
#   |  B G
#   |
# is stored as:
# A := [ B [ [C D E]
#            [C F]
#            [G]
#            []
#          ]
#       ]


class StatementToken(Token):
    """Description of a Statement or Clause parsed by the Parser"""

    def __init__(self, created_class, sub_tokens=None, sub_clauses=None):
        super().__init__(sub_tokens, sub_clauses)
        self.created_class = created_class
        self.name = created_class.name
        self.help = created_class.help
        self.sub_tokens = sub_tokens if sub_tokens is not None else []

        # TODO: Create a better description for the StatementToken

    def parse_one_level(self, workbook: NamedWB, command: Cmd,
                        values: list[str], parameters: list[Token],
                        arg_list: list[Arg]):
        """
        :param workbook: the command being parsed (cannot be None)
        :param command: The command being executed
        :param values: list of actual values
        :param parameters: list of formal arguments, with potential options
        :param arg_list: the list of actual Arg being built, will be passed to the class creation

        :returns (errs, args)
            errs = None if the list of values matches the list of attributes
                  otherwise 1 string describing the error
            arg_list = list of Args, or []
        """

        value = values[0] if len(values) > 0 else None
        parameter = parameters[0] if len(parameters) > 0 else None

        if parameter is None:
            if value is not None:
                return f" extra value '{value}' at end of syntax ", []
            return None, arg_list

        if isinstance(parameter, list):
            # multiple choices

            error_list = ""
            for option in parameter:
                # arg_list COULD be modified by choices:we copy it
                next_error, next_arg_list = self.parse_one_level(workbook, command, values, option, list(arg_list))
                if next_error is None:
                    return None, next_arg_list
                error_list += next_error
            return error_list, []

        current_error, current_arg = parameter.complies(workbook, command, value)
        if current_error is not None:
            return current_error, []

        if current_arg is None:
            raise PyxlSqlInternalError("arg None")
        else:
            return self.parse_one_level(workbook, command, values[1:], parameters[1:], arg_list + [current_arg])

    def parse_statement(self, worksheet: NamedWS, command: Cmd, clause: Clause, values, cells):
        """parses the list of values
        in case of error, raises a PyxlSqlParseError"""

        parameters = self.sub_tokens

        errors, parameters = self.parse_one_level(worksheet.father, command, values, parameters, [])
        if errors is None:
            if self.is_a_command():  # TODO: same call signature for commands & clauses
                return self.created_class(worksheet.father, *parameters)
            else:
                return self.created_class(command, clause, cells, *parameters)

        raise PyxlSqlParseError(f" '{self.name}' followed by no valid syntax ", errors)

    def is_a_command(self):
        return False


class CmdToken(StatementToken):
    def __init__(self, created_class, sub_tokens=None, sub_clauses=None):
        """
        :param created_class: the class been created
        :param sub_tokens:  list[Token]:
        :param sub_clauses: list[ClauseToken]: the list of clauses that are added
        """
        super().__init__(created_class, sub_tokens, sub_clauses)

    def is_a_command(self):
        return True


class ClauseToken(StatementToken):
    def __init__(self, created_class, sub_tokens=None, sub_clauses=None):
        super().__init__(created_class, sub_tokens, sub_clauses)

    def is_a_command(self):
        return False


# ---------------------------------------------------------------------------------------------------
# class InitializedParser
# ---------------------------------------------------------------------------------------------------


class Parser:
    """ Parser for all possible commands and clauses"""

    def __init__(self):
        self.items = {}  # a dictionary CMD/CLAUSE --> ParsedItem
        self.help = None
        self.current_cmd: Optional[Statement] = None
        self.current_clause: Optional[Statement] = None
        self.current_cmd_token: Optional[Token] = NoneToken()
        self.current_clause_token: Optional[Token] = NoneToken()

        #
        # ---------------------------------------------------------
        # Keywords are inserted directly in the sub_tokens lists

        #
        # ---------------------------------------------------------
        # Clauses

        # Set_clause     := "SET" dst_field ("=" src_value ["WHEN" src_expr]       |
        #                                    "AGGREGATES" expr() "WITH" red_expr   |
        #                                    Aggregation_key expr()                )
        # Aggregation_key := "COUNT" | "MIN" | "MAX" | "SUM" | "AVG"
        set_parser = ClauseToken(SetClause,
                                 sub_tokens=[FieldToken('DstField'), [
                                     [KeywordToken("="), ValueToken("src_expr"),
                                      [[KeywordToken("WHEN"), ValueToken("test_expr")],  []]],
                                     [KeywordToken("AGGREGATES"), ValueToken("src_expr"),
                                      KeywordToken("WITH"), ValueToken("red_expr")],
                                     [MultiKeywordToken("COUNT", "MIN", "MAX", "SUM", "AVG"), ValueToken("src_expr")]
                                 ]])
        self.add(set_parser)

        # UID_clause     := "UID" dst_field "=" example
        uid_parser = ClauseToken(UidClause,
                                 sub_tokens=[FieldToken('dst_field'), KeywordToken("="), StringToken('Example')])
        self.add(uid_parser)

        # Format_clause  := "FORMAT" dst_field "=" example
        format_parser = ClauseToken(FormatClause,
                                    sub_tokens=[FieldToken('dst_field'), KeywordToken("="), StringToken('Example')])
        self.add(format_parser)

        # From_clause := "FROM" src_sheet ("AS" alias)
        from_parser = ClauseToken(FromClause, sub_tokens=[SheetToken('src_sheet'),
                                                          [[],
                                                           [KeywordToken("AS"), StringToken("alias")]]])
        self.add(from_parser)

        on_parser = ClauseToken(OnClause, sub_tokens=[FieldToken("first_expr"),
                                                      KeywordToken("="), ValueToken("second_expr")])
        self.add(on_parser)

        # Join_clause    := Join_key src_sheet ("AS" alias)
        join_parser = ClauseToken(JoinClause, sub_clauses=[on_parser],
                                  sub_tokens=[SheetToken('src_sheet'),
                                              [[],
                                               [KeywordToken("AS"), StringToken("alias")]]])
        self.add(join_parser)
        left_join_parser = ClauseToken(LeftJoinClause, sub_clauses=[on_parser],
                                       sub_tokens=[SheetToken('src_sheet'),
                                                   [[],
                                                    [KeywordToken("AS"), StringToken("alias")]]])
        self.add(left_join_parser)
        right_join_parser = ClauseToken(RightJoinClause, sub_clauses=[on_parser],
                                        sub_tokens=[SheetToken('src_sheet'),
                                                    [[],
                                                     [KeywordToken("AS"), StringToken("alias")]]])
        self.add(right_join_parser)

        inner_join_parser = ClauseToken(InnerJoinClause, sub_clauses=[on_parser],
                                        sub_tokens=[SheetToken('src_sheet'),
                                                    [[],
                                                     [KeywordToken("AS"), StringToken("alias")]]])
        self.add(inner_join_parser)

        # Where_clause   := "WHERE" expr(0,1,2)
        where_parser = ClauseToken(WhereClause, sub_tokens=[ValueToken("src_expr")])
        self.add(where_parser)

        # Group_clause   := "GROUP BY" dst_expr *
        group_parser = ClauseToken(GroupClause, sub_tokens=[ValueToken("dst_expr")])
        self.add(group_parser)

        # Having_clause  := "HAVING" expr
        having_parser = ClauseToken(HavingClause, sub_tokens=[ValueToken('dst_expr')])
        self.add(having_parser)

        # Order_by_clause  := "ORDER BY" expr
        order_by_parser = ClauseToken(OrderByClause, sub_tokens=[ValueToken('dst_expr')])
        self.add(order_by_parser)

        # Comment_clause := "COMMENT" Any *
        comments_parser = ClauseToken(CommentsClause, sub_tokens=[StringToken('Example')])
        self.add(comments_parser)

        #
        # ---------------------------------------------------------
        # Commands

        # Select_cmd     := "SELECT INTO"  dst_sheet: string ("AS" alias) {
        #                    Set_clause *
        #                    UID_clause *
        #                    Format_clause *
        #                    From_clause ?
        #                    Join_clause *
        #                    Where_clause ?
        #                    Group_clause ?
        #                    Having_clause ?
        #                    Order_by_clause ?}
        self.add(CmdToken(SelectIntoCmd,
                          sub_tokens=[SheetToken("dst_sheet"), [[],
                                                                [KeywordToken("AS"), StringToken("alias")]]],
                          sub_clauses=[set_parser, uid_parser, format_parser, from_parser, join_parser, on_parser,
                                       left_join_parser, right_join_parser, inner_join_parser,
                                       where_parser, group_parser, having_parser, order_by_parser]))

        # Update_cmd     := "UPDATE" dst_sheet: string ("AS" alias) {
        #                    Set_clause *
        #                    UID_clause *
        #                    Format_clause *
        #                    From_clause ?
        #                    Join_clause *
        #                    Where_clause ?
        #                    Group_clause ?
        #                    Having_clause ?
        #                    Order_by_clause ?}
        self.add(CmdToken(UpdateCmd,
                          sub_tokens=[SheetToken("dst_sheet"), [[],
                                                                [KeywordToken("AS"), StringToken("alias")]]],
                          sub_clauses=[set_parser, uid_parser, format_parser, from_parser, join_parser, on_parser,
                                       left_join_parser, right_join_parser, inner_join_parser,
                                       where_parser, group_parser, having_parser, order_by_parser]))
        # Import_cmd     := "IMPORT" module ("SUBS" sub_modules)
        self.add(CmdToken(ImportCmd,
                          sub_tokens=[StringToken("Module"), [[KeywordToken("SUBS"), StringToken("submodules")], []]]))

        # Delete_cmd     := "DELETE" dst_sheet
        self.add(CmdToken(DeleteCmd, sub_tokens=[StringToken("Filename")]))

        # Save_cmd       := "SAVE" filename ("FROM" dst_sheet)
        self.add(CmdToken(SaveCmd,
                          sub_tokens=[StringToken("Filename"), [[],
                                                                [KeywordToken("FROM"), StringToken("workbook")]]]))

        # TODO:
        # Pivot_cmd      := "PIVOT" dst_field "FROM" src_sheet
        # self.add(CmdToken(PivotCmd, sub_tokens=[StringToken("Field"), KeywordToken("FROM"), StringToken("Sheet")]))

        # Load_cmd       := "LOAD" filename
        # Insert_cmd     := "INSERT" dst_sheet "AS" new_name
        # Rename_cmd     := "RENAME" dst_sheet "AS" new_name

    def add(self, item: Token):
        """
        :param item: Token
        :return: None
        """
        self.items[item.name] = item
        if self.help is None:
            self.help = item.name
        else:
            self.help += " | " + item.name

    def parse(self, worksheet: NamedWS, values: list[str], cells):
        """Parses one line of excel statements
        :param worksheet: NamedWS, the WS been executed
        :param values: list[str]
        :param cells: list[] : the cells, (deeper info than the values)
        """
        first = values[0]
        # if self.current_cmd is None:
        #    self.current_cmd = None

        if first == "COMMENTS":
            return CommentsClause()  # there is always a command, so we can always add a clause

        if first not in self.items:
            raise PyxlSqlParseError(f"unknown command/clause '{first}'", f"--- known commands: {self.help}")

        token_item = self.items[first]
        if token_item.is_a_command():
            self.current_cmd = None  # Not yet available
        elif not self.current_cmd_token.accepts(token_item) and \
                not self.current_clause_token.accepts(token_item):
            msg = "---  possible clauses:"
            for cl in self.current_cmd_token.sub_clauses_names:
                msg += " '" + cl + "'"
            if self.current_cmd:
                raise PyxlSqlParseError(f"clause '{first}' incompatible with command '{self.current_cmd.name}'", msg)
            else:
                raise PyxlSqlParseError(f"clause '{first}' MUST be included in a command", msg)

        statement_item = token_item.parse_statement(worksheet, self.current_cmd, self.current_clause, values[1:], cells)

        if token_item.is_a_command():
            self.current_cmd = statement_item
            self.current_cmd_token = token_item
            self.current_clause_token = NoneToken()
            self.current_clause = None
        elif len(token_item.sub_clauses_names) > 0:
            self.current_clause_token = token_item
            self.current_clause = statement_item
            # we will look into its clauses to validate

        return statement_item
