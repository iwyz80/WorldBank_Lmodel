
This repo contains 3 files and 1 folder.

	1.  requirement.txt
	2.  create_db.sh
	3.  worldbank_code.py
	4.  worldbank_data/
	

Run  ```pip3 install -r requirement.txt```

> -This will install all the necessary dependencies.

Run ```bash create_db.sh```
> This will create a Postgres Database named mudano_testdb. 
> 
> Username and password for the owner of the Database is also created.
 
	username:mudano0710
	
	password:mudano0710

Run ```python3 worldbank_code.py```

> -This will run the python script and save the necessary data to the mudano_testdb Database.

You can query the database directly from the python script by uncommenting the SQL queries section 
in the python script.

# OR

Run ```psql -h localhost -U mudano0710 mudano_testdb```

Enter the password given above to connect to the Database.

Query the Database using the listed SQL queries

	1. sql_statement_1 = SELECT "Name" FROM "country_GDP_Data" WHERE "IncomeLevel" ='Upper middle income'; 
	2. sql_statement_2 = SELECT "Name", "Region", "IncomeLevel", COUNT("Region")  OVER(PARTITION BY "Region")FROM "country_GDP_Data"  WHERE "IncomeLevel" = 'Low income';
	3. sql_statement_3 = SELECT "Region","IncomeLevel",COUNT("IncomeLevel")  OVER (PARTITION BY "Region") FROM "country_GDP_Data" WHERE "IncomeLevel" = 'High income' ORDER BY count DESC FETCH First 1 row only; 
	4. sql_statement_4 = SELECT "Name","Region","IncomeLevel", "Y_2018", "Y_2019", "Y_2020", "Y_2021", "Y_2022", "Y_2023", SUM("Y_2018") OVER(PARTITION BY "Region") as sum_2018, SUM("Y_2019") 			OVER(PARTITION BY "Region") as sum_2019 , SUM("Y_2020") OVER(PARTITION BY "Region") as 	sum_2020, SUM("Y_2021") OVER(PARTITION BY "Region") as sum_2021, SUM("Y_2022") OVER(PARTITION BY "Region") as sum_2022, SUM("Y_2023") OVER(PARTITION BY "Region") as sum_2023 FROM 		"country_GDP_Data" ORDER BY("incomelevel_weight","Name");

	5. sql_statement_5 = SELECT "Name","YonY_2018_2019", "YonY_2019_2020", "YonY_2020_2021", "YonY_2021_2022", "YonY_2022_2023" FROM "country_GDP_Data";
	6. sql_statement_6 = SELECT "Name", "cumulativeGDP","Region",  Min("cumulativeGDP")  OVER (PARTITION BY "Region") FROM "country_GDP_Data";
