# studentclass.py

class Student:
	def __init__(self,name):
		# self แทนตัวแปล
		# name คือตัวแปรที่ใส่เพิ่มเข้าไป
		self.name = name
		self.exp = 0
		self.lesson = 0
		# student1.name
		# self = student1

		#Call Function()
		#self.AddExp(10)

	def Hello(self):
		print('Hello World, My name is {}.'.format(self.name))
		#self สามารถดึง input จาก __init__ ได้หมดเลย

	def Coding(self):
		print('{}: กำลังเขียนโปรแกรม.'.format(self.name))
		self.exp += 5
		self.lesson += 1

	def ShowEXP(self):
		print('- {} มีประสบการณ์ {} EXP'.format(self.name,self.exp))
		print('- เรียนไป {} ครั้งแล้ว'.format(self.lesson))

	def AddExp(self, score):
		self.exp += score
		self.lesson += 1

class SpecialScore():
	def __init__(self):
		self.score = 500
		
		

class SpecialStudent(Student):

	def __init__(self,name,father):
		super().__init__(name)
		self.father = father
		mafia = ['Bill Gates','Thomas Edison']
		if father in mafia:
			self.exp += 100
	
	def AddExp(self, score):
		self.exp += score * 3
		self.lesson += 1

	def AskEXP(self,score=10):
		print('ครู!! ขอคะแนนให้ผมหน่อยสิสัก {} EXP'.format(score))
		self.AddExp(score)

if __name__ == '__main__':
	
	print('=========2021, 1 Jan=========')

	student0 = SpecialStudent('Mark Zuckerberg','Bill Gates')
	student0.ShowEXP()
	student0.AskEXP(200)
	student0.ShowEXP()

	student1 = Student('Pawit')
	print(student1.name)
	student1.Hello()


	print('-------------')
	student2 = Student('Steve')
	print(student2.name)
	student2.Hello()
	print('=========2021, 2 Jan=========')
	print('------ใครอยากเรียน coding บ้าง---(10 exp)---')
	student1.AddExp(10)

	print('=========2021, 3 Jan=========')

	print('ตอนนี้ exp ของแต่ละคนได้เท่าไหร่กันแล้ว')

	print(student1.name, student1.exp)
	print(student2.name, student2.exp)

	print('=========2021, 4 Jan=========')

	for i in range(5):
		student2.Coding()

	# print('- {} มีประสบการณ์ {} EXP\n- เรียนไป {} ครั้ง'.format(student2.name,student2.exp,student2.lesson))
	student1.ShowEXP()
	student2.ShowEXP()