#!/bin/sh

alias getopt="$(brew --prefix gnu-getopt)/bin/getopt"

num_play=100

##### parameters #####
workdir=$(pwd)

timekey=$RANDOM

##### usage #####
function usage_exit() {
cat << EOF
Usage: $(echo $(basename $0)) [option] param
  param:  --out <file>: set output file
  option: --numplay <val>: set number of game (current: $num_play)
          -f|--force  : allow overwrite
EOF
exit 1
}
set -e

OPT=$(getopt -o f,h \
              -l out:,numplay:,force,help \
              -- "$@")
[ $? != 0 ] && usage_exit

eval set -- "$OPT"
while true; do
  case $1 in
    --out) outfile=$2; shift;;
    --numplay) num_play=$2; shift;;
    -f|--force) flag_force=1;;
    -h|--help) usage_exit;;
    --) shift; break;;
  esac
  shift
done
shift $(( OPTIND -1 ))

##### error handling #####
if [[ -z $outfile ]]; then
  echo "set output file"
  usage_exit
fi
if [[ -f $outfile ]]; then
  if [[ -z $flag_force ]]; then
    echo "$outfile exist!"
    usage_exit
  else
    rm $outfile
  fi
fi

##### main method #####

tmpdir=$(mktemp -d)
cp nimmt*.py $tmpdir/
for ((i=1;i<=$num_play;i++)); do
  sh progress -i 1 -n $i -f $num_play --time $timekey
  python3 $tmpdir/nimmt.py >> $outfile
done
