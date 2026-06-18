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


## [0.1.0] - 22-05-2026

### Added
- [feat] Working trajectory for the spacecraft ([#3])

[#3]: https://github.com/annkonieczna/Space-trajectory-visualizer/issues/3
- [feat] Methods for ploting the trajectory of a singular object with starting and ending point ([#10])

[#10]: https://github.com/annkonieczna/Space-trajectory-visualizer/issues/10

- [feat] Main file responsible for starting the programme and plotting the results ([#11])

[#11]: https://github.com/annkonieczna/Space-trajectory-visualizer/issues/11

- [feat] Animated 3D trajectory visualization.([#19])

[#19]: https://github.com/annkonieczna/Space-trajectory-visualizer/issues/19

- [feat] Prek-based pre-commit configuration ([#20])

[#20]: https://github.com/annkonieczna/Space-trajectory-visualizer/issues/20

- [feat] GitHub Actions workflow for automatic code checks. ([#20])

[#20]: https://github.com/annkonieczna/Space-trajectory-visualizer/issues/20

### Changed
- [feat]  Change trajectory file to make it work for plotting the results
([#4])

[#4]: https://github.com/annkonieczna/Space-trajectory-visualizer/issues/4

- [feat]  Change analysis file, add dataframe for keeping the results
([#8])

[#8]: https://github.com/annkonieczna/Space-trajectory-visualizer/issues/8

- [feat]  Change main file to animate objects
([#19])

[#19]: https://github.com/annkonieczna/Space-trajectory-visualizer/issues/19

## [0.1.0] - 18-06-2026

### Added

- [feat] Add a streamlit user interface that integrates plots, animation and data analysis ([#22])

[#22]: https://github.com/annkonieczna/Space-trajectory-visualizer/issues/22

- [feat] Handle relative kernel paths during SPICE kernel loading ([#25])

[#25]: https://github.com/annkonieczna/Space-trajectory-visualizer/issues/25

- [feat] Change imports to package ([#26])

[#26]: https://github.com/annkonieczna/Space-trajectory-visualizer/issues/26



### Notes
- Project currently focuses on Cassini analysis relative to Saturn and Titan.
