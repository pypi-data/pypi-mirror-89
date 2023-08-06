from contextlib import contextmanager
from openpyxl.cell.cell import Cell
from openpyxl.utils.cell import coordinate_to_tuple
from openpyxl.workbook.defined_name import SHEETRANGE_RE
from time import time


@contextmanager
def timeit(description: str, enabled:bool=False) -> None:
    """
    Generic Context manager  simple Timeit

    :param description:
    :param enabled:
    :return:
    """
    t0 = time()
    yield
    ellapsed_time = time() - t0

    if enabled:
        print(f"{description} done in {ellapsed_time:.3f} s.")


def de_dollar(s:str)-> str:
    """
    Remove useless dollars

    :param s: string representing a coordinate
    :return: same cell cleanup

    de_dollar('$AA$4') -> 'AA4

    """
    return s.replace('$','')

def is_vertical_range(rng:list)->bool:
    """

    :param rng:
    :return:
    """
    rows_cols = [coordinate_to_tuple(de_dollar(x)) for x in rng]
    rows = set((x[0] for x in rows_cols))
    cols = set((x[1] for x in rows_cols))
    if len(rows)==1:
        if len(cols)>1:
            return True
        else:
            raise ValueError("Cannot recognize if {} is vertical model range")
    else:
        # We assume it was >1
        if len(cols) == 1:
            return False
        else:
            raise ValueError("Cannot recognize if {} is horizontal model range")


def split_sheet_coordinates(s):
    """

    :param s:
    :return:
    """
    match = SHEETRANGE_RE.match(s)
    if match is None:
        return None, s
    else:
        match = match.groupdict()
        return match['quoted'] or match['notquoted'] , match['cells']
