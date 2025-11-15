from utils import save_csv, read_processed, read_csv, plot_combined_graph


def format_base_file_name(file_base_name, label):
    return f"CONTAGEM_POR_{label}_{file_base_name}"


def format_csv_file_name(file_base_name, label):
    return f"data/{format_base_file_name(file_base_name, label)}.csv"


def process_count(file_base_name, column, label):
    data = read_processed(file_base_name)[column].value_counts().reset_index()
    data.columns = [column, "QUANTIDADE"]
    save_csv(data, format_csv_file_name(file_base_name, label))


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


def graph_count_per(year, label, x_column, x_label, title_prefix, sort_by, limit=None):
    exp_file = f"EXP_{year}"
    imp_file = f"IMP_{year}"

    data_exp = read_csv(format_csv_file_name(exp_file, label))
    data_imp = read_csv(format_csv_file_name(imp_file, label))

    y_column = "QUANTIDADE"
    data_exp[y_column] = data_exp[y_column] / 1_000
    data_imp[y_column] = data_imp[y_column] / 1_000

    file_name = f"data/graphics/CONTAGEM_POR_{label}_{year}.png"
    title = f"{title_prefix} - {year}"

    plot_combined_graph(
        data_exp,
        data_imp,
        x_column=x_column,
        x_label=x_label,
        y_column=y_column,
        y_label="Quantidade (em milhares)",
        title=title,
        file_name=file_name,
        sort_by=sort_by,
        limit=limit,
    )


def graph_count_country(year):
    graph_count_per(
        year,
        label="PAIS",
        x_column="NOME_PAIS",
        x_label="País",
        title_prefix="Contagem por País",
        sort_by="y",
        limit=10,
    )


def graph_count_uf(year):
    graph_count_per(
        year,
        label="UF",
        x_column="NOME_UF",
        x_label="Unidade Federativa",
        title_prefix="Contagem por Unidade Federativa",
        sort_by="y",
    )


def graph_count_month(year):
    graph_count_per(
        year,
        label="MES",
        x_column="CO_MES",
        x_label="Mês",
        title_prefix="Contagem por Mês",
        sort_by="x",
    )


count_graph_callbacks = [
    graph_count_country,
    graph_count_uf,
    graph_count_month,
]
