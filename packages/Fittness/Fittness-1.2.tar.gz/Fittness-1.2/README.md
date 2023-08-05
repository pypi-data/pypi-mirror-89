# data533Lab4

**Build Stamp**
[![Build Status](https://travis-ci.com/RaineShen/data533Lab4.svg?token=hQ3AocuezT1bi6bTQVJS&branch=main)](https://travis-ci.com/RaineShen/data533Lab4)

**PyPi Link**
https://pypi.org/project/Fittness/

**Screenshot of code coverage for Intake Package**
![Alt text](https://github.com/RaineShen/data533Lab4/blob/main/Fittness/calories_intake/Code_Coverage_Intake.PNG)

**Screenshot of code coverage for Burn Package**
![Alt text](https://github.com/RaineShen/data533Lab4/blob/main/Fittness/calories_burn/Burn_coverage.png)

### **Subpackage - calories_intake**

This subpackage contains two modules: *__nutrients__* and *__visualization__*.

#### **nutrients** module:

- a super class **Nutrients** has self, name and amount attributes, and a display method. **Protein**, **Fat**, and **Carbohydrate** are 3 subclasses of **Nutrients** class, which inherent attributes and methods from **Nutrients** and also have attribute calPerGram (calories per gram of the nutrient) as well as their own method to calculate and display total calories. 

- **entry()** function obtains information from the user for daily protein, fat, and carbohydrate intakes in gram, as well as user's weight(kg), height(cm), age, sex, and activity level. 

- **calCalories(protI, fatI, carbI)** function takes the user inputs for protein, fat, and carbohydrate intakes and creates an object of each nutrients class to print the total calories from all three nutrients intake.

- **bodyNeeds(w, h, s, age, proAmt, fatAmt, carbAmt, fac)** function takes user's weight(g), height(cm), sex, age, and activity level (by choose one of the options) as well as daily protein, fat, and carbohydrate intake to print the summaries and suggestions for three different nutrients intake, and for the total calorie intake based on activity level and dietray intake.

#### **visualization** module:

- **entry()** function obtains amount of each of three nutrients daily intake in a certain of time period into a list. This function asks for 3 list input, each of them needs to be at least 7 elements long and all 3 lists need to have the same length. Otherwise, errors will be thrown. It also calculates the calories intake based on the 3 nutrients.

- **nutriTrack(lst1, lst2, lst3, lst4)** function takes all 3 lists of protein, fat, and carbohydrate intake, as well as the sequential number of days to show 3 linked plots. Each of the plot tracks the amount change of the nutrient over time in that particular period. 

- **calorieTrack(lst1, lst2, num)** function takes the list of daily calories intake calulated by the **entry()** function in a particular period, as well as the sequential number of days to show the graph of daily total calories intake over time. The calorie intake for a specific day can be obtained when hover on each point on the graph.





In the subpackage **calories_burned**, it has two modules, *records* and *monitoring*. *Records* is the super class of *Monitoring* and it has 5 funcitons.

***Records***
1. In the initializing stage. It takes name,gender,age,height,weight as arguments 
2. **Records.display()** takes self as argument and print out the details such as name, gender,age ,height and weight in the initializing stage
3. **Records.BMI()** calculates the body mass index based on generated perosnal information and tells the weight status in the ragne from underweiht to obse.
4. **Records.BMR()** calcualtes the Basal metabolic rate. BMR is a measurement of the number of calories needed to perform a person's most basic funcitons such as breathing. Each gender has different formular to calculate BMR
    - ***Female_bmr= 655 + (9.6 * self.weight) + (1.8* self.height- (4.7* self.age))**
    - ***Male_bmr= 66 + (13.7*self.weight) + (5*self.height) - (6.8*self.age)***
5. **Records.totalcal()** calcuates the total borned calories based on BMR, intensity of excerise and the excerise time.Excersise intensity and time are getting from the user's input, for simlicity reason, intensity has only 3 levels 3(Light),4(Moderate),7(Vigorous) and time is measured in minutes,require BMR to be calcualted.

**Prerequisite**
Have pygal installed
pip install pygal


***Monitoring***
Monitoring is the sub class of Records, It could be used to monitory weight and calory changes in weekly or monthly basis
1. In the initializing stage. It  takes all the arguemtns from Records and an additional new arguments calory 
2. **Monitoring.new_weight(newweight)** append daily weight to weight_list
3. **Monitoring.new_calory(newcalory)** append daily burned calory to calory_list
4. **Monitoring.weight_change_plot()** create a line chart which shows the daily weight and the changes overtime 
5. **Monitoring.calory_change_plot()** create a line chart which shows the daily burned calories and the changes overtime
6. **Monitoring.weight_calory_plot()** create a bar chart that contians both daily weight and burned calory in the same graph  

