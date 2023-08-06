# inspired to: excelExpr by Paul McGuire
from openpyxl.utils.cell import coordinate_to_tuple
from . import log
from .utils import de_dollar
from pyparsing import (
    CaselessKeyword, Word, alphas, alphanums, nums, Optional, Group, oneOf, Forward,
    infixNotation, opAssoc, dblQuotedString, delimitedList, Combine, Literal, QuotedString, ParserElement,
    LineEnd, pyparsing_common as ppc)
ParserElement.enablePackrat()





class Parser:
    def __init__(self, collector=None):
        self.current_sheet = None
        self.collector = collector
        EQ, LPAR, RPAR, COLON, COMMA, EXCL, DOLLAR = map(Literal, "=():,!$")
        multOp = oneOf("* /")
        addOp = oneOf("+ -")
        words = Word(alphas, alphanums + '_')
        sheetRef = words | QuotedString("'", escQuote="''")
        colRef = Optional(DOLLAR) + Word(alphas, max=2)
        rowRef = Optional(DOLLAR) + Word(nums)

        cellRef = Combine(
            Group(Optional(sheetRef("sheet") + EXCL) + colRef("col") + rowRef("row"))
        ).setParseAction(self.cell_action)

        cellRange = (
                Group(cellRef("start") + COLON + cellRef("end"))("range")
                | cellRef
                | Word(alphas, alphanums)
        )('cells')

        expr = Forward()

        COMPARISON_OP = oneOf("< = > >= <= != <>")
        condExpr = expr + Optional(COMPARISON_OP + expr)

        ifFunc = (
                CaselessKeyword("if")
                + LPAR
                + Group(condExpr)("condition")
                + COMMA
                + Group(expr)("if_true")
                + COMMA
                + Group(expr)("if_false")
                + RPAR
        )

        def stat_function(name):
            return Group(CaselessKeyword(name) + Group(LPAR + delimitedList(expr, combine=True) + RPAR))

        sumFunc = stat_function("sum")
        minFunc = stat_function("min")
        maxFunc = stat_function("max")
        aveFunc = stat_function("ave")
        sqrFunc = stat_function("sqrt")
        unknowFunc = words + Group(LPAR + expr + RPAR)

        funcCall = ifFunc | sumFunc | minFunc | maxFunc | aveFunc | sqrFunc | unknowFunc

        numericLiteral = ppc.number
        operand = numericLiteral | funcCall | cellRange | cellRef
        arithExpr = infixNotation(
            operand, [(multOp, 2, opAssoc.LEFT),
                      (addOp, 2, opAssoc.LEFT)],
            lpar=LPAR, rpar=RPAR
        )

        textOperand = dblQuotedString | cellRef
        textExpr = infixNotation(textOperand, [("&", 2, opAssoc.LEFT), ])

        atom = (arithExpr | textExpr)
        expr << Optional(addOp) + atom
        bnf = Optional(EQ|addOp) + expr + LineEnd()
        self.bnf = bnf

    def transform(self, *args, **kwargs):
        """
        a simple hook to transformString function from pyparsing

        :param args: delegated to child function
        :param kwargs: delegated to child function
        :return: delegated to child function
        """
        return self.bnf.transformString(*args, **kwargs)

    def parse(self, *args, **kwargs):
        return self.bnf.parseString(*args, **kwargs)

    def set_current(self, sheet, coordinate):
        self.current_sheet = sheet
        self.current_row, self.current_col = coordinate
        self.current_pos_to_label = self.collector.pos_to_label[sheet]
        self.current_sheet_is_vertical = self.collector.sheet_is_vertical[sheet]

    def cell_action(self, tok):
        """
        over all token occurrence we do transliteration action!

        tok is a cell reference, in these cases we can transliterate syntax in a
        python way.
        Depending on flag self.current_sheet_is_vertical we choose the right
        direction for the time stepper

        :param tok: exel token like E5, $AA$12
        :return: transliterated syntax
        """
        if self.collector is not None:
            if not self.current_sheet:
                raise ValueError("ggg")

            tok = tok[0]
            if '!' in tok:
                # maybe from other sheet!
                sheet, f_tok = tok.split('!')
                if sheet != self.current_sheet:
                    log.warning(f"In sheet {self.current_sheet} cell {tok} found input from external sheet. Treated as exogenous value")
                    val = self.collector.wb_data[sheet][f_tok].value
                    return val

            tok = de_dollar(tok)

            row, col = coordinate_to_tuple(tok)
            pos = col if self.current_sheet_is_vertical else row
            if pos in self.current_pos_to_label:
                label = self.current_pos_to_label[pos]
            else:
                val = self.collector.wb_data[self.current_sheet][tok].value
                log.info("Found params sheet {} cell {}:{}".format(self.current_sheet,tok,val))
                return val

            delta_time = row-self.current_row if self.current_sheet_is_vertical else col-self.current_col
            if delta_time:
                return("{}[T{}]".format(label,delta_time))
            else:
                return("{}[T]".format(label))
