import os, json, sqlparse
from openai_dbd import (
    generate_sql, 
    sql_prompt, 
    correct_schema,
    json_prompt, 
    generate_excel, 
    convert_json_to_sql, 
    json_to_python_models, 
    json_to_sequelize_models,
)

AI_KEY = os.getenv('OPENAI_API_KEY')
URL = os.getenv('OPENAI_API_URL')

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AI_KEY}"
}

def myExcl(data, sql=None):
    try:
        json_data = None

        projectCategory = data['project_title']
        featureOfDBStructure = data['project_feature']

        AIdata = sql_prompt(projectCategory, featureOfDBStructure, {"url": URL, "headers": HEADERS}) if sql else json_prompt(projectCategory, featureOfDBStructure, {"url": URL, "headers": HEADERS})
        
        if(sql):
            data = AIdata['choices'][0]['message']['content'].replace("\n", "").replace(";", ";\n\n")

            return generate_sql(projectCategory, data)
        else:
            json_data = json.loads(AIdata['choices'][0]['message']['content'].replace("\n", "").replace("\\", ""))

            return generate_excel(projectCategory, json_data)
    except Exception as ex:
        print(ex)
        return None

def myJson(data):
    try:
        projectCategory = data['project_title']
        featureOfDBStructure = data['project_feature']

        AIdata = json_prompt(projectCategory, featureOfDBStructure, {"url": URL, "headers": HEADERS})
        
        return json.loads(AIdata['choices'][0]['message']['content'].replace("\n", "").replace("\\", ""))
    except Exception as ex:
        print(ex)
        return None
    
def jsonToExcel(data):
    try:
        return generate_excel(data['title'], data['json_obj'])
    except Exception as ex:
        print(ex)
        return None
    
def jsonToSql(data):
    try:
        data = convert_json_to_sql(json.dumps(data['json_obj']), {"url": URL, "headers": HEADERS})
        return sqlparse.parse(data['choices'][0]['message']['content'].replace("\n", "").replace("\\", ""))
    except Exception as ex:
        print(ex)
        return None
    
def jsonToPythonModels(data):
    try:
        return json_to_python_models(data['json_obj'])
    except Exception as ex:
        print(ex)
        return None

def jsonToSequelizeModels(data):
    try:
        return json_to_sequelize_models(data['json_obj'])
    except Exception as ex:
        print(ex)
        return None
    
def correctExistingDB(data):
    try:
        if data['sql_file']:
            AIdata = correct_schema(data['feature_change'], data['sql_file'], {"url": URL, "headers": HEADERS})
            if('error' in AIdata.keys()):
                return None
        
            return sqlparse.format(AIdata['choices'][0]['message']['content'].replace("\n", "").replace("\\", ""), reindent=True, keyword_case='upper')

    except Exception as ex:
        print(ex)
        return None