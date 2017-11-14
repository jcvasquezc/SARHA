#!/bin/bash

. ./path.sh || exit 1
. ./cmd.sh || exit 1
 
nj=1       # number of parallel jobs - 1 is perfect for such a small data set
lm_order=1 # language model order (n-gram quantity) - 1 is enough for digits grammar
 
# Safety mechanism (possible running this script with modified arguments)
. utils/parse_options.sh || exit 1
[[ $# -ge 1 ]] && { echo "Wrong arguments!"; exit 1; }

rm -rf data/test/spk2utt data/test/cmvn.scp data/test/feats.scp data/test/split1
rm -rf exp/tri1/decode
echo
echo "===== PREPARING ACOUSTIC DATA ====="
echo
 
# Needs to be prepared by hand (or using self written scripts):
#
# spk2gender  [<speaker-id> <gender>]
# wav.scp     [<uterranceID> <full_path_to_audio_file>]
# text           [<uterranceID> <text_transcription>]
# utt2spk     [<uterranceID> <speakerID>]
# corpus.txt  [<text_transcription>]

utils/utt2spk_to_spk2utt.pl data/test/utt2spk > data/test/spk2utt
 
echo
echo "===== FEATURES EXTRACTION ====="
echo
 
# Making feats.scp files
mfccdir=mfcc
steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" data/test exp/make_mfcc/test $mfccdir
 
# Making cmvn.scp files
#steps/compute_cmvn_stats.sh data/train exp/make_mfcc/train $mfccdir
steps/compute_cmvn_stats.sh data/test exp/make_mfcc/test $mfccdir

 echo
 echo "===== TRI1 (first triphone pass) DECODING ====="
 echo
  
 utils/mkgraph.sh data/lang exp/tri1 exp/tri1/graph || exit 1
 steps/decode.sh --config conf/decode.config --nj $nj --cmd "$decode_cmd" exp/tri1/graph data/test exp/tri1/decode
  
 echo
 echo "===== run.sh script is finished ====="
 echo
