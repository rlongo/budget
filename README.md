# Budget Tracking App 

My personal utility for managing and visualizing expenses and income throughout the year(s).
Note that this is meant to be a quick to use, easy(ish) to maintain script!

## Usage

1. Setup the dependencies in `requirements.txt`.
2. Setup a directory called `inputs` with a set of csv files tracking your income and expenses (see next section).
Note that every file in the directory is read, so you can manage the granularity you want.
3. Basic `make` commands to get what you want:
    1. `make show` to open the budget output (in firefox)
    2. `make tracker` to get the output file
    3. `make clean` ;p

## Budget Files

Budget files work on an organization scheme with 3 indices:
1. First index is either one of `income` or `expense`
2. Any general second category.
3. A subcategory to #2

After that, you setup:
1. A `budget` (How much you wanted to spend)
2. `spend` (the actual damage)

Also note that you need to have the same header line just like in my file below

Here is an example to get you started:

```csv
type,category,subcategory,date-year,date-month,budget,spend
income,revenue,salary,2019,10,1000,1000
income,revenue,side hustle,2019,10,100,150
expense,living,gas,2019,10,100,50
expense,living,food,2019,10,300,250
expense,purchases,other,2019,10,50,75
expense,debt,car,2019,10,300,250
expense,services,phone,2019,10,20,20
expense,services,gym,2019,10,15,15
expense,savings,emergency,2019,10,100,110
```
