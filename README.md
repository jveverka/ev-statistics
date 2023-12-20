# EV statistics calculations

Simple script to calculate EV trip statistics for a single trip data file recorder using [Car Scanner ELM OBD2](https://play.google.com/store/apps/details?id=com.ovz.carscanner&hl=en&gl=US) 
app connected to EV via [ELM327](https://www.alza.sk/mobilly-obd-ii-bt-d4624328.htm) OBD bluetooth adapter. One CSV file is one trip.

To calculate statistics from data file:
```
./ev-stats.py <data-file.csv>
```

## Actual Stats Calculations

| Variable        | Description                                                        |
|-----------------|--------------------------------------------------------------------|
| trip total time | total driving time (may include parking or waiting time)           |
| power consumed  | total power consumtion for the trip in kWh                         |
| trip distance   | trip distance in km                                                |
| avg. speed      | average trip speed in km/h                                         |
| avg. consumtion | average power consumption in kWh per 100km for the trip conditions |
| avg. amb. temp. | average ambient temperature in ℃                                   |
| avg. bat. temp. | average battery temperature in ℃                                   |
| battery SoH     | battery State of Health for the trip in %                          |
| max battery cap.| estimated max. battery capacity for the trip in kWh                |
| max range estim.| estimated max. range for the trip conditions in km                 |

* [Peugeot e-208 GT 2022](Peugeot_e-208_data/README.md)



