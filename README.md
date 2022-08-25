# Molad Sensor
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

Molad Sensor for [HACS](https://github.com/hacs/integration)

## Installation
Use [HACS](https://github.com/hacs/integration) download the molad directory from inside the apps directory here to your local apps directory

## Usage
No configuration is required. The timezone and location are fetched from your Home Assistant configuration.]
This app adds two sensors exposing Molad details for the upcoming Jewish Month:

1. `sensor.molad` with the upcoming Molad as the value and more detailed properties as attributes
2. `sensor.is_shabbos_mevorchim` - `true` if today is Shabbos Mevorchim, `false` if not
