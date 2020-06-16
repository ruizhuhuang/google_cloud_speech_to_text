from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from google.cloud import speech
import pickle 
import time, os,csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_file_path")
args = parser.parse_args()

client = speech.SpeechClient()
encoding = enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
sample_rate_hertz = 16000
language_code = 'en-US'

config = {'encoding': encoding, 'sample_rate_hertz': sample_rate_hertz, 'language_code': language_code}

wav_file = args.input_file_path
#wav_file = 'MBY007850_mono_16khz_59s.WAV'
gs_dir = 'gs://speech-rhuang/'
working_dir = '/work/03076/rhuang/maverick2/google-cloud-speech-to-text/'


runtime_dir = working_dir + 'out_pickle/'
runtime_name = runtime_dir + 'runtime.csv'
print(runtime_name)

out_pickle_dir = working_dir + 'out_pickle/'
pickle_name = wav_file.split('.')[0] + '.pickle'
out_pickle_path = out_pickle_dir + pickle_name
print(out_pickle_path)


out_txt_dir = working_dir + 'out_txt/'
trans_file = wav_file.split('.')[0] + "_google.txt"
out_txt_path = out_txt_dir + trans_file
print(out_txt_path)

# copy file from local to google storage
source_audio_path = wav_file
cmd = ' ~/google-cloud-sdk/bin/gsutil' + ' ' + 'cp' + ' ' + source_audio_path +  ' ' + gs_dir
print(cmd)
os.system(cmd)
time.sleep(5)


uri = gs_dir + wav_file



audio = {'uri': uri}

audio = speech.types.RecognitionAudio(uri=uri)

operation = client.long_running_recognize(config=config, audio=audio)

start_time = time.time()

op_result = operation.result()

total_time = time.time() - start_time

print(total_time)

with open(runtime_name, 'a') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow([wav_file,round(total_time,2)])



# write output to a pickle file
outfile = open(out_pickle_path, 'wb')
pickle.dump(op_result, outfile)
outfile.close()
time.sleep(5)

dat=pickle.load(open(out_pickle_path, 'rb'))

res_text = ''
for res in dat.results:
    for alternative in res.alternatives:
        text = alternative.transcript
        res_text += text

with open(out_txt_path, 'w') as f:
    f.write(res_text + '\n')

# reomve file from google storage
cmd = ' ~/google-cloud-sdk/bin/gsutil' + ' ' + 'rm' + ' ' + gs_dir + wav_file
print(cmd)
os.system(cmd)
print('ALL DONE')


