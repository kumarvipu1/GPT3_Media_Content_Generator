import tkinter as tk
from tkinter import ttk
from tkinter import *
import openai
from gpt import GPT
from gpt import Example
import pandas as pd
import config
import openai


openai.api_key = config.api_key

gpt = GPT(engine="davinci-instruct-beta",
          temperature=0.5,
          max_tokens=800,
          )


train_data = pd.read_csv('example.csv')

def train_gpt():
    stakeholder, response = train_data.columns
    for i in range(len(train_data)):
        gpt.add_example(Example(train_data[stakeholder].iloc[i],
                                train_data[response].iloc[i]))

def generate_response(input_prompt = 'text'):
    response = openai.Completion.create(
        engine="davinci-instruct-beta",
        prompt= input_prompt,
        temperature=0.7,
        max_tokens=800,
        top_p=1,
        frequency_penalty=0.7,
        presence_penalty=1,
    )
    return response['choices'][0]['text']

'''===========GUI======='''
window = tk.Tk()
window.title('Update Generator')
window.geometry('350x250')

frame = Frame(window, width=300, height=160)
'''================Media Dropdown==============================='''
# Label 1
ttk.Label(window, text="Select a media :",
          font=("Times New Roman", 10)).pack()

v = tk.StringVar()
Facebook = tk.Radiobutton(window,
text="Facebook",
padx = 20,
variable=v,
value= 'fb').pack()

LinkedIn = tk.Radiobutton(window,
text="LinkedIn",
padx = 20,
variable=v,
value= 'linkedin').pack()

Twitter = tk.Radiobutton(window,
text="Twitter",
padx = 20,
variable=v,
value= 'twitter').pack()

E_mail = tk.Radiobutton(window,
text="E-mail",
padx = 20,
variable=v,
value= 'email').pack()


'''======================Stakeholders Dropdown========================'''
# Label 2
ttk.Label(window, text="Stakeholders:",
          font=("Times New Roman", 10)).pack()
n = tk.StringVar()
Stakeholders = ttk.Combobox(window, width=27,
                            textvariable=n)

# Add stakeholders here
Stakeholders['values'] = ('Public', 'Project Sponsors', 'Team Members')

# update row numbers as per the numbers of media
Stakeholders.pack()
Stakeholders.current(1)

''''=======================INPUT======================================='''
# Label 3
ttk.Label(window, text="Enter project content",
          font=("Times New Roman", 10)).pack()

name_var = tk.StringVar()
user_prmt = tk.Entry(window, width=50, textvariable=name_var)
user_prmt.pack()

'''==========================OUTPUT=================================='''
# Label 4
ttk.Label(window, text="Response",
          font=("Times New Roman", 10)).pack()
name = tk.StringVar()
response = tk.Text(window, height=8, width=80)
response.pack()

ttk.Label(window, text="Input Prompt",
          font=("Times New Roman", 10)).pack()
name = tk.StringVar()
input_prmt = tk.Text(window, height=3, width=40)
input_prmt.pack()


stk = Stakeholders.get()
media_val = v.get()
custom_prmt = user_prmt.get()
modifier1 = 'in casual tone'
modifier2 = 'in formal tone'
modifier3 = '/nDear,/n'


def generate_input_prompt():
    final_prompt = 'summarise key points from: ' + media_val + ' for ' + stk
    input_prmt.insert(tk.END, final_prompt)
    final_prompt = final_prompt + ' from ' + custom_prmt
    if stk == 'Project Sponsors':
        final_prompt = final_prompt + modifier2
    else:
        final_prompt = final_prompt + modifier1

    if media_val == 'email':
        final_prompt = final_prompt + modifier3

    return final_prompt

'''================================================'''


def myClick():
    input_prompt = generate_input_prompt()
    output = generate_response(input_prompt)
    response.insert(tk.END, output)

def clearTextInput():
    response.delete("1.0","end")
    input_prmt.delete("1.0","end")


myButton = Button(window, text = 'Get Response', command = myClick).pack()

myButton2 = Button(window, text = 'Train', command = train_gpt).pack()
myButton3 = Button(window, text = 'Clear', command = clearTextInput).pack()

window.mainloop()



