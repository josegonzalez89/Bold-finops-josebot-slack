import requests
import os

# 1. Obtener la URL de Slack desde los Secrets
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def ejecutar_reporte():
    try:
        # 2. Consultar TRM (Dólar a Peso)
        res_trm = requests.get("https://www.datos.gov.co/resource/32sa-8pi3.json?$order=vigenciadesde DESC&$limit=1")
        datos_trm = res_trm.json()
        usd_cop = float(datos_trm[0]['valor'])
        fecha_vigencia = datos_trm[0]['vigenciadesde'].split('T')[0]

        # 3. Consultar Tasa Internacional (Soles a Dólar)
        # Usamos esta API que es muy estable para monedas latinas
        res_sol = requests.get("https://open.er-api.com/v6/latest/USD")
        datos_sol = res_sol.json()
        usd_pen = datos_sol['rates']['PEN']

        # 4. Cálculos
        sol_cop = usd_cop / usd_pen
        sol_usd = 1 / usd_pen

        # 5. Construir el mensaje
        mensaje = (
            f"🏦 *bot-finops-Joseslack* | Reporte Oficial\n"
            f"📅 *Vigencia desde:* {fecha_vigencia}\n"
            f"──────────────────────────\n"
            f"💵 *1 USD:* ${usd_cop:,.2f} COP\n"
            f"🇵🇪 *1 SOL:* ${sol_cop:,.2f} COP\n"
            f"💱 *1 SOL:* ${sol_usd:,.4f} USD\n"
            f"──────────────────────────\n"
            f"_Dato obtenido de SuperFinanciera_"
        )

        # 6. Enviar a Slack
        final = requests.post(SLACK_WEBHOOK_URL, json={"text": mensaje})
        
        if final.status_code == 200:
            print("✅ Mensaje enviado con éxito a Slack")
        else:
            print(f"❌ Error en Slack: {final.status_code}")

    except Exception as e:
        # Si algo falla, esto nos dirá qué fue en la pantalla negra de GitHub
        print(f"❌ ERROR CRÍTICO: {e}")

if __name__ == "__main__":
    ejecutar_reporte()
