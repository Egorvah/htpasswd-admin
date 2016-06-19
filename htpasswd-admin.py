#!/usr/bin/python3
# Hello world python program

print("Htpasswd Admin - v. 0.1.0");

# File list

import glob, os, sys

class User:

	login = ""
	password = ""
	active = True

	def __init__(self, path, index = None):
		self.path = path
		self.index = index

		with open(self.path) as f:
			userList = f.readlines()
			userData = userList[self.index]

			self.login = userData.split(':')[0]
			self.password = userData.split(':')[1]
	
	def changePassword(self, password):
		print(password)

	def save(self):
		print("save user")
			


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
			tableData.append([index, user.login])

		from terminaltables import AsciiTable
		table = AsciiTable(tableData)
		print(table.table)


	def actions(self):
		actionList = ['add user', 'change password', 'disable/enable user', 'delete user']
		for index, action in enumerate(actionList):
			print("[" + str(index) + "]" + " " + action)

		actionIndex = inputIndex(None, 'Plese input action number')
		print(actionIndex)

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

	for index, file in enumerate(glob.glob(".htpasswd") + glob.glob("*.htpasswd")):
		fileObject = Htpasswd(file)
		files.append(fileObject)
		tableData.append([index, fileObject.path])


	from terminaltables import AsciiTable
	table = AsciiTable(tableData)
	print(table.table)
	
	fileIndex = inputIndex(0)
	files[fileIndex].printUsers()
	files[fileIndex].actions()



scan()
