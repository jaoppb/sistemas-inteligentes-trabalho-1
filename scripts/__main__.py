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
