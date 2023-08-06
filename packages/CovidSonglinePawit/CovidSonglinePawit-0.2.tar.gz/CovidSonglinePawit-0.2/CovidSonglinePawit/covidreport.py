import requests as req
import json
from songline import Sendline


class report():
	"""docstring for __init__"""
	def __init__(self ,token):
		self.url = 'https://covid19.th-stat.com/api/open/today'
		self.token = token
		self.detail = req.get(self.url).json()
		self.text = (' จำนวนคนที่ติดเชื้อเพิ่มขึ้นในประเทศไทย {} คน\n ติดเชื้อสะสม {} คน\n Update: {}'.format(self.detail['NewConfirmed'],self.detail['Confirmed'],self.detail['UpdateDate']))
		print(self.text)

	def sendline(self):
		Sendline(self.token).sendtext(self.text)

if __name__ == '__main__':
	token = '2fbPbPL1GzyUNpRgDukn24DALZq1qc88r1TfZCV5AUR'
	re = report(token)
	re.sendline()

