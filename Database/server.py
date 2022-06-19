import mysql.connector
from flask import Flask, redirect, url_for, request,render_template, flash, session,redirect

# import datetime  
from datetime import datetime
import re
import os
# from flask_wtf import FlaskForm
# from wtforms import (StringField, SubmitField)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="Emergencydep"
)
mycursor = mydb.cursor()
def convert_to_RFC_datetime(year, month, day, hour, minute):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt
   
def findDay(date): 
    year , month, day = (int(i) for i in date.split('-'))     
    born = datetime.date(year, month, day) 
    return born.strftime("%A")
 
def get_doctors():
   Doctor_FNames=[]
   Doctor_LNames=[]
   Doctor_SSN = []
   Dnames=[]
   mycursor.execute('SELECT * FROM doctors')
   doctors = mycursor.fetchall()

   for doctor in doctors:
      Doctor_FNames.append(doctor[0])
      Doctor_LNames.append(doctor[1])
      Doctor_SSN.append(doctor[3])

   for fname,lname,dssn in zip(Doctor_FNames,Doctor_LNames,Doctor_SSN):
      Dnames.append('Dr. ' + fname+' '+lname+' '+ ' - ' + str(dssn))
   return Dnames

app = Flask(__name__)
app.secret_key="secret"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
global fnm
global R1 
global R2
global R3
global R4
global R5 
global ct
global cn
global finalfn
global finalln
R1=0 
R2=0 
R3=0 
R4=0 
R5=0
ct=[]
cn=[]
finalfn=[]
finalln=[]





@app.route('/',methods=['GET','POST'])
def home():
   
   ispatient=False
   isadmin=False
   isdr=False
   isnurse=False
   isreceptionist=False
   if request.method=="POST":
      ssn= request.form['SSN']
      passward=request.form['pass']
      global ssn2             #global variable carrying the current signed in ssn
      ssn2=int(ssn)
    
      #patient check sign in
      mycursor.execute("SELECT P_ssn FROM Patients WHERE P_ssn=%s AND P_password=%s" ,(ssn2,passward,))
     
      patresult=mycursor.fetchall()
      print(patresult)
      if  patresult:
         ispatient=True
         
#admin check in sign in
      mycursor.execute("SELECT A_ssn FROM Admin WHERE A_ssn=%s AND  A_password=%s ",(ssn2,passward,))
      adminresult=mycursor.fetchall()
      print(adminresult)
      if adminresult:
          isadmin=True

#doctor check in sign in
      mycursor.execute("SELECT D_ssn FROM Doctors WHERE D_ssn=%s AND D_password=%s", (ssn2,passward,))
      docresult=mycursor.fetchall()
      if docresult:
          isdr=True

#receptionist check in sign in
      mycursor.execute("SELECT R_ssn FROM Receptionists WHERE R_ssn=%s AND R_password=%s", (ssn2,passward,))
      recresult=mycursor.fetchall()
      if recresult:
          isreceptionist=True

     # nurse check in sign in     
      mycursor.execute("SELECT N_ssn FROM Nurses WHERE N_ssn=%s AND N_password=%s",(ssn2,passward,))
      nuresult=mycursor.fetchall()
      if nuresult:
         isnurse=True

      if(ispatient==True):
         print("patient")
         return redirect("/Patient_homepage")
      elif(isadmin==True):
         print("admin")
         return redirect("/admin")
      elif(isdr==True):
         print("doctor")
         return redirect("/doctor_homepage")
      elif(isreceptionist==True):
         print("doctor")
         return redirect("/doctor_contact_info")
      elif(isnurse==True):
         print("nurse")
         return redirect("/doctor_contact_info")

      else:
             flash("Incorrect SSN or Password!")
             return render_template("signin.html")   
   else:
      print("signin")
      return render_template("signin.html")


@app.route('/signup_doctor',methods = ['POST', 'GET'])
def adddoctor():
   ispatient=False
   isadmin=False
   isdr=False
   isnurse=False
   isreceptionist=False
   if request.method == 'POST': ##check if there is post data
      try:
        gender = request.form['gender'] 
      except:
         print("Catchhhhh")
         flash("Please fill in all fields!")
         return render_template('signup_doctor.html')

      ssn = request.form['ssn']
      firstname = request.form['firstname'] 
      lastname = request.form['lastname']  
      email = request.form['email']
      password = request.form['password']
      address = request.form['address']
      phone = request.form['phone']
      salary = request.form['salary']
      departmentno = request.form['departmentno']
      scientificArea = request.form['scientificarea']
      birthdate = request.form['birthdate'] 
#patient check sign in
      mycursor.execute("SELECT P_ssn FROM Patients WHERE P_ssn=%s" ,(ssn,))

      patresult=mycursor.fetchall()
      print(patresult)
      if  patresult:
         ispatient=True

#admin check in sign in
      mycursor.execute("SELECT A_ssn FROM Admin WHERE A_ssn=%s ",(ssn,))
      adminresult=mycursor.fetchall()
      print(adminresult)
      if adminresult:
          isadmin=True

#doctor check in sign in
      mycursor.execute("SELECT D_ssn FROM Doctors WHERE D_ssn=%s", (ssn,))
      docresult=mycursor.fetchall()
      if docresult:
          isdr=True

#receptionist check in sign in
      mycursor.execute("SELECT R_ssn FROM Receptionists WHERE R_ssn=%s ", (ssn,))
      recresult=mycursor.fetchall()
      if recresult:
          isreceptionist=True

     # nurse check in sign in
      mycursor.execute("SELECT N_ssn FROM Nurses WHERE N_ssn=%s ",(ssn,))
      nuresult=mycursor.fetchall()
      if nuresult:
         isnurse=True

      if(ispatient==True or isadmin==True or isdr==True or isreceptionist==True or isnurse==True):
        flash("SSN already exist!")
        return render_template("signup_doctor.html")

      else:

         if(firstname=="" or lastname=="" or email==""  or password=="" or address=="" or ssn=="" or phone=="" or salary=="" or departmentno=="" or scientificArea==""): #check that none of the fields are empty
            # print("innnnnn")
            flash("Please fill in all fields!")
            return render_template('signup_doctor.html')

         birthdate = datetime.fromisoformat(birthdate)
         today = datetime.today()
         age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
         
         print(ssn,firstname,lastname,gender,email,password,address,phone,salary,birthdate,age,departmentno,scientificArea)

         sql = """INSERT INTO Doctors(D_ssn,D_fname,D_lname,D_gender,D_email,D_password,D_address,D_phone,D_salary,D_birthDate,D_age,Dep_no,
                  Scientific_area) values(%s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s, %s, %s)"""
         val = (ssn,firstname,lastname,gender,email,password,address,phone,salary,birthdate,age,departmentno,scientificArea)
         mycursor.execute(sql, val)

      # mycursor.execute("Select LAST_INSERT_ID() from Employees") #if ssn used as primary key, these 3 lines won't be needed
      # myresult = mycursor.fetchall()
      # doctorID = myresult[0][0]  ###

      # sql = """INSERT INTO Doctors(ID,Department,ScientificArea) values(%s, %s, %s)""" 
      # val = (doctorID,department,scientificArea) #and ssn would be instead of doctorID here
      # mycursor.execute(sql, val)

         mydb.commit()   
         return render_template('admin.html')
   else:
      print("hereeee")
      return render_template('signup_doctor.html')


@app.route('/signup_nurse',methods = ['POST', 'GET'])
def addnurse():
   ispatient=False
   isadmin=False
   isdr=False
   isnurse=False
   isreceptionist=False
   if request.method == 'POST': ##check if there is post data
      try:
        gender = request.form['gender'] 
      except:
         print("Catchhhhh")
         flash("Please fill in all fields!")
         return render_template('signup_nurse.html')

      ssn = request.form['ssn']
      firstname = request.form['firstname'] 
      lastname = request.form['lastname']  
      email = request.form['email']
      password = request.form['password']
      address = request.form['address']
      phone = request.form['phone']
      salary = request.form['salary']
      departmentno = request.form['departmentno']
   
      birthdate = request.form['birthdate'] 

#patient check sign in
      mycursor.execute("SELECT P_ssn FROM Patients WHERE P_ssn=%s" ,(ssn,))

      patresult=mycursor.fetchall()
      print(patresult)
      if  patresult:
         ispatient=True

#admin check in sign in
      mycursor.execute("SELECT A_ssn FROM Admin WHERE A_ssn=%s ",(ssn,))
      adminresult=mycursor.fetchall()
      print(adminresult)
      if adminresult:
          isadmin=True

#doctor check in sign in
      mycursor.execute("SELECT D_ssn FROM Doctors WHERE D_ssn=%s", (ssn,))
      docresult=mycursor.fetchall()
      if docresult:
          isdr=True

#receptionist check in sign in
      mycursor.execute("SELECT R_ssn FROM Receptionists WHERE R_ssn=%s ", (ssn,))
      recresult=mycursor.fetchall()
      if recresult:
          isreceptionist=True

     # nurse check in sign in
      mycursor.execute("SELECT N_ssn FROM Nurses WHERE N_ssn=%s ",(ssn,))
      nuresult=mycursor.fetchall()
      if nuresult:
         isnurse=True

      if(ispatient==True or isadmin==True or isdr==True or isreceptionist==True or isnurse==True):
        flash("SSN already exist!")
        return render_template("signup_nurse.html")

      else:

         if(firstname=="" or lastname=="" or email==""  or password=="" or address=="" or ssn=="" or phone=="" or salary=="" or departmentno==""): #check that none of the fields are empty
            # print("innnnnn")
            flash("Please fill in all fields!")
            return render_template('signup_nurse.html')

         birthdate = datetime.fromisoformat(birthdate)
         today = datetime.today()
         age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
         
         print(ssn,firstname,lastname,gender,email,password,address,phone,salary,birthdate,age,departmentno)

         sql = """INSERT INTO Nurses(N_ssn,N_fname,N_lname,N_gender,N_email,N_password,N_address,N_phone,N_salary,N_birthDate,N_age,Dep_no) 
                  values(%s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s, %s)"""
         val = (ssn,firstname,lastname,gender,email,password,address,phone,salary,birthdate,age,departmentno)
         mycursor.execute(sql, val)

         # mycursor.execute("Select LAST_INSERT_ID() from Employees") #if ssn used as primary key, these 3 lines won't be needed
         # myresult = mycursor.fetchall()
         # doctorID = myresult[0][0]  ###

         # sql = """INSERT INTO Doctors(ID,Department,ScientificArea) values(%s, %s, %s)""" 
         # val = (doctorID,department,scientificArea) #and ssn would be instead of doctorID here
         # mycursor.execute(sql, val)

         mydb.commit()   
         return render_template('admin.html')
   else:
      return render_template('signup_nurse.html')

@app.route('/signup_receptionist',methods = ['POST', 'GET'])
def addreceptionist():
   ispatient=False
   isadmin=False
   isdr=False
   isnurse=False
   isreceptionist=False
   if request.method == 'POST': ##check if there is post data
      try:
        gender = request.form['gender'] 
      except:
         print("Catchhhhh")
         flash("Please fill in all fields!")
         return render_template('signup_receptionist.html')

      ssn = request.form['ssn']
      firstname = request.form['firstname'] 
      lastname = request.form['lastname']  
      email = request.form['email']
      password = request.form['password']
      address = request.form['address']
      phone = request.form['phone']
      salary = request.form['salary']
      departmentno = request.form['departmentno']
      birthdate = request.form['birthdate'] 

#patient check sign in
      mycursor.execute("SELECT P_ssn FROM Patients WHERE P_ssn=%s" ,(ssn,))

      patresult=mycursor.fetchall()
      print(patresult)
      if  patresult:
         ispatient=True

#admin check in sign in
      mycursor.execute("SELECT A_ssn FROM Admin WHERE A_ssn=%s ",(ssn,))
      adminresult=mycursor.fetchall()
      print(adminresult)
      if adminresult:
          isadmin=True

#doctor check in sign in
      mycursor.execute("SELECT D_ssn FROM Doctors WHERE D_ssn=%s", (ssn,))
      docresult=mycursor.fetchall()
      if docresult:
          isdr=True

#receptionist check in sign in
      mycursor.execute("SELECT R_ssn FROM Receptionists WHERE R_ssn=%s ", (ssn,))
      recresult=mycursor.fetchall()
      if recresult:
          isreceptionist=True

     # nurse check in sign in
      mycursor.execute("SELECT N_ssn FROM Nurses WHERE N_ssn=%s ",(ssn,))
      nuresult=mycursor.fetchall()
      if nuresult:
         isnurse=True

      if(ispatient==True or isadmin==True or isdr==True or isreceptionist==True or isnurse==True):
        flash("SSN already exist!")
        return render_template("signup_doctor.html")

      else:

         if(firstname=="" or lastname=="" or email==""  or password=="" or address=="" or ssn=="" or phone=="" or salary=="" or departmentno=="" ): #check that none of the fields are empty
            # print("innnnnn")
            flash("Please fill in all fields!")
            return render_template('signup_receptionist.html')

         birthdate = datetime.fromisoformat(birthdate)
         today = datetime.today()
         age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
         
         print(ssn,firstname,lastname,gender,email,password,address,phone,salary,birthdate,age,departmentno)

         sql = """INSERT INTO Receptionists(R_ssn,R_fname,R_lname,R_gender,R_email,R_password,R_address,R_phone,R_salary,R_birthDate,R_age,Dep_no)
               values(%s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s, %s)"""
         val = (ssn,firstname,lastname,gender,email,password,address,phone,salary,birthdate,age,departmentno)
         mycursor.execute(sql, val)

         # mycursor.execute("Select LAST_INSERT_ID() from Employees") #if ssn used as primary key, these 3 lines won't be needed
         # myresult = mycursor.fetchall()
         # doctorID = myresult[0][0]  ###

         # sql = """INSERT INTO Doctors(ID,Department,ScientificArea) values(%s, %s, %s)""" 
         # val = (doctorID,department,scientificArea) #and ssn would be instead of doctorID here
         # mycursor.execute(sql, val)

         mydb.commit()   
         return render_template('admin.html')
   else:
      return render_template('signup_receptionist.html')




@app.route('/signup_patient',methods=['Get','POST'])
def addpatient():

   ispatient=False
   isadmin=False
   isdr=False
   isnurse=False
   isreceptionist=False 
   if request.method=="POST":
      patFname=request.form['P_first_name']
      patLname=request.form['P_last_name']
      patssn=request.form['PSSNn']
      patadds=request.form['address']
      patgender=request.form['gender']
      patpasswd=request.form['user_password']
      patbdate=request.form['Bdate']
      Admission=request.form['Edate']

 #patient check sign in
      mycursor.execute("SELECT P_ssn FROM Patients WHERE P_ssn=%s" ,(patssn,))
     
      patresult=mycursor.fetchall()
      print(patresult)
      if  patresult:
         ispatient=True
         
#admin check in sign in
      mycursor.execute("SELECT A_ssn FROM Admin WHERE A_ssn=%s ",(patssn,))
      adminresult=mycursor.fetchall()
      print(adminresult)
      if adminresult:
          isadmin=True

#doctor check in sign in
      mycursor.execute("SELECT D_ssn FROM Doctors WHERE D_ssn=%s", (patssn,))
      docresult=mycursor.fetchall()
      if docresult:
          isdr=True

#receptionist check in sign in
      mycursor.execute("SELECT R_ssn FROM Receptionists WHERE R_ssn=%s ", (patssn,))
      recresult=mycursor.fetchall()
      if recresult:
          isreceptionist=True
     # nurse check in sign in     
      mycursor.execute("SELECT N_ssn FROM Nurses WHERE N_ssn=%s ",(patssn,))
      nuresult=mycursor.fetchall()
      if nuresult:
         isnurse=True
      if(ispatient==True or isadmin==True or isdr==True or isreceptionist==True or isnurse==True):
        flash("SSN already exist!")
        return render_template("signup_patient.html")  
      else:
         if(patFname=="" or patLname=="" or patssn==""  or patadds=="" or patgender=="" or patpasswd=="" or patbdate=="" or Admission=="" ): #check that none of the fields are empty
            # print("innnnnn")
            flash("Please fill in all fields!")
            return render_template('signup_patient.html')
         mycursor.execute("SELECT D_ssn,D_fname,D_lname FROM Doctors WHERE Available=1")
         D_result=mycursor.fetchall()
         if D_result:
            print(D_result[0][2])
            dfname=D_result[0][1]
            dlname=D_result[0][2]
            dssn=D_result[0][0]
            sql="INSERT INTO Patients (P_fname,P_lname,P_ssn,P_address,P_gender,P_password,P_birthdate,Admission,Dr_ssn) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) "
            val=(patFname,patLname,patssn,patadds,patgender,patpasswd,patbdate,Admission,dssn)
            # # try:
            mycursor.execute(sql,val) 
            mydb.commit()
            # except:
            #    flash("SSN already exist or empty!")
            #    return render_template("signup_patient.html")
            flash("You've signed up successfully!")
            flash("You've been assigned to Dr. "+dfname+" "+dlname)
            return redirect("/")
         else:
            flash("You've been signed up successfully,no Drs are currently available.You will be assigned a Dr soon")
   else:
      return render_template("signup_patient.html")

@app.route('/Patient_homepage',methods=['Get','POST'])
def Patient_homepage():
   if  request.method == "POST":
      rate=request.form['rate']
      if rate == '1':
         global R1
         R1+=1
      elif rate == '2':
         global R2
         R2+=1
      elif rate == '3':
         global R3
         R3+=1
      elif rate == '4':
         global R4
         R4+=1
      elif rate == '5':
         global R5
         R5+=1
      flash("Thank you for rating us!")
      return render_template("patient_homepage.html")

   else:

      sql1 = (""" SELECT P_fname FROM Patients WHERE P_ssn = %s""")
      val1 = (ssn2,)
      mycursor.execute(sql1,val1)
      myresult1 = mycursor.fetchone()
      sql2 = (""" SELECT P_lname FROM Patients WHERE P_ssn = %s """)
      val2 = (ssn2,)
      mycursor.execute(sql2,val2)
      myresult2 = mycursor.fetchone()
      return render_template("Patient_homepage.html", fname = myresult1[0], lname = myresult2[0])
     

@app.route('/admin')
def ad():
   mycursor.execute("SELECT COUNT(D_ssn) FROM Doctors")
   myresult1 = mycursor.fetchone()
   mycursor.execute("SELECT COUNT(P_ssn) FROM Patients")
   myresult2 = mycursor.fetchone()
   mycursor.execute("SELECT COUNT(N_ssn) FROM Nurses")
   myresult3 = mycursor.fetchone()
   mycursor.execute("SELECT SUM(D_salary) FROM Doctors")
   myresult4 = mycursor.fetchone()
   mycursor.execute("SELECT SUM(N_salary) FROM Nurses")
   myresult5 = mycursor.fetchone()
   mycursor.execute("SELECT AVG(D_salary) FROM Doctors")
   myresult6 = mycursor.fetchone()
   mycursor.execute("SELECT AVG(N_salary) FROM Nurses")
   myresult7 = mycursor.fetchone()
   sql8 =(""" SElECT A_fname FROM Admin WHERE A_ssn = %s""")
   val8 =(ssn2,)
   mycursor.execute(sql8,val8)
   myresult8 = mycursor.fetchone()
   sql9 =(""" SElECT A_lname FROM Admin WHERE A_ssn = %s""")
   val9 =(ssn2,)
   mycursor.execute(sql9,val9)
   myresult9 = mycursor.fetchone()
   #male/female drs
   mycursor.execute(""" SELECT COUNT(D_ssn) FROM Doctors WHERE D_gender='female'""")
   FemD=mycursor.fetchone()
   mycursor.execute(""" SELECT COUNT(D_ssn) FROM Doctors WHERE D_gender='male'""")
   mD=mycursor.fetchone()
   #male/female nurse
   mycursor.execute(""" SELECT COUNT(N_ssn) FROM Nurses WHERE N_gender='female'""")
   FemN=mycursor.fetchone()
   mycursor.execute(""" SELECT COUNT(N_ssn) FROM Nurses WHERE N_gender='male'""")
   mN=mycursor.fetchone()
   # current year
   now = datetime.now()
   print(now)
   ysql="SELECT COUNT(P_ssn) FROM Patients WHERE year(Admission)=%s"
   yval=(now.year,)
   mycursor.execute(ysql,yval)
   EnterD = mycursor.fetchone()
   # nsql="SELECT COUNT(P_ssn) FROM Examine WHERE year(EXdate)=%s"
   # nval=(now.year,)
   # mycursor.execute(nsql,nval)
   # ExD=mycursor.fetchone()
   dsql="SELECT COUNT(D_ssn) FROM Doctors WHERE year(J_date)=%s"
   dval=(now.year,)
   mycursor.execute(dsql,dval)
   JD = mycursor.fetchone()
   return render_template("admin.html", Dcount=myresult1[0], Pcount=myresult2[0], Ncount=myresult3[0], Total_dsal=myresult4[0], 
                      Total_nsal=myresult5[0], AVG_dsal=myresult6[0], AVG_nsal=myresult7[0], fname=myresult8[0], lname=myresult9[0],
                      FD=FemD[0],MD=mD[0],FN=FemN[0],MN=mN[0],r1=R1,r2=R2,r3=R3,r4=R4,r5=R5, newP=EnterD[0],newD=JD[0])

#  newE=ExD[0], 


@app.route('/admin/Rdoctor', methods=['GET',"POST"])
def Remove_doctor():
   if request.method=="POST":
      sn= request.form['drsn']
      mycursor.execute("SET FOREIGN_KEY_CHECKS=0")
      sql2="DELETE FROM Examine WHERE D_ssn=%s"
      val2=(sn,)
      mycursor.execute(sql2,val2)
      mydb.commit()
      sql1="DELETE FROM Doctors WHERE D_ssn= %s "
      val1=(sn,)
      mycursor.execute(sql1,val1)
      mycursor.execute("SET FOREIGN_KEY_CHECKS=1")
      mydb.commit()

      return redirect("/admin")
   else:
      return render_template("Rdoctor.html")

@app.route('/admin/Rnurse', methods=['GET',"POST"])
def Remove_nurse():
    if request.method=="POST":
      sn= request.form['nsn']
      mycursor.execute("SET FOREIGN_KEY_CHECKS=0")
      sql="DELETE FROM Nurses WHERE N_ssn= %s "
      val=(sn,)
      mycursor.execute("SET FOREIGN_KEY_CHECKS=1")
      mycursor.execute(sql,val)
      mydb.commit()
      return redirect("/admin")
    else:
      return render_template("Rnurse.html")

@app.route('/admin/Rreceptionist', methods=['GET',"POST"])
def Remove_receptionist():
    if request.method=="POST":
      sn= request.form['nsn']
      mycursor.execute("SET FOREIGN_KEY_CHECKS=0")
      sql="DELETE FROM Receptionists WHERE R_ssn= %s "
      val=(sn,)
      mycursor.execute("SET FOREIGN_KEY_CHECKS=1")
      mycursor.execute(sql,val)
      mydb.commit()
      return redirect("/admin")
    else:
      return render_template("Rreceptionist.html")

@app.route('/view',methods = ['POST', 'GET'])
def viewdoctor():
   if request.method == 'POST':
      return render_template('index.html')
   else:
      mycursor.execute("SELECT * FROM Doctors")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
      }
      return render_template('view.html',data=data)



































@app.route('/doctor_homepage',methods = ['POST', 'GET'])
def doctor_homepage():
   
      # mycursor.execute("SELECT P_ssn FROM Patients WHERE P_ssn=%s AND P_password=%s" ,(ssn2,passward,))

      mycursor.execute("SELECT P_ssn,P_fname,P_lname FROM Patients WHERE Dr_ssn=%s",(ssn2,))
      D_result=mycursor.fetchall()
      if D_result:
         global pssn       
         pssn=str(D_result[0][0])
         pfname=D_result[0][1]
         plname=D_result[0][2]
         data={
         'msg':["You are assigned to Patient: "+pfname+" "+plname+",","with the ID: "+pssn]
          }
         return render_template('doctor_homepagecurr.html', data=data)
      else:
         data={
         'msg':["You aren't assigned to any Patient currently"]
          }
         return render_template('doctor_homepage.html', data=data)

    

@app.route('/Patient_homepage/contact',methods=["GET",'POST'])
def contactus():
   if request.method =="POST":
      global complain
      global ssn_compl
      
      
   
      complain=request.form['contact']
      ssn_compl=request.form['complpainSSN']
      paswrd=request.form['pas']
      
      sql=("SELECT P_ssn FROM Patients Where P_ssn= %s AND P_password=%s")
      val=(ssn_compl,paswrd,)
      mycursor.execute(sql,val)
      myresult=mycursor.fetchone()
      if myresult:
         ct.append(complain)
         cn.append(ssn_compl)
         flash("Your comment has been recorded successfully!")
         return redirect("/Patient_homepage")
      else:
       return redirect("/Patient_homepage/contact")

   else:
       return render_template("contact.html")


@app.route('/admin/complain',methods=['Get','POST'])
def complain_cont():
   checking=[]
 
   for x in cn:
       strings = [str(y) for y in x]
       a_string = "".join(strings)
       an_integer = int(a_string)
       sql1=("SELECT P_fname FROM Patients WHERE P_ssn = %s")
       val1 = (an_integer,)
       mycursor.execute(sql1,val1)
       myresult1 = mycursor.fetchall()
       finalfn.append(myresult1)
       sql2=("SELECT P_lname FROM Patients WHERE P_ssn = %s")
       val2 = (an_integer,)
       mycursor.execute(sql2,val2)
       myresult2 = mycursor.fetchall()
       finalln.append(myresult2)      
       
   for x in zip(cn,ct):
          checking.append("Patient with SSN: "+ str(x[0])+":  "+"  "+x[1]+"  ")

   if len(checking)>0:
      x=True
      return render_template("complain.html",cssn=cn,comp=checking)
      
      
   else:
      return redirect("/admin")

@app.route('/Patient_viewDoctors')
def patient_view():
   mycursor.execute("SELECT D_ssn,D_fname,D_lname,Scientific_area,Available FROM Doctors")
   myresult = mycursor.fetchall()
   return render_template("Patient_viewDoctors.html",doctorsData=myresult)


@app.route('/Doctor_Prescription' ,methods = ['POST', 'GET'])
def Doctor_Prescription():
   if request.method == 'POST':
      D_ID=ssn2
      P_ID = request.form['Patient ID']
      #p_date = request.form['Prescription Date']
      today=datetime.today()
      p_date= today.strftime('%Y/%m/%d')
      #p_date = today().date()
      Diagnose = request.form['Diagnose']
      mycursor.execute("SELECT COUNT(Pres_no) FROM prescriptions") 
      PresID = mycursor.fetchone() [0]+1
      pid=int(P_ID)
      mycursor.execute("SELECT P_ssn FROM Patients ")
      myresult=mycursor.fetchall()
      cm=0
      cond1=0
      for x in myresult:
         strings = [str(y) for y in x]
         a_string = "".join(strings)
         an_integer = int(a_string)
         if(an_integer==pid):
            cm=cm+1
      if (cm!=0):
         sql = "INSERT INTO prescriptions (P_date,Diagnosis,Pres_no,P_ssn,D_ssn) VALUES (%s, %s,%s,%s,%s)"
         val = (p_date,Diagnose,PresID,P_ID,D_ID)
         mycursor.execute(sql, val) 
         mydb.commit() 
         global presid
         presid = PresID
         return redirect('/Doctor_sh')
      else:
         cond1 = 1   
         return render_template('Doctor_Prescription.html', msg="The ID you have entered does not exist", condition1=cond1 )
   else:
      return render_template('Doctor_Prescription.html')




@app.route('/Doctor_CurrentPatientPres' ,methods = ['POST', 'GET'])
def Doctor_CurrentPatientPres():
   if request.method == 'POST':
      D_ID=ssn2
      P_ID=pssn
      #p_date = request.form['Prescription Date']
      today=datetime.today()
      p_date= today.strftime('%Y/%m/%d')
      #p_date = today().date()
      Diagnose = request.form['Diagnose']
      mycursor.execute("SELECT COUNT(Pres_no) FROM prescriptions") 
      PresID = mycursor.fetchone() [0]+1
      pid=int(P_ID)
      print(p_date,Diagnose,PresID,P_ID,D_ID)
      sql = "INSERT INTO prescriptions (P_date,Diagnosis,Pres_no,P_ssn,D_ssn) VALUES (%s, %s,%s,%s,%s)"
      val = (p_date,Diagnose,PresID,P_ID,D_ID)
      mycursor.execute(sql, val) 

      sql = "UPDATE Patients SET Dr_ssn = null WHERE P_ssn=%s"
      val = (P_ID,)
      mycursor.execute(sql, val) 
      sql = "UPDATE Doctors SET Available = 1 WHERE D_ssn=%s"
      val = (D_ID,)
      mycursor.execute(sql, val) 
   
      mydb.commit() 

      global presid
      presid = PresID
      return redirect('/Doctor_sh')
   else:
      data={
         'msg':["Current Patient ID: "+pssn]
          }
      return render_template('Doctor_CurrPrescription.html',data=data)



@app.route('/Doctor_sh',methods = ['POST', 'GET'])
def Doctor_sh():
   if request.method == 'GET':
      id=presid
      sql=("SELECT P_date,Diagnosis FROM prescriptions WHERE Pres_no = %s")
      val=(id,)
      mycursor.execute(sql,val) 
      myresult = mycursor.fetchall()
      sql1=("SELECT Med_name,Times_day,Startdate,Enddate FROM Medications WHERE Pres_no = %s")
      val1=(id,)
      mycursor.execute(sql1,val1) 
      myresult1 = mycursor.fetchall()
      sql2=("SELECT MP_Name,Type FROM medical_procedures WHERE Pres_no = %s")
      val2=(id,)
      mycursor.execute(sql2,val2) 
      myresult2 = mycursor.fetchall()
      return render_template('Doctor_sh.html', Prescriptions=myresult, Medications=myresult1, Medicalprocedures=myresult2)
   else:
      return render_template('Doctor_sh.html')
          

@app.route('/Doctor_Medications',methods = ['POST', 'GET'])
def Doctor_Medications():
   if request.method == 'POST':
      presID=presid
      MN = request.form['Medication Name']
      TPD = request.form['Dosage Per Day']
      SD = request.form['Start Date']
      ED = request.form['End Date']
      mycursor.execute("SELECT COUNT(Med_no) FROM Medications") 
      Mno = mycursor.fetchone() [0] + 1
      sql = "INSERT INTO Medications (Med_name,Times_day,Pres_no,Startdate,Enddate,Med_no) VALUES (%s, %s,%s,%s, %s,%s)"
      val = (MN,TPD,presID,SD,ED,Mno)
      mycursor.execute(sql, val)
      mydb.commit() 
      return redirect("/Doctor_sh")
   else:
      return render_template('Doctor_Medications.html')

@app.route('/Doctor_Medicalprocedures',methods = ['POST', 'GET'])
def Doctor_Medicalprocedures():
   if request.method == 'POST':
      presID=presid
      MPT = str(request.form['Medical Procedures Type'])
      MPN = request.form['Medical Procedures Name']
      print(MPN)
      print(MPT)
      mycursor.execute("SELECT COUNT(MP_No) FROM medical_procedures") 
      MP = mycursor.fetchone() [0] + 1
      sql = "INSERT INTO medical_procedures (MP_No,Pres_no,Type,MP_Name) VALUES (%s, %s,%s,%s)"
      val = (MP,presID,MPT,MPN)
      mycursor.execute(sql, val)
      mydb.commit() 
      return redirect("/Doctor_sh")
   else:
      return render_template('Doctor_Medicalprocedures.html')



@app.route('/DoctorsPatient_Examination',methods=['GET','POST'])
def DoctorsPatient_Examination():
   if request.method=="POST":
      idi= request.form['Patients_pssn'] 
      id=int(idi)
      mycursor.execute("SELECT P_ssn FROM Patients ")
      myresult0=mycursor.fetchall()
      c=0
      cond=0
      for x in myresult0:
         strings = [str(y) for y in x]
         a_string = "".join(strings)
         an_integer = int(a_string)
         if(an_integer==id):
            c=c+1
      if (c!=0):
         global pid
         pid=id
         sql0=" SELECT P_fname, P_lname,Admission,P_gender,P_birthdate FROM Patients WHERE Patients.P_ssn=%s"
         val0=(id,)
         mycursor.execute(sql0,val0)
         patientinfo = mycursor.fetchall()
         val=(id,)
         sql ="SELECT Med_name,Times_day,Startdate,Enddate  FROM Patients JOIN prescriptions ON Patients.P_ssn=prescriptions.P_ssn JOIN Medications ON prescriptions.Pres_no=Medications.Pres_no WHERE Patients.P_ssn=%s"
         mycursor.execute(sql, val)
         myresult = mycursor.fetchall()
         sql1 ="SELECT P_Date, MP_Name, Type  FROM Patients JOIN prescriptions ON Patients.P_ssn=prescriptions.P_ssn JOIN medical_procedures ON prescriptions.Pres_no=medical_procedures.Pres_no WHERE Patients.P_ssn=%s"
         mycursor.execute(sql1, val)
         myresult1 = mycursor.fetchall()
         sql2="SELECT Diagnosis,P_date FROM Patients JOIN prescriptions ON Patients.P_ssn=prescriptions.P_ssn WHERE Patients.P_ssn=%s"
         mycursor.execute(sql2,val)
         diagnoss=mycursor.fetchall()
         return  render_template("Doctor_ph.html",medication=myresult,patient=patientinfo,diagnosesinfo=diagnoss, medicalpro=myresult1, msg="") 
      else:  
         cond=1
         return render_template('DoctorsPatient_Examination.html', msg="The ID you have entered does not exist", condition=cond)
   else:
      return render_template("DoctorsPatient_Examination.html")






@app.route('/Doctor_viewcurrentPatient',methods=['GET','POST'])
def Doctor_viewcurrentPatient():
   if request.method=="GET":   
      try: 
       idi = pssn
      except:
       idi = ssn2   
      id=int(idi)
      mycursor.execute("SELECT P_ssn FROM Patients ")
      myresult0=mycursor.fetchall()
      c=0
      cond=0
      for x in myresult0:
         strings = [str(y) for y in x]
         a_string = "".join(strings)
         an_integer = int(a_string)
         if(an_integer==id):
            c=c+1
      if (c!=0):
         global pid
         pid=id
         sql0=" SELECT P_fname, P_lname,Admission,P_gender,P_birthdate FROM Patients WHERE Patients.P_ssn=%s"
         val0=(id,)
         mycursor.execute(sql0,val0)
         patientinfo = mycursor.fetchall()
         val=(id,)
         sql ="SELECT Med_name,Times_day,Startdate,Enddate  FROM Patients JOIN prescriptions ON Patients.P_ssn=prescriptions.P_ssn JOIN Medications ON prescriptions.Pres_no=Medications.Pres_no WHERE Patients.P_ssn=%s"
         mycursor.execute(sql, val)
         myresult = mycursor.fetchall()
         sql1 ="SELECT P_Date, MP_Name, Type  FROM Patients JOIN prescriptions ON Patients.P_ssn=prescriptions.P_ssn JOIN medical_procedures ON prescriptions.Pres_no=medical_procedures.Pres_no WHERE Patients.P_ssn=%s"
         mycursor.execute(sql1, val)
         myresult1 = mycursor.fetchall()
         sql2="SELECT Diagnosis,P_date FROM Patients JOIN prescriptions ON Patients.P_ssn=prescriptions.P_ssn WHERE Patients.P_ssn=%s"
         mycursor.execute(sql2,val)
         diagnoss=mycursor.fetchall()
         return  render_template("Doctor_ph.html",medication=myresult,patient=patientinfo,diagnosesinfo=diagnoss, medicalpro=myresult1, msg="") 
      else:  
         cond=1
         return render_template('DoctorsPatient_Examination.html', msg="The ID you have entered does not exist", condition=cond)
   else:
      return render_template("DoctorsPatient_Examination.html")

































@app.route('/doctor_patients',methods = ['POST', 'GET'])
def doctor_patients():

   mycursor = mydb.cursor()
   mycursor.execute("SELECT P_fname, P_lname, P_phone, P_email, P_birthdate, Med_no, LR_no, Rec_no FROM Patients WHERE Dr_ssn=ssn2 ")
   row_headers=[x[0] for x in mycursor.description]
   myresult = mycursor.fetchall() 
   data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
      }

   return render_template('doctor_patients.html', data=data)

@app.route('/doctor_contact_info',methods = ['POST', 'GET'])
def doctor_contact_info():
   if request.method == 'POST':
      
      return render_template('doctor_contact_info.html')

   else:
      # mycursor.execute("SELECT Doctors.D_fname, Doctors.D_lname, Doctors.D_phone, Doctors.D_email, Nurses.N_fname, Nurses.N_lname, Nurses.N_phone, Nurses.N_email FROM Doctors, Nurses")
      mycursor = mydb.cursor()
      mycursor.execute("SELECT D_fname, D_lname, D_phone, D_email FROM Doctors")
      myresult = mycursor.fetchall() 
      data={
            'message':"data retrieved",
            'rec':myresult,
         }
      mycursor = mydb.cursor()
      mycursor.execute("SELECT N_fname, N_lname, N_phone, N_email FROM Nurses")
      myresult = mycursor.fetchall() 
      data1={
            'message':"data retrieved",
            'rec':myresult,
         }
      mycursor = mydb.cursor()
      mycursor.execute("SELECT R_fname, R_lname, R_phone, R_email FROM Receptionists")
      myresult = mycursor.fetchall() 
      data2={
            'message':"data retrieved",
            'rec':myresult,
         }
      return render_template('doctor_contact_info.html', data=data, data1=data1, data2=data2)

@app.route('/doctor_personalinfo',methods = ['POST', 'GET'])
def doctor_personalinfo():
   mycursor.execute("SELECT * FROM Doctors WHERE D_ssn=ssn2")
   row_headers=[x[0] for x in mycursor.description] #this will extract row headers
   myresult = mycursor.fetchall()
   data={
      'message':"data retrieved",
      'rec':myresult,
      'header':row_headers
   }
   return render_template('doctor_personalinfo.html', data=data)





@app.route('/viewnurse',methods = ['POST', 'GET'])
def viewnurse():
   if request.method == 'POST':
      return render_template('index.html')
   else:
      mycursor.execute("SELECT * FROM Nurses")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
      }
      return render_template('view_nurse.html',data=data)

@app.route('/nurse_patients',methods = ['POST', 'GET'])
def nurse_patients():
   
   mycursor = mydb.cursor()
   mycursor.execute("SELECT P_fname, P_lname, P_phone, P_email, P_birthdate, Med_no, LR_no, Rec_no FROM Patients WHERE Nr_ssn=ssn2 ")
   row_headers=[x[0] for x in mycursor.description]
   myresult = mycursor.fetchall() 
   data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
   }
   return render_template('nurse_patients.html', data=data)

@app.route('/nurse_homepage',methods = ['POST', 'GET'])
def nurse_homepage():


   return render_template('nurse_homepage.html')

@app.route('/nurse_personalinfo',methods = ['POST', 'GET'])
def nurse_personalinfo():
   mycursor.execute("SELECT * FROM Nurses WHERE N_ssn=ssn2")
   row_headers=[x[0] for x in mycursor.description] #this will extract row headers
   myresult = mycursor.fetchall()
   data={
      'message':"data retrieved",
      'rec':myresult,
      'header':row_headers
   }
   return render_template('nurse_personalinfo.html', data=data)

@app.route('/receptionist_patients',methods = ['POST', 'GET'])
def receptionist_patients():
   mycursor = mydb.cursor()
   mycursor.execute("SELECT P_fname, P_lname, P_phone, P_email, P_birthdate, Med_no, LR_no, Rec_no FROM Patients")
   row_headers=[x[0] for x in mycursor.description]
   myresult = mycursor.fetchall() 
   data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
   }

   return render_template('receptionist_patients.html', data=data)

@app.route('/receptionist_homepage',methods = ['POST', 'GET'])
def receptionist_homepage():


   return render_template('receptionist_homepage.html')

@app.route('/receptionist_personalinfo',methods = ['POST', 'GET'])
def receptionist_personalinfo():
   mycursor.execute("SELECT * FROM Receptionists WHERE R_ssn=ssn2")
   row_headers=[x[0] for x in mycursor.description] #this will extract row headers
   myresult = mycursor.fetchall()
   data={
      'message':"data retrieved",
      'rec':myresult,
      'header':row_headers
   }
   return render_template('receptionist_personalinfo.html', data=data)


if __name__ == '__main__':
   app.run()