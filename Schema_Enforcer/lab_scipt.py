import csv
import json 
import pandas as pd

df = [
    ['student_id', 'major', 'GPA', 'is_cs_major', 'credits_taken'],
    [101, 'Computer Science', 4, 'Yes', '78.0'],
    [102, 'Behavioral Neuroscience', 3.9, 'No', '80.5'],                
    [103, 'Anthropology',3.6, 'No', '105.0'],
    [104, 'Data Science', 3, 'Yes','65.1'],
    [105,'Media Studies', 2.9, 'No', '15.0']
]
with open('raw_survey_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(df)
print("yay it worked") 

list_dict = [
  {
    "course_id": "DS2002",
    "section": "001",
    "title": "Data Science Systems",
    "level": 200,
    "instructors": [
      {"name": "Austin Rivera", "role": "Primary"}, 
      {"name": "Heywood Williams-Tracy", "role": "TA"} 
    ]
  },
  {
    "course_id": "DS2003",
    "title": "Communicating Data",
    "level": 2000,
    "instructors": [
      {"name": "Aaron Abrams", "role": "Professor"}
    ]
  },
  {
    "course_id": "PSYC2100",
    "title": "Neuroscience of Behavior",
    "level": 2000,
    "instructors": [
      {"name": "Cedric Williams", "role": "Professor"}
    ]
  },
  {
    "course_id": "ANTH2280",
    "title": "Medical Anthropology",
    "level": 2000,
    "instructors": [
      {"name": "Jarrett Zigon", "role": "Professor"}
    ]
  },
  {
    "course_id": "PSYC2006",
    "title": "Research Methods and Data Analysis II",
    "level": 2000,
    "instructors": [
      {"name": "Schmidt", "role": "Professor"}
    ]
  }
]
with open('raw_course_catalog.json', 'w') as myfile:
    json.dump(list_dict, myfile)
print("YASSS")


df = pd.read_csv('raw_survey_data.csv')
df['is_cs_major'] = df['is_cs_major'].replace({
    "Yes": True,
    "No": False
})

int_df = df.astype({
    'credits_taken': 'float64',
    'GPA': 'float64'
})

int_df.to_csv("clean_survey_data.csv", index=False)
print("nice and tidy")

with open("raw_course_catalog.json") as myfile:
    df = json.load(myfile)

df_json = pd.json_normalize(df, record_path=['instructors'], meta=['course_id', 'title', 'level'])
df_json.to_csv('clean_course_catalog.csv', index=False)
print("all done here")

