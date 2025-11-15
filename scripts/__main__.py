import argparse
import sys
import io
import pandas as pd

import encode
import countries
import states


base_names = ["EXP_2024", "IMP_2024", "EXP_2025", "IMP_2025"]


def remove_columns(data: pd.DataFrame, columns: list[str]):
    for column in columns:
        if column in data.columns:
            del data[column]


def process_total_per(file_base_name, column, label):
    pd.read_csv(f"data/{file_base_name}_processed.csv", sep=";").groupby(column)[
        "VL_FOB"
    ].sum().reset_index().rename(columns={"VL_FOB": "TOTAL_VL_FOB"}).sort_values(
        by="TOTAL_VL_FOB", ascending=False
    ).to_csv(f"data/TOTAL_POR_{label}_{file_base_name}.csv", index=False)


def process_per_country(file_base_name):
    process_total_per(file_base_name, "NOME_PAIS", "PAIS")


def process_per_uf(file_base_name):
    process_total_per(file_base_name, "NOME_UF", "UF")


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


def read_processed(file_base_name):
    with open(f"data/{file_base_name}_processed.csv", "r", encoding="utf-8") as file:
        data = pd.read_csv(file, sep=";")
    return data


def print_statistics(data: pd.DataFrame):
    value_sum = data["VL_FOB"].sum()
    value_avg = data["VL_FOB"].mean()
    value_mode = data["VL_FOB"].mode()[0]
    value_deviation = data["VL_FOB"].std()
    print(f"Total VL_FOB: {value_sum}")
    print(f"Average VL_FOB: {value_avg}")
    print(f"Mode VL_FOB: {value_mode}")
    print(f"Standard Deviation VL_FOB: {value_deviation}")


def statistics():
    for file_base_name in ["EXP_2025", "IMP_2025"]:
        print(f"Statistics for {file_base_name}_processed.csv:")
        data = read_processed(file_base_name)
        print_statistics(data)


def process():
    process_callbacks = [process_per_country, process_per_uf]
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
        choices=["parse", "statistics", "process"],
        help="The command to execute.",
    )

    args = parser.parse_args()
    if args.command == "parse":
        parse()
    elif args.command == "statistics":
        statistics()
    elif args.command == "process":
        process()
    else:
        parser.print_help()
        sys.exit(1)
