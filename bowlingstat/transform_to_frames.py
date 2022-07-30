from .analyize_data_utlis import *
import pandas as pd


def transform_to_frames(_data, _game_type, num_baker_games, num_of_baker_games_per_block, baker_match_play_1, baker_match_play_2, baker_match_play_3, **args):
    data_entries = []
    _df = _data.copy()
    baker_match_distributions = [baker_match_play_1, baker_match_play_2, baker_match_play_3]
    event_type = args["event_type"]
    pass_game_group = args["game_group"]

    for row_no in range(len(_df)):
        game_no = row_no + 1
        game_group = getGameGroup(num_of_baker_games_per_block, game_no, _game_type, num_baker_games, baker_match_distributions)
        if event_type == "CHAMPIONSHIP":
            game_group = pass_game_group

        current_row_data = _df.iloc[row_no]

        for i in range(12):
            frame_no = i + 1
            data_entry = [
                _game_type,
                game_group,
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
