#!/usr/bin/env python
import sys

spam_count = 0
ham_count = 0

for line in sys.stdin:
    line = line.rstrip()
    if line == "Spam":
        spam_count += 1
    elif line == "Innocent":
        ham_count += 1
    else:
        print line

if sys.argv[1] == "spam":
    print "FP: %s, %s" % (ham_count, 1.0*ham_count/(ham_count + spam_count))
elif sys.argv[1] == "ham":
    print "FN: %s, %s" % (spam_count, 1.0*spam_count/(spam_count + ham_count))



