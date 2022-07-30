# analysisBowlingData(team_name=team_name, filePath=women_files_dir + "QU Women 2021-2022 (7).csv", event_name="Big Red Invite", location="Hollywood Bowl", year="2021 - 2022", num_of_baker_games=5, baker_match_play_distributions=[7, 5])
import pandas as pd
from .names import *
import numpy as np
from .analyize_data_utlis import *
from .transform_to_frames import transform_to_frames
from .serializers import EventSummaryDataSerializer


def analyize_data(file, team_name, event_name, location, season, num_of_baker_games, num_of_baker_games_per_block, baker_match_play_1, baker_match_play_2, baker_match_play_3, **args):
    df = pd.read_csv(file[0], index_col=False)
    df = df.drop(columns="Event")
    df = df.drop(columns="EventType")

    event_name = event_name[0]
    event_id = event_name.replace(" ", "-").lower() + "--" + season[0].replace(" ", "")
    (start_date, end_date) = getEventDate(df)
    season = season[0]
    location = location[0]

    num_of_baker_games = int(num_of_baker_games[0])
    num_of_baker_games_per_block = int(num_of_baker_games_per_block[0])
    baker_match_play_1 = int(baker_match_play_1[0])
    baker_match_play_2 = int(baker_match_play_2[0])
    baker_match_play_3 = int(baker_match_play_3[0])
    team_name = team_name[0]
    team_id = "-".join(team_name.split(" ")).lower()

    # 1. Divided into Baker, Baker Match and Baker
    _df_team = df[df["GameType"] == "Team"]
    _df_baker = df[df["GameType"] == "Baker"].iloc[0 : num_of_baker_games_per_block * num_of_baker_games]
    _df_baker_match = pd.DataFrame()
    _df_baker_match = df[df["GameType"] == "Baker"].iloc[num_of_baker_games_per_block * num_of_baker_games :]
    _df_baker_match["GameType"] = "Baker Match Play"

    # 2. transform to frames
    team_data = transform_to_frames(_data=_df_team, _game_type="Team", num_baker_games=num_of_baker_games, num_of_baker_games_per_block=num_of_baker_games_per_block, baker_match_play_1=baker_match_play_1, baker_match_play_2=baker_match_play_2, baker_match_play_3=baker_match_play_3, event_type="NORMAL_GAME", game_group=None)
    baker_data = transform_to_frames(_data=_df_baker, _game_type="Baker", num_baker_games=num_of_baker_games, num_of_baker_games_per_block=num_of_baker_games_per_block, baker_match_play_1=baker_match_play_1, baker_match_play_2=baker_match_play_2, baker_match_play_3=baker_match_play_3, event_type="NORMAL_GAME", game_group=None)
    baker_match_data = transform_to_frames(_data=_df_baker_match, _game_type="Baker Match Play", num_baker_games=num_of_baker_games, num_of_baker_games_per_block=num_of_baker_games_per_block, baker_match_play_1=baker_match_play_1, baker_match_play_2=baker_match_play_2, baker_match_play_3=baker_match_play_3, event_type="NORMAL_GAME", game_group=None)

    (analysized_data, summary_data) = transform_to_table([baker_data, team_data, baker_match_data], num_of_baker_games)

    analysized_data = addMetaData(analysized_data, team_name, team_id, event_name, season, event_id, location, start_date, end_date)
    summary_data = addMetaData(summary_data, team_name, team_id, event_name, season, event_id, location, start_date, end_date)
    return (analysized_data.to_dict(orient="records"), summary_data.to_dict(orient="records"), team_id, event_id)
