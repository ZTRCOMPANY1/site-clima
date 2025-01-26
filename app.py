from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "e954dbe4a031487598c220527252601"  # Substitua pela sua chave da WeatherAPI
BASE_URL = "http://api.weatherapi.com/v1/forecast.json"

@app.route("/", methods=["GET", "POST"])
def index():
    clima = None
    previsao_horas = None

    if request.method == "POST":
        cidade = request.form["cidade"]
        url = f"{BASE_URL}?key={API_KEY}&q={cidade}&lang=pt&days=1&aqi=no&alerts=no"
        resposta = requests.get(url).json()
        
        if "error" not in resposta:
            estado = resposta["location"].get("region", "")  # Busca o estado/região
            cidade_com_estado = f"{estado} - {resposta['location']['name']}" if estado else resposta['location']['name']

            # Pega chance de chuva e se vai chover
            chance_chuva = resposta["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"]
            vai_chover = "Sim" if chance_chuva > 50 else "Não"

            clima = {
                "cidade": cidade_com_estado,  # Nome da cidade com estado
                "pais": resposta["location"]["country"],
                "data_hora": resposta["location"]["localtime"],
                "temperatura": resposta["current"]["temp_c"],
                "sensacao": resposta["current"]["feelslike_c"],
                "minima": resposta["forecast"]["forecastday"][0]["day"]["mintemp_c"],
                "maxima": resposta["forecast"]["forecastday"][0]["day"]["maxtemp_c"],
                "condicao": resposta["current"]["condition"]["text"],
                "icone": resposta["current"]["condition"]["icon"],
                "vento_kph": resposta["current"]["wind_kph"],
                "umidade": resposta["current"]["humidity"],
                "vai_chover": vai_chover,
                "chance_chuva": chance_chuva
            }
           
            # Pegando previsão para as próximas 5 horas
            previsao_horas = []
            for hora in resposta["forecast"]["forecastday"][0]["hour"][:5]:  # Pega as primeiras 5 horas
                previsao_horas.append({
                    "hora": hora["time"].split(" ")[1],  # Pega só a hora (HH:mm)
                    "temperatura": hora["temp_c"],
                    "condicao": hora["condition"]["text"],
                    "icone": hora["condition"]["icon"],
                    "chance_chuva": hora["chance_of_rain"]  # Chance de chuva por hora
                })

        else:
            clima = {"erro": "Cidade não encontrada!"}

    return render_template("index.html", clima=clima, previsao_horas=previsao_horas)

if __name__ == "__main__":
    app.run(debug=True)
