import shodan

API_KEY = "VhQPgB0RKHN3SfHwyz5JxFZI9V0MZBFq"  

api = shodan.Shodan(API_KEY)

try:
    # Probar autenticación
    info = api.info()
    print("✅ API Key válida, información de la cuenta:")
    print(info)

except shodan.APIError as e:
    print(f"❌ Error con la API Key: {e}")
