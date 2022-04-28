import requests

url = "https://dad-jokes.p.rapidapi.com/random/joke/png"

headers = {
	"X-RapidAPI-Host": "dad-jokes.p.rapidapi.com",
	"X-RapidAPI-Key": "01fe08d0d3msh031ed42bd480f4cp16d8fejsn3e9a11f62331"
}

#response = requests.request("GET", url, headers=headers)
#test = response.json()

#print(test)

class Dad_jokes:
	def get_joke(self):
		response = requests.request("GET", url, headers=headers)
		test = response.json()
		return test