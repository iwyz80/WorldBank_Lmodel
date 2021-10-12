"""
This python script analyses the world bank GDP data for countries.
Run the createdb.sh file first to create the database
"""

# import packages
import requests, json
from sqlalchemy import create_engine
import numpy as np
import pandas as pd

# GDP data for countries
file_path ='./worldbank_data/countryGDP.csv'
worldbank_api = 'https://api.worldbank.org/v2/country/?format=json'

#create connection to already existing database
db_engine = create_engine('postgresql://mudano0710:mudano0710@localhost/mudano_testdb')

#Make connection to database
db_connect = db_engine.connect()


# Make a request to retrieve countries data from worldBank API and read the response with json
req = requests.get (worldbank_api)
json_res = req.json()

#Read the country's GDP csv file
df_gdp = pd.read_csv(file_path, sep = ',', usecols = ['Country Name', '2018 [2018]','2019 [2019]','2020 [2020]','2021 [2021]','2022 [2022]','2023 [2023]'])

#Rename the columns
columns_rename={'2018 [2018]':'Y_2018','2019 [2019]':'Y_2019','2020 [2020]':'Y_2020','2021 [2021]':'Y_2021','2022 [2022]':'Y_2022','2023 [2023]':'Y_2023'}

df_gdp = df_gdp.rename(columns = columns_rename)

#Drop NAN values
df_gdp.dropna(inplace = True)



#Create an empty dataframe to hold the data from the web response.
df = pd.DataFrame(columns = ['Name', 'IncomeLevel', 'Region'])

#Json data is a dictionary contained in a list.
#Loop through list to extract needed data

for data in json_res[1]: #List has length 2
	Name = data['name']
	IncomeLevel = data['incomeLevel']['value']
	Region = data['region']['value']
	#Append to empty dataframe
	df = df.append({'Name':Name, 'IncomeLevel':IncomeLevel, 'Region':Region}, ignore_index = True)


#Filter the dataframe for incomelevel values that are not aggregate
df = df[df['IncomeLevel']!='Aggregates'].reset_index(drop = True)

#Merge both dataframes together
#Since both dataframe has different length merge on same country name

df_data_merge = pd.merge(df, df_gdp, left_on = 'Name', right_on = 'Country Name').drop(columns = 'Country Name')

#Y_2022 and Y_2023 columns are of string object type. Convert to float
df_data_merge[['Y_2022', 'Y_2023']] = df_data_merge[['Y_2022', 'Y_2023']].astype(float)

#Calculate cummulative GDP
df_data_merge['cumulativeGDP'] = df_data_merge[['Y_2018', 'Y_2019', 'Y_2020', 'Y_2021', 'Y_2022', 'Y_2023']].sum(axis = 1)

#Order IncomeLevel. Create a new column to set integer values according to income level
def order_income(dataframe):
	for k in dataframe:
		for keys,values in {'High income':4, 'Upper middle income':3, 'Lower middle income':2,'Low income':1}.items():
			if k ==keys:
			
				return values
df_data_merge['incomelevel_weight'] = df_data_merge.apply(order_income, axis = 1)

#Calculate the year on Year GDP percentage
yOny_list = ['YonY_2018_2019','YonY_2019_2020','YonY_2020_2021','YonY_2021_2022','YonY_2022_2023']
gdp_year = ['Y_2018','Y_2019','Y_2020','Y_2021','Y_2022','Y_2023']
l = 0
while l <= len(gdp_year)-2:
	df_data_merge[''+yOny_list[l]] = round((df_data_merge[''+gdp_year[l+1]]-df_data_merge[''+gdp_year[l]])/df_data_merge[''+gdp_year[l]]*100,2)
	l+=1




#Store data in the database
df_data_merge.to_sql('country_GDP_Data', db_connect, if_exists = 'replace', index = False)

#commit changes to Database
db_connect.execute ('commit')


#SQL Statements
'''
sql_statement_1 = """SELECT "Name" FROM "country_GDP_Data" WHERE "IncomeLevel" ='Upper middle income'; """
sql_statement_2 = """SELECT "Name", "Region", "IncomeLevel", COUNT("Region")  OVER(PARTITION BY "Region")FROM "country_GDP_Data"  WHERE "IncomeLevel" = 'Low income'; """
sql_statement_3 = """SELECT "Region","IncomeLevel",COUNT("IncomeLevel")  OVER (PARTITION BY "Region") FROM "country_GDP_Data" WHERE "IncomeLevel" = 'High income' ORDER BY count DESC FETCH First 1 row only; """
sql_statement_4 = """SELECT "Name","Region","IncomeLevel", "Y_2018", "Y_2019", "Y_2020", "Y_2021", "Y_2022", "Y_2023", SUM("Y_2018") OVER(PARTITION BY "Region") as sum_2018, SUM("Y_2019") OVER(PARTITION BY "Region") as sum_2019 , SUM("Y_2020") OVER(PARTITION BY "Region") as sum_2020, SUM("Y_2021") OVER(PARTITION BY "Region") as sum_2021, SUM("Y_2022") OVER(PARTITION BY "Region") as sum_2022, SUM("Y_2023") OVER(PARTITION BY "Region") as sum_2023 FROM "country_GDP_Data" ORDER BY("incomelevel_weight","Name"); """

sql_statement_5 = """SELECT "Name","YonY_2018_2019", "YonY_2019_2020", "YonY_2020_2021", "YonY_2021_2022", "YonY_2022_2023" FROM "country_GDP_Data";"""
sql_statement_6 = """SELECT "Name", "cumulativeGDP","Region",  Min("cumulativeGDP")  OVER (PARTITION BY "Region") FROM "country_GDP_Data";"""
sql_list = [sql_statement_1, sql_statement_2, sql_statement_3, sql_statement_4, sql_statement_5, sql_statement_6]
count_q = 0
for query in sql_list:
	count_q+=1
	sql_execute =  (db_engine.execute(query))
	print ("\n","SQL Result "+ str(count_q) +": " ,query, "\n"*2 )
	for result in sql_execute:
		print (result)'''

#Read data from database
print (pd.read_sql ('country_GDP_Data', db_connect))

#Close database connection
db_connect.close()

	

