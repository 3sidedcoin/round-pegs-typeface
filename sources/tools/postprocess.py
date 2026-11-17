"""Add gasp + smart-dropout prep to an unhinted TTF (what gftools fix-nonhinting does for GF)."""
import sys
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import ttProgram
p = sys.argv[1]
f = TTFont(p)
g = newTable('gasp'); g.version = 1; g.gaspRange = {0xFFFF: 0x000F}; f['gasp'] = g
prep = newTable('prep'); prep.program = ttProgram.Program()
prep.program.fromBytecode(bytes.fromhex('B801FF85B0048D'))
f['prep'] = prep
f.save(p)
