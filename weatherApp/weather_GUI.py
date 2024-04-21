import tkinter as tk
import requests	

root = tk.Tk()
root.title('Open Weather')
root.geometry('600x400')

background_image = tk.PhotoImage(file='/Users/miaxu/Desktop/UT/SP24/360/W5-GUI/weather_app/landscape.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# top frame for outgoing requests
frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=40)
entry.place(relwidth=0.65, relheight=1)

# lower frame to responses
lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

label = tk.Label(lower_frame)
label.place(relwidth=1, relheight=1)

def format_response(weather):
	try:
		country = weather['country_code']
		name = weather['cityname']
		temp_cel = '{:.2f}'.format(float(weather['temp_cel']))
		pressure = weather['pressure']
		humid = weather['humidity']
		final_str = 'City: %s, %s \nTemperature (°F): %s \nPressure: %s \nHumidity: %s' % (name, country, temp_cel, pressure, humid)
	except Exception as err:
		final_str = f'Problem: {err}, unable to check the information'

	return final_str

def get_weather(city, label):
	url = 'http://127.0.0.1:5000' #server address, followed with urls if any
	try: 
		if city: 
			# requests.post() makes a post request to an url; returns a requests.Response object from the server
			resp = requests.post(url, data={"city": city}) # data: the http post request form
		else:
			resp = requests.get(url)

		weather = resp.json() #check out the json response to a python dictionary
		print('weather:', weather) 

		# to respond to users request
		label['text'] = format_response(weather)

	except requests.exceptions.ConnectionError as err:
		print(err)


button = tk.Button(frame, text="Get Weather", font=40, command=lambda: get_weather(entry.get(), label))
button.place(relx=0.7, relheight=1, relwidth=0.3)


root.mainloop()


