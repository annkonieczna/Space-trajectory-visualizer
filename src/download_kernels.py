from pathlib import Path
from urllib.request import urlretrieve

KERNELS = {
    "naif0012.tls": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls",
    "pck00011.tpc": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00011.tpc",
    "de440s.bsp": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp",
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