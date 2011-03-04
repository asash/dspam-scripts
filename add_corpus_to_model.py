#! /usr/bin/env python
import sys
import os
import subprocess

dspam_binary = "/home/firexel/dspam/bin/dspam"
dspam_home = "/home/firexel/dspam/var/dspam/"

username = sys.argv[1]
spam_folder = sys.argv[2]
ham_folder = sys.argv[3]

def add_any(folder, email_type):
    for email in os.listdir(folder):
        cmd = [dspam_binary, "--user", username, "--class=spam", "--source=corpus", "--debug"]
        filename = folder + "/" + email
        print "adding %s to model as %s" % (filename, email_type)
        email_text = open(filename).read()
        pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        pipe.communicate(email_text)

add_any(spam_folder, "spam")
add_any(ham_folder, "innocent")

