#!/bin/bash
export GOOGLE_APPLICATION_CREDENTIALS=/work/03076/rhuang/maverick2/google-cloud-speech-to-text/speech-to-text-rhuang-8c9d63f2a0ca.json

#AUDIO_DIR=/work/03076/rhuang/maverick2/google-cloud-speech-to-text/MBY007850_mono_16khz_59s.WAV
AUDIO_DIR=/work/03076/rhuang/maverick2/google-cloud-speech-to-text/AudioFiles
#AUDIO_FILES=/work/03076/rhuang/maverick2/google-cloud-speech-to-text/AudioFiles/MBY005*_mono_16khz.WAV
AUDIO_FILES=/work/03076/rhuang/maverick2/google-cloud-speech-to-text/AudioFiles/MBY006*_mono_16khz.WAV

PY_SCRIPT=/work/03076/rhuang/maverick2/google-cloud-speech-to-text/speech_to_text_gcloud_final.py
#echo $AUDIO_DIR

for f in $AUDIO_FILES;
do
  filename=$(basename "$f")
  #echo $filename
  cd $AUDIO_DIR
  echo python $PY_SCRIPT $filename
  python $PY_SCRIPT $filename &

done

#python speech_to_text_gcloud.py
#python  oRssing_result_pickle.py
