# Molad Sensor
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)


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
This app adds three sensors exposing Molad details for the upcoming Jewish Month:

1. `sensor.molad` with the upcoming Molad as the value and more detailed properties as attributes:

| Attribute      | Description | Example |
| ----------- | ----------- | --- |
| day | Day of the week of the next Molad occurence | Sunday |
| hours | Hour of the next Molad occurence | 3 |
| minutes | Minutes of the next Molad occurence | 36 |
| am_or_pm | AM/PM of the next Molad occurence | pm |
| chalakim | Chalakim of the next Molad occurence | 15 |
| friendly | Human readable text of the next Molad occurence | Sunday, 3:36 pm and 15 chalakim |
| rosh_chodesh | Days of the week of next Rosh Chodesh | Monday & Tuesday |
| rosh_chodesh_days | List of days of the week of next Rosh Chodesh | Monday, Tuesday |
| rosh_chodesh_dates | List of dates of next Rosh Chodesh | 2024-12-31, 2025-01-01 |
| is_shabbos_mevorchim |  `true` if today is Shabbos Mevorchim, `false` if not | false |
| is_upcoming_shabbos_mevorchim |  `true` if the upcoming Shabbos is Shabbos Mevorchim, `false` if not | false |
| month_name | Month name of next Rosh Chodesh | Tammuz |

2. `sensor.is_shabbos_mevorchim` - `true` if today is Shabbos Mevorchim, `false` if not

3. `sensor.is_upcoming_shabbos_mevorchim` - `true` if the upcoming Shabbos is Shabbos Mevorchim, `false` if not (known limitation: this sensor works purely on secular days of the week and will count the upcoming Shabbos from Sunday and not Motzei Shabbos)