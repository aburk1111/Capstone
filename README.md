# Capstone
Capstone Project
Amanda Brach

REMOVED -Net worth information taken from https://www.opensecrets.org/personal-finances/top-net-worth 

partyCode was readily available information on the internet as it is a standardized code structure.

generations.csv was generated using ChatGPT and converted to a csv format

lifeExpectancy.csv was generated using ChatGPT

REMOVED -VM steps -> Powershell script to pull data sources from GitHub -> SSIS then uses Execute Process Task to run the Powershell and put the exported data in the SQL Integration 

Due to the VM being difficult I moved the ETL steps to Python and removed all SQL steps for the process. 
Python script 
1. reads the csv files from GitHub
2. runs transformation steps 
3. drops them in a dedicated C drive location
  
C Drive location is where the documents are being pulled into Power BI

Additional transformations in Power BI
- Added Generation Sort table and column
- Creates a birth year column in fact_congress by subtracting their age from the year they served
- Creates a column in the fact table that brings in the Life Expectancy for their birth year
- Subtracts the age from life expectancy to see the variance per person serving in congress at the time of service
  
