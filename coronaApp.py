import tkinter as tk
from tkinter import font
import requests
import json
import re

API_KEY = "tDX6rC2Et6aL"
PROJECT_TOKEN = "tYb4SDCQGxFz"
RUN_TOKEN = "tTYBOSZEu78_"

response = requests.get(f"https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data", params={"api_key": API_KEY})

data = json.loads(response.text)

class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.get_data()

    def get_data(self):
        response = requests.get(f"https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data", params={"api_key": API_KEY})
        self.data = json.loads(response.text)
    
    def get_total_cases(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Coronavirus Cases:":
                return content['value']
    
    def get_country_data(self, country):
        data = self.data['country']

        for content in data:
            if content['name'].lower() == country.lower():
                return content
        return "0"

    def get_list_of_countries(self):
        countries = []
        for country in self.data['country']:
            countries.append(country['name'].upper())

        return countries





root = tk.Tk()

HEIGHT = 700
WIDTH = 800

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

root.title("Coronavirus Cases Tracker")

background_image = tk.PhotoImage(file='landscape.png')
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=('Courier', 12))
entry.place(relwidth=0.65, relheight=1)

lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely= 0.25, relwidth=0.75, relheight=0.6, anchor='n')





def method(place):


    data = Data(API_KEY, PROJECT_TOKEN)
    END_PHRASE = "stop"
    country_list = data.get_list_of_countries()
    result = None
    text = "How many cases in " + entry.get().upper()

    TOTAL_PATTERNS = {
                    re.compile("[\w\s]+ total [\w\s]+ cases"):data.get_total_cases,
                    re.compile("[\w\s]+ total cases"):data.get_total_cases,

                    }

    COUNTRY_PATTERNS = {
                    re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
                        }
        
    for pattern, func in COUNTRY_PATTERNS.items():
        if pattern.match(text):
            words = set(text.split(" "))
            for country in country_list:
                if country in words:
                    result = func(country)
                    break

    for pattern, func in TOTAL_PATTERNS.items():
        if pattern.match(text):
            result = func()
            break

    if result:
        label['text'] = result

    

        

            
    











button = tk.Button(frame, text="Get Cases" , font=('Courier', 12), command=lambda: method(entry.get()))
button.place(relx=0.7, relwidth=0.3, relheight=1)

label = tk.Label(lower_frame, font=('Courier', 50), anchor='nw', justify='left', bd=4)
label.place(relwidth=1, relheight=1)




root.mainloop()