import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
openagent_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(openagent_dir)


from openagent.tools.toolkits.SQL import SQLDatabaseToolkit
from openagent.helpers.sql_database import SQLDatabase
from openagent.llms._openai import OpenAI

llm=OpenAI(
    model_name = "gpt-3.5-turbo",
    openai_api_key=""
    )

#Connect to database using connection string
db = SQLDatabase.from_uri("postgresql://zdacfiltaeqgfboocygtccgo%40psql-mock-database-cloud:mgsnfujnrvpcbvunovxzizhk@psql-mock-database-cloud.postgres.database.azure.com:5432/ecom1690210583529ypqrqrnjpngzufrw")


toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()


print(tools[0]._run("select * from customers")) #QUERYSQLDataBase tool
print("----------------------------------------------------------------------------------------------------------------------------------")

print(tools[1]._run("customers, employees, offices")) #INFOSQLDataBase tool
print("----------------------------------------------------------------------------------------------------------------------------------")

print(tools[2]._run())  #LISTSQLDataBase tool
