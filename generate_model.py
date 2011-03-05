#! /usr/bin/env python
from collections import defaultdict
import operator
import subprocess


dspam_home = "/home/firexel/dspam/var/dspam/"
svm_train_binary = "/home/firexel/dspam_test_scripts/svm-train"
max_dimention = 2000

raw_model_filename = dspam_home + "raw_model"
tmp_model_filename = "/tmp/tmp_dspam_model"
frequences = defaultdict(lambda:0)
uids = dict()
uids_count = 0

#calculating frequences and uids
raw_model_file = open(raw_model_filename)
for message in raw_model_file:
    words = message.rstrip().split(" ")
    message_class = words[0]
    username = words[1]
    if not (username in uids):
        uids[username] = uids_count
        uids_count += 1
    for word in words[2:]:
        name, frequency = word.split(":")
        frequences[name] += int(frequency)
raw_model_file.close()
sorted_words = sorted(frequences.iteritems(), key=operator.itemgetter(1))
sorted_words.reverse()
dimention = min(len(sorted_words), max_dimention)
positions = dict()

for i in range(0, dimention):
    word = (sorted_words[i])[0]
    positions[word] = i


tmp_model_file = open(tmp_model_filename, "w")

#writing tmp model
raw_model_file = open(raw_model_filename)
for message in raw_model_file:
    result_vector = defaultdict(lambda: 0)
    words = message.rstrip().split(" ")
    message_class = words[0]
    username = words[1]
    uid = uids[username]
    for word in words[2:]:
        name, frequency = word.split(":")
        if name in positions:
            result_vector[positions[name]] += int(frequency)

    if (message_class == "Spam"):
        tmp_model_file.write("1.0 ")
    else:
        tmp_model_file.write("0.0 ")

    for i in range(0, uids_count):
        if (i == uid):
            tmp_model_file.write("%s:1 " % i)
        else:
            tmp_model_file.write("%s:0" % i)

    for i in range(0, dimention):
        tmp_model_file.write("%s:%s " % (i + uids_count, result_vector[i]))
    tmp_model_file.write("\n")

tmp_model_file.close()
raw_model_file.close()

model_index_filename = dspam_home + "model_index"

model_index_file = open(model_index_filename, "w")
model_index_file.write("%s\n" % uids_count)
for username in uids:
    model_index_file.write("%s %s\n" % (username, uids[username]))
model_index_file.write("%s\n" % dimention)

for i in range(0, dimention):
    model_index_file.write("%s\n" % (sorted_words[i])[0])
model_index_file.close()
model_filename = dspam_home + "model"
cmd = [svm_train_binary, "-s", "3", tmp_model_filename, model_filename]
print cmd
subprocess.call(cmd)
