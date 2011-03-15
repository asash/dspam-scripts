#! /bin/bash

PARTS_COUNT=5
CORPUS="corpus"
USERNAME="firexel"
DSPAM_TRAIN="./add_corpus_to_model.py"
DSPAM_PROFILE=/home/firexel/dspam/var/dspam/data/
GENERATE_MODEL="./generate_model.py"
TESTING_TYPE=$1

function split_dir {
   dir=$1
   for email in `ls -1 $dir`;
   do
       new_dir=$(( $RANDOM % $PARTS_COUNT ))
       echo $new_dir
       mkdir -p $new_dir/$dir
       echo "cp $dir/$email $new_dir/$dir/$email"
       cp $dir/$email $new_dir/$dir/$email
   done
}

#split_dir "$CORPUS/spam"
#split_dir "$CORPUS/ham"

MAX_PART_NUM=$(( $PARTS_COUNT - 1))

for CONTROL in `seq 0 $MAX_PART_NUM`; do
    for TRAIN in `seq 0 $MAX_PART_NUM`; do
        if [ $CONTROL != $TRAIN ]; then
            echo "training on part $TRAIN.."
            $DSPAM_TRAIN $USERNAME $TRAIN/$CORPUS/spam $TRAIN/$CORPUS/ham > /dev/null
        fi
    done;
    echo "checking on part $CONTROL.."
    ./dspam_test.sh $CONTROL/$CORPUS/spam | ./analyze.py spam
    ./dspam_test.sh $CONTROL/$CORPUS/ham | ./analyze.py ham
    if [ "$TESTING_TYPE" -eq "svm" ]; then
        echo "generating model..."
        $GENERATE_MODEL
    fi

    echo "removing profile.."
    rm -rf $DSPAM_PROFILE/$USERNAME
    rm -rf $DSPAM_PROFILE/../raw_model  $DSPAM_PROFILE/../model $DSPAM_PROFILE/../model_index
done;

