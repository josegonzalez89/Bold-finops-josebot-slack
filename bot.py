def enviar_slack():
    datos = obtener_datos()
    if not datos: return
    
    # Formateamos la fecha para que se vea más amigable (opcional)
    mensaje = (
        f"🏦 *Reporte Financiero bot-finops-Joseslack*\n"
        f"📅 *Tasa Oficial para el día:* {datos['fecha']}\n"
        f"──────────────────────────\n"
        f"💵 *Dólar (TRM):* ${datos['usd_cop']:,.2f} COP\n"
        f"🇵🇪 *Soles a Pesos:* ${datos['sol_cop']:,.2f} COP\n"
        f"💱 *Soles a Dólar:* ${datos['sol_usd']:,.4f} USD\n"
        f"──────────────────────────\n"
        f"_Fuente: SuperFinanciera & ExchangeRate API_"
    )
    
    requests.post(SLACK_WEBHOOK_URL, json={"text": mensaje})
