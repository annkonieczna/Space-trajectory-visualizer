# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Added
- Initial project structure for SPICE-based trajectory analysis.
- Configuration module with default time range, reference frame, aberration correction, and object names.
- Kernel download script for generic NAIF kernels and Cassini mission kernels.
- Kernel loading and clearing utilities using SpiceyPy.
- Time conversion utilities between UTC and Ephemeris Time (ET).
- State vector utilities for retrieving position and velocity from SPICE.

### Changed
- Organized constants related to time settings, reference frame, and object names into a dedicated configuration module.


## [1.1.1] - 1-05-2026

### Added
- [feat] Working trajectory for the spacecraft ([#3])

[#3]: https://github.com/annkonieczna/Space-trajectory-visualizer/issues/3
- [feat] Methods for ploting the trajectory of a singular object with starting and ending point ([#10])

[#10]: https://github.com/annkonieczna/Space-trajectory-visualizer/issues/10

- [feat] Main file responsible for starting the programme and plotting the results ([#11])

[#11]: https://github.com/annkonieczna/Space-trajectory-visualizer/issues/10

### Changed
- [feat]  Change trajectory file to make it work for plotting the results
([#4])

[#4]: https://github.com/annkonieczna/Space-trajectory-visualizer/issues/4

- [feat]  Change analysis file, add dataframe for keeping the results
([#8])

[#8]: https://github.com/annkonieczna/Space-trajectory-visualizer/issues/4


### Notes
- Project currently focuses on Cassini analysis relative to Saturn and Titan.
