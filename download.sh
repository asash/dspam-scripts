URL=http://spamassassin.apache.org/publiccorpus/
SPAM_DIR="corpus/spam"
HAM_DIR="corpus/ham"
mkdir -p $SPAM_DIR
mkdir -p $HAM_DIR
for i in `curl "$URL" | grep -Po "<a.*?</a>" | grep bz2 | grep -o '".*"' | sed 's/"//g'`;
    do
        wget "$URL/$i";
done
for i in `ls -1 | grep "bz2"`; do
    tar xjvf $i
    rm $i -rf
done

function copy {
    TYPE=$1
    DIR=$2
    for i in `ls  -1F | grep "/" |grep $TYPE`; do
        for EMAIL in `find $i/* | grep -v "cmds"`; do
            echo  "mv $EMAIL $DIR"
            mv $EMAIL $DIR
        done
        rm -rf $i
    done
}

copy spam $SPAM_DIR
copy ham $HAM_DIR



