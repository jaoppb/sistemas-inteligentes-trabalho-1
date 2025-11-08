import pandas as pd
import unicodedata

states_data = pd.read_csv("data/estados.csv", delimiter=";")


def remove_accents(text):
    if not isinstance(text, str):
        return text
    nfd = unicodedata.normalize("NFD", text)
    return "".join([char for char in nfd if unicodedata.category(char) != "Mn"]).upper()


states = {
    each["SIGLA_UF"]: remove_accents(each["NOME_UF"])
    for each in states_data.to_dict("records")
}


def parse_state(code):
    return states.get(code, "UNKNOWN")


def parse_state_columns(data: pd.DataFrame, from_name="SIGLA_UF", to_name="NOME_UF"):
    data[to_name] = data[from_name].apply(parse_state)
