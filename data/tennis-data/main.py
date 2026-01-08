import os
import time
from urllib import request, error

BASE_URL = "http://www.tennis-data.co.uk/{year}/{year}.xls"
OUTPUT_DIR = "tennis_data"

def download_year(year: int, outdir: str, retries: int = 2, timeout: int = 30):
    """Descarga el archivo XLSX de un año. Devuelve (year, status)."""
    url = BASE_URL.format(year=year)
    dest = os.path.join(outdir, f"{year}.xls")

    # Evita descargas repetidas
    if os.path.exists(dest):
        return (year, "skip")

    # Asegura carpeta
    os.makedirs(outdir, exist_ok=True)

    # Intentos con backoff simple
    for attempt in range(retries + 1):
        try:
            req = request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with request.urlopen(req, timeout=timeout) as resp:
                if resp.status != 200:
                    raise error.HTTPError(url, resp.status, "HTTP error", resp.headers, None)
                with open(dest, "wb") as f:
                    f.write(resp.read())
            return (year, "ok")

        except error.HTTPError as e:
            if e.code == 404:
                # El archivo no existe en el servidor para ese año
                return (year, "404_not_found")
            if attempt == retries:
                return (year, f"http_error_{e.code}")
            time.sleep(1 + attempt)

        except Exception as e:
            if attempt == retries:
                return (year, f"error_{e.__class__.__name__}")
            time.sleep(1 + attempt)

def main():
    years = range(2000, 2013)  # 2000–2023 inclusive
    results = []

    for y in years:
        year, status = download_year(y, OUTPUT_DIR)
        print(f"{y}: {status}")
        results.append((year, status))

    downloaded = [y for y, s in results if s in ("ok", "skip")]
    failed = [(y, s) for y, s in results if s not in ("ok", "skip")]

    print(f"\nGuardados en '{OUTPUT_DIR}'.")
    print(f"Descargados o ya existentes: {len(downloaded)} de {len(list(years))}")
    if failed:
        print("Fallidos:")
        for y, s in failed:
            print(f"  - {y}: {s}")

if __name__ == "__main__":
    main()
