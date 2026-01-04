import pandas as pd 


df = pd.read_csv("BMW sales data (2010-2024) (1) (1).csv")

column = df.columns.to_list()

print(column)


