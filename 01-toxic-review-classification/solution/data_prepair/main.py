from data_prepair.utils import clean_one
import pandas as pd

df = pd.read_excel("../data/code-review-dataset-full.xlsx")

# Убираем явный мусор
df = df.dropna()
df = df.drop_duplicates().reset_index(drop=True)

# Очищаем текст
df["message"] = df["message"].map(clean_one)

# Удаляем пустые строки после очистки
df = df[df["message"].str.len() > 0].reset_index(drop=True)

df.to_csv("../data/code-review-dataset-clear.csv", index=False)
