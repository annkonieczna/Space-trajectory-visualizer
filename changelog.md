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

### Fixed
- 

### Notes
- Project currently focuses on Cassini analysis relative to Saturn and Titan.