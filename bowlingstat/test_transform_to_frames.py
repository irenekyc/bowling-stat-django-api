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
