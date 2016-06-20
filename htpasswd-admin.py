#!/usr/bin/python3

import glob, os, getpass, sys, crypt 

print(" \nHtpasswd Admin - v. 0.1.0");
print("==========================\n");


class User:

	login = ""
	password = ""
	active = True

	def __init__(self, path, index = None):
		self.path = path
		self.index = index
		if self.index is not None:
			with open(self.path) as f:
				userList = f.readlines()
				userData = userList[self.index]

				self.login = userData.split(':')[0]
				self.password = userData.split(':')[1]

				if self.login[:1] == '#':
					self.login = self.login.replace("#", "")
					self.active = False
	
	def getLoginWithColor(self):
		colorLogin = ""

		if self.active is False:
			colorLogin += "\033[91m"
		else:
			colorLogin += "\033[92m"

		colorLogin += self.login
		colorLogin += "\033[0m"

		return colorLogin

	def create(self):
		self.login = input("Please enter user name : ")
		self.changePassword(True)
		self.save()

	def delete(self):
		with open(self.path) as f:
			userList = f.readlines()
			userList.remove(userList[self.index])

			with open(self.path, 'w') as file:
				for userData in userList:
					file.write("%s\n" % userData.replace("\n", ""))



	def changePassword(self, withoutSave = False):
		password = getpass.getpass("Please enter new password (hidden) : ")
		self.password = crypt.crypt(password, "$6$saltsalt$")
		if withoutSave == False:
			self.save()

	def activeToggle(self):
		self.active = not self.active
		self.save()

	def save(self):
		line = ""

		if self.active is False:
			line += "#"

		line += self.login + ":" + self.password
		
		with open(self.path) as f:
			userList = f.readlines()

			if self.index is None:
				userList.append(line)
			else:
				userList[self.index] = line

			with open(self.path, 'w') as file:
				for userData in userList:
					file.write("%s\n" % userData.replace("\n", ""))

class Htpasswd:

	users = []

	def __init__(self, path):
		self.path = path
		self.scanUsers()

	def scanUsers(self):
		
		with open(self.path) as f:
			userList = f.readlines()
			for index, user in enumerate(userList):
				self.users.append(User(self.path, index))

	
	def printUsers(self):
		tableData = [['Index', 'User']]
		for index, user in enumerate(self.users):
			tableData.append([index, user.getLoginWithColor()])

		from terminaltables import AsciiTable
		table = AsciiTable(tableData)
		print(table.table)


	def actions(self):
		actionList = ['add user', 'change password', 'disable/enable user', 'delete user']
		for index, action in enumerate(actionList):
			print("[" + str(index) + "]" + " " + action)

		actionIndex = inputIndex(None, 'Plese input action number')
		print(actionIndex)

		
		if actionIndex == 0:
			user = User(self.path)
			user.create()
			return False

		user = self.users[inputIndex()]

		if actionIndex == 1:
			user.changePassword()

		if actionIndex == 2:
			user.activeToggle()

		if actionIndex == 3:
			user.delete()

	def addUser(self):
		print("add user to file")

	

def inputIndex(defaultVal = None, title = None):

	if title is None:
		title = "Enter index"


	titleDefaultVal = ""
	if defaultVal is not None:
		titleDefaultVal += "(default " + str(defaultVal) + ") : "

	index = input(title + " : " + titleDefaultVal)
	
	if not index and defaultVal is not None:
		index = defaultVal

	try:
		index = int(index)
		return index
	except ValueError:
		print("Please input number!")
		return inputIndex(defaultVal, title)



def scan():
	files = []
	tableData = [['Index', 'File name']] 

	foundFiles = glob.glob(".htpasswd") + glob.glob("*.htpasswd")
	
	for index, file in enumerate(foundFiles):
		fileObject = Htpasswd(file)
		files.append(fileObject)
		tableData.append([index, fileObject.path])


	if len(foundFiles) == 0:
		print("Not found file(s) *.htpasswd")
		return False
	elif len(foundFiles) == 1:
		fileIndex = 0
	else:
		from terminaltables import AsciiTable
		table = AsciiTable(tableData)
		print(table.table)
	
		fileIndex = inputIndex(0)

	files[fileIndex].printUsers()
	files[fileIndex].actions()



scan()
