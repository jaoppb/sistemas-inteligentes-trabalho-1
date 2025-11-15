import argparse
import sys
import io
import pandas as pd

import encode
import countries
import states
from count import count_callbacks, count_graph_callbacks
from total import total_callbacks, total_graph_callbacks
from utils import remove_columns, read_processed


base_names = ["EXP_2024", "IMP_2024", "EXP_2025", "IMP_2025"]


def parse_data(file_base_name):
    with open(f"data/{file_base_name}.csv", "r", encoding="latin-1") as file:
        content = file.read()

    converted_content = encode.convert(content, from_codec="latin-1", to_codec="utf-8")
    data = pd.read_csv(io.StringIO(converted_content), sep=";")

    countries.parse_country_columns(data)
    states.parse_state_columns(data, "SG_UF_NCM")
    remove_columns(data, ["CO_NCM", "CO_URF", "CO_PAIS", "SG_UF_NCM"])

    with open(f"data/{file_base_name}_processed.csv", "w", encoding="utf-8") as file:
        data.to_csv(file, index=False, sep=";")


def parse():
    for file_base_name in base_names:
        parse_data(file_base_name)


def generate_statistics_per_country(data: pd.DataFrame, file_base_name: str):
    top_countries = (
        data.groupby("NOME_PAIS")["VL_FOB"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .index.tolist()
    )

    top_data = data[data["NOME_PAIS"].isin(top_countries)]

    stats_list = []
    for country in top_countries:
        country_data = top_data[top_data["NOME_PAIS"] == country]["VL_FOB"]
        stats_list.append(
            {
                "NOME_PAIS": country,
                "COUNT": country_data.count(),
                "SUM_VL_FOB": country_data.sum(),
                "MEAN_VL_FOB": country_data.mean(),
                "MODE_VL_FOB": country_data.mode()[0]
                if len(country_data.mode()) > 0
                else 0,
                "STD_VL_FOB": country_data.std(),
            }
        )

    stats_df = pd.DataFrame(stats_list)
    output_file = f"data/ESTATISTICAS_POR_PAISES_{file_base_name}.csv"
    stats_df.to_csv(output_file, index=False, sep=";", encoding="utf-8")


def statistics():
    for file_base_name in base_names:
        data = read_processed(file_base_name)
        generate_statistics_per_country(data, file_base_name)


def graphs():
    years = ["2024", "2025"]
    graph_callbacks = [*total_graph_callbacks, *count_graph_callbacks]
    for year in years:
        for call in graph_callbacks:
            call(year)


def process():
    process_callbacks = [
        *total_callbacks,
        *count_callbacks,
    ]
    for file_base_name in base_names:
        for call in process_callbacks:
            call(file_base_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process and analyze trade data files.",
        epilog=f"Example usage: python {sys.argv[0]} parse",
    )

    parser.add_argument(
        "command",
        choices=["parse", "statistics", "process", "graphs"],
        help="The command to execute.",
    )

    args = parser.parse_args()
    if args.command == "parse":
        parse()
    elif args.command == "statistics":
        statistics()
    elif args.command == "process":
        process()
    elif args.command == "graphs":
        graphs()
    else:
        parser.print_help()
        sys.exit(1)
