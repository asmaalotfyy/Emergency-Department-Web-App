import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root"
)

mycursor = mydb.cursor()
mycursor.execute("DROP DATABASE IF EXISTS Emergencydep")
mycursor.execute("CREATE DATABASE Emergencydep")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="Emergencydep"
)
mycursor = mydb.cursor()


mycursor.execute("DROP TABLE IF EXISTS Admin")
mycursor.execute("""CREATE TABLE Admin (A_ssn INT PRIMARY KEY NOT NULL, A_fname VARCHAR(255),A_lname VARCHAR(255), A_password VARCHAR(255))""")

mycursor.execute("DROP TABLE IF EXISTS Department")
mycursor.execute("""CREATE TABLE Department (Dep_name VARCHAR(255), Dep_no INT, PRIMARY KEY(Dep_no))""")


mycursor.execute("DROP TABLE IF EXISTS Records")
mycursor.execute("CREATE TABLE Records(Rec_no INT PRIMARY KEY NOT NULL, Medical_status VARCHAR(255),Medical_history VARCHAR(255))")


mycursor.execute("DROP TABLE IF EXISTS Doctors")
mycursor.execute("""CREATE TABLE Doctors (D_ssn INT PRIMARY KEY NOT NULL,D_fname VARCHAR(255),D_lname VARCHAR(255) ,D_gender VARCHAR(255), 
                    D_email VARCHAR(255) UNIQUE,D_password VARCHAR(255),D_address VARCHAR(255),D_phone INT,D_salary DECIMAL(10,2),
                    D_birthDate DATE,D_age INT,Scientific_area VARCHAR(255),Dep_no INT,FOREIGN KEY (Dep_no) REFERENCES Department(Dep_no),
                    J_date DATE,St_DATE DATE, End_DATE DATE,Available BIT NOT NULL DEFAULT 1)""")

mycursor.execute("DROP DATABASE IF EXISTS Nurses")
mycursor.execute("""CREATE TABLE Nurses (N_ssn INT PRIMARY KEY NOT NULL,N_fname VARCHAR(255),N_lname VARCHAR(255) ,N_gender VARCHAR(255) , 
                    N_email VARCHAR(255) UNIQUE,N_password VARCHAR(255),N_address VARCHAR(255),N_phone INT,N_salary DECIMAL(10,2),
                    N_birthDate DATE,N_age INT,Dep_no INT,FOREIGN KEY (Dep_no) REFERENCES Department(Dep_no),J_date DATE)""")


  #  LR_no INT,FOREIGN KEY (LR_no) REFERENCES Lab_Radiology(LR_no),
# Med_no INT,FOREIGN KEY (Med_no) REFERENCES Medications(Med_no),




                  

mycursor.execute("DROP TABLE IF EXISTS Lab_Radiology")
mycursor.execute("""CREATE TABLE Lab_Radiology(LR_no INT PRIMARY KEY NOT NULL, LR_name VARCHAR(255), LR_date DATE, LR_price INT,
                    LR_Scans BLOB DEFAULT NULL)""")


mycursor.execute("DROP DATABASE IF EXISTS Rooms")
mycursor.execute("""CREATE TABLE Rooms (R_no INT, R_type VARCHAR(255), R_period INT, PRIMARY KEY (R_no),N_ssn INT,
                    FOREIGN KEY (N_ssn) REFERENCES Nurses(N_ssn))""")

mycursor.execute("DROP DATABASE IF EXISTS Receptionists")
mycursor.execute("""CREATE TABLE Receptionists (R_ssn INT PRIMARY KEY NOT NULL,R_fname VARCHAR(255),R_lname VARCHAR(255) ,
                    R_gender VARCHAR(255), R_email VARCHAR(255) UNIQUE,R_password VARCHAR(255),R_address VARCHAR(255),
                    R_phone INT,R_salary DECIMAL(10,2),R_birthDate DATE,R_age INT,Dep_no INT,FOREIGN KEY (Dep_no) REFERENCES Department(Dep_no),
                    J_date DATE)""")




mycursor.execute("DROP TABLE IF EXISTS Patients")
mycursor.execute("""CREATE TABLE Patients (P_ssn INT PRIMARY KEY NOT NULL,P_fname VARCHAR(255), P_lname VARCHAR(255),
                    P_gender VARCHAR(255), P_email VARCHAR(255) UNIQUE,P_password VARCHAR(255),P_address VARCHAR(255), P_birthdate DATE,
                    Rec_no INT,FOREIGN KEY (Rec_no) REFERENCES Records(Rec_no), Dr_ssn INT,
                    FOREIGN KEY (Dr_ssn) REFERENCES Doctors(D_ssn),Nr_ssn INT,FOREIGN KEY (Nr_ssn) REFERENCES Nurses(N_ssn) , 
                    Admission DATE,Discharge DATE,R_no INT,FOREIGN KEY (R_no) REFERENCES Rooms (R_no))""")




mycursor.execute("DROP TABLE IF EXISTS prescriptions")
mycursor.execute(""" CREATE TABLE prescriptions ( Pres_no INT, P_ssn INT,D_ssn INT,P_Date DATE, Diagnosis VARCHAR(255),
                    PRIMARY KEY(Pres_no), FOREIGN KEY (P_ssn) REFERENCES Patients(P_ssn),
                    FOREIGN KEY (D_ssn) REFERENCES doctors(D_ssn))""")


mycursor.execute("DROP TABLE IF EXISTS Medications")
mycursor.execute(""" CREATE TABLE Medications( Med_name VARCHAR(255),Med_no INT PRIMARY KEY NOT NULL,DATEs INT,Doses INT,Startdate DATE,
                     Enddate DATE,Med_price INT,FOREIGN KEY (Pres_no) REFERENCES prescriptions(pres_no),Pres_no INT,Times_day INT)""")



mycursor.execute("DROP TABLE IF EXISTS Medical_Procedures")
mycursor.execute(""" CREATE TABLE  Medical_Procedures (MP_No INT, Pres_no INT,MP_Name VARCHAR(255),Type VARCHAR(255), PRIMARY KEY(MP_No),
                    FOREIGN KEY (Pres_no) REFERENCES prescriptions(Pres_no))""")                  


mycursor.execute("DROP TABLE IF EXISTS Examine")
mycursor.execute(""" CREATE TABLE Examine( P_ssn INT, D_ssn INT, FOREIGN KEY (P_ssn) REFERENCES Patients(P_ssn),
                     FOREIGN KEY (D_ssn) REFERENCES Doctors(D_ssn),Ex_time TIME)""")

# mycursor.execute("DROP TABLE IF EXISTS Prescribe")
# mycursor.execute("CREATE TABLE Prescribe(Prescribe_no INT, PRIMARY KEY(Prescribe_no), FOREIGN KEY(DSSN) REFERENCES Doctor(DSSN), FOREIGN KEY(LR_ID) REFERENCES LAB_Radiology(LR_ID),FOREIGN KEY(M_no) REFERENCES Medications(M_no))")

# mycursor.execute("DROP TABLE IF EXISTS Treatment")
# mycursor.execute("CREATE TABLE Treatment(T_no INT, T_price INT, PRIMARY KEY(T_no), FOREIGN KEY(PSSN) REFERENCES Patient(PSSN)) ")
 


mycursor.execute("""INSERT INTO admin (A_ssn, A_password, A_fname ,A_lname) VALUES ('1','12345','Ayman','Anwar')""")
mycursor.execute("""INSERT INTO Department (Dep_no, Dep_name) VALUES ('1','Emergency')""")

mydb.commit()
print("Database Created Successfully")

# mycursor.execute("DROP TABLE IF EXISTS Employees")
# mycursor.execute("""CREATE TABLE Doctors (ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,SSN INT,
#                     Fname VARCHAR(255),Lname VARCHAR(255) ,Gender BIT, Email VARCHAR(255) UNIQUE,
#                     Password VARCHAR(255),Address VARCHAR(255),Salary DECIMAL(10,2),BirthDate DATE,Age INT)""")
# mycursor.execute("DROP DATABASE IF EXISTS Nurses")
# mycursor.execute("CREATE TABLE Nurses (ID INT PRIMARY KEY REFERENCES Employees(ID),Dep_id INT,)") #inherit
# mycursor.execute("DROP DATABASE IF EXISTS Receptionists")
# mycursor.execute("CREATE TABLE Receptionists (ID INT PRIMARY KEY REFERENCES Employees(ID))")
# mycursor.execute("CREATE TABLE EmpQualifications (ID INT REFERENCES Employees(ID) ,qualifications varchar(11),PRIMARY KEY(ID, qualifications))")
# mycursor.execute("CREATE TABLE EmpPhone (ID INT REFERENCES Employees(ID),Phone INT,PRIMARY KEY(ID, Phone))")
