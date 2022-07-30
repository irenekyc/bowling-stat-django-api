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


def getIsFillBallkStrike(x):
    if x["is_fill_ball"] == 0:
        return 0
    elif x["is_fill_ball"] == 1 and x["first_ball"] == 10:
        return 1
    else:
        return 0


def getIsFillBallNotStrike(x):
    if x["is_fill_ball"] == 0:
        return 0
    elif x["is_fill_ball"] == 1 and x["first_ball"] < 10:
        return 1
    else:
        return 0


def getFillBallStrikePercentage(x):
    fill_balls = x["fill_balls"]
    fill_balls_strikes = x["fill_ball_strikes"]
    if math.isnan(fill_balls) or math.isnan(fill_balls_strikes) or fill_balls == 0 or fill_balls_strikes == 0:
        return 0
    else:
        return fill_balls_strikes / fill_balls


def transform_to_table(data_sets, num_of_baker_games):
    _data_sets_arr = []
    for data_set in data_sets:
        if len(data_set) > 0:
            _data_sets_arr.append(data_set)
    _data_sets = pd.concat(_data_sets_arr, axis=0, ignore_index=True)
    _df_combine = pd.DataFrame()
    _df_summary = pd.DataFrame()

    # num_frames = num of first ball attempt
    # num_first_balls = num of first ball attempt
    # first_ball_average = first ball average
    _df_first_ball = _data_sets.groupby(["game_type", "game_group", "bowler"]).agg(first_balls=("first_ball_attempt", "sum"), first_ball_average=("first_ball", "sum")).reset_index()
    _df_first_ball["first_ball_average"] = _df_first_ball.apply(lambda x: x["first_ball_average"] / x["first_balls"], axis=1)

    def calcFrameNo(x):
        return x[x != 0].count()

    # # frame_average
    # _df_frame_average = _data_sets[_data_sets["frame_score"] != '-' ]
    _df_frame_average = _data_sets.groupby(["game_type", "game_group", "bowler"]).agg(frames=("frame_score", calcFrameNo), frame_no=("first_ball_attempt", "sum"), frame_average=("frame_score", "sum")).reset_index()
    _df_frame_average["frame_average"] = _df_frame_average.apply(lambda x: 0 if x["frames"] == 0 else x["frame_average"] / x["frames"], axis=1)

    # # num_strikes = sum of strikes
    # # num_spares = sum of spares
    # # num_opens = sum of opens
    # # num_doubles = sum of doubles - team only
    # # scores = sum of scores
    _df_all = _data_sets.copy()
    _df_all["is_fill_ball_strike"] = _df_all.apply(lambda x: getIsFillBallkStrike(x), axis=1)
    _df_all["is_fill_ball_non_strike"] = _df_all.apply(lambda x: getIsFillBallNotStrike(x), axis=1)
    _df_all["double"] = _df_all["double"].apply(lambda x: 0 if x == "-" else x)
    _df_all["double_attempt"] = _df_all["double_attempt"].apply(lambda x: 0 if x == "-" else x)
    _df_all["frame_score"] = _df_all["frame_score"].apply(lambda x: 0 if x == "-" else x)
    _df_all["accumulated_score"] = _df_all["accumulated_score"].apply(lambda x: 0 if x == "-" else x)
    _df_all = (
        _df_all.groupby(["game_type", "game_group", "bowler"])
        .agg(num_strikes=("strike", "sum"), num_spares=("spare", "sum"), num_opens=("open", "sum"), num_doubles=("double", "sum"), num_double_attempts=("double_attempt", "sum"), score=("frame_score", "sum"), fill_balls=("is_fill_ball", "sum"), fill_ball_strikes=("is_fill_ball_strike", "sum"), fill_ball_non_strikes=("is_fill_ball_non_strike", "sum"))
        .reset_index()
    )

    _df_combine = pd.concat([_df_first_ball, _df_frame_average, _df_all], axis=1, join="outer")
    _df_combine = _df_combine.T.drop_duplicates().T
    _df_combine["fill_ball_non_strikes"] = _df_all["fill_ball_non_strikes"]

    # # spares_per_game - baker game only
    # # opens_per_game - baker game only
    # # strikes_per_game - baker game only
    _df_combine["spares_per_game"] = _df_combine.apply(lambda x: "-" if x["game_type"] == "Team" else x["num_spares"], axis=1)
    _df_combine["opens_per_game"] = _df_combine.apply(lambda x: "-" if x["game_type"] == "Team" else x["num_opens"], axis=1)
    _df_combine["strikes_per_game"] = _df_combine.apply(lambda x: "-" if x["game_type"] == "Team" else x["num_strikes"], axis=1)
    # double percentage - team game only
    _df_combine["double_percentage"] = _df_combine.apply(lambda x: 0 if x["num_doubles"] == 0 else x["num_doubles"] / x["num_double_attempts"], axis=1)
    _df_combine["double_percentage"] = _df_combine.apply(lambda x: "-" if x["game_type"] != "Team" else x["double_percentage"], axis=1)
    # strikes_percentage
    _df_combine["strikes_percentage"] = _df_combine.apply(lambda x: 0 if x["num_strikes"] == 0 else x["num_strikes"] / x["first_balls"], axis=1)

    # fill_ball_striles_percentage
    _df_combine["fill_ball_strikes_percentage"] = _df_combine.apply(lambda x: getFillBallStrikePercentage(x), axis=1)
    _df_summary = calculatesummarydata(_df_combine)

    return (_df_combine, _df_summary)


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
        # if frame 10 and frame 11 are not stikes but they in combine finished a frame
        elif data_row["Frame10Ball1"] + data_row["Frame10Ball2"] == 10:
            return 1
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
