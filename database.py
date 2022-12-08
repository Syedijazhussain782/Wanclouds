# These are the queries you need to execute to your local DB

"""
CREATE TABLE `car_model_schema`.`car_model` (
  `objectId` VARCHAR(10) NOT NULL,
  `Year` INT NULL,
  `Make` VARCHAR(50) NULL,
  `Model` VARCHAR(500) NULL,
  `Category` VARCHAR(500) NULL,
  PRIMARY KEY (`objectId`));

ALTER TABLE `car_model_schema`.`car_model` 
ADD COLUMN `createdAt` VARCHAR(100) NULL AFTER `Category`,
ADD COLUMN `updatedAt` VARCHAR(100) NULL AFTER `createdAt`;

"""

import mysql.connector    
# MySQL connector
# Here in place of user, password and database we have to write our credentials.
cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='car_model_schema')
cursor = cnx.cursor()

# Function used to insert data into database
# Data will be inserted if not exist and will be updated otherwise.
def insert(data):
    query = """INSERT INTO car_model (objectId, Year, Make, Model, Category, createdAt, updatedAt) VALUES (%s, %s, %s, %s, %s, %s, %s) AS new 
            ON DUPLICATE KEY UPDATE Year=new.Year, Make=new.Make, Category=new.Category, createdAt=new.createdAt, updatedAt=new.updatedAt
            ;""",data
    cursor.execute(*query)

# For the Search APIs
# syntax is /get?make=Ford&year=2013&model=Mustang
# all these parameters are optional if none of the parameter is used then it will fetch all the data.
def search_db(make,model,year):
  query_string = []
  if make:
    query_string.append("make='"+str(make)+"'")
  if year:
    query_string.append("year='"+str(year)+"'")
  if model:
    query_string.append("model='"+str(model)+"'")

  if len(query_string)>0:
    query_string = " AND ".join(query_string)
    query_string = " WHERE "+query_string
  else:
    query_string = ""
  query = "SELECT * FROM car_model %s;" % (query_string)

  cursor.execute(query)
  result = cursor.fetchall()
  return result

# function used to commit data
def commit():
  cnx.commit()
  print("Data inserted successfully.")



    
    