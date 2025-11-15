from utils import read_processed, save_csv


def process_total_per(file_base_name, column, label):
    data = (
        read_processed(file_base_name)
        .groupby(column)["VL_FOB"]
        .sum()
        .reset_index()
        .rename(columns={"VL_FOB": "TOTAL_VL_FOB"})
        .sort_values(by="TOTAL_VL_FOB", ascending=False)
    )
    save_csv(data, f"data/TOTAL_POR_{label}_{file_base_name}.csv")


def total_per_country(file_base_name):
    process_total_per(file_base_name, "NOME_PAIS", "PAIS")


def total_per_uf(file_base_name):
    process_total_per(file_base_name, "NOME_UF", "UF")


def total_per_month(file_base_name):
    process_total_per(file_base_name, "CO_MES", "MES")


total_callbacks = [
    total_per_country,
    total_per_uf,
    total_per_month,
]
