import shodan
from collections import defaultdict

# =========================
# CONFIGURACIÓN
# =========================
# recordar instalar la librería shodan: pip install shodan
# =========================
API_KEY = "VhQPgB0RKHN3SfHwyz5JxFZI9V0MZBFq"  # API Key de Shodan
CARNET = "1990-21-1428"  # 
NOMBRE = "Mario Laureano Subuyuc Toma"  # 
CURSO = "Seguridad de sistemas"  # 
SECCION = "B"  # 
# =========================

# Inicializar API
api = shodan.Shodan(API_KEY)

def main():
    try:
        # Consulta a Shodan filtrando por país Guatemala
        query = "Google"
        print(f"Ejecutando búsqueda: {query}\n")

        # Ejecutar búsqueda
        results = api.search(query)

        # Diccionario para contar IPs por puerto
        puerto_count = defaultdict(int)
        ip_list = set()

        # Mostrar resultados
        for match in results['matches']:
            ip = match['ip_str']
            puerto = match['port']
            org = match.get('org', 'N/A')
            data = match.get('data', '')

            print("="*50)
            print(f"IP: {ip}")
            print(f"Puerto: {puerto}")
            print(f"Organización: {org}")
            print(f"Banner:\n{data[:200]}...")  # solo muestra primeros 200 chars

            # Contabilizar IP y puerto
            ip_list.add(ip)
            puerto_count[puerto] += 1

        # =========================
        # RESUMEN FINAL
        # =========================
        print("\n" + "#"*60)
        print("RESUMEN DE RESULTADOS")
        print("#"*60)
        print(f"Total de direcciones IP identificadas: {len(ip_list)}")

        print("\nTotal de IPs por puerto abierto:")
        for puerto, count in puerto_count.items():
            print(f"  Puerto {puerto}: {count} IPs")

        print("\nDATOS DEL ESTUDIANTE:")
        print(f"Carnet: {CARNET}")
        print(f"Nombre: {NOMBRE}")
        print(f"Curso: {CURSO}")
        print(f"Sección: {SECCION}")
        print("#"*60)

    except shodan.APIError as e:
        print(f"Error en la consulta: {e}")

if __name__ == "__main__":
    main()