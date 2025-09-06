

import requests
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Config:
    API_KEY: str = "zY58t3w03oMMZ0OB8dOk9eG0v7LJiZtwIH9MmgrbNegkZWgI"  # <-- Reemplazar
    CARNET: str = "1990-21-1428"
    NOMBRE: str = "Mario Laureano Subuyuc Toma"
    CURSO: str = "Seguridad y Auditoría de Sistemas"
    SECCION: str = "B"

    COUNTRY: str = "Guatemala"    
    CITY: str = "Guatemala"        
    EXTRA: str = ""                # ej. 'port:80' (NO usar org:)
    PAGES: int = 1                 

LEAKIX_URL = "https://leakix.net/search"

def _forbidden(q: str) -> bool:
    ql = q.lower()
    return " org:" in f" {ql} "

def _build_query(cfg: Config) -> str:
    blocks = [f'(country:"{cfg.COUNTRY}")']
    if cfg.CITY.strip():
        blocks.append(f'(geoip.city_name:"{cfg.CITY.strip()}")')
    extra = cfg.EXTRA.strip()
    if extra:
        if _forbidden(extra):
            raise ValueError("El filtro 'org:' está prohibido por el enunciado.")
        blocks.append(f'({extra})')
    return " AND ".join(blocks)

def _print_header(cfg: Config, q: str) -> None:
    print("\n=== DATOS DEL ESTUDIANTE ===")
    print(f"Carnet : {cfg.CARNET}")
    print(f"Nombre : {cfg.NOMBRE}")
    print(f"Curso  : {cfg.CURSO}")
    print(f"Sección: {cfg.SECCION}")
    print("=============================\n")
    print("Consulta (LeakIX):")
    print(q)
    print("\n--- RESULTADOS (formato CSV) ---")
    print("IP,PUERTO,PROTO,CIUDAD,PRODUCTO")

def _row(ip, port, proto, city, product) -> None:
    ip = ip or "-"
    port = "-" if port is None else str(port)
    proto = proto or "-"
    city = city or "-"
    product = product or "-"
    print(f"{ip},{port},{proto},{city},{product}")

def main():
    cfg = Config()

    if not cfg.API_KEY or cfg.API_KEY.startswith("PON_AQUI_"):
        print("[X] Configura tu API_KEY en el archivo antes de ejecutar.")
        return

    try:
        q = _build_query(cfg)
    except ValueError as e:
        print(f"[X] {e}")
        return

    _print_header(cfg, q)

    s = requests.Session()
    s.headers.update({"accept": "application/json", "api-key": cfg.API_KEY})

    unique_ips = set()
    ips_por_puerto = defaultdict(set)
    filas_impresas = 0

    for page in range(max(1, cfg.PAGES)):
        params = {"scope": "service", "page": page, "q": q}
        r = s.get(LEAKIX_URL, params=params, timeout=60)
        if r.status_code != 200:
            print(f"[X] Error HTTP {r.status_code}: {r.text}")
            break

        data = r.json()
        hits = data if isinstance(data, list) else data.get("results", [])
        if not hits:
            if page == 0:
                print("No se obtuvieron resultados para la consulta.")
            break

        for h in hits:
            ip   = h.get("ip") or (h.get("endpoint") or {}).get("ip")
            port = h.get("port") or (h.get("endpoint") or {}).get("port")
            proto = h.get("protocol") or "-"
            geo   = h.get("geoip") or {}
            city  = geo.get("city_name") or "-"
            product = (h.get("service") or {}).get("product") if isinstance(h.get("service"), dict) else None

            _row(ip, port, proto, city, product)

            if ip:
                unique_ips.add(ip)
                if port is not None:
                    try:
                        ips_por_puerto[int(port)].add(ip)
                    except Exception:
                        pass
            filas_impresas += 1

        if len(hits) < 100:
            break

    print("\n=== RESUMEN ===")
    print(f"Filas impresas           : {filas_impresas}")
    print(f"IPs únicas identificadas : {len(unique_ips)}")
    print("IPs únicas por puerto:")
    for p in sorted(ips_por_puerto.keys()):
        print(f"  - Puerto {p}: {len(ips_por_puerto[p])} IPs")
    print("=================\n")

if __name__ == "__main__":
    main()
