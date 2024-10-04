import pandas as pd

with open('vlr90.json', encoding='utf-8') as inputfile:
    df = pd.read_json(inputfile)

df.to_csv('vlr90.csv', encoding='utf-8', index=False)