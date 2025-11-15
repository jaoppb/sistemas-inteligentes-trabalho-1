import pandas as pd


def read_csv(file_name: str) -> pd.DataFrame:
    return pd.read_csv(file_name, sep=";")


def save_csv(data: pd.DataFrame, file_name: str):
    data.to_csv(file_name, index=False, sep=";")


def remove_columns(data: pd.DataFrame, columns: list[str]):
    for column in columns:
        if column in data.columns:
            del data[column]


def read_processed(file_base_name):
    with open(f"data/{file_base_name}_processed.csv", "r", encoding="utf-8") as file:
        data = pd.read_csv(file, sep=";")
    return data
