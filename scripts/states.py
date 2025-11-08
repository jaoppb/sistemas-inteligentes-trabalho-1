import pandas as pd

states_data = pd.read_csv("data/estados.csv", delimiter=";")

states = {each["SIGLA_UF"]: each["NOME_UF"] for each in states_data.to_dict("records")}


def parse_state(code):
    return states.get(code, "UNKNOWN")


def parse_state_columns(data: pd.DataFrame, from_name="SIGLA_UF", to_name="NOME_UF"):
    data[to_name] = data[from_name].apply(parse_state)
