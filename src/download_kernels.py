from pathlib import Path
from urllib.request import urlretrieve

KERNELS = {
    # generic kernels:
    "naif0012.tls": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls",  # used for time conversion
    "pck00011.tpc": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00011.tpc",  # planetary constant
    "de442s.bsp": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de442s.bsp",  # ephemeris for vehicles, planets, satelites
    "sat458.bsp": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/sat458.bsp",  # saturn system
    # kernels specifically for Cassini mission:
    "200128RU_SCPSE_17098_17126.bsp": "https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/200128RU_SCPSE_17098_17126.bsp",
    "200128RU_SCPSE_17126_17158.bsp": "https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/200128RU_SCPSE_17126_17158.bsp",
    "200128RU_SCPSE_17158_17177.bsp": "https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/200128RU_SCPSE_17158_17177.bsp",
    "200128RU_SCPSE_17177_17208.bsp": "https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/200128RU_SCPSE_17177_17208.bsp",
    "200128RU_SCPSE_17208_17235.bsp": "https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/200128RU_SCPSE_17208_17235.bsp",
    "200128RU_SCPSE_17235_17258.bsp": "https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/200128RU_SCPSE_17235_17258.bsp",
}


def main():
    target = Path("data/kernels")
    target.mkdir(parents=True, exist_ok=True)

    for filename, url in KERNELS.items():
        out = target / filename
        if out.exists():
            print(f"[OK] It already exists: {out}")
            continue
        print(f"[Dowloading] {filename}")
        urlretrieve(url, out)
        print(f"[Saved] {out}")


if __name__ == "__main__":
    main()
