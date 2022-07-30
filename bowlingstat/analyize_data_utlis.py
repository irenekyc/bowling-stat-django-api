import math
import numpy as np
import pandas as pd

transformed_excel_columns = ["game_type", "game_group", "game_no", "frame_no", "bowler", "first_ball", "second_ball", "pin_leave", "pin_leave_2", "first_ball_attempt", "spares", "strikes", "double", "double_attempt", "opens", "accumulated_score", "frame_score"]

output_excel_columns = ["game_type", "game_group", "game_no", "frame_no", "bowler", "num_frames", "first_ball", "first_ball_attempt", "first_ball_average", "spares", "spares_per_game", "strikes", "strikes_percentage", "strikes_per_game", "double", "double_attempt", "double_percentage", "opens", "opens_per_game", "frame_average"]

event_summary_excel_columns = [
    "bowler",
    "baker_num_frames",
    "baker_frame_ave",
    "baker_num_strikes",
    "baker_num_strikes_attempt",
    "baker_strikes_percentage",
    "baker_first_ball_ave",
    "team_num_frames",
    "team_frame_ave",
    "team_num_strikes",
    "team_num_strikes_attempt",
    "team_strikes_percentage",
    "team_first_ball_ave",
    "team_doubles",
    "team_doubles_attempt",
    "team_double_percentage",
    "baker_mp_num_frames",
    "baker_mp_frame_ave",
    "baker_mp_num_strikes",
    "baker_mp_num_strikes_attempt",
    "baker_mp_strikes_percentage",
    "baker_mp_first_ball_ave",
    "all_num_frames",
    "all_frame_ave",
    "all_num_strikes",
    "all_num_strikes_attempt",
    "all_strikes_percentage",
    "all_first_ball_ave",
]


def calculatesummarydata(df):
    _df = df.copy()
    _df_all = _df
    _df_baker = _df[_df["game_type"] == "Baker"]
    _df_team = _df[_df["game_type"] == "Team"]
    _df_baker_mp = _df[_df["game_type"] == "Baker Match Play"]

    _df_baker = (
        _df_baker.groupby(["bowler"])
        .agg(
            baker_num_frames=("first_balls", "sum"),
            baker_frame_ave=("frame_average", "mean"),
            baker_num_strikes=("num_strikes", "sum"),
            baker_num_strikes_attempt=("first_balls", "sum"),
            baker_strikes_percentage=("strikes_percentage", "mean"),
            baker_first_ball_average=("first_ball_average", "mean"),
            baker_fill_balls=("fill_balls", "sum"),
            baker_fill_ball_strikes=("fill_ball_strikes", "sum"),
            baker_fill_ball_non_strikes=("fill_ball_non_strikes", "sum"),
            baker_fill_ball_strikes_percentage=("fill_ball_strikes_percentage", "mean"),
        )
        .reset_index()
        .set_index("bowler")
    )
    _df_team = (
        _df_team.groupby(["bowler"])
        .agg(
            team_num_frames=("first_balls", "sum"),
            team_frame_ave=("frame_average", "mean"),
            team_num_strikes=("num_strikes", "sum"),
            team_num_strikes_attempt=("first_balls", "sum"),
            team_strikes_percentage=("strikes_percentage", "mean"),
            team_first_ball_average=("first_ball_average", "mean"),
            team_doubles=("num_doubles", "sum"),
            team_doubles_attempt=("num_double_attempts", "sum"),
            team_double_percentage=("double_percentage", "mean"),
            team_fill_balls=("fill_balls", "sum"),
            team_fill_ball_strikes=("fill_ball_strikes", "sum"),
            team_fill_ball_non_strikes=("fill_ball_non_strikes", "sum"),
            team_fill_ball_strikes_percentage=("fill_ball_strikes_percentage", "mean"),
        )
        .reset_index()
        .set_index("bowler")
    )
    _df_baker_mp = (
        _df_baker_mp.groupby(["bowler"])
        .agg(
            baker_mp_num_frames=("first_balls", "sum"),
            baker_mp_frame_ave=("frame_average", "mean"),
            baker_mp_num_strikes=("num_strikes", "sum"),
            baker_mp_num_strikes_attempt=("first_balls", "sum"),
            baker_mp_strikes_percentage=("strikes_percentage", "mean"),
            baker_mp_first_ball_average=("first_ball_average", "mean"),
            baker_mp_fill_balls=("fill_balls", "sum"),
            baker_mp_fill_ball_strikes=("fill_ball_strikes", "sum"),
            baker_mp_fill_ball_non_strikes=("fill_ball_non_strikes", "sum"),
            baker_mp_fill_ball_strikes_percentage=("fill_ball_strikes_percentage", "mean"),
        )
        .reset_index()
        .set_index("bowler")
    )
    _df_all = _df_all.groupby(["bowler"]).agg(all_num_frames=("first_balls", "sum"), all_frame_ave=("frame_average", "mean"), all_num_strikes=("num_strikes", "sum"), all_num_strikes_attempt=("first_balls", "sum"), all_strikes_percentage=("strikes_percentage", "mean"), all_first_ball_average=("first_ball_average", "mean")).reset_index().set_index("bowler")

    _df_combine = pd.concat([_df_baker, _df_team, _df_baker_mp, _df_all], axis=1).reset_index()

    return _df_combine


# TODO: need to write test
def getIsFillBallkStrike(x):
    if x["is_fill_ball"] == 0:
        return 0
    elif x["is_fill_ball"] == 1 and x["first_ball"] == 10:
        return 1
    else:
        return 0


# TODO: need to write test
def getIsFillBallNotStrike(x):
    if x["is_fill_ball"] == 0:
        return 0
    elif x["is_fill_ball"] == 1 and x["first_ball"] < 10:
        return 1
    else:
        return 0


# TODO: need to write test
def getFillBallStrikePercentage(x):
    fill_balls = x["fill_balls"]
    fill_balls_strikes = x["fill_ball_strikes"]
    if math.isnan(fill_balls) or math.isnan(fill_balls_strikes) or fill_balls == 0 or fill_balls_strikes == 0:
        return 0
    else:
        return fill_balls_strikes / fill_balls


def getIsStrike(frame_no, data_row):
    first_ball = 0
    if frame_no <= 10:
        first_ball = data_row["Frame" + str(frame_no) + "Ball1"]
    elif frame_no == 11:
        if data_row["Frame10Ball1"] == 10:
            first_ball = data_row["Frame10Ball2"]
        else:
            first_ball = data_row["Frame10Ball3"]
    elif frame_no == 12:
        if data_row["Frame10Ball2"] == 10:
            first_ball = data_row["Frame10Ball3"]
    if first_ball == 10:
        return 1
    else:
        return 0


def getGameGroup(num_baker_games_per_block, row_no, game_type, num_baker_games, baker_match_distributions):
    if game_type == "Team":
        return math.floor((row_no + 4) / 5)
    elif game_type == "Baker":
        return math.floor((row_no + num_baker_games_per_block - 1) / num_baker_games_per_block)
    elif game_type == "Baker Match Play":
        match_group = math.nan
        if row_no <= baker_match_distributions[0]:
            match_group = 1
        elif row_no <= np.sum(baker_match_distributions[0:2]):
            match_group = 2
        elif row_no <= np.sum(baker_match_distributions[0:3]):
            match_group = 3
        elif row_no <= np.sum(baker_match_distributions[0:4]):
            match_group = 4
        return match_group


def getCurrentFrameBowler(frame_no, data_row):
    if frame_no <= 10:
        return data_row["Frame" + str(frame_no) + "Ball1Bowler"].strip()
    elif frame_no == 11:
        return data_row["Frame10Ball2Bowler"].strip()
    elif frame_no == 12:
        return data_row["Frame10Ball3Bowler"].strip()
    else:
        return ""


def getCurrentFrameFirstBall(frame_no, data_row):
    if frame_no <= 10:
        return data_row["Frame" + str(frame_no) + "Ball1"]
    elif frame_no == 11:
        if data_row["Frame10Ball1"] == 10:
            return data_row["Frame10Ball2"]
        elif data_row["Frame10Ball1"] + data_row["Frame10Ball2"] == 10:
            return data_row["Frame10Ball3"]
        else:
            return 0
    elif frame_no == 12:
        if data_row["Frame10Ball1"] == 10 and data_row["Frame10Ball2"] == 10:
            return data_row["Frame10Ball3"]
        else:
            return 0
    else:
        return 0


def getCurrentFrameSecondBall(frame_no, data_row):
    if frame_no < 10:
        return data_row["Frame" + str(frame_no) + "Ball2"]
    elif frame_no == 10:
        if data_row["Frame10Ball1"] == 10:
            return 0
        else:
            return data_row["Frame10Ball2"]
    elif frame_no == 11:
        if data_row["Frame10Ball1"] == 10 and data_row["Frame10Ball2"] == 10:
            return 0
        elif data_row["Frame10Ball1"] == 10 and data_row["Frame10Ball2"] < 10:
            return data_row["Frame10Ball3"]
        else:
            return 0
    else:
        return 0


def getFirstBallAttempt(frame_no, data_row):
    if frame_no <= 10:
        return 1
    elif frame_no == 11:
        if data_row["Frame10Ball1"] == 10:
            return 1
        elif data_row["Frame10Ball1"] < 10 and data_row["Frame10Ball1"] + data_row["Frame10Ball2"] == 10:
            return 1
        else:
            return 0
    elif frame_no == 12:
        # if frame 11 is a strike
        if data_row["Frame10Ball2"] == 10:
            return 1
        # if frame 10 is a strike
        elif data_row["Frame10Ball1"] == 10:
            # if frame 11 is also finished:
            if data_row["Frame10Ball2"] == 10:
                return 1
            else:
                return 0
        else:
            return 0


def getIsSpare(frame_no, data_row):
    if frame_no <= 10:
        first_ball = data_row["Frame" + str(frame_no) + "Ball1"]
        second_ball = data_row["Frame" + str(frame_no) + "Ball2"]
        if second_ball == math.isnan:
            second_ball = 0
        if first_ball < 10 and first_ball + second_ball == 10:
            return 1
        else:
            return 0
    elif frame_no == 11:
        # if frame 10 is a strike: frame 11 first ball will be Frame10Ball2 and second ball will be Frame10Ball3
        if data_row["Frame10Ball1"] == 10:
            first_ball = data_row["Frame10Ball2"]
            second_ball = data_row["Frame10Ball3"]
            if second_ball == math.isnan:
                second_ball = 0
            if first_ball < 10 and first_ball + second_ball == 10:
                return 1
            else:
                return 0
        # if frame 10 is not a strike, frame 11 first ball will be Frame10Ball3
        else:
            return 0
    else:
        return 0


def getIsOpen(frame_no, data_row):
    first_ball = 0
    second_ball = 0
    if frame_no <= 10:
        first_ball = data_row["Frame" + str(frame_no) + "Ball1"]
        if math.isnan(data_row["Frame" + str(frame_no) + "Ball2"]):
            second_ball = 0
        else:
            second_ball = data_row["Frame" + str(frame_no) + "Ball2"]
        if first_ball + second_ball < 10:
            return 1
        else:
            return 0
    elif frame_no == 11:
        frame_10_ball = data_row["Frame10Ball1"]
        frame_11_ball = data_row["Frame10Ball2"]
        frame_12_ball = data_row["Frame10Ball3"]
        if frame_12_ball is math.isnan:
            frame_12_ball = 0

        if frame_10_ball == 10 and frame_11_ball + frame_12_ball < 10:
            return 1
        else:
            return 0
    elif frame_no == 12:
        return 0


# TODO: need to write test
def getCurrentFrameScore(frame_no, data_row):
    current_frame_score = 0
    previous_frame_score = 0
    if frame_no <= 10:
        current_frame_score = data_row["Frame" + str(frame_no) + "Score"]
        if frame_no != 1:
            previous_frame_score = data_row["Frame" + str(frame_no - 1) + "Score"]
        return current_frame_score - previous_frame_score
    else:
        return 0


# TODO: need to write test
def getAccumulatedScore(frame_no, data_row):
    if frame_no <= 10:
        return data_row["Frame" + str(frame_no) + "Score"]
    else:
        return 0


def getIsDouble(game_type, frame_no, data_row):
    if game_type != "Team":
        return "-"
    else:
        if frame_no == 1:
            return 0
        elif frame_no <= 10:
            previous_ball1 = data_row["Frame" + str(frame_no - 1) + "Ball1"]
            current_ball1 = data_row["Frame" + str(frame_no) + "Ball1"]
            if previous_ball1 == 10 and current_ball1 == 10:
                return 1
            else:
                return 0
        elif frame_no == 11:
            previous_ball1 = data_row["Frame10Ball1"]
            current_ball1 = data_row["Frame10Ball2"]
            if previous_ball1 == 10 and current_ball1 == 10:
                return 1
            else:
                return 0
        elif frame_no == 12:
            previous_ball1 = data_row["Frame10Ball2"]
            current_ball1 = data_row["Frame10Ball3"]
            if previous_ball1 == 10 and current_ball1 == 10:
                return 1
            else:
                return 0
        else:
            return 0


def getIsDoubleAttempt(game_type, frame_no, data_row):
    if game_type != "Team":
        return "-"
    else:
        if frame_no == 1:
            return 0
        elif frame_no <= 10:
            previous_ball1 = data_row["Frame" + str(frame_no - 1) + "Ball1"]
            if previous_ball1 == 10:
                return 1
            else:
                return 0
        elif frame_no == 11:
            previous_ball1 = data_row["Frame10Ball1"]
            if previous_ball1 == 10:
                return 1
            else:
                return 0
        elif frame_no == 12:
            previous_ball1 = data_row["Frame10Ball2"]

            if previous_ball1 == 10:
                return 1
            else:
                return 0
        else:
            return 0


def getPinLeave(frame_no, data_row):
    frame_10_ball1 = data_row["Frame10Ball1"]
    frame_10_ball2 = data_row["Frame10Ball2"]
    if frame_no <= 10:
        pin = data_row["Frame" + str(frame_no) + "Ball1Pins"]
        if pin == "":
            return "-"
        else:
            return pin
    elif frame_no == 11:
        if frame_10_ball1 == 10:
            pin = data_row["Frame10Ball3Pins"]
            if pin == "":
                return "-"
            else:
                return pin
        elif frame_10_ball1 + frame_10_ball2 == 10:
            pin = data_row["Frame10Ball2Pins"]
        else:
            return "-"
    elif frame_no == 12:
        if frame_10_ball1 == 10 and frame_10_ball2 == 10:
            pin = data_row["Frame10Ball3Pins"]
            if pin == "":
                return "-"
            else:
                return pin
        else:
            return "-"
    else:
        return "-"


def getPin2Leave(frame_no, data_row):
    if frame_no <= 10:
        pin = data_row["Frame" + str(frame_no) + "Ball2Pins"]
        if pin == "":
            return "-"
        else:
            return pin
    else:
        return "-"


def getIsFillBall(frame_no, data_row):
    frame_10_ball1 = data_row["Frame10Ball1"]
    frame_10_ball2 = data_row["Frame10Ball2"]
    frame_10_ball3 = data_row["Frame10Ball3"]

    if frame_no <= 10:
        return 0
    elif frame_no == 11:
        if frame_10_ball1 < 10 and frame_10_ball1 + frame_10_ball2 == 10:
            return 1
        else:
            return 0
    elif frame_no == 12:
        if frame_10_ball1 == 10 and frame_10_ball2 == 10:
            return 1
        else:
            return 0


def addMetaData(df, team_name, team_id, event_name, season, event_id, location, start_date, end_date):
    original_columns = df.columns
    _df = df.copy()
    _df["team_name"] = team_name
    _df["event_name"] = event_name
    _df["event_season"] = season
    _df["event_id"] = event_id
    _df["event_location"] = location
    _df["start_date"] = start_date
    _df["end_date"] = end_date
    _df["team_id"] = team_id
    new_columns = np.concatenate((["event_id", "team_name", "team_id", "event_name", "event_season", "event_location", "start_date", "end_date"], original_columns), axis=None)
    _df = _df.reindex(columns=new_columns)
    return _df


def getEventDate(df):
    _df = df.copy()
    _df["Date - Pandas"] = pd.to_datetime(_df["Date"])
    _df["Date - Date"] = _df["Date - Pandas"].dt.date
    date = _df["Date - Date"].dropna().unique()

    start_date = min(date)
    end_date = max(date)

    return (start_date, end_date)
