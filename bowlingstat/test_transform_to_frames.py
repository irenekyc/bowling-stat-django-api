from django.test import TestCase
from .transform_to_frames import transform_to_frames
from .testcase import *


class TestTransformToFrames(TestCase):
    def test_transform_to_frames_baker(self):
        """This is the function transform a csv row to 12 frames data
        frames data should be correctly identified"""
        ###### REGULAR GAME #######
        ### Baker ###
        result_frames = transform_to_frames(_data=test_data_baker, _game_type="Baker", num_baker_games=1, num_of_baker_games_per_block=5, baker_match_play_1=7, baker_match_play_2=0, baker_match_play_3=0, game_group=0, event_type="Regular")
        # General #
        self.assertEqual(len(result_frames), 60)
        # Baker game one data #
        bakerGameOne = result_frames.iloc[0:12]
        for i in range(0, 12):
            frame_data = bakerGameOne.to_dict(orient="records")[i]
            # bowler
            self.assertEqual(frame_data["bowler"], bakerGameOneBowler[i])
            # first ball
            self.assertEqual(frame_data["first_ball"], bakerGameOneFirstBall[i])
            # second_ball
            if math.isnan(frame_data["second_ball"]):
                self.assertTrue(math.isnan(frame_data["second_ball"]))
            else:
                self.assertEqual(frame_data["second_ball"], bakerGameOneSecondBall[i])
            # first_ball_attempt
            self.assertEqual(frame_data["first_ball_attempt"], bakerGameOneFirstBallAttempt[i])
            # spare
            self.assertEqual(frame_data["spare"], bakerGameOneIsSpare[i])
            # strikes
            self.assertEqual(frame_data["strike"], bakerGameOneIsStrike[i])
            # double
            self.assertEqual(frame_data["double"], "-")
            # double_attempt
            self.assertEqual(frame_data["double_attempt"], "-")
            # open
            self.assertEqual(frame_data["open"], bakerGameOneIsOpen[i])
            # is fill ball
            self.assertEqual(frame_data["is_fill_ball"], bakerGameOneIsFill[i])
        # Baker Game Five #
        bakerGameFive = result_frames.iloc[-12::]
        for i in range(0, 12):
            frame_data = bakerGameFive.to_dict(orient="records")[i]
            # bowler
            self.assertEqual(frame_data["bowler"], bakerGameFiveBowler[i])
            # first ball
            self.assertEqual(frame_data["first_ball"], bakerGameFiveFirstBall[i])
            # second_ball
            if math.isnan(frame_data["second_ball"]):
                self.assertTrue(math.isnan(frame_data["second_ball"]))
            else:
                self.assertEqual(frame_data["second_ball"], bakerGameFiveSecondBall[i])
            # first_ball_attempt
            self.assertEqual(frame_data["first_ball_attempt"], bakerGameFiveFirstBallAttempt[i])
            # spare
            self.assertEqual(frame_data["spare"], bakerGameFiveIsSpare[i])
            # strikes
            self.assertEqual(frame_data["strike"], bakerGameFiveIsStrike[i])
            # double
            self.assertEqual(frame_data["double"], "-")
            # double_attempt
            self.assertEqual(frame_data["double_attempt"], "-")
            # open
            self.assertEqual(frame_data["open"], bakerGameFiveIsOpen[i])
            # is fill ball
            self.assertEqual(frame_data["is_fill_ball"], bakerGameFiveIsFill[i])

    def test_transform_to_frames_team(self):
        ###### REGULAR GAME #######
        ### Team ###
        result_frames = transform_to_frames(_data=test_data_team, _game_type="Team", num_baker_games=1, num_of_baker_games_per_block=5, baker_match_play_1=7, baker_match_play_2=0, baker_match_play_3=0, game_group=0, event_type="Regular")
        # General #
        num_team_game = 2
        team_member = 5
        self.assertEqual(len(result_frames), team_member * num_team_game * 12)
        # Team game one data #
        teamGameOneData = result_frames.iloc[0:12]
        teamGameOneBowler = "Test BowlerD"
        for i in range(0, 12):
            frame_data = teamGameOneData.to_dict(orient="records")[i]
            # bowler
            self.assertEqual(frame_data["bowler"], teamGameOneBowler)
            # first ball
            self.assertEqual(frame_data["first_ball"], teamGameOneFirstBall[i])
            # second_ball
            if math.isnan(frame_data["second_ball"]):
                self.assertTrue(math.isnan(frame_data["second_ball"]))
            else:
                self.assertEqual(frame_data["second_ball"], teamGameOneSecondBall[i])
            # first_ball_attempt
            self.assertEqual(frame_data["first_ball_attempt"], teamGameOneFirstBallAttempt[i])
            # spare
            self.assertEqual(frame_data["spare"], teamGameOneIsSpare[i])
            # strikes
            self.assertEqual(frame_data["strike"], teamGameOneIsStrike[i])
            # double
            self.assertEqual(frame_data["double"], teamGameOneIsDouble[i])
            # double_attempt
            self.assertEqual(frame_data["double_attempt"], teamGameOneIsDoubleAttempt[i])
            # open
            self.assertEqual(frame_data["open"], teamGameOneIsOpen[i])
            # is fill ball
            self.assertEqual(frame_data["is_fill_ball"], teamGameOneIsFill[i])

        # Team Game Six #
        teamGameSeven = result_frames.iloc[72:84]
        teamGameSevenBower = "Test BowlerE"
        for i in range(0, 12):
            frame_data = teamGameSeven.to_dict(orient="records")[i]
            # bowler
            self.assertEqual(frame_data["bowler"], teamGameSevenBower)
            # first ball
            self.assertEqual(frame_data["first_ball"], teamGameSevenFirstBall[i])
            # second_ball
            if math.isnan(frame_data["second_ball"]):
                self.assertTrue(math.isnan(frame_data["second_ball"]))
            else:
                self.assertEqual(frame_data["second_ball"], teamGameSevenSecondBall[i])
            # first_ball_attempt
            self.assertEqual(frame_data["first_ball_attempt"], teamGameSevenFirstBallAttempt[i])
            # spare
            self.assertEqual(frame_data["spare"], teamGameSevenIsSpare[i])
            # strikes
            self.assertEqual(frame_data["strike"], teamGameSevenIsStrike[i])
            # double
            self.assertEqual(frame_data["double"], teamGameSevenIsDouble[i])
            # double_attempt
            self.assertEqual(frame_data["double_attempt"], teamGameSevenIsDoubleAttempt[i])
            # open
            self.assertEqual(frame_data["open"], teamGameSevenIsOpen[i])
            # is fill ball
            self.assertEqual(frame_data["is_fill_ball"], teamGameSevenIsFill[i])

    def test_transform_to_frames_baker_mp(self):
        """This is the function transform a csv row to 12 frames data
        frames data should be correctly identified"""
        ###### REGULAR GAME #######
        ### Baker Match Play Version one ###
        result_frames = transform_to_frames(_data=test_data_baker_match_play, _game_type="Baker Match Play", num_baker_games=1, num_of_baker_games_per_block=5, baker_match_play_1=7, baker_match_play_2=0, baker_match_play_3=0, game_group=0, event_type="Regular")
        # General #
        self.assertEqual(len(result_frames), 7 * 12)
        # should be seven games and only one group
        self.assertEqual(max(result_frames["game_no"]), 7)
        self.assertEqual(max(result_frames["game_group"]), 1)

        # Baker Match Play game three data #
        bakerMPGameThree = result_frames.iloc[24:36]
        for i in range(0, 12):
            frame_data = bakerMPGameThree.to_dict(orient="records")[i]
            # bowler
            self.assertEqual(frame_data["bowler"], bakerMPGameThreeBowler[i])
            # first ball
            self.assertEqual(frame_data["first_ball"], bakerMPGameThreeFirstBall[i])
            # second_ball
            if math.isnan(frame_data["second_ball"]):
                self.assertTrue(math.isnan(frame_data["second_ball"]))
            else:
                self.assertEqual(frame_data["second_ball"], bakerMPGameThreeSecondBall[i])
            # first_ball_attempt
            self.assertEqual(frame_data["first_ball_attempt"], bakerMPGameThreeFirstBallAttempt[i])
            # spare
            self.assertEqual(frame_data["spare"], bakerMPGameThreeIsSpare[i])
            # strikes
            self.assertEqual(frame_data["strike"], bakerMPGameThreeIsStrike[i])
            # double
            self.assertEqual(frame_data["double"], "-")
            # double_attempt
            self.assertEqual(frame_data["double_attempt"], "-")
            # open
            self.assertEqual(frame_data["open"], bakerMPGameThreeIsOpen[i])
            # is fill ball
            self.assertEqual(frame_data["is_fill_ball"], bakerMPGameThreeIsFill[i])

        # Baker Match Play Game SIX #
        bakerMPGameSix = result_frames.iloc[60:72]
        for i in range(0, 12):
            frame_data = bakerMPGameSix.to_dict(orient="records")[i]
            # bowler
            self.assertEqual(frame_data["bowler"], bakerMPGameSixBowler[i])
            # first ball
            self.assertEqual(frame_data["first_ball"], bakerMPGameSixFirstBall[i])
            # second_ball
            if math.isnan(frame_data["second_ball"]):
                self.assertTrue(math.isnan(frame_data["second_ball"]))
            else:
                self.assertEqual(frame_data["second_ball"], bakerMPGameSixSecondBall[i])
            # first_ball_attempt
            self.assertEqual(frame_data["first_ball_attempt"], bakerMPGameSixFirstBallAttempt[i])
            # spare
            self.assertEqual(frame_data["spare"], bakerMPGameSixIsSpare[i])
            # strikes
            self.assertEqual(frame_data["strike"], bakerMPGameSixIsStrike[i])
            # double
            self.assertEqual(frame_data["double"], "-")
            # double_attempt
            self.assertEqual(frame_data["double_attempt"], "-")
            # open
            self.assertEqual(frame_data["open"], bakerMPGameSixIsOpen[i])
            # is fill ball
            self.assertEqual(frame_data["is_fill_ball"], bakerMPGameSixIsFill[i])
