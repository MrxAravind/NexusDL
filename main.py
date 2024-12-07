import requests

def get_data():
    try:
        url = "https://stupidfucker79.github.io/Shiny-Scarper/links.txt"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.text.split("\n")
            return [[i.split("|-|")[0],i.split("|-|")[-1]] for i in data]
        else:
            return f"Error: Received status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"


response_data = get_data()
