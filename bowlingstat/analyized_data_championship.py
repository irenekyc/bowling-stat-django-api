import pandas as pd
from .analyize_data_utlis import *
from .analyize_data import transform_to_frames
from .transform_to_table import transform_to_table


def getGameType(x, num_bakers, num_bakers_mp):
    entries_index = x.name + 1
    if entries_index <= num_bakers:
        return "Baker"
    else:
        return "Baker Match Play"


def analysisBowlingDataChampionships(**meta_data):
    file = meta_data["file"][0]
    df = pd.read_csv(file, index_col=False)
    df = df.drop(columns="Event")
    df = df.drop(columns="EventType")
    (start_date, end_date) = getEventDate(df)

    num_championship_matches = meta_data["num_of_championship_matches"][0]
    _game_start_entry = 1
    _team_data_arr = []
    _baker_data_arr = []
    _baker_mp_data_arr = []

    for index in range(int(num_championship_matches)):
        game_no = index + 1
        team_entries = int(meta_data["champ_" + str(game_no) + "_team_games"][0]) * 5
        baker_entries = int(meta_data["champ_" + str(game_no) + "_baker_games"][0]) * 5
        # baker_mp_entries = int(meta_data["champ_" + str(game_no) + "_baker_mp_games"][0])
        baker_mp_entries = 0
        total_entries = baker_entries + team_entries + baker_mp_entries

        _df = df.copy()
        _df = _df.iloc[_game_start_entry : total_entries + _game_start_entry]
        _game_start_entry = _game_start_entry + total_entries
        _df["championship_match_no"] = game_no
        _df["event_type"] = "CHAMPIONSHIP"
        _df_team = _df[_df["GameType"] == "Team"].reset_index()
        _df_baker = _df[_df["GameType"] == "Baker"].reset_index()
        _df = pd.concat([_df_team, _df_baker], axis=0)
        # _df_set_arr.append(_df)

        # transform to frames
        team_data = transform_to_frames(_data=_df_team, _game_type="Team", num_baker_games=baker_entries, num_of_baker_games_per_block=5, baker_match_play_1=0, baker_match_play_2=0, baker_match_play_3=0, event_type="CHAMPIONSHIP", game_group=game_no)
        _team_data_arr.append(team_data)
        baker_data = transform_to_frames(_data=_df_baker, _game_type="Baker", num_baker_games=baker_entries, num_of_baker_games_per_block=5, baker_match_play_1=0, baker_match_play_2=0, baker_match_play_3=0, event_type="CHAMPIONSHIP", game_group=game_no)
        _baker_data_arr.append(baker_data)

        # baker_match_data = transform_to_frames(_data=_df_baker_match, _game_type="Baker Match Play", num_baker_games=num_of_baker_games, num_of_baker_games_per_block=num_of_baker_games_per_block, baker_match_play_1=baker_match_play_1, baker_match_play_2=baker_match_play_2, baker_match_play_3=baker_match_play_3)

    _df_team = pd.concat(_team_data_arr, axis=0, ignore_index=True)
    _df_baker = pd.concat(_baker_data_arr, axis=0, ignore_index=True)

    (analysized_data, summary_data) = transform_to_table([_df_baker, _df_team])
    event_name = meta_data["event_name"][0]
    season = meta_data["season"][0]
    event_id = event_name.replace(" ", "-").lower() + "--" + season.replace(" ", "")
    team_name = meta_data["team_name"][0]
    team_id = "-".join(team_name.split(" ")).lower()
    location = meta_data["location"][0]

    analysized_data = addMetaData(analysized_data, team_name, team_id, event_name, season, event_id, location, start_date, end_date)
    summary_data = addMetaData(summary_data, team_name, team_id, event_name, season, event_id, location, start_date, end_date)

    return (analysized_data.to_dict(orient="records"), summary_data.to_dict(orient="records"), team_id, event_id)
