import pandas as pd
import os
import json
from sqlalchemy import create_engine
import sys
sys.path.insert(1, '../telegram_bot')
from config import USER_NAME, DATABASE_NAME, PASSWORD, HOST_NAME, PORT

# Enter path to JSON files for import
path_to_data = '/home/cats/Files/Homework/DevDays/files2/'


# Extract all files with data in directory
def extract_data_files(path):
    file_list = [file for file in os.listdir(path) if
                 os.path.isfile(os.path.join(path, file))]
    return file_list


# Convert JSON data stored in file into dataframe
def json_to_sql(path):
    df_result = pd.DataFrame(columns=['title', 'description', 'examples', 'hints', 'constraints', 'difficulty',
                                      'related_topics', 'company', 'stage', 'link'])
    file_list = extract_data_files(path)
    for i in range(len(file_list)):
        with open(path + str(file_list[i])) as file:
            data = json.load(file)
            df_data = pd.DataFrame([data])
            if df_data['link'][0] not in list(df_result['link']):
                df_result = pd.concat([df_result, df_data], ignore_index=True, sort=False)

    return df_result


# Json data stored in dataframe insert into PostgreSQL table
def insert_into_table_postgres(path, table_name='tasks'):
    result = json_to_sql(path)
    engine = create_engine(f'postgresql://{USER_NAME}:{PASSWORD}@{HOST_NAME}:{PORT}/{DATABASE_NAME}')
    result.to_sql(table_name, engine, if_exists='append', index=False)


insert_into_table_postgres(path_to_data)
