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
file_name = "[1]game_logs.csv"

def change_types(my_df: pd.DataFrame):
    memory_stats = get_memory_stats(my_df, file_name)
    write_stats_to_file(memory_stats[0], memory_stats[1], memory_stats[2], "without_optimization.json")
    change_obj_to_cat(my_df)
    memory_stats = get_memory_stats(my_df, file_name)
    write_stats_to_file(memory_stats[0], memory_stats[1], memory_stats[2], "optimization.json")


def select_columns(my_df: pd.DataFrame):
    column_names = [
        "date",
        "number_of_game",
        "day_of_week",
        "v_league",
        "v_score",
        "day_night",
        "forefeit",
        "v_homeruns",
        "h_walks",
        "v_manager_name",
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

# Распределение игр по дням недели с течением времени
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['day_of_week'])
plt.title('Распределение игр по дням недели с течением времени')
plt.xlabel('Дата')
plt.ylabel('День недели')
plt.savefig('plot1.png')

# Гистограмма количества игр по каждому дню недели
plt.figure(figsize=(8, 6))
sns.countplot(x='day_of_week', data=df)
plt.title('Количество сыгранных игр по каждому дню недели')
plt.xlabel('День недели')
plt.ylabel('Количество игр')
plt.savefig('plot2.png')

# Пай-чарт распределения топ-10 имен менеджеров
top_managers = df['v_manager_name'].value_counts().nlargest(10).index
df['v_manager_name_top'] = df['v_manager_name'].apply(lambda x: x if x in top_managers else 'Другие')

# Удаление временной колонки v_manager_name_top
df.drop('v_manager_name_top', axis=1, inplace=True)

# Создание графика рассеяния для счета и дня недели
plt.figure(figsize=(10, 6))
sns.scatterplot(x='v_score', y='day_of_week', data=df)
plt.title('Диаграмма рассеяния счета и дня недели')
plt.xlabel('Счет')
plt.ylabel('День недели')
plt.savefig('plot3.png')

# Создание box plot по дням недели
plt.figure(figsize=(10, 5))
sns.boxplot(x='day_of_week', y='v_homeruns', data=df)
plt.title('Статистика v_homeruns по дням недели')
plt.xlabel('День недели')
plt.ylabel('v_homeruns')
plt.savefig('plot4.png')

# Создание гистограммы для распределения h_walks
plt.figure(figsize=(10, 6))
plt.hist(df['h_walks'], bins=20, color='skyblue', edgecolor='black')
plt.title('Распределение h_walks')
plt.xlabel('h_walks')
plt.ylabel('Частота')
plt.savefig('plot5.png')

plt.figure(figsize=(10, 6))
plt.plot(df['day_of_week'], df['v_score'])
plt.title('График счета в определенные дни недели')
plt.xlabel('День недели')
plt.ylabel('Счет')
plt.savefig('plot6.png')
