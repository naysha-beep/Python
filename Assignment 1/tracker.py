#Task 1: Setup & Introduction

#Naysha Kamboj
#21-09-2025
#Mini Project Assignment: Daily Calorie Tracker CLI
print("""
👋 Welcome to CalTrack – Your Personal Calorie Companion!

Whether you're a student juggling classes or just someone trying to eat smarter, CalTrack is here to help you stay on top of your daily calorie intake with ease.

🍽️ Log your meals  
🔥 Track your total calories  
🎯 Compare against your personal daily limit  
🗂️ Save your session logs for future reference

Let’s build healthier habits one meal at a time. Ready to take control of your nutrition? Let’s get started!
""")

#Task 2: Input & Data Collection
meals=[]
calorie_intake=[]
choice="y"
while choice=="y":
    meal_name=input("Please enter the meal name you want to log:-")
    calorie=int(input("Please enter the calorie intake associated with the logged meal:-"))
    meals.append(meal_name)
    calorie_intake.append(calorie)
    x=input("Do you want to log more meals?(Y/N)")
    choice=x.lower()
print("Meals logged by you:-")
print(meals)
print("Calories associated with the logged meals:-")
print(calorie_intake)

#Task 3: Calorie Calculations

total_calorie_intake=sum(calorie_intake)
print("Total calorie intake according to your logged meals is:-")
print(total_calorie_intake)

no_of_meals=len(meals)
average=total_calorie_intake/no_of_meals
print("The average calorie per meal is:-")
print(average)


daily_limit=int(input("Enter your daily calorie limit:-"))


#Task 4: Exceed Limit Warning System
if daily_limit>=total_calorie_intake:
    print("""
                    🎉 Great job! You're right on track! 🌟

                    You've stayed within your daily calorie goal — that’s a win for your health and your discipline.
                    """)
else:
    print("""
                    😌 Hey, it looks like you went a bit over your daily calorie goal today — and that’s okay!

                    Progress isn’t about perfection, it’s about consistency.
                    """)

#Task 5: Neatly Formatted Output

s="Meal Name                 Calorie"
x=len(s)
print(s)
print("-"*x)
for i in meals:
    a=meals.index(i)
    j=calorie_intake[a]
    print(f"{i}                 {j}")
print(f"Total            {total_calorie_intake}")
print(f"Average          {average}")



#Task 6 Save Session Log to File
choice=input("Do you want to save the data in a seperate file?(Y/N)")
if choice.lower()=="y":
    from datetime import datetime,timedelta
    now=datetime.now()
    now=str(now)
    filename="calorietrack.txt"
    with open(filename,"w") as file:
        file.write("Calorie Track File.\n")
        file.write("current time:\n")
        file.write(now)
        for i in meals:
            file.write("Meals Logged=\n")
            file.write(str(i))
            file.write("\n")
        for x in calorie_intake:
            file.write("Corresponding calories=\n")
            file.write(str(x))
            file.write("\n")
            

        
        file.write("average meal calorie=\n")
        file.write(str(average))
        file.write("\n")
        file.write("total calorie=\n")
        file.write(str(total_calorie_intake))
        file.write("\n")
        file.write("Limit was=\n")
        file.write(str(daily_limit))
        file.write("\n")
        
        

    















      
