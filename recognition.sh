#!/bin/bash


. ./path.sh || exit 1

#Recording
echo "Recording during one second"
arecord -f cd -d 0 --channels=1 --rate=48000 /home/felipe/kaldi/egs/ASR/audio.wav

mfcc_config=conf/mfcc.conf
thread_string="-parallel --num-threads=$num_threads"
filename="audio.wav"
max_active=7000
first_beam=10.0
beam=13.0
lattice_beam=6.0
acwt=0.083333 # note: only really affects pruning (scoring is on lattices).
graphdir=exp/mono/graph
data=data/test
dir=exp/mono/decode
srcdir=`dirname $dir`;
model=$srcdir/final.mdl;
cmvn_opts=`cat $srcdir/cmvn_opts 2>/dev/null`

compute-mfcc-feats  --config=$mfcc_config scp:audio.scp ark:audio.ark 
#compute-cmvn-stats ark:audio.ark ark:cmvn.ark⁠⁠⁠⁠
#apply-cmvn $cmvn_opts ark:cmvn.ark ark:audio.ark ark,t:-

feats="ark:add-deltas $delta_opts ark:audio.ark ark:- | apply-cmvn-sliding --norm-vars=false --center=true --cmn-window=300 ark:- ark:- |";


gmm-latgen-faster --max-active=$max_active --beam=$beam --lattice-beam=$lattice_beam \
  --acoustic-scale=$acwt --allow-partial=true --word-symbol-table=$graphdir/words.txt \
  $model $graphdir/HCLG.fst "$feats" "ark:lattice.ark"

lattice-depth-per-frame "ark:lattice.ark" "ark,t:depth.ark" ark:- | \
lattice-best-path --acoustic-scale=$acwt ark:- ark,t:transcription.ark "ark,t:aligment.ark"

codigo=$(cat transcription.ark)
for i in ${codigo[@]}; do
	cat words.txt | grep $i | head -n 1 | cut -d " " -f 1	
done



