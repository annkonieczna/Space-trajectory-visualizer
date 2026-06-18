# Space-trajectory-visualizer

# Space Trajectory Analysis with SPICE in Python

This project focuses on the analysis and visualization of trajectories of celestial bodies using NASA's SPICE system via Python.

It leverages the SpiceyPy library to work with precise ephemeris data provided by NASA.

The project specifically analyzes the final phase of the Cassini-Huygens mission in 2017.

The application includes:
- trajectory calculations for selected objects,
- distance analysis over time,
- minimum and maximum distance detection,
- static 3D trajectory plots,
- animated trajectory visualizations,
- a simple Streamlit user interface for changing analysis parameters.

---

## 👩‍💻 Author
- Anna Konieczna


## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/annkonieczna/Space-trajectory-visualizer
cd Space-trajectory-visualizer
```
### 2. Create and activate a virtual environment
Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```
Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
## 🛰️ Download SPICE Kernels


This project does NOT include SPICE kernels in the repository due to their size.

Download them using:
```bash

python -m src.kernel_handling.download_kernels
```

This will save kernels into:
```bash

data/kernels/
```
## 📦 Required Kernels

The project uses generic kernels provided by NASA NAIF:

### Time
- naif0012.tls - time conversion
### Planetary data
- pck00011.tpc - planetary constants
- de442s.bsp - planetary ephemerides
- sat458.bsp - Saturn system (including its moons)
### Cassini trajectory (2017)
- 200128RU_SCPSE_17098_17126.bsp
- 200128RU_SCPSE_17126_17158.bsp
- 200128RU_SCPSE_17158_17177.bsp
- 200128RU_SCPSE_17177_17208.bsp
- 200128RU_SCPSE_17208_17235.bsp
- 200128RU_SCPSE_17235_17258.bsp

All kernels are loaded using a meta-kernel (meta.tm)

## ▶️ Running the Project

After setup and downloading kernels, the project can be used in two ways.

### Streamlit interface

The main interactive version of the project is the Streamlit application:

```bash
streamlit run app.py
```

The interface allows the user to:
- choose single-object or two-object analysis,
- select the analyzed objects and observer,
- set the time range and sampling step,
- display Saturn as the central body,
- view static Plotly charts,
- view Plotly animations,
- inspect summary statistics and data tables,
- download calculated data as CSV.

### Script version

The project can also be run as a script:

```bash
python -m src.main
```

This generates plots and animation files in the `output/` directory.
The `output/` directory is ignored by git because generated files can be large.
## Code quality

This project uses `prek`, a Rust-based drop-in replacement for `pre-commit`, to run formatting and linting checks.

Install prek:

```bash
uv tool install prek
```

## 🧠 About SPICE

SPICE is a system developed by NASA for space mission geometry.

It provides:

- precise spacecraft and planetary positions
- time conversions
- reference frame transformations

SpiceyPy is a Python wrapper around the original SPICE Toolkit.

## 📚 Useful Resources

[NAIF official website:](https://naif.jpl.nasa.gov)

[SpiceyPy documentation:](https://spiceypy.readthedocs.io)
