#!/usr/bin/env python

'''Compare the dependent libraries of two executable files on Linux'''

import sys
import os
import re
from commands import getstatusoutput


def get_ldd_info(filename):
    p_dyn_lib = re.compile('^\s*(.*?)\s*=>\s*(.*?)\s*\((.*?)\)$')
    p_abs_lib = re.compile('^\s*(.*?)\s*\((.*?)\)$')
    
    status, output = getstatusoutput('/usr/bin/ldd %s' % filename)
    ldd = {}
    if status == os.EX_OK:
        for line in output.splitlines():
            m = p_dyn_lib.match(line)
            if m:
                ldd[m.group(1)] = m.group(2)
            else:
                m = p_abs_lib.match(line)
                if m:
                    ldd[m.group(1)] = m.group(1)
    return filename, ldd


def main():
    if len(sys.argv) < 2:
        print 'Compare dependent libraries of two executable files on Linux'
        print 'Syntax: %s FILE1 [FILE2]'
        return 1
    elif len(sys.argv) == 2:
        os.execlp('ldd', sys.argv[0], sys.argv[1])
    else:
        fnA, lddA = get_ldd_info(sys.argv[1])
        fnB, lddB = get_ldd_info(sys.argv[2])
        libnames = set(lddA.keys() + lddB.keys())
        libnamemax = max([len(fn) for fn in libnames])
        libA = []
        libB = []
        
        print 'A =', fnA
        print 'B =', fnB
        print '-'*(max(len(fnA), len(fnB)) + 4)
        for libfn in sorted(libnames):
            print
            print ('%%-%ds' % libnamemax) % libfn,
            if lddA.has_key(libfn) and lddB.has_key(libfn):
                if lddA[libfn] == lddB[libfn]:
                    print '[ OK ]'
                    print '\t%s' % libfn
                else:
                    print '[FAIL]'
                    print '\tA:', lddA[libfn]
                    print '\tB:', lddB[libfn]
            elif lddA.has_key(libfn):
                print '[FAIL]'
                print '\tA:', lddA[libfn]
                libA.append(lddA[libfn])
            else:
                print '[FAIL]'
                print '\tB:', lddB[libfn]
                libB.append(lddB[libfn])
                
        print '-'*(max(len(fnA), len(fnB)) + 4)
        print 'SUMMARY:',
        if len(libA) == len(libB):
            if libA:
                print 'A == B, but PATH'
            else:
                print 'A == B'
        if libA and not libB:
            print 'B in A'
            for libfn in libA:
                print '\tA: %s' % libfn
        elif libB and not libA:
            print 'A in B'
            for libfn in libB:
                print '\tB: %s' % libfn
        

if __name__ == '__main__':
    sys.exit(main())
