from utils import read_processed, save_csv, read_csv, plot_combined_graph


def format_base_file_name(file_base_name, label):
    return f"TOTAL_POR_{label}_{file_base_name}"


def format_csv_file_name(file_base_name, label):
    return f"data/{format_base_file_name(file_base_name, label)}.csv"


def format_graph_file_name(file_base_name, label):
    return f"data/graphics/{format_base_file_name(file_base_name, label)}.png"


def process_total_per(file_base_name, column, label):
    data = (
        read_processed(file_base_name)
        .groupby(column)["VL_FOB"]
        .sum()
        .reset_index()
        .rename(columns={"VL_FOB": "TOTAL_VL_FOB"})
        .sort_values(by="TOTAL_VL_FOB", ascending=False)
    )
    save_csv(data, format_csv_file_name(file_base_name, label))


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


def graph_total_per(year, label, x_column, x_label, title_prefix, sort_by, limit=None):
    exp_file = f"EXP_{year}"
    imp_file = f"IMP_{year}"

    data_exp = read_csv(format_csv_file_name(exp_file, label))
    data_imp = read_csv(format_csv_file_name(imp_file, label))

    y_column = "TOTAL_VL_FOB"
    data_exp[y_column] = data_exp[y_column] / 1_000_000_000
    data_imp[y_column] = data_imp[y_column] / 1_000_000_000

    file_name = f"data/graphics/TOTAL_POR_{label}_{year}.png"
    title = f"{title_prefix} - {year}"

    plot_combined_graph(
        data_exp,
        data_imp,
        x_column=x_column,
        x_label=x_label,
        y_column=y_column,
        y_label="Em Dolar Por Bilhão",
        title=title,
        file_name=file_name,
        sort_by=sort_by,
        limit=limit,
    )


def graph_total_per_country(year):
    graph_total_per(
        year,
        "PAIS",
        "NOME_PAIS",
        "Países",
        "Volume Total por País",
        "y",
        12,
    )


def graph_total_per_uf(year):
    graph_total_per(
        year,
        "UF",
        "NOME_UF",
        "Unidades Federais",
        "Volume Total por UF",
        "y",
    )


def graph_total_per_month(year):
    graph_total_per(
        year,
        "MES",
        "CO_MES",
        "Meses",
        "Volume Total por Mês",
        None,
    )


total_graph_callbacks = [
    graph_total_per_country,
    graph_total_per_uf,
    graph_total_per_month,
]
