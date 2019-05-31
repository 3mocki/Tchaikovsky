import requests, json, time, csv
from Msgtype import *
from ResultCode import *
from globalVar import *
from Sender2 import *
from Sender3 import *
from State import *

class RAD_class:
    currentState_4 = CID_INFORMED_STATE
    sspRadTrnRetries = 0
    row = [[], [], [], [], [], [], [], [], [], []]
    lost = []

    # msgHeader[0]
    msgtype = SSP_RADTRN

    # Collect per 1 sec
    payload = {
        "airQualityDataListEncodings": {
            "dataTupleLen": '10',
            "airQualityDataTuples": row
        }
    }

    # msgHeader[3:5]
    eId = ""

    def fnPackSspRadTrn(self):
        packedMsg = {
            "header": {
                "msgType": self.msgtype,
                "msgLen": len(str(self.payload)),
                "endpointId": self.eId
            },
            "payload": self.payload
        }
        return packedMsg

    def fnSendSspRadTrn(self):
        global rt
        print("| SEN | SET | RAD STATE | " + str(self.currentState_4) + "=> CID INFORMED STATE")
        if self.fnPackSspRadTrn() == None:
            print("NULL in row.")
            quit()

        else:
            response = requests.post(url_2, json=self.fnPackSspRadTrn())
            print("| SEN | SEND| REQ | SSP:RAD-REQ | " + str(self.fnPackSspRadTrn()))
            self.stateChange()
            print("| SEN | SET | RAD STATE | " + str(self.currentState_4))
            rt = response.elapsed.total_seconds()
            print('Response Time : ' + str(rt) + 'sec')

            t = response.json()
            print("| SEN | RCVD| RSP | " + str(t))
            data = response.text
            self.json_response = json.loads(data)


    def fnReceiveMsg(self):
        global rt
        if rt > 10:
            print("Response time is exceeded 5 sec")
            self.sspRadTrnRetries += 1
            if self.sspRadTrnRetries == 5:
                self.stateChange_2()
                print("| SEN | SET | RAD STATE | " + str(self.currentState_4) + "=> IDLE State")
                quit()
            else:
                self.fnReceiveMsg()
        else:
            self.verifyMsgHeader()
            if rcvdPayload != RES_FAILED:
                return rcvdPayload
            else:
                self.fnReceiveMsg()

    def verifyMsgHeader(self):
        global rcvdPayload
        rcvdType = self.json_response['header']['msgType']  # rcvdMsgType
        rcvdPayload = self.json_response['payload']
        # rcvdLength = len(str(self.rcvdPayload)) # rcvdLenOfPayload
        rcvdeId = self.json_response['header']['endpointId']  # rcvdEndpointId
        # expLen = rcvdLength - msg.header_size

        if rcvdeId == self.eId:
            stateCheckResult = self.stateChange_3
            if stateCheckResult == RES_SUCCESS:
                if rcvdType == self.msgtype:
                    # if rcvdLength == expLen:
                    return rcvdPayload
        else:
            return RES_FAILED

    def UnpackMsg(self):
        if self.json_response['payload']['retransReqFlg'] == 1:
            for i in range():
                self.lost[i] = self.json_response['payload']['listOfUnsuccessfulTs'][i]
            for x in air_sender_2():
                if self.lost[x] == air_sender_2[x][0]:
                    air_sender_3[x][0] = self.lost[x]
                    air_sender_3[x][1] = air_sender_2[x][1]
                    air_sender_3[x][2] = air_sender_2[x][2]
                    air_sender_3[x][3] = air_sender_2[x][3]
                    air_sender_3[x][4] = air_sender_2[x][4]
                    air_sender_3[x][5] = air_sender_2[x][5]
                    air_sender_3[x][6] = air_sender_2[x][6]
                    air_sender_3[x][7] = air_sender_2[x][7]
                    air_sender_3[x][8] = air_sender_2[x][8]
                    air_sender_3[x][9] = air_sender_2[x][9]
                    air_sender_3[x][10] = air_sender_2[x][10]
                    air_sender_3[x][11] = air_sender_2[x][11]
                    air_sender_3[x][12] = air_sender_2[x][12]
                    air_sender_3[x][13] = air_sender_2[x][13]
                    air_sender_3[x][14] = air_sender_2[x][14]
                    air_sender_3[x][15] = air_sender_2[x][15]
                    air_sender_3[x][16] = air_sender_2[x][16]
                    air_sender_3[x][17] = air_sender_2[x][17]
        else:
            pass

    def stateChange(self):
        self.currentState_4 = 'CID_INFORMED_STATE'
        return self.currentState_4

    def stateChange_2(self):
        if self.currentState_4 == 'CID_INFORMED_STATE':
            self.currentState_4 = IDLE_STATE

        return self.currentState_4

    def stateChange_3(self):
        if self.currentState_4 == 'CID_INFORMED STATE':
            return True

    def read_RAD(self):

        f = open('temp_RAD.csv', 'r')
        rad_data = csv.reader(f)

        # It is current data from the Sensor
        for idx, line in enumerate(rad_data):
            air_sender_2[idx][0] = int(line[0])
            air_sender_2[idx][5] = float(line[5])
            air_sender_2[idx][6] = float(line[6])
            air_sender_2[idx][7] = float(line[7])
            air_sender_2[idx][8] = float(line[8])
            air_sender_2[idx][9] = float(line[9])
            air_sender_2[idx][10] = float(line[10])
            air_sender_2[idx][11] = float(line[11])
            air_sender_2[idx][12] = int(line[12])
            air_sender_2[idx][13] = int(line[13])
            air_sender_2[idx][14] = int(line[14])
            air_sender_2[idx][15] = int(line[15])
            air_sender_2[idx][16] = int(line[16])
            air_sender_2[idx][17] = int(line[17])

        f.close()


    def init(self):

        self.read_RAD()

        for x in range(0, 10):
            self.row[x] = air_sender_2[x]
            print('RAD_class self.row[' + str(x) + '] => ' + str(self.row[x]))

        self.fnPackSspRadTrn()
        self.fnSendSspRadTrn()
        self.fnReceiveMsg()
        self.UnpackMsg()
