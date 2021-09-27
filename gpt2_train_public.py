"""
gpt2_train.py
"""

import gpt_2_simple as gpt2
import os
import requests
dir_path = os.getcwd()


model_name = "124M"

if not os.path.isdir(os.path.join("models", model_name)):
	print(f"Downloading {model_name} model...")
	gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/

#I trained it on a file called 'tanakh.txt', feel free to do your own though...

file_name = dir_path+'\\'+"tanakh.txt"

sess = gpt2.start_tf_sess()
gpt2.finetune(sess,
              file_name,
              model_name=model_name,
              steps=1000)   # steps is max number of training steps

gpt2.generate(sess)
