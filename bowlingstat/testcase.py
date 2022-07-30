import pandas as pd
import math
import numpy

# TEST CASES for fill ball
is_fill_ball_data_row = pd.DataFrame([[10, 10, 10]], columns=["Frame10Ball1", "Frame10Ball2", "Frame10Ball3"]).iloc[0]
is_fill_ball_data_row2 = pd.DataFrame([[9, 1, 6]], columns=["Frame10Ball1", "Frame10Ball2", "Frame10Ball3"]).iloc[0]
is_not_fill_ball_data_row = pd.DataFrame([[10, 6, 2]], columns=["Frame10Ball1", "Frame10Ball2", "Frame10Ball3"]).iloc[0]


# TEST CASES for Pins ball
frame1ball1pin = "1-2"
frame1ball2pin = ""
frame2ball1pin = "3-4"
frame2ball2pin = "3"
frame3ball1pin = ""
frame3ball2pin = ""
frame10ball1pin = "5-6-7-8"
frame10ball2pin = ""
frame10ball3pin = "7-8"
frame10ball1 = 6
frame10ball2 = 4
frame10ball3 = 8

pin_ball_row = pd.DataFrame(
    [[frame1ball1pin, frame1ball2pin, frame2ball1pin, frame2ball2pin, frame3ball1pin, frame3ball2pin, frame10ball1, frame10ball2, frame10ball1pin, frame10ball2pin, frame10ball3pin]],
    columns=[
        "Frame1Ball1Pins",
        "Frame1Ball2Pins",
        "Frame2Ball1Pins",
        "Frame2Ball2Pins",
        "Frame3Ball1Pins",
        "Frame3Ball2Pins",
        "Frame10Ball1",
        "Frame10Ball2",
        "Frame10Ball1Pins",
        "Frame10Ball2Pins",
        "Frame10Ball3Pins",
    ],
).iloc[0]

### TEST CASES for frames and strikes ###
frame_data_row = pd.DataFrame(
    [[10, math.nan, 6, 4, 10, math.nan, 9, math.nan, 10, math.nan, 10, 10, 6]],
    columns=[
        "Frame1Ball1",
        "Frame1Ball2",
        "Frame2Ball1",
        "Frame2Ball2",
        "Frame3Ball1",
        "Frame3Ball2",
        "Frame4Ball1",
        "Frame4Ball2",
        "Frame5Ball1",
        "Frame5Ball2",
        "Frame10Ball1",
        "Frame10Ball2",
        "Frame10Ball3",
    ],
).iloc[0]

frame_data_row_case_2 = pd.DataFrame(
    [[10, math.nan, 10, math.nan, 10, math.nan, 9, "", 10, "", 6, 4, 10]],
    columns=[
        "Frame1Ball1",
        "Frame1Ball2",
        "Frame2Ball1",
        "Frame2Ball2",
        "Frame3Ball1",
        "Frame3Ball2",
        "Frame4Ball1",
        "Frame4Ball2",
        "Frame5Ball1",
        "Frame5Ball2",
        "Frame10Ball1",
        "Frame10Ball2",
        "Frame10Ball3",
    ],
).iloc[0]

frame_data_row_case_3 = pd.DataFrame(
    [[10, "", 6, 4, 10, "", 9, "", 10, "", 6, 3, math.nan]],
    columns=[
        "Frame1Ball1",
        "Frame1Ball2",
        "Frame2Ball1",
        "Frame2Ball2",
        "Frame3Ball1",
        "Frame3Ball2",
        "Frame4Ball1",
        "Frame4Ball2",
        "Frame5Ball1",
        "Frame5Ball2",
        "Frame10Ball1",
        "Frame10Ball2",
        "Frame10Ball3",
    ],
).iloc[0]


frame_bowler_row = pd.DataFrame(
    [["A", "B", "C", "D", "E", "D", "A", "A"]],
    columns=[
        "Frame1Ball1Bowler",
        "Frame2Ball1Bowler",
        "Frame3Ball1Bowler",
        "Frame4Ball1Bowler",
        "Frame5Ball1Bowler",
        "Frame10Ball1Bowler",
        "Frame10Ball2Bowler",
        "Frame10Ball3Bowler",
    ],
).iloc[0]

test_data = pd.read_csv("bowlingstat/Test Data.csv")
test_data_baker = test_data[test_data["GameType"] == "Baker"].iloc[0:5]

## TEST CASE Baker One ##
bakerGameOneBowler = ["Test BowlerA", "Test BowlerB", "Test BowlerC", "Test BowlerD", "Test BowlerE", "Test BowlerA", "Test BowlerB", "Test BowlerC", "Test BowlerD", "Test BowlerE", "Test BowlerE", "Test BowlerE"]
bakerGameOneFirstBall = [9, 10, 9, 10, 9, 10, 9, 10, 0, 10, 10, 10]
bakerGameOneSecondBall = [1, 0, 1, 0, 1, 0, 1, 0, 10, 0, 0, 0]
bakerGameOneFirstBallAttempt = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
bakerGameOneIsSpare = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0]
bakerGameOneIsStrike = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1]
bakerGameOneIsOpen = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
bakerGameOneIsFill = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
## TEST CASE Baker Five ##
bakerGameFiveBowler = ["Test BowlerA", "Test BowlerB", "Test BowlerC", "Test BowlerD", "Test BowlerE", "Test BowlerA", "Test BowlerB", "Test BowlerC", "Test BowlerD", "Test BowlerE", "Test BowlerE", "Test BowlerE"]
bakerGameFiveFirstBall = [10, 10, 10, 10, 10, 10, 10, 10, 10, 9, 10, 0]
bakerGameFiveSecondBall = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
bakerGameFiveFirstBallAttempt = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
bakerGameFiveIsSpare = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
bakerGameFiveIsStrike = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0]
bakerGameFiveIsOpen = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
bakerGameFiveIsFill = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
