#Name-Naysha Kamboj
#Roll no.-2501730379
#date-8/11/2025
#Title-GradeBook Analyzer



#Menu 
print("Welcome to GradeBook Analyzer")
print("'No more spreadsheet chaos — just enter names and marks,and we’ll handle the stats, grades, and summaries. Fast, simple, and teacher-friendly.'")
print("Select one of the following commands to continue:")
print("1.Calculate average marks of individual students")
print("2.Calculate median marks")
print("3.Find maximum score")
print("4.Find minimum score")
print("5.Grade assignment")
print("6.Pass/Fail asseement")
print("7.Show all data in tabulated form")
print("8.Exit")



def info():
    #Gatehering info from proffessor about students' names and marks
    
    n=int(input("Enter the total number of students in class:"))
    global name
    global marks
    global record
    name=[]
    marks=[]
    for i in range(n):
        name1=input("enter name of students:")
        marks1=int(input("enter marks of that student:"))
        name.append(name1)
        marks.append(marks1)
        #adding names and marks in adictionary
    record={}
    record=dict(zip(name,marks))
    print("recored of student and marks :",record)


def average():
    #Calculating average of marks of the class
    avg=sum(marks)/len(marks)
    print("Average marks of all students:",avg)

def median():
    #calculating the median of marks in class
    marks.sort()
    n = len(marks)
    mid = n // 2
    if n % 2 == 0:
        median = (marks[mid - 1] + marks[mid]) / 2
    else:
        median = marks[mid]

    print("Median:", median)
def max1():
    #Finding the mamximum in the class
    print("Maximum marks in class is:",max(marks))

def min1():
     #Finding the minimum in the class
    print("Minimum marks of class is:",min(marks))


def grade():
    #assigning the grades and storing it in a list
    global grades
    grades=[]
    for i in record.items():
        j=i[1]
        x=i[0]
        if j<=100 and j>=90:
            print(x,"has  an A grade")
            grades.append("A")
        elif j>=80 and j<90:
            print(x,"has a B grade")
            grades.append("B")
        elif j>=70 and j<80:
            print(x,"has a C grade")
            grades.append("C")
        elif j<=60 and j<70:
            print(x,"has a D grade")
            grades.append("D")
        elif j<60:
            print(x,"has F grade")
            grades.append("F")
        else:
            print("there is an error")
    print(grades)

def pf():
    #Determining whether the student passed or failed
    passed_students = [names for names, m in record.items() if m >= 40]
    failed_students = [names for names, m in record.items() if m < 40]
    print("Lists of passed students:",passed_students)
    print("Count of passed students:",len(passed_students))
    print("Lists of failed students:",failed_students)
    print("Count of failed students:",len(failed_students))

def tabulated():
    #Table 
    print("Record of name, marks and grades of students")
    
    # Header
    print("+------------+--------+--------+")

    print("| {:<10} | {:<6}  | {:<6} |".format("Name", "Marks","Grade"))
    print("+------------+--------+--------+")


    # Rows
    for n, m, g in zip(name, marks, grades):
       print("| {:<10} | {:<6} | {:<6} |".format(n, m, g))



    # Footer
    print("+------------+--------+--------+")


info()
x="Y"
while x.lower()=="y":
        choice=int(input("Enter the command number you want to perform"))
        if choice==1:
             average()
        elif choice==2:
            median()
        elif choice==3:
            max1()
        elif choice==4:
            min1()
        elif choice==5:
            grade()
        elif choice==6:
            pf()
        elif choice==7:
            tabulated()
        elif choice==8:
            x="n"
            






          
