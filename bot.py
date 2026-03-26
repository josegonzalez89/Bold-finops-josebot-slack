import requests
import os

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def obtener_datos():
    url_trm = "https://www.datos.gov.co/resource/32sa-8pi3.json?$order=vigenciadesde DESC&$limit=1"
    url_soles = "https://open.er-api.com/v6/latest/USD"
    try:
        res_trm = requests.get(url_trm).json()
        usd_cop = float(res_trm[0]['valor'])
        fecha = res_trm[0]['vigenciadesde'].split('T')[0]
        res_int = requests.get(url_soles).json()
        usd_pen = res_int['rates']['PEN']
        sol_cop = usd_cop / usd_pen
        sol_usd = 1 / usd_pen
        return {"fecha": fecha, "usd_cop": usd_cop, "sol_cop": sol_cop, "sol_usd": sol_usd}
    except Exception as e:
        print(f"Error: {e}")
        return None

def enviar_slack():
    datos = obtener_datos()
    if not datos: return
    mensaje = (
        f"🤖 *bot-finops-Joseslack*\n"
        f"📅 *Vigencia:* {datos['fecha']}\n"
        f"💵 *Dólar:* ${datos['usd_cop']:,.2f} COP\n"
        f"🇵🇪 *Soles a Pesos:* ${datos['sol_cop']:,.2f} COP\n"
        f"💱 *Soles a Dólar:* ${datos['sol_usd']:,.4f} USD"
    )
    requests.post(SLACK_WEBHOOK_URL, json={"text": mensaje})

if __name__ == "__main__":
    enviar_slack()
