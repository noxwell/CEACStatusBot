from .handle import NotificationHandle
from CEACStatusBot.request import query_status
from CEACStatusBot.captcha import CaptchaHandle,OnnxCaptchaHandle

class NotificationManager():
    def __init__(self,location:str,number:str,passport_number:str,surname:str,captchaHandle:CaptchaHandle=OnnxCaptchaHandle("captcha.onnx")) -> None:
        self.__handleList = []
        self.__location = location
        self.__number = number
        self.__captchaHandle = captchaHandle
        self.__passport_number = passport_number
        self.__surname = surname

    def addHandle(self, notificationHandle:NotificationHandle) -> None:
        self.__handleList.append(notificationHandle)

    def send(self,) -> None:
        res = query_status(self.__location, self.__number, self.__passport_number, self.__surname, self.__captchaHandle)

        if 'status' not in res:
            print(f'Response does not contain status. Available fields: {list(res.keys())}')
            return
        elif res['status'] == "Refused":
            import os,pytz,datetime
            try:
                TIMEZONE = os.environ["TIMEZONE"]
                localTimeZone = pytz.timezone(TIMEZONE)
                localTime = datetime.datetime.now(localTimeZone)
            except pytz.exceptions.UnknownTimeZoneError:
                print("UNKNOWN TIMEZONE Error, use default")
                localTime = datetime.datetime.now()
            except KeyError:
                print("TIMEZONE Error")
                localTime = datetime.datetime.now()

            if localTime.hour < 8 or localTime.hour > 22:
                print(f"In Manager: it is {localTime}, which is between 22:00 and 08:00. Not sending notification because of do not disturb.")
                return

        for notificationHandle in self.__handleList:
            notificationHandle.send(res)
