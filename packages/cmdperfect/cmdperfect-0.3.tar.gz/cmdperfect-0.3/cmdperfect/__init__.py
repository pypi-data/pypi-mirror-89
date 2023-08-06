import os
import time
from numba import prange
import random
from . import fonts
from . import models
os.system("cls")
symbols_list = []
class Screen():
	def __init__(self,rows=10,columns=10,main_symbol=" "):
		self.main_symbol=main_symbol
		self.rows = rows
		self.columns = columns
		self.symbols_list = []
		symbols_list = []
		for r in prange(self.rows):
			for c in prange(self.columns):
				symbol_dict={"row":r, "column":c, "main_symbol":self.main_symbol}
				symbols_list.append(symbol_dict)
		self.symbols_list = symbols_list
		self.main_symbol = main_symbol
		symbols_list = []
		for r in prange(self.rows):
			for c in prange(self.columns):
				symbol_dict={"row":r, "column":c, "symbol":self.main_symbol}
				symbols_list.append(symbol_dict)
		self.symbols_list = symbols_list

	# Change size
	def ChangeSize(self,rows,columns):
		self.rows = rows
		self.columns = columns
		symbols_list = []
		for r in prange(self.rows):
			for c in prange(self.columns):
				symbol_dict={"row":r, "column":c, "main_symbol":self.main_symbol}
				symbols_list.append(symbol_dict)
		self.symbols_list = symbols_list

	# Make border arguments(border_size,symbol,border_width,border_height)
	def ChangeBorder(self,border_size=1,symbol='█',**kwargs):
		border_width=border_size
		border_height=border_size
		if 'border_width' in kwargs:
			border_width=kwargs['border_width']
		if 'border_height' in kwargs:
			border_height=kwargs['border_height']
			


		symbols_list = self.symbols_list
		for l in prange(len(symbols_list)):
			if (((symbols_list[l]['row']>=0) and (symbols_list[l]['row']<=border_height-1)) or ((symbols_list[l]['row']<=self.rows) and (symbols_list[l]['row']>=(self.rows-border_height)))) or (((symbols_list[l]['column']>=0) and (symbols_list[l]['column']<=border_width-1)) or ((symbols_list[l]['column']<=self.columns) and (symbols_list[l]['column']>=(self.columns-border_width)))):
				symbols_list[l]['symbol'] = symbol
		self.symbols_list = symbols_list


	# Set main symbol
	def MainSymbol(self,main_symbol):
		self.main_symbol = main_symbol
		symbols_list = []
		for r in prange(self.rows):
			for c in prange(self.columns):
				symbol_dict={"row":r, "column":c, "symbol":self.main_symbol}
				symbols_list.append(symbol_dict)
		self.symbols_list = symbols_list

	# Change symbol selcting row and column
	def ChangeSymbol(self,row,column,symbol):
		symbols_list = self.symbols_list
		for l in prange(len(symbols_list)):
			if (symbols_list[l]['row'] == row-1) and (symbols_list[l]['column'] == column-1):
				symbols_list[l]['symbol'] = symbol
		self.symbols_list = symbols_list

	# Change symbols in list 
	def ChangeSymbols(self,symbols): 
		symbols_list = self.symbols_list
		for symb in symbols:
			row=symb[0]
			column=symb[1]
			symbol=symb[2]
			for l in prange(len(symbols_list)):
				if (symbols_list[l]['row'] == row-1) and (symbols_list[l]['column'] == column-1):
					symbols_list[l]['symbol'] = symbol
		self.symbols_list = symbols_list

	# Change all symbols in row
	def ChangeRow(self,row,symbol):
		symbols_list = self.symbols_list
		for l in prange(len(symbols_list)):
			if (symbols_list[l]['row'] == row-1):
				symbols_list[l]['symbol'] = symbol
		self.symbols_list = symbols_list

	# Change all symbols in column
	def ChangeColumn(self,column,symbol):
		symbols_list = self.symbols_list
		for l in prange(len(symbols_list)):
			if (symbols_list[l]['column'] == column-1):
				symbols_list[l]['symbol'] = symbol
		self.symbols_list = symbols_list

	# Change all rectangle symbols
	def MakeRectangle(self,a,b,symbol=" "):
		if a[0]>=b[0]:
			x1=b[0]
			x2=a[0]
		else:
			x1=a[0]
			x2=b[0]
		if a[1]>=b[1]:
			y1=b[1]
			y2=a[1]
		else:
			y1=a[1]
			y2=b[1]
		symbols = []
		for y in prange(x1,x2+1):
			for x in prange(y1,y2+1):
				second_list = [y,x,symbol]
				symbols.append(second_list)


		symbols_list = self.symbols_list
		for symb in symbols:
			row=symb[0]
			column=symb[1]
			symbol=symb[2]
			for l in prange(len(symbols_list)):
				if (symbols_list[l]['row'] == row-1) and (symbols_list[l]['column'] == column-1):
					symbols_list[l]['symbol'] = symbol
		self.symbols_list = symbols_list

	# Make a Rhombus
	def MakeRhombus(self,center,symbol):
		r = 2
		symbols_list = self.symbols_list
		list_symbols = []
		list_1 = []
		i = 0
		for pos in prange(center[0]-r,center[1]-1):
			list_1 = []
			row = pos
			column = center[1] + i
			list_1.append(row)
			list_1.append(column)
			list_1.append(symbol)
			list_symbols.append(list_1)
			list_1 = []
			row = pos
			column = center[1] - i
			list_1.append(row)
			list_1.append(column)
			list_1.append(symbol)
			list_symbols.append(list_1)
			if row <= center[0]+r:
				i += 1
			if row > center[0]+r:
				i -= 1

		for symb in list_symbols:
			row=symb[0]
			column=symb[1]
			symbol=symb[2]
			for l in prange(len(symbols_list)):
				if (symbols_list[l]['row'] == row-1) and (symbols_list[l]['column'] == column-1):
					symbols_list[l]['symbol'] = symbol
		self.symbols_list = symbols_list

				


	# Move object
	def move(self,object2,position,step,symbol=" "):
		list_main = []
		new_list = []
		# For moving left 
		if position == 'left':
			for symb in object2:
				new_list.append(symb[0])
				new_list.append(symb[1])
				new_list.append(symbol)
				list_main.append(new_list)	
				new_list = []
			for symb in object2:
				new_list.append(symb[0])
				new_list.append(symb[1]-step)
				new_list.append(symb[2])
				list_main.append(new_list)	
				new_list = []
		# For moving right
		if position == 'right':
			for symb in object2:
				new_list.append(symb[0])
				new_list.append(symb[1])
				new_list.append(symbol)
				list_main.append(new_list)	
				new_list = []
			for symb in object2:
				new_list.append(symb[0])
				new_list.append(symb[1]+step)
				new_list.append(symb[2])
				list_main.append(new_list)	
				new_list = []
		# For moving up
		if position == 'up':
			for symb in object2:
				new_list.append(symb[0])
				new_list.append(symb[1])
				new_list.append(symbol)
				list_main.append(new_list)	
				new_list = []
			for symb in object2:
				new_list.append(symb[0]-step)
				new_list.append(symb[1])
				new_list.append(symb[2])
				list_main.append(new_list)	
				new_list = []
		# For moving down
		if position == 'down':
			for symb in object2:
				new_list.append(symb[0])
				new_list.append(symb[1])
				new_list.append(symbol)
				list_main.append(new_list)	
				new_list = []
			for symb in object2:
				new_list.append(symb[0]+step)
				new_list.append(symb[1])
				new_list.append(symb[2])
				list_main.append(new_list)	
				new_list = []
		symbols_list = self.symbols_list
		for symb in list_main:
			row=symb[0]
			column=symb[1]
			symbol=symb[2]
			for l in prange(len(symbols_list)):
				if (symbols_list[l]['row'] == row-1) and (symbols_list[l]['column'] == column-1):
					symbols_list[l]['symbol'] = symbol
		self.symbols_list = symbols_list


		# Make text in screen
	def WriteString(self,text,row= 0,column= 0):
		x=0
		list_of_letters = []
		for i in text:
			list_new=[]
			list_new.append(row)
			list_new.append(column+x)
			list_new.append(i)
			list_of_letters.append(list_new)
			x += 1
		symbols_list = self.symbols_list
		for symb in list_of_letters:
			row=symb[0]
			column=symb[1]
			symbol=symb[2]
			for l in prange(len(symbols_list)):
				if (symbols_list[l]['row'] == row-1) and (symbols_list[l]['column'] == column-1):
					symbols_list[l]['symbol'] = symbol
		self.symbols_list = symbols_list

	def WriteText(self,text,row=0,column=0,remove_background=True):
		if remove_background==True:
			text = text.replace(' ',self.main_symbol)
		symbols_list = self.symbols_list
		x=0
		list_of_letters = []
		symbols = []
		add_row = row
		add_column = column
		for item in text:
			if item =="\n":
				add_row+=1
				add_column=column
				list_for_symbol = []
			else:
				list_for_symbol=[]
				list_for_symbol.append(add_row)				
				list_for_symbol.append(add_column)				
				list_for_symbol.append(item)
				symbols.append(list_for_symbol)
				add_column+=1	
		
		symbols_list = self.symbols_list
		for symb in symbols:
			row=symb[0]
			column=symb[1]
			symbol=symb[2]
			for l in prange(len(symbols_list)):
				if (symbols_list[l]['row'] == row-1) and (symbols_list[l]['column'] == column-1):
					symbols_list[l]['symbol'] = symbol
		self.symbols_list = symbols_list





	# Setup terminal and text color 
	def color(self,bgcolor="black",fgcolor="white"):
		dict_of_colors = {
		"black" : "0",
		"blue" : "1",
		"green" : "2",
		"aqua" : "3",
		"red" : "4",
		"purple" : "5",
		"yellow" : "6",
		"white" : "7",
		"gray" : "8",
		"LightBlue" : "9",
		"LightGreen" : "A",
		"LightAqua" : "B",
		"LightRed" : "C",
		"LightPurple" : "D",
		"LightYellow" : "E",
		"BrightWhite" : "F",}
		color = "color " + dict_of_colors[bgcolor] + dict_of_colors[fgcolor]
		os.system(color)

	# Random Screen
	def Fill(self,style,**kwargs):
		style = style.lower()
		if style=='random':
			example_list=["█░ ","0oO",'1IilL|','\\/|','███ ','1234567890','!@#$%^&*','.,','<>','[]','}{','\'\"`~','-=+',': ']
			if 'symbols' in kwargs:
				symbols = kwargs['symbols']
			else:
				symbols='`1234567890-=qwertyuiop][\\asdfghjkl;\'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP}{|ASDFGHJKL:\"ZXCVBNM<>?'
			symbols_list = []
			if 'index' in kwargs:
				symbols=example_list[kwargs['index']]
			for r in prange(self.rows):
				for c in prange(self.columns):
					symbol=random.choice(symbols)
					symbol_dict={"row":r, "column":c, "symbol":symbol}
					symbols_list.append(symbol_dict)
			self.symbols_list = symbols_list

	# Font Text
	def FontText(self,text,row=1,column=1,font=0,letter_spaceing=1,space=2,each_other=False):
		symbols = []
		list_of_letters = []
		add_column = column	
		text = str(text.lower())
		add_row = row
		if each_other==False:
			last_letter_column = column
		for letter in text:
			if each_other==False:
				if letter == ' ':
					last_letter_column += letter_spaceing+space
				else:
					column = last_letter_column+letter_spaceing
			list_of_letters = []
			if each_other == False:
				add_row = row
			try:
				text2 = fonts.fonts[font][letter]
			except:
				if letter==' ':
					pass
				else:
					continue
			symbols_list = self.symbols_list
			x=0
			if each_other==True:
				if letter == ' ':
					add_row += letter_spaceing+space
				else:
					add_row += letter_spaceing

			if each_other==False:
				if letter == ' ':
					column = last_letter_column+letter_spaceing+space
				else:
					column = last_letter_column+letter_spaceing
			if letter != ' ':
				list_of_letters = []
				for item in text2:
					if item =="\n":
						add_row+=1
						if each_other == False:
							if add_column > last_letter_column:
								last_letter_column = add_column
							add_column = column
						else:
							add_column=column
						list_for_symbol = []
					else:
						list_for_symbol=[]
						list_for_symbol.append(add_row)				
						list_for_symbol.append(add_column)				
						list_for_symbol.append(item)
						symbols.append(list_for_symbol)
						add_column+=1	
				add_row += letter_spaceing
		
		symbols_list = self.symbols_list
		for symb in symbols:
			row=symb[0]
			column=symb[1]
			symbol=symb[2]
			for l in prange(len(symbols_list)):
				if (symbols_list[l]['row'] == row-1) and (symbols_list[l]['column'] == column-1):
					symbols_list[l]['symbol'] = symbol
		self.symbols_list = symbols_list




	# Load .txt file
	def LoadTxt(self,path,row=0,column=0):
		with open(path,'r') as textfile:
			text=textfile.read()

		symbols = []
		add_row = row
		add_column = column
		for item in text:
			if item =="\n":
				add_row+=1
				add_column=column
				list_for_symbol = []
			else:
				list_for_symbol=[]
				list_for_symbol.append(add_row)				
				list_for_symbol.append(add_column)				
				list_for_symbol.append(item)
				symbols.append(list_for_symbol)
				add_column+=1				
		
		symbols_list = self.symbols_list
		for symb in symbols:
			row=symb[0]
			column=symb[1]
			symbol=symb[2]
			for l in prange(len(symbols_list)):
				if (symbols_list[l]['row'] == row-1) and (symbols_list[l]['column'] == column-1):
					symbols_list[l]['symbol'] = symbol
		self.symbols_list = symbols_list

	# Printing all .txt files from folder path
	#def LoadAnimation(self,path,row=1,column=1,stop_time=0.5,remove_background=True,clear=True):
	#	pass
			



	# Replace all symbols wich is our symbol
	def ReplaceSymbol(self,symbol,rpsymbol):
		symbols_list = self.symbols_list	
		for l in prange(len(symbols_list)):
			if (symbols_list[l]['symbol'] == symbol):
				symbols_list[l]['symbol'] = rpsymbol
		self.symbols_list = symbols_list

	# Some objects for drawing
	def DrawModel(self,model,row=1,column=1,**kwargs):
		model = model.lower()
		if model=="arrow":
			length=3
			position='right'
			if 'length' in kwargs:
				length=kwargs['length']
			if 'position' in kwargs:
				position=kwargs['position']
				position = position.lower()
			if position=='right':
				text=((length-1)*'-')+">"
			elif position=='left':
				text="<"+((length-1)*'-')
			else:
				raise f"Bad Position of arrow {position} (left or right)"
		

		if (model=="telephone") or (model=="phone"):
			index=0
			

			if index==0:
				phone_model='SAMSUNG'
				if 'index' in kwargs:
					index = kwargs['index']
				if 'phone_model' in kwargs:
					if len(kwargs['phone_model']) <= 10:
						phone_model = kwargs['phone_model']
					elif len(kwargs['phone_model']) > 10:
						phone_model = kwargs['phone_model'][0:10]
				if 'screen_text' in kwargs:
					try:
						r1 = kwargs['screen_text'][0] + (13-len(kwargs['screen_text'][0]))*' '
					except:
						r1 = 13*' '
					try:
						r2 = kwargs['screen_text'][1] + (13-len(kwargs['screen_text'][1]))*' '
					except:
						r2 = 13*' '
					try:
						r3 = kwargs['screen_text'][2] + (13-len(kwargs['screen_text'][2]))*' '
					except:
						r3 = 13*' '
					try:
						r4 = kwargs['screen_text'][3] + (13-len(kwargs['screen_text'][3]))*' '
					except:
						r4 = 13*' '
					try:
						r5 = kwargs['screen_text'][4] + (13-len(kwargs['screen_text'][4]))*' '
					except:
						r5 = 13*' '
				else:
					r1 = 13*' '
					r2 = 13*' '
					r3 = 13*' '
					r4 = 13*' '
					r5 = 13*' '


				text='''
   _
  | |
  |_|
  /_\\    \\ | /
.-"""------.----.
|          U    |
|               |
| ============= |
|_______________|
| ___{} |
||{}||
||{}||
||{}||
||{}||
||{}||
||_____________||
|__.---"""---.__|
|---------------|
|[Yes][(|)][ No]|
| ___  ___  ___ |
|[<-\'][CLR][.->]|
| ___  ___  ___ |
|[1__][2__][3__]|
| ___  ___  ___ |
|[4__][5__][6__]|
| ___  ___  ___ |
|[7__][8__][9__]|
| ___  ___  ___ |
|[*__][0__][#__]|
`--------------\' '''.format((( (10-len(phone_model))*"_")+phone_model), r1,r2,r3,r4,r5)






		symbols_list = self.symbols_list
		x=0
		list_of_letters = []
		symbols = []
		add_row = row
		add_column = column
		for item in text:
			if item =="\n":
				add_row+=1
				add_column=column
				list_for_symbol = []
			else:
				list_for_symbol=[]
				list_for_symbol.append(add_row)				
				list_for_symbol.append(add_column)				
				list_for_symbol.append(item)
				symbols.append(list_for_symbol)
				add_column+=1	

		symbols_list = self.symbols_list
		for symb in symbols:
			row=symb[0]
			column=symb[1]
			symbol=symb[2]
			for l in prange(len(symbols_list)):
				if (symbols_list[l]['row'] == row-1) and (symbols_list[l]['column'] == column-1):
					symbols_list[l]['symbol'] = symbol
		self.symbols_list = symbols_list


	# Import text art from models.py
	def ImportModel(self,name,index=0,row=1,column=1,remove_background=False):
		name = name.lower()
		text = models.models[name][index]
		if remove_background==True:
			text = text.replace(' ',self.main_symbol)
		symbols_list = self.symbols_list
		x=0
		list_of_letters = []
		symbols = []
		add_row = row
		add_column = column
		for item in text:
			if item =="\n":
				add_row+=1
				add_column=column
				list_for_symbol = []
			else:
				list_for_symbol=[]
				list_for_symbol.append(add_row)				
				list_for_symbol.append(add_column)				
				list_for_symbol.append(item)
				symbols.append(list_for_symbol)
				add_column+=1	
		
		symbols_list = self.symbols_list
		for symb in symbols:
			row=symb[0]
			column=symb[1]
			symbol=symb[2]
			for l in prange(len(symbols_list)):
				if (symbols_list[l]['row'] == row-1) and (symbols_list[l]['column'] == column-1):
					symbols_list[l]['symbol'] = symbol
		self.symbols_list = symbols_list

	# Make checkbox 
	def CheckboxList(self,choice_list,row=0,column=0,style=1,name=''):
		text='{}\n'.format(name)
		if style == 1:
			for i in prange(len(choice_list)):
				text += "[{}] {}\n".format(i+1,choice_list[i])
		if style == 2:
			for i in prange(len(choice_list)):
				text += "{}. {}\n".format(i+1,choice_list[i])
		if style == 3:
			for i in prange(len(choice_list)):
				text += "• {}\n".format(choice_list[i])
		if style == 4:
			for i in prange(len(choice_list)):
				text += "[({}) {}]\n".format(i+1,choice_list[i])
		if style == 5:
			for i in prange(len(choice_list)):
				text += "{}) {}\n".format(i+1,choice_list[i])
		 
		symbols_list = self.symbols_list
		x=0
		list_of_letters = []
		symbols = []
		add_row = row
		add_column = column
		for item in text:
			if item =="\n":
				add_row+=1
				add_column=column
				list_for_symbol = []
			else:
				list_for_symbol=[]
				list_for_symbol.append(add_row)				
				list_for_symbol.append(add_column)				
				list_for_symbol.append(item)
				symbols.append(list_for_symbol)
				add_column+=1	
		
		symbols_list = self.symbols_list
		for symb in symbols:
			row=symb[0]
			column=symb[1]
			symbol=symb[2]
			for l in prange(len(symbols_list)):
				if (symbols_list[l]['row'] == row-1) and (symbols_list[l]['column'] == column-1):
					symbols_list[l]['symbol'] = symbol
		self.symbols_list = symbols_list
	# Write all in screen
	def update(self,rptime=0,rpcount=1):
		for i in prange(rpcount):
			os.system('cls')
			i = 0
			for r in prange(self.rows):
				for c in prange(self.columns):
					print(self.symbols_list[i]['symbol'],end="")
					i += 1
				print()
			time.sleep(rptime)
