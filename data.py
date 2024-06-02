import json
from match_data import MatchData


def save(data: MatchData) -> None:
    with open('./assets/match_data.json', 'w',encoding='utf-8') as data_file:
        json.dump(data, data_file)


def load() -> MatchData:
    with open('./assets/match_data.json', 'r',encoding='utf-8') as data_file:
        match_data = json.load(data_file)
    return match_data
