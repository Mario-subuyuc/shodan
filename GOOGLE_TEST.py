import shodan

API_KEY = "VhQPgB0RKHN3SfHwyz5JxFZI9V0MZBFq"
api = shodan.Shodan(API_KEY)

try:
    ipinfo = api.host("8.8.8.8")  # Google DNS
    print("===============================")
    print("Información de la IP 8.8.8.8:")
    print("===============================")
    print(f"Organización: {ipinfo.get('org', 'N/A')}")
    print(f"País: {ipinfo.get('country_name', 'N/A')}")
    print("Puertos abiertos:", ipinfo.get('ports', []))

except shodan.APIError as e:
    print(f"Error: {e}")
