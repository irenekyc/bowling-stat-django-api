import pandas as pd
from .analyize_data_utlis import *


def transform_to_table(data_sets):
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

    # _df_combine = pd.concat([_df_first_ball, _df_frame_average.drop(["game_type", "game_group", ], axis = 1, inplace = True), _df_all], axis=1, join="inner")
    _df_combine = _df_first_ball.copy()
    _df_combine["frame_average"] = _df_frame_average["frame_average"]
    _df_combine["num_strikes"] = _df_all["num_strikes"]
    _df_combine["num_spares"] = _df_all["num_spares"]
    _df_combine["num_opens"] = _df_all["num_opens"]
    _df_combine["num_doubles"] = _df_all["num_doubles"]
    _df_combine["num_double_attempts"] = _df_all["num_double_attempts"]
    _df_combine["score"] = _df_all["score"]
    _df_combine["fill_balls"] = _df_all["fill_balls"]
    _df_combine["fill_ball_strikes"] = _df_all["fill_ball_strikes"]
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
