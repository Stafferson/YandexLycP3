import requests

url = "https://motivational-content.p.rapidapi.com/pics"

querystring = {"limit":"1"}

headers = {
	"X-RapidAPI-Host": "motivational-content.p.rapidapi.com",
	"X-RapidAPI-Key": "01fe08d0d3msh031ed42bd480f4cp16d8fejsn3e9a11f62331"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)