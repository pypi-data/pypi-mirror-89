import pytest
from xltoy.parser import Parser
from xltoy.utils import split_sheet_coordinates

p = Parser(collector=None)

test_set = """
=3*A7+5
=+3
=3*Sheet1!$A$7+5
=3*'Sheet 1'!$A$7+5
=3*'O''Reilly''s sheet'!$A$7+5
=if(Sum(A1:A25)>42,Min(B1:B25),if(Sum(C1:C25)>3.14, (Min(C1:C25)+3)*18,Max(B1:B25)))
=sum(a1:a25,10,min(b1,c2,d3))
=if("T"&a2="TTime", "Ready", "Not ready")
=E3
=+8
=E4+Y6+AA3
=(E3+D3)/2
=+LOG(F11)
=(E4+D4)/2
=IF(D7,D7+E7,D7-E7)
=1/(1+EXP(LN(1/INPUT_M!$G$62-1)-E$543))
=+IF(A4+B4, 1/(1+EXP(LN(1/INPUT_M!$G$62-1)-E$543)), IF(A4+B4, 1, PRIVFUN(E4)))
=+IF(PARAM!$B$135=0, 1/(1+EXP(LN(1/INPUT_M!$G$62-1)-E$543)), IF(PARAM!$B$135=1,PRIVFUN(FUNCT(INPUT_M!$G$62)+E$543),PRIVFUN((FUNCT(INPUT_M!$G$62)+SQRT(INPUT_M!$G$45)*E$543)/SQRT(1-INPUT_MATRIX!$G$45))))
=K13-MIN(L$10,0)+IF(SHEE1!M20=1,0,MIN(K10,0))+L15+L16
=+INTERBANK!FS221
""".splitlines()

@pytest.mark.parser
@pytest.mark.parametrize("s", filter(None,test_set))
def test_parser(s):
    assert p.parse(s)


@pytest.mark.parser
def test_split_sheet_coordinates():
    assert split_sheet_coordinates('E4')          == (None, 'E4')
    assert split_sheet_coordinates('MYSH!E4')     == ('MYSH','E4')
    assert split_sheet_coordinates("'M Y SH'!E4") == ('M Y SH', 'E4')

