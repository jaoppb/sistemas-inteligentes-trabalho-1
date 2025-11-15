import pandas as pd
import matplotlib.pyplot as plt


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


month_names = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]


def plot_combined_graph(
    data_exp: pd.DataFrame,
    data_imp: pd.DataFrame,
    x_column: str,
    x_label: str,
    y_column: str,
    y_label: str,
    title: str,
    file_name: str,
    sort_by: str | None = None,
):
    merged = pd.merge(
        data_exp[[x_column, y_column]],
        data_imp[[x_column, y_column]],
        on=x_column,
        how="outer",
        suffixes=("_EXP", "_IMP"),
    )

    if sort_by == "y":
        merged["_total"] = merged[f"{y_column}_EXP"] + merged[f"{y_column}_IMP"]
        merged = merged.sort_values("_total", ascending=False).drop(columns=["_total"])
    elif sort_by == "x":
        merged = merged.sort_values(x_column)

    ax = merged.plot(
        kind="bar",
        x=x_column,
        y=[f"{y_column}_EXP", f"{y_column}_IMP"],
        title=title,
        color=["#2E86AB", "#A23B72"],
        figsize=(12, 6),
    )

    ax.legend(["Exportação", "Importação"])

    plt.xticks(rotation=45, ha="right")
    plt.xlabel(x_label)

    plt.ticklabel_format(axis="y", style="plain")
    plt.ylabel(y_label)

    plt.tight_layout()
    plt.savefig(file_name)
    plt.close()
