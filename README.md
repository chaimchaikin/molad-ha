# Molad Sensor
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

Molad Sensor for [HACS](https://github.com/hacs/integration)

## Installation
### Download
Use [HACS](https://github.com/hacs/integration) or download the molad directory from inside the apps directory here to your local apps directory

### Integration Setup
- Browse to your Home Assistant instance.
- In the sidebar click on Configuration.
- From the configuration menu select: Integrations.
- In the bottom right, click on the Add Integration button.
- From the list, search and select "Molad".
- Follow the instruction on screen to complete the set up.
- After completing, the Molad sensors will be immediately available for use.

## Usage
The timezone and location are fetched from your Home Assistant configuration.
This app adds two sensors exposing Molad details for the upcoming Jewish Month:

1. `sensor.molad` with the upcoming Molad as the value and more detailed properties as attributes
2. `sensor.is_shabbos_mevorchim` - `true` if today is Shabbos Mevorchim, `false` if not
