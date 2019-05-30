from CalAQI import *
from Sender import *

#for 24 hours
class Average_24:
    calAqiPm25 = 0
    calAqiPm10 = 0

    avg_pm25 = 0
    avg_pm10 = 0

    past_pm25 = 0
    past_pm10 = 0

    def insertData(self, pm25, pm10, i, m):
        recent_pm25 = pm25
        recent_pm10 = pm10

        if i == 0:
            self.avg_pm25 = recent_pm25
            self.avg_pm10 = recent_pm10

            self.calAqiPm25 = int(pm25Aqi(self.avg_pm25))
            self.calAqiPm10 = int(pm10Aqi(self.avg_pm10))

            air_sender[i][16] = int(pm25Aqi(self.avg_pm25))
            air_sender[i][17] = int(pm10Aqi(self.avg_pm10))

            self.past_pm25 = recent_pm25
            self.past_pm10 = recent_pm10

        elif 1 <= i < 86400:
            self.avg_pm25 = ((i+1)*self.avg_pm25 + recent_pm25 - self.past_pm25) / (i + 1)
            self.avg_pm10 = ((i+1)*self.avg_pm10 + recent_pm10 - self.past_pm10) / (i + 1)

            self.calAqiPm25 = int(pm25Aqi(self.avg_pm25))
            self.calAqiPm10 = int(pm10Aqi(self.avg_pm10))

            self.past_pm25 = recent_pm25
            self.past_pm10 = recent_pm10

        # based on a day
        elif i >= 86400:
            for x in range(0, 2):
                if x == 0:
                    self.avg_pm25 = ((i+1)*self.avg_pm25 + recent_pm25 - self.past_pm25) / (i + 1)
                    self.calAqiPm25 = int(pm25Aqi(self.avg_pm25))
                elif x == 1:
                    self.avg_pm10 = ((i+1)*self.avg_pm10 + recent_pm10 - self.past_pm10) / (i + 1)
                    self.calAqiPm10 = int(pm10Aqi(self.avg_pm10))

            self.past_pm25 = recent_pm25
            self.past_pm10 = recent_pm10

        if i % 10 == m:
            air_sender[m][16] = self.calAqiPm25
            air_sender[m][17] = self.calAqiPm10