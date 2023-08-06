#studentclass.py

class Student:
	def __init__(self,name):
		self.name = name
		self.exp = 0
		self.lesson = 0
		#self.AddEXP(10) #call function

	def Hello(self):
		print('Hello!!!!! My name is {}.'.format(self.name) )

	def Coding(self):
		print('{}:--Coding--'.format(self.name))
		self.exp += 5
		self.lesson += 1

	def ShowEXP(self):
		print('- {} has {} EXP'.format(self.name,self.exp))
		print('- Learn {} time'.format(self.lesson))


	def AddEXP(self,score):
		self.exp += score #self.exp = student1.exp + 10
		self.lesson += 1

#class SpecialScore():
	
#	def __init__(self):
#		self.score = 500

class SpecialStudent(Student):

	def __init__(self,name,father):
		super().__init__(name)
		self.father = father
		mafia = ['Bill Gates','Thomas Edison']
		if father in mafia:
			self.exp += 100

	def AddEXP(self,score):
		self.exp += (score * 3)
		self.lesson += 1

	def AskEXP(self,score=10):
		print('I want special score. {} EXP'.format(score))
		self.AddEXP(score)


if __name__ == '__main__':
	
	print('=======1 Jan ========')
	student0 = SpecialStudent('Mark Zukerberg','Bill Gates')
	student0.ShowEXP()
	student0.AskEXP()
	student0.ShowEXP()
	student1 = Student('Albert')
	print(student1.name)
	student1.Hello()

	print('--------------------')

	student2 = Student('Steve')
	print(student2.name)
	student2.Hello()
	print('=======2 Jan ========')
	print('-------Uncle: Who want to learn coding?---(10 exp)---')


	print('=======3 Jan ========')
	student1.name = 'Albert Einstein'
	print('Now exp of each people:')
	student1.AddEXP(10)
	print(student1.name,student1.exp)
	print(student2.name,student2.exp)

	print('=======4 Jan ========')

	for i in range(5):
		student2.Coding()

	student1.ShowEXP()
	student2.ShowEXP()

	print('--------------------')