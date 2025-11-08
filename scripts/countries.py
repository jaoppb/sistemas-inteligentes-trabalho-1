import pandas as pd

country_data = pd.read_excel("data/paises.xlsx", header=6)

by_code = {
    each["SISCOMEX"]: each["NO_PAIS_POR"] for each in country_data.to_dict("records")
}


def parse_code(code):
    return by_code.get(code, "UNKNOWN")


def parse_country_columns(data: pd.DataFrame, from_name="CO_PAIS", to_name="NOME_PAIS"):
    data[to_name] = data[from_name].apply(parse_code)
