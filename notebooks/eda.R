# RStudio EDA (spec tool checklist) — run after generating data
d <- read.csv("data/raw/climate_records.csv")
summary(d); aggregate(temperature_c ~ station, data=d, mean)
plot(d$temperature_c, d$co2_ppm, main="Temp vs CO2", xlab="Temp C", ylab="CO2 ppm")
