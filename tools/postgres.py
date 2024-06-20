import os
import re
import json

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv


class PostgresHelper:
    """
    A helper class to interact with PostgreSQL using SQLAlchemy.
    """
    
    def __init__(self) -> None:
        """
        Initialize the PostgresHelper class by loading environment variables
        and creating a SQLAlchemy engine.
        """
        load_dotenv()
        self.conn_string = os.getenv('POSTGRES_CONN_STRING')
        if not self.conn_string:
            raise ValueError("POSTGRES_CONN_STRING environment variable not set")
        self.engine = create_engine(self.conn_string)
        
    def get_engine(self):
        """
        Get the SQLAlchemy engine. If it does not exist, create a new one.
        
        Returns:
            engine (Engine): SQLAlchemy engine.
        """
        if not self.engine:
            self.engine = create_engine(self.conn_string)
        return self.engine

    def create_table_from_dataframe(self, df: pd.DataFrame, table_name: str):
        """
        Create a table in the database from a DataFrame.
        
        Args:
            df (pd.DataFrame): The DataFrame to be converted into a table.
            table_name (str): The name of the table to be created.
            
        Raises:
            SQLAlchemyError: If there is an error creating the table.
        """
        try:
            # Sanitize column names
            sanitized_columns = {col: re.sub(r"\W+", "_", col) for col in df.columns}
            df = df.rename(columns=sanitized_columns)
            
            # Create table from DataFrame
            df.to_sql(table_name, self.engine, if_exists='fail', index=False)
            print(f"Table {table_name} created successfully.")
        except SQLAlchemyError as e:
            print(f"Error creating table {table_name}: {e}")

    def save_table_object(self, table):
        """
        Save a table object to the database.
        
        Args:
            table (object): An object with 'name' and 'data' attributes.
        """
        table_name = table.name
        df = pd.DataFrame(table.data)
        self.create_table_from_dataframe(df, table_name)
        

if __name__ == "__main__":
    postgres = PostgresHelper()
    
    try:
        with open('table.json') as file:
            json_data = json.loads(file.read())
            table_name = json_data['name']
            df = pd.DataFrame(json_data['data'])
            postgres.create_table_from_dataframe(df, table_name)
    except FileNotFoundError:
        print("The file 'table.json' was not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON from 'table.json'.")
    except KeyError as e:
        print(f"Missing key in JSON data: {e}")
