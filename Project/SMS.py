import matplotlib.pyplot as plt
from tkinter.scrolledtext import *
from tkinter.messagebox import *
import numpy as np
import pandas as pd

from sqlite3 import *
from tkinter import *
import requests
import bs4


root = Tk()
#---------------------------------------SMS PAGE FUNCTIONS-----------------------------------------------

def ap():
	root.withdraw()
	add_page.deiconify()
	ap_entRno.delete(0,END)
	ap_entName.delete(0,END)
	ap_entMarks.delete(0,END)
	ap_entRno.focus()
def vp():
	root.withdraw()
	view_page.deiconify()
	vp_display()
def up():
	root.withdraw()
	update_page.deiconify()
	up_entRno.delete(0,END)
	up_entName.delete(0,END)
	up_entMarks.delete(0,END)
	up_entRno.focus()
def dp():
	root.withdraw()
	delete_page.deiconify()
	dp_entRno.delete(0,END)
	dp_entRno.focus()
def cp():
	root.withdraw()
	charts_page.deiconify()
	

def quote():
	try:
		web_add = "https://www.brainyquote.com/quote_of_the_day"
		res = requests.get(web_add)
		data = bs4.BeautifulSoup(res.text,"html.parser")
		info = data.find('img', {"class":"p-qotd"})
		quote = info['alt']
		ent_2.delete(0, END)
		ent_2.insert(0, "  Quote Of The Day:  '" + quote + "'")
	except Exception as e:
		showerror("Issue: ",e)

def loc():
	web_address = "https://ipinfo.io/"
	res = requests.get(web_address)
		
	data = res.json()
	
	city_name = data['city']
	return city_name
def loc_time():
	try:
		city_name = loc()
		a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
		a2 = "&q=" + city_name
		a3 = "&appid=c6e315d09197cec231495138183954bd"
		web_address = a1 + a2 + a3
		res = requests.get(web_address)
		
		data = res.json()
		main_data = data['main']
		ent_1.delete(0, END)
		ent_1.insert(0, "  Location:  " + city_name + "\t\t\t\t\t\t\t          Temperature: " + str(data['main']['temp']))
		
	except Exception as e:
		showerror("Issue: ",e)


#-------------------------------------------------------------------------------------------------------------

#--------------------------------------- ADD PAGE FUNCTIONS ---------------------------------------

def ap_back():
	add_page.withdraw()
	root.deiconify()

def str_validation(name):
	for s in name:
		if not (s.isalpha()): 
			return False
			break
	return True

def add_db(rno , name , marks):
	con = None
	try:
		con  = connect('student_db.db')
		print('connected')
		sql = "insert into student values('%d','%s','%d')"
		cursor = con.cursor()
		cursor.execute(sql % (rno,name,marks))
		con.commit()
		showinfo("Success","Record added successfully")
	except Exception as e:
		showerror("ERROR",'Roll number already assigned')
		con.rollback()
	finally:
		if con is not None:
			con.close()
			print("disconnected")
		
		
	

def ap_save():
	try:
		rno = int(ap_entRno.get())
		if rno < 0:
			showerror('ERROR','Roll number must be greater than 0')
			ap_entRno.delete(0,END)
			ap_entRno.focus()
		else:
			try:
				name = ap_entName.get()
				if len(name)<2 :
					showerror('ERROR','Name should be of minimum length 2')
					ap_entName.delete(0,END)
					ap_entName.focus()
				else:
					if not (str_validation(name)):
						showerror('ERROR','Name cannot contain digits or any special characters')
						ap_entName.delete(0,END)
						ap_entName.focus()
					else:
						try:
							marks = int(ap_entMarks.get())
							if not (0 <= marks <= 100):
								showerror('ERROR','Marks must be in the range 0 - 100')
								ap_entMarks.delete(0,END)
								ap_entMarks.focus()
							else:
								add_db(rno , name , marks)
						except Exception:
							showerror('ERROR','Marks must be positive integers only')
							ap_entMarks.delete(0,END)
							ap_entMarks.focus()
				
			except Exception as e:
				showerror('Error',e)
				ap_entName.delete(0,END)
				ap_entName.focus()
	except Exception:
		showerror('ERROR','Roll number must be positive integers only')
		ap_entRno.delete(0,END)
		ap_entRno.focus()
		
#-------------------------------------------------------------------------------------------------------------

#--------------------------------------- VIEW PAGE FUNCTIONS ---------------------------------------
def vp_back():
	view_page.withdraw()
	root.deiconify()

def vp_searchName():
	vp_data.delete(1.0,END)
	print("Hi")
	con = None
	try  :
		nm = vp_entSearchByName.get()
		if len(nm)>=2:
			if str_validation(nm):
				con = connect("student_db.db")
				print("connected")
				sql = "select * from student where name = '%s'"
				cursor = con.cursor()
				cursor.execute(sql%(nm))
				data = cursor.fetchall()
				info = ""
				for d in data:
					info = info + "Rno: " + str(d[0]) + " Name: " + str(d[1]) + " Marks: " + str(d[2]) + "\n"
				vp_data.insert(INSERT,info)
				if info == "":
					showwarning('NOT FOUND',"NO Record Found for Name: " + nm)
			else:
				showerror('ERROR','Name cannot contain digits or any special characters')
		else:
			showerror("Issue: ",'Name should be of minimum length 2')
					
	except Exception as e:
		showerror("Issue: ",e)
	finally:
		if con is not None:
			con.close()
			print("vp disconnected")

def vp_searchMarks():
	vp_data.delete(1.0,END)
	
	con = None
	try  :
		m = int(vp_entSearchByMarks.get())
		
		con = connect("student_db.db")
		print("connected")
		sql = "select * from student where marks = '%d'"
		cursor = con.cursor()
		cursor.execute(sql%(m))
		data = cursor.fetchall()
		info = ""
		for d in data:
			info = info + "Rno: " + str(d[0]) + " Name: " + str(d[1]) + " Marks: " + str(d[2]) + "\n"
		vp_data.insert(INSERT,info)
		if info == "":
			showwarning('NOT FOUND',"NO Record Found for Marks: " + str(m))
			
	except Exception as e:
		showerror("Issue: ",e)
	finally:
		if con is not None:
			con.close()
			print("vp disconnected")

def vp_searchRollNo():
	vp_data.delete(1.0,END)
	
	con = None
	try  :
		rno = int(vp_entSearchByRollNo.get())
		
		con = connect("student_db.db")
		print("connected")
		sql = "select * from student where rno = '%d'"
		cursor = con.cursor()
		cursor.execute(sql%(rno))
		data = cursor.fetchall()
		info = ""
		for d in data:
			info = info + "Rno: " + str(d[0]) + " Name: " + str(d[1]) + " Marks: " + str(d[2]) + "\n"
		vp_data.insert(INSERT,info)
		if info == "":
			showwarning('NOT FOUND',"NO Record Found for Roll No: " + str(rno))
				
	except Exception as e:
		showerror("Issue: ",e)
	finally:
		if con is not None:
			con.close()
			print("vp disconnected")



def vp_display():
	vp_data.delete(1.0,END)
	con = None
	try:
		con = connect("student_db.db")
		print("vp connected")
		sql = "select * from student;"
		cursor = con.cursor()
		cursor.execute(sql)
		data = cursor.fetchall()
		info = ""
		for d in data:
			info = info + "Rno: " + str(d[0]) + " Name: " + str(d[1]) + " Marks: " + str(d[2]) + "\n"
		vp_data.insert(INSERT,info)
	except Exception as e:
		showerror("Issue: ",e)
	finally:
		if con is not None:
			con.close()
			print("vp disconnected")

#-------------------------------------------------------------------------------------------------------------

#--------------------------------------- UPDATE PAGE FUNCTIONS ------------------------------------------ 
def up_back():
	update_page.withdraw()
	root.deiconify()

def str_validation(name):
	for s in name:
		if not (s.isalpha()): 
			return False
			break
	return True

def up_db(rno , name , marks):
	con = None
	try:
		con  = connect('student_db.db')
		print('update connected')
		sql = "update student set name = '%s' , marks = '%d' where rno = '%d'"
		cursor = con.cursor()
		cursor.execute(sql % (name,marks,rno))
		if cursor.rowcount == 1:
			con.commit()
			showinfo("Success","Record updated successfully")
		else:
			showerror("ERROR","Record does not exist")
	except Exception as e:
		showerror("ERROR",'Roll number already assigned')
		con.rollback()
	finally:
		if con is not None:
			con.close()
			print("update disconnected")
def up_save():
	try:
		rno = int(up_entRno.get())
		if rno < 0:
			showerror('ERROR','Roll number must be greater than 0')
			up_entRno.delete(0,END)
			up_entRno.focus()
		else:
			try:
				name = up_entName.get()
				if len(name)<2 :
					showerror('ERROR','Name should be of minimum length 2')
					up_entName.delete(0,END)
					up_entName.focus()
				else:
					if not (str_validation(name)):
						showerror('ERROR','Name cannot contain digits or any special characters')
						up_entName.delete(0,END)
						up_entName.focus()
					else:
						try:
							marks = int(up_entMarks.get())
							if not (0 <= marks <= 100):
								showerror('ERROR','Marks must be in the range 0 - 100')
								up_entMarks.delete(0,END)
								up_entMarks.focus()
							else:
								up_db(rno , name , marks)
						except Exception:
							showerror('ERROR','Marks must be positive integers only')
							up_entMarks.delete(0,END)
							up_entMarks.focus()
				
			except Exception as e:
				showerror('Error',e)
				up_entName.delete(0,END)
				up_entName.focus()
	except Exception:
		showerror('ERROR','Roll number must be positive integers only')
		up_entRno.delete(0,END)
		up_entRno.focus()
		


#-------------------------------------------------------------------------------------------------------------

#--------------------------------------- DELETE PAGE FUNCTIONS ---------------------------------------
def dp_back():
	delete_page.withdraw()
	root.deiconify()

def dp_db(rno):
	con = None
	try:
		con = connect("student_db.db")
		print("dp connected")
		cursor = con.cursor()
		sql = "Delete from student where rno='%d'"
		cursor.execute(sql % (rno))
		if cursor.rowcount == 1:
			con.commit()
			showwarning("Note","Record Deleted")
		else:
			showerror("Error","Record does not exist")
	except Exception as e:
		print("Issue","e")
		con.rollback()
	finally:
		if con is not None:
			con.close()
			print("Disconnected")

def dp_delete():
	try:
		rno = int(dp_entRno.get())
		if rno < 0:
			showerror('ERROR','Roll number must be greater than 0')
			dp_entRno.delete(0,END)
			dp_entRno.focus()
		else : 
			dp_db(rno)
	except Exception:
		showerror('ERROR','Roll number must be positive integers only')
		dp_entRno.delete(0,END)
		dp_entRno.focus()

#-------------------------------------------------------------------------------------------------------------

#--------------------------------------- CHARTS PAGE FUNCTIONS ---------------------------------------
def cp_back():
	charts_page.withdraw()
	root.deiconify()

def cp_plot():
	list_rno ,list_name,list_marks = cp_db()

	plt.plot(list_name,list_marks,linewidth = 2,marker = 'o',markersize = 10,markerfacecolor='darkblue')

	plt.xlabel("Student")
	plt.ylabel("Marks")
	plt.title("BATCH INFORMATION")
	plt.grid()
	plt.show()

def cp_pie():
	list_rno ,list_name,list_marks = cp_db()
	exp = []
	passed , fail = 0,0
	for m in list_marks:
		if m >= 30 :
			passed = passed + 1
		else:
			fail = fail + 1
	marks_obtained = []
	marks_obtained.append(passed)
	marks_obtained.append(fail)
	for m in marks_obtained:
		exp.append(0)
	marks_category = []
	marks_category = ['Passed', 'Failed: Marks Below 30']
	exp[1] = 0.1
	plt.pie(marks_obtained,labels=marks_category,autopct='%.2f%%',radius=1.1,explode = exp,shadow =True)

	plt.title("BATCH INFORMATION")
	plt.show()

def cp_bar():
	list_rno ,list_name,list_marks = cp_db()
	x = np.arange(len(list_name))
	
	plt.bar(x,list_marks,width=0.25)
		

	plt.xticks(x,list_name)
	plt.xlabel("Student")
	plt.ylabel("Marks")
	plt.title("BATCH INFORMATION")
	plt.grid()
	
	plt.show()
	
	
def cp_db():
	con = None
	list_rno=[]
	list_name=[]
	list_marks=[]
	try:
		con = connect("student_db.db")
		print("connected")
		sql = "select * from student;"
		cursor = con.cursor()
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			list_rno.append(d[0])
			list_name.append(d[1])
			list_marks.append(d[2])
		return list_rno , list_name , list_marks
	except Exception as e:
		showerror("Issue: ",e)
	finally:
		if con is not None:
			con.close()
			print("disconnected")
	
	
#-------------------------------------------------------------------------------------------------------------


#--------------------------------------- MAIN PAGE ---------------------------------------

btnAdd = Button(root , text="Add" , width = 20 , font = ('Arial',18,'bold') , command = ap)
btnView = Button(root , text="View" , width = 20 , font = ('Arial',18,'bold') , command = vp)
btnUpdate = Button(root , text="Update" , width = 20 , font = ('Arial',18,'bold') , command = up)
btnDelete = Button(root , text="Delete" , width = 20 , font = ('Arial',18,'bold') , command = dp)
btnCharts = Button(root , text="Charts" , width = 20 , font = ('Arial',18,'bold') , command = cp)

ent_1 = Entry(root , bd = 5 , width = 100 , font = ('Arial',10,'bold'))
ent_2 = Entry(root , bd = 5 , width = 100 , font = ('Arial',10,'bold'))
quote()
loc_time()




def focus_out(entry, str_var, msg):
    if(str_var.get() == ''):#Put the placeholder only if the field is empty
        entry.insert(0, msg)

btnAdd.pack(pady = 5)
btnView.pack(pady = 5)
btnUpdate.pack(pady = 5)
btnDelete.pack(pady = 5)
btnCharts.pack(pady = 5)
ent_1.pack(pady = 10)
ent_2.pack(pady = 5)

root.title('S.M.S')
root.geometry("700x400+150+50")


#-------------------------------------------------------------------------------------------------------------

#--------------------------------------- ADD PAGE ---------------------------------------

add_page = Toplevel(root)
add_page.title("Add st.")
add_page.geometry("700x400+150+50")

ap_lblRno   = Label(add_page , text = 'Enter Rno: ' , width = 10 , font = ('arial' , 15 , 'bold'))   
ap_entRno   = Entry(add_page , bd = 5 , width = 98 , font = ('Arial',18))
ap_lblName  = Label(add_page , text = 'Enter Name: ' , width = 10 , font = ('arial' , 15 , 'bold'))
ap_entName  = Entry(add_page , bd = 5 , width = 98 , font = ('Arial',18))
ap_lblMarks = Label(add_page , text = 'Enter Marks: ' , width = 10 , font = ('arial' , 15 , 'bold'))
ap_entMarks = Entry(add_page , bd = 5 , width = 98 , font = ('Arial',18))
ap_btnSave  = Button(add_page , text = 'SAVE' , width = 10 , font = ('arial' , 12 , 'bold') , command = ap_save)
ap_btnBack  = Button(add_page , text = 'BACK' , width = 10 , font = ('arial' , 12 , 'bold') , command = ap_back)

ap_lblRno.pack(pady = 5)
ap_entRno.pack(pady = 5)
ap_lblName.pack(pady = 5)
ap_entName.pack(pady = 5)
ap_lblMarks.pack(pady = 5)
ap_entMarks.pack(pady = 5)
ap_btnSave.pack(pady = 5)
ap_btnBack.pack(pady = 5)

add_page.withdraw()


#-------------------------------------------------------------------------------------------------------------



#--------------------------------------- VIEW PAGE ---------------------------------------

view_page = Toplevel(root)
view_page.title("View st.")
view_page.geometry("700x700+150+25")

vp_data = ScrolledText(view_page , width = 50 , height = 13 , font = ('arial' , 15 , 'bold'))
vp_btnBack  = Button(view_page , text = 'BACK' , width = 10 , font = ('arial' , 12 , 'bold') , command = vp_back)
vp_btnSearchByName  = Button(view_page , text = 'SEARCH by name' , width = 15 , font = ('arial' , 12 , 'bold') , command = vp_searchName)
vp_entSearchByName = Entry(view_page, width=20, bd = 5 , font = ('arial' , 15 , 'bold'))

vp_btnSearchByRollNo  = Button(view_page , text = 'SEARCH by roll no' , width = 15 , font = ('arial' , 12 , 'bold') , command = vp_searchRollNo)
vp_entSearchByRollNo = Entry(view_page, width=20, bd = 5 , font = ('arial' , 15 , 'bold'))

vp_btnSearchByMarks  = Button(view_page , text = 'SEARCH by marks' , width = 15 , font = ('arial' , 12 , 'bold') , command = vp_searchMarks)
vp_entSearchByMarks = Entry(view_page, width=20, bd = 5 , font = ('arial' , 15 , 'bold'))

vp_btnViewAll =  Button(view_page , text = "View All" , width = 15 , font = ('arial' , 12 , 'bold') , command = vp_display)
vp_data.pack(pady = 10)
vp_btnBack.pack(pady = 5)
vp_btnViewAll.pack(pady = 10)
vp_entSearchByName.place(x=150,y=430)
vp_btnSearchByName.place(x=420,y=430)
vp_entSearchByRollNo.place(x=150,y=500)
vp_btnSearchByRollNo.place(x=420,y=500)
vp_entSearchByMarks.place(x=150,y=570)
vp_btnSearchByMarks.place(x=420,y=570)

view_page.withdraw()

#-------------------------------------------------------------------------------------------------------------



#--------------------------------------- UPDATE PAGE ---------------------------------------

update_page = Toplevel(root)
update_page.title("Update st.")
update_page.geometry("700x400+150+50")

up_lblRno   = Label(update_page  , text = 'Enter Rno: ' , width = 10 , font = ('arial' , 15 , 'bold'))   
up_entRno   = Entry(update_page  , bd = 5 , width = 98 , font = ('Arial',18,'bold'))
up_lblName  = Label(update_page  , text = 'Enter Name: ' , width = 10 , font = ('arial' , 15 , 'bold'))
up_entName  = Entry(update_page  , bd = 5 , width = 98 , font = ('Arial',18,'bold'))
up_lblMarks = Label(update_page  , text = 'Enter Marks: ' , width = 10 , font = ('arial' , 15 , 'bold'))
up_entMarks = Entry(update_page  , bd = 5 , width = 98 , font = ('Arial',18,'bold'))
up_btnSave  = Button(update_page  , text = 'UPDATE' , width = 10 , font = ('arial' , 12 , 'bold') , command = up_save)
up_btnBack  = Button(update_page  , text = 'BACK' , width = 10 , font = ('arial' , 12 , 'bold') , command = up_back)

up_lblRno.pack(pady = 5)
up_entRno.pack(pady = 5)
up_lblName.pack(pady = 5)
up_entName.pack(pady = 5)
up_lblMarks.pack(pady = 5)
up_entMarks.pack(pady = 5)
up_btnSave.pack(pady = 5)
up_btnBack.pack(pady = 5)

update_page.withdraw()


#-------------------------------------------------------------------------------------------------------------



#--------------------------------------- DELETE PAGE ---------------------------------------

delete_page = Toplevel(root)
delete_page.title("Delete st.")
delete_page.geometry("700x400+150+50")

dp_lblRno   = Label(delete_page  , text = 'Enter Rno: ' , width = 10 , font = ('arial' , 15 , 'bold'))   
dp_entRno   = Entry(delete_page  , bd = 5 , width = 98 , font = ('Arial',18,'bold'))

dp_btnDelete  = Button(delete_page  , text = 'DELETE' , width = 10 , font = ('arial' , 12 , 'bold') , command = dp_delete)
dp_btnBack  = Button(delete_page  , text = 'BACK' , width = 10 , font = ('arial' , 12 , 'bold') , command = dp_back)

dp_lblRno.pack(pady = 10)
dp_entRno.pack(pady = 10)
dp_btnDelete.pack(pady = 5)
dp_btnBack.pack(pady = 5)

delete_page.withdraw()


#-------------------------------------------------------------------------------------------------------------



#--------------------------------------- CHARTS PAGE ---------------------------------------

charts_page = Toplevel(root)
charts_page.title("Charts st.")
charts_page.geometry("700x400+150+50")

cp_btnBack  = Button(charts_page  , text = 'BACK' , width = 10 , font = ('arial' , 12 , 'bold') , command = cp_back)

cp_btnBar = Button(charts_page , text = 'Bar Plot Representation' , width = 20 , font = ('arial' , 15 , 'bold') , command = cp_bar)
cp_btnPlot = Button(charts_page , text = 'Line Plot Representation' , width = 20 , font = ('arial' , 15 , 'bold') , command = cp_plot)
cp_btnPie = Button(charts_page , text = 'Pie Plot Representation' , width = 20 , font = ('arial' , 15 , 'bold') , command = cp_pie)

cp_btnBar.pack(pady = 10)
cp_btnPlot.pack(pady = 10)
cp_btnPie.pack(pady = 10)
cp_btnBack.pack(pady = 10)

charts_page.withdraw()


#-------------------------------------------------------------------------------------------------------------
root.mainloop() 