from utils import save_csv, read_processed


def process_count(file_base_name, column, label):
    data = read_processed(file_base_name)[column].value_counts().reset_index()
    data.columns = [column, "QUANTIDADE"]
    save_csv(data, f"data/CONTAGEM_POR_{label}_{file_base_name}.csv")


def process_count_country(file_base_name):
    process_count(file_base_name, "NOME_PAIS", "PAIS")


def process_count_uf(file_base_name):
    process_count(file_base_name, "NOME_UF", "UF")


def process_count_month(file_base_name):
    process_count(file_base_name, "CO_MES", "MES")


count_callbacks = [
    process_count_country,
    process_count_uf,
    process_count_month,
]
