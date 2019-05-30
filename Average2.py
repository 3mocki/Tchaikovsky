from CalAQI import *
from Sender import *

# for 8 hours
class Average_8:
    calAqiO3 = 0
    calAqiCo = 0

    avg_co = 0
    avg_o3 = 0

    past_co = 0
    past_o3 = 0

    def insertData(self, o3, co, i, m):
        recent_o3 = o3
        recent_co = co

        if i == 0:
            self.avg_co = recent_co
            self.calAqiCo = int(coAqi(self.avg_co))
            air_sender[i][12] = self.calAqiCo
            self.past_co = recent_co

        # before 8 hours
        elif 1 <= i < 28800:
            self.avg_co = ((i + 1) * self.avg_co + recent_co - self.past_co) / (i + 1)
            self.calAqiCo = int(coAqi(self.avg_co))
            if i % 10 == m:
                air_sender[m][12] = self.calAqiCo

            self.past_co = recent_co

        # after 8 hours
        elif i >= 28800:
            for x in range(0, 2):
                if x == 0:
                    self.avg_o3 = ((i + 1) * self.avg_o3 + recent_o3 - self.past_o3) / (i + 1)
                    self.calAqiO3 = int(o3Aqi_8(self.avg_o3))
                elif x == 1:
                    self.avg_co = ((i + 1) * self.avg_co + recent_co - self.past_co) / (i + 1)
                    self.calAqiCo = int(coAqi(self.avg_co))

            if i % 10 == m:
                air_sender[m][13] = self.calAqiO3
                air_sender[m][12] = self.calAqiCo

            self.past_o3 = recent_o3
            self.past_co = recent_co