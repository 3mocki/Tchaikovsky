from CalAQI import *
from Sender import *

# for a hour
class Average_1:
    calAqiNo2 = 0
    calAqiO3 = 0
    calAqiSo2 = 0

    avg_no2 = 0
    avg_o3 = 0
    avg_so2 = 0

    past_no2 = 0
    past_o3 = 0
    past_so2 = 0

    def insertData(self, no2, o3, so2, i, m):
        recent_no2 = no2
        recent_o3 = o3
        recent_so2 = so2

        if i == 0:
            self.avg_no2 = recent_no2
            self.avg_o3 = recent_o3
            self.avg_so2 = recent_so2

            self.calAqiNo2 = int(no2Aqi(self.avg_no2))
            self.calAqiO3 = int(o3Aqi_1(self.avg_o3))
            self.calAqiSo2 = int(so2Aqi(self.avg_so2))

            air_sender[i][14] = self.calAqiNo2
            air_sender[i][13] = self.calAqiO3
            air_sender[i][15] = self.calAqiSo2

            self.past_no2 = recent_no2
            self.past_o3 = recent_o3
            self.past_so2 = recent_so2

        elif 1 <= i < 3600:

            self.avg_no2 = ((i+1)*self.avg_no2 + recent_no2 - self.past_no2) / (i + 1)
            self.avg_o3 = ((i+1)*self.avg_o3 + recent_o3 - self.past_o3) / (i + 1)
            self.avg_so2 = ((i+1)*self.avg_so2 + recent_so2 - self.past_so2) / (i + 1)

            self.past_no2 = recent_no2
            self.past_o3 = recent_o3
            self.past_so2 = recent_so2

            self.calAqiNo2 = int(no2Aqi(self.avg_no2))
            self.calAqiO3 = int(o3Aqi_1(self.avg_o3))
            self.calAqiSo2 = int(so2Aqi(self.avg_so2))

            if i % 10 == m:
                air_sender[m][14] = self.calAqiNo2
                air_sender[m][13] = self.calAqiO3
                air_sender[m][15] = self.calAqiSo2

        # After 1 hour
        elif 3600 <= i < 28800:
            for x in range(0, 2):
                if x == 0:
                    self.avg_no2 = ((i + 1) * self.avg_no2 + recent_no2 - self.past_no2) / (i + 1)
                    self.calAqiNo2 = int(no2Aqi(self.avg_no2))
                elif x == 1:
                    self.avg_o3 = ((i + 1) * self.avg_o3 + recent_o3 - self.past_o3) / (i + 1)
                    self.calAqiO3 = int(o3Aqi_1(self.avg_o3))
                elif x == 2:
                    self.avg_so2 = ((i + 1) * self.avg_so2 + recent_so2 - self.past_so2) / (i + 1)
                    self.calAqiSo2 = int(so2Aqi(self.avg_so2))
            if i % 10 == m:
                air_sender[m][12] = self.calAqiNo2
                air_sender[m][13] = self.calAqiO3
                air_sender[m][15] = self.calAqiSo2

            self.past_no2 = recent_no2
            self.past_o3 = recent_o3
            self.past_so2 = recent_so2

        elif i > 28800:
            for x in range(0, 1):
                if x == 0:
                    self.avg_no2 = ((i+1)*self.avg_no2 + recent_no2 - self.past_no2) / (i + 1)
                    self.calAqiNo2 = int(no2Aqi(self.avg_no2))
                elif x == 1:
                    self.avg_so2 = ((i+1)*self.avg_so2 + recent_so2 - self.past_so2) / (i + 1)
                    self.calAqiSo2 = int(so2Aqi(self.avg_so2))
            if i % 10 == m:
                air_sender[m][14] = self.calAqiNo2
                air_sender[m][15] = self.calAqiSo2

            self.past_no2 = recent_no2
            self.past_so2 = recent_so2
