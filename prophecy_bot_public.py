'''
prophesy bot (public) by Zac Picker 2021 
'''
import markovify as mfy
import random
import os
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import sys
import json
from numpy.random import rand
import re
import gpt_2_simple as gpt2

regex = re.compile('[^a-zA-Z ]')
#re.sub('',stringhere)
dir_path = os.getcwd()

'''
this is where the twitter API stuff would go but I'm not publishing that here sorry, easy to do yourself tho
'''

#try: #to test if its connecting to twitter
#    api.verify_credentials()
#    print("Authentication OK")
#except:
#    print("Error during authentication")
    
#%%
'''
model creations
'''
#training based on 'tanakh.txt', feel free to do your own model though

#markov model:
dothis = 0
if dothis==1:            
    tanakhfile = 'tanakh.txt'
    tanakh_fulltext = open(dir_path+'\\'+tanakhfile, "r" ).readlines() #full text including chords and lyrics               
    tanakh_model = mfy.NewlineText(tanakh_fulltext)
    with open('tanakh_text_model.json','w') as f:
        json.dump(tanakh_model.to_json(),f)
if dothis==0:
    tanakh_model = mfy.Text.from_json(json.load(open('tanakh_text_model.json',)))

#you'll need to train gpt2 on the model yourself since its too big to upload... see other script
#just set your checkpoint and model directory to wherever you saved it.
    
chkdir = 'your checkpoint directory'
mdldir = 'your model directory'
#gpt2 model:
if not 'sess' in vars():
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess,
                  checkpoint_dir=chkdir,
                  model_dir=mdldir)

#%%
'''
menu program
'''
def menu():
    class GetEntry():
    
        def __init__(self, master):
    
            self.master=master
            self.master.title('Prophecy Bot')
            self.entry_contents=None
                       
            #title labels
            self.title = ttk.Label(text='Zechariah Bot')
            self.title['font'] = font.Font(size=30)
            self.title.grid(row=0,column=0,sticky='w',columnspan=3)
            ttk.Label(text='').grid(row=1,column=0)
            self.name = ttk.Label(text = '\"According to the prophet Zechariah, in the messianic era, Sukkot will become a universal festival and all nations will make pilgrimages annually to Jerusalem\"',wraplength = 600)
            self.name.grid(row=2,column=0,sticky='w',columnspan=4)
            self.name['font']=font.Font(size=12)
            ttk.Label(text='').grid(row=3,column=0)
            
                        
            #quick prophecy button
            self.quickprophbut = tk.Button(text="Quick Prophecy",command=self.prophecy_button)
            self.quickprophbut['font'] = font.Font(size=18)
            self.quickprophbut.grid(row=4,column=0,sticky='w')
            #"smart" prophecy button
            self.smartprophbut = tk.Button(text="\"Smart\" Prophecy",command=self.smart_prophecy_button)
            self.smartprophbut['font'] = font.Font(size=18)
            self.smartprophbut.grid(row=4,column=1,sticky='w')
            #tweet button. tweets whatever text is there
            self.tweetbutt = tk.Button(text="Tweet that baby",command=self.tweet_button)
            self.tweetbutt['font'] = font.Font(size=18)
            self.tweetbutt.grid(row=4,column=3,sticky='w')
            #answer space
            self.quickproph = tk.Label(text='',wraplength=550,anchor='w')
            self.quickproph.grid(row=6,column=0,sticky='w',columnspan=4)
            self.quickproph['font'] = font.Font(size=16)
            master.rowconfigure(6, minsize=170)
            
            #ask zecheriah
            self.askzech = ttk.Entry(master,width=46)
            self.askzech['font']=font.Font(size=16)
            self.askzech.insert(0,'')
            self.askzech.grid(row=7,column=0,sticky='w',columnspan=4,padx=10)
            self.asktext = tk.Button(text='Ask Zechariah',command=self.callback)
            self.asktext['font']=font.Font(size=18)
            self.asktext.grid(row=8,column=0)

            
            #quit code on exit press
            self.master.protocol("WM_DELETE_WINDOW",self.on_closing)
            
        def on_closing(self):
            self.master.destroy()
            sys.exit()
            
        def prophecy_button(self):
            statesize=random.randint(2,8)          
            book = 'Zechariah'
            self.prophecy = tanakh_model.make_short_sentence(300,tries=100,state_size=statesize)
            if self.prophecy == None:
                self.prophecy = '1:1 Not today, kiddo'
            self.quickproph['text'] = book.capitalize()+', '+self.prophecy
        
        def smart_prophecy_button(self):
            #generate smart proph
            book = 'Zechariah'
            ans = gpt2.generate(sess,
              checkpoint_dir=chkdir,
              model_dir=mdldir,
              length = 100,
              temperature = (rand()+.1)/1.2,
              return_as_list=True)[0]
            anssplit = ans.split('\n')[0]
            self.quickproph['text'] = book.capitalize()+', '+anssplit
            
            
        def tweet_button(self):
            if self.quickproph['text'] == '':
                self.quickproph['text'] = '1:1 Not today, kiddo'
            #tweet command would go here usually!"
        
        def callback(self):
            self.entry_contents=[self.askzech.get()]
            query = self.entry_contents[0]
            #generate response
            book = 'Zechariah'
            ans = gpt2.generate(sess,
              checkpoint_dir=chkdir,
              model_dir=mdldir,
              length = 100,
              temperature = (rand()+.1)/1.2,
              prefix = query+"\n",
              return_as_list=True)[0]
            anssplit = ans.split('\n')[0:3]
            self.quickproph['text'] = anssplit[0]+'\n\n'+book.capitalize()+', '+anssplit[2]

    master = tk.Tk()
    outs=GetEntry(master)
    master.mainloop()
    output=outs.entry_contents
    return output

menu()












