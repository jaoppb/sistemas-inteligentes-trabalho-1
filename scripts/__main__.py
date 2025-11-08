import io

import encode
import countries
import states
import pandas as pd


def remove_columns(data: pd.DataFrame, columns: list[str]):
    for column in columns:
        if column in data.columns:
            del data[column]


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


def main():
    for file_base_name in ["EXP_2025", "IMP_2025"]:
        parse_data(file_base_name)


if __name__ == "__main__":
    main()
