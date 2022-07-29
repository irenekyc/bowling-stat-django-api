# analysisBowlingData(team_name=team_name, filePath=women_files_dir + "QU Women 2021-2022 (7).csv", event_name="Big Red Invite", location="Hollywood Bowl", year="2021 - 2022", num_of_baker_games=5, baker_match_play_distributions=[7, 5])
import pandas as pd
from .names import *
import numpy as np
from .analyize_data_utlis import *
from .serializers import EventSummaryDataSerializer


def getEventDate(df):
    _df = df.copy()
    _df["Date - Pandas"] = pd.to_datetime(_df["Date"])
    _df["Date - Date"] = _df["Date - Pandas"].dt.date
    date = _df["Date - Date"].dropna().unique()

    start_date = min(date)
    end_date = max(date)

    return (start_date, end_date)


def transform_to_frames(_data, _game_type, num_baker_games, num_of_baker_games_per_block, baker_match_play_1, baker_match_play_2, baker_match_play_3):
    data_entries = []
    _df = _data.copy()
    baker_match_distributions = [baker_match_play_1, baker_match_play_2, baker_match_play_3]

    for row_no in range(len(_df)):
        game_no = row_no + 1
        current_row_data = _df.iloc[row_no]
        for i in range(12):
            frame_no = i + 1
            data_entry = [
                _game_type,
                getGameGroup(num_of_baker_games_per_block, game_no, _game_type, num_baker_games, baker_match_distributions),
                game_no,
                frame_no,
                getCurrentFrameBowler(frame_no, current_row_data),
                getCurrentFrameFirstBall(frame_no, current_row_data),
                getCurrentFrameSecondBall(frame_no, current_row_data),
                getPinLeave(frame_no, current_row_data),
                getPin2Leave(frame_no, current_row_data),
                getFirstBallAttempt(frame_no, current_row_data),
                getIsSpare(frame_no, current_row_data),
                getIsStrike(frame_no, current_row_data),
                getIsDouble(_game_type, frame_no, current_row_data),
                getIsDoubleAttempt(_game_type, frame_no, current_row_data),
                getIsOpen(frame_no, current_row_data),
                getAccumulatedScore(frame_no, current_row_data),
                getCurrentFrameScore(frame_no, current_row_data),
                getIsFillBall(frame_no, current_row_data),
            ]
            data_entries.append(data_entry)
    return pd.DataFrame(data_entries, columns=["game_type", "game_group", "game_no", "frame_no", "bowler", "first_ball", "second_ball", "pin_leave", "pin_2_leave", "first_ball_attempt", "spare", "strike", "double", "double_attempt", "open", "accumulated_score", "frame_score", "is_fill_ball"])


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
    team_data = transform_to_frames(_data=_df_team, _game_type="Team", num_baker_games=num_of_baker_games, num_of_baker_games_per_block=num_of_baker_games_per_block, baker_match_play_1=baker_match_play_1, baker_match_play_2=baker_match_play_2, baker_match_play_3=baker_match_play_3)
    baker_data = transform_to_frames(_data=_df_baker, _game_type="Baker", num_baker_games=num_of_baker_games, num_of_baker_games_per_block=num_of_baker_games_per_block, baker_match_play_1=baker_match_play_1, baker_match_play_2=baker_match_play_2, baker_match_play_3=baker_match_play_3)
    baker_match_data = transform_to_frames(_data=_df_baker_match, _game_type="Baker Match Play", num_baker_games=num_of_baker_games, num_of_baker_games_per_block=num_of_baker_games_per_block, baker_match_play_1=baker_match_play_1, baker_match_play_2=baker_match_play_2, baker_match_play_3=baker_match_play_3)

    (analysized_data, summary_data) = transform_to_table([baker_data, team_data, baker_match_data], num_of_baker_games)

    analysized_data = addMetaData(analysized_data, team_name, team_id, event_name, season, event_id, location, start_date, end_date)
    summary_data = addMetaData(summary_data, team_name, team_id, event_name, season, event_id, location, start_date, end_date)
    return (analysized_data.to_dict(orient="records"), summary_data.to_dict(orient="records"), team_id, event_id)
