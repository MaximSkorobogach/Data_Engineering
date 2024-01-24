#https://www.kaggle.com/datasets/ryanholbrook/dl-course-data/data

import pandas as pd
import sys
import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns


# fix int64 is not serializable
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def insert_data(file_name, data_to_insert):
    with open(file_name, "w", encoding="utf-8") as json_file:
        json.dump(data_to_insert, json_file, indent=2, ensure_ascii=False)

def get_memory_stats(df, file_name):
    file_size = {"file_size_KB": os.path.getsize(file_name) // 1024}

    memory_usage = df.memory_usage(deep=True)
    total_memory = memory_usage.sum()
    in_memory_size = {"file_in_memory_size_KB": total_memory // 1024}

    column_stat = pd.DataFrame(
        {
            "column_name": df.columns,
            "memory_abs": [memory_usage[key] // 1024 for key in df.columns],
            "memory_per": [
                round(memory_usage[key] / total_memory * 100, 4)
                for key in df.columns
            ],
            "dtype": df.dtypes.values,
        }
    )

    column_stat_sorted = column_stat.sort_values(by="memory_abs", ascending=False)
    return (file_size, in_memory_size, column_stat_sorted)

def change_obj_to_cat(df):
    for column in df.columns:
        if df[column].dtype == "object":
            unique_values = len(df[column].unique())
            total_values = len(df[column])
            if unique_values / total_values < 0.5:
                df[column] = df[column].astype("category")
        if pd.api.types.is_integer_dtype(df[column]):
            df[column] = pd.to_numeric(df[column], downcast="unsigned")
        if pd.api.types.is_float_dtype(df[column]):
            df[column] = pd.to_numeric(df[column], downcast="float")

def write_stats_to_file(file_stat, mem_stat, by_columns, output_file_name):
    with open(output_file_name, "w", encoding="utf-8") as r_json:
        combined_json = {}
        combined_json.update(file_stat)
        combined_json.update(mem_stat)
        res = by_columns.to_json(orient="index", default_handler=str)
        parsed = json.loads(res)
        combined_json.update(parsed)
        json.dump(combined_json, r_json, indent=2, ensure_ascii=False, cls=NpEncoder)


pd.set_option("display.max_rows", 20, "display.max_columns", 60)
sys.path.append("..")
file_name = "diamonds.csv"

def change_types(my_df: pd.DataFrame):
    memory_stats = get_memory_stats(my_df, file_name)
    write_stats_to_file(memory_stats[0], memory_stats[1], memory_stats[2], "without_optimization.json")
    change_obj_to_cat(my_df)
    memory_stats = get_memory_stats(my_df, file_name)
    write_stats_to_file(memory_stats[0], memory_stats[1], memory_stats[2], "optimization.json")


def select_columns(my_df: pd.DataFrame):
    column_names = [
        "carat",
        "cut",
        "color",
        "clarity",
        "depth",
        "table",
        "price",
        "x",
        "y",
        "z",
    ]
    types = my_df.dtypes.to_dict()
    first_chunk = True
    for chunk in pd.read_csv(
        file_name,
        usecols=lambda x: x in column_names,
        dtype=types,
        chunksize=100_000,
    ):
        chunk.to_csv("columns.csv", mode= 'w' if first_chunk else 'a', header=first_chunk, index=False)
        first_chunk = False

    with open("types.pkl", "wb") as file:
        pd.to_pickle(types, file)


my_df = pd.read_csv(file_name)
change_types(my_df)
select_columns(my_df)

with open("types.pkl", "rb") as file:
    loaded_column_types = pd.read_pickle(file)
df = pd.read_csv("columns.csv", dtype=loaded_column_types)

# 1. Диаграмма рассеяния: Карат vs. Цена
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='carat', y='price')
plt.title('Диаграмма рассеяния: Карат vs. Цена')
plt.xlabel('Карат')
plt.ylabel('Цена')
plt.savefig('plot1.png')

# 2. Столбчатая диаграмма: Количество по огранке
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='cut')
plt.title('Столбчатая диаграмма: Количество по огранке')
plt.xlabel('Огранка')
plt.ylabel('Количество')
plt.savefig('plot2.png')

# 3. Коробчатая диаграмма: Цена по огранке
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='cut', y='price')
plt.title('Коробчатая диаграмма: Цена по огранке')
plt.xlabel('Огранка')
plt.ylabel('Цена')
plt.savefig('plot3.png')

# 4. Круговая диаграмма: Распределение по цветам
plt.figure(figsize=(10, 6))
df['color'].value_counts().plot.pie(autopct='%1.1f%%')
plt.title('Круговая диаграмма: Распределение по цветам')
plt.savefig('plot4.png')

# 5. Гистограмма: Распределение по глубине
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='depth', bins=30, kde=True)
plt.title('Гистограмма: Распределение по глубине')
plt.xlabel('Глубина')
plt.ylabel('Частота')
plt.savefig('plot5.png')
