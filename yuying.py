import pythoncom
from win32com import client

pythoncom.CoInitialize()
engine = client.Dispatch("SAPI.SpVoice")
#可以语言读出来
engine.Speak('hello world')
engine.Speak('新北市十二年國民基本教育資訊網')
engine.Speak('クローラ')