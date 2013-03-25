#!/usr/bin/env python

'''Compare symbols in two object files'''

import sys
import os
import re
from commands import getstatusoutput

MEANINGLESS_TYPES = ('t', 'T', 'r', 'R')

def nm(filename):
    p_symbol = re.compile('^([0-f]+|\s+) (\S) (.*?)$')
    
    status, output = getstatusoutput('/usr/bin/nm %s' % filename)
    symbols = {}
    if status == os.EX_OK:
        for line in output.splitlines():
            m = p_symbol.match(line)
            if m:
                a = m.group(1)  # Address
                t = m.group(2)  # Type
                s = m.group(3)  # Symbol
                if not symbols.has_key(s):
                    symbols[s] = {'type':  t,
                                  'count': 1}
                else:
                    symbols[s]['count'] += 1
    return os.path.realpath(filename), symbols


def main():
    if len(sys.argv) < 2:
        print 'Compare symbols in two object files'
        print 'Syntax: %s FILE1 [FILE2]'
        return 1
    elif len(sys.argv) == 2:
        os.execlp('nm', sys.argv[0], sys.argv[1])
    else:
        fnA, symA = nm(sys.argv[1])
        fnB, symB = nm(sys.argv[2])
        sym_set = set(symA.keys() + symB.keys())
        symAset = set(symA.keys())
        symBset = set(symB.keys())
        
        filenamemax = max(len(fnA), len(fnB))
        print ('A = %%-%ds  %%12d (bytes)' % filenamemax) % (fnA, os.path.getsize(fnA))
        print ('B = %%-%ds  %%12d (bytes)' % filenamemax) % (fnB, os.path.getsize(fnB))
        print '-'*(max(len(fnA), len(fnB)) + 4)
        
        print 'A \ B'
        for sym in sorted(symAset - symBset):
            type = symA[sym]['type']
            if not type in MEANINGLESS_TYPES:
                print '\t%s %s' % (type, sym)
        print 'B \ A'
        for sym in sorted(symBset - symAset):
            type = symB[sym]['type']
            if not type in MEANINGLESS_TYPES:
                print '\t%s %s' % (type, sym)
        

if __name__ == '__main__':
    sys.exit(main())
