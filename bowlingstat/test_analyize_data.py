from django.test import TestCase
from .analyize_data_utlis import *
from .testcase import *


class TestAnalyizeDataUtlis(TestCase):
    # def setUp(self):
    #     Animal.objects.create(name="lion", sound="roar")
    #     Animal.objects.create(name="cat", sound="meow")

    def test_correctly_identify_fill_ball(self):
        """Fill ball should be correctly identified"""
        #### Test row One ####
        # if frame is less than or equal to 10, it is always 0, only return 1 when it is frame 12
        self.assertEqual(getIsFillBall(1, is_fill_ball_data_row), 0)
        self.assertEqual(getIsFillBall(2, is_fill_ball_data_row), 0)
        self.assertEqual(getIsFillBall(10, is_fill_ball_data_row), 0)
        self.assertEqual(getIsFillBall(11, is_fill_ball_data_row), 0)
        self.assertEqual(getIsFillBall(12, is_fill_ball_data_row), 1)

        #### Test row Two ####
        self.assertEqual(getIsFillBall(11, is_fill_ball_data_row2), 1)

        #### Test row Three ####
        self.assertEqual(getIsFillBall(12, is_not_fill_ball_data_row), 0)

    def test_correctly_get_pin_2_leave(self):
        """Pin 2 leave should be correctly identified"""
        self.assertEqual(getPin2Leave(1, pin_ball_row), "-")
        self.assertEqual(getPin2Leave(2, pin_ball_row), frame2ball2pin)
        self.assertEqual(getPin2Leave(3, pin_ball_row), "-")
        self.assertEqual(getPin2Leave(10, pin_ball_row), "-")
        self.assertEqual(getPin2Leave(11, pin_ball_row), "-")

    def test_correctly_get_pin_1_leave(self):
        """Pin leave should be correctly identified"""
        self.assertEqual(getPinLeave(1, pin_ball_row), frame1ball1pin)
        self.assertEqual(getPinLeave(2, pin_ball_row), frame2ball1pin)
        self.assertEqual(getPinLeave(3, pin_ball_row), "-")
        self.assertEqual(getPinLeave(10, pin_ball_row), frame10ball1pin)
        ## TODO: revisit
        self.assertEqual(getPinLeave(11, pin_ball_row), None)
        self.assertEqual(getPinLeave(12, pin_ball_row), "-")

    def test_correctly_get_is_strike(self):
        """Strike should be correctly identified"""
        #### Test row One ####
        self.assertEqual(getIsStrike(1, frame_data_row), 1)
        self.assertEqual(getIsStrike(2, frame_data_row), 0)
        self.assertEqual(getIsStrike(10, frame_data_row), 1)
        self.assertEqual(getIsStrike(11, frame_data_row), 1)
        self.assertEqual(getIsStrike(12, frame_data_row), 0)

        #### Test row Two ####
        self.assertEqual(getIsStrike(10, frame_data_row_case_2), 0)
        self.assertEqual(getIsStrike(11, frame_data_row_case_2), 1)
        self.assertEqual(getIsStrike(12, frame_data_row_case_2), 0)

        #### Test row Three ####
        self.assertEqual(getIsStrike(10, frame_data_row_case_3), 0)
        self.assertEqual(getIsStrike(11, frame_data_row_case_3), 0)
        self.assertEqual(getIsStrike(12, frame_data_row_case_3), 0)

    def test_correctly_set_game_group_for_regular_game(self):
        """game group should be correctly identified"""
        ## FOR BAKER ##
        self.assertEqual(getGameGroup(num_baker_games_per_block=4, row_no=1, game_type="Baker", num_baker_games=5, baker_match_distributions=[1, 1, 1]), 1)
        self.assertEqual(getGameGroup(num_baker_games_per_block=4, row_no=5, game_type="Baker", num_baker_games=5, baker_match_distributions=[1, 1, 1]), 2)
        self.assertEqual(getGameGroup(num_baker_games_per_block=4, row_no=9, game_type="Baker", num_baker_games=5, baker_match_distributions=[1, 1, 1]), 3)
        self.assertEqual(getGameGroup(num_baker_games_per_block=4, row_no=13, game_type="Baker", num_baker_games=5, baker_match_distributions=[1, 1, 1]), 4)

        self.assertEqual(getGameGroup(num_baker_games_per_block=5, row_no=5, game_type="Baker", num_baker_games=5, baker_match_distributions=[1, 1, 1]), 1)
        self.assertEqual(getGameGroup(num_baker_games_per_block=5, row_no=10, game_type="Baker", num_baker_games=5, baker_match_distributions=[1, 1, 1]), 2)
        self.assertEqual(getGameGroup(num_baker_games_per_block=5, row_no=15, game_type="Baker", num_baker_games=5, baker_match_distributions=[1, 1, 1]), 3)
        self.assertEqual(getGameGroup(num_baker_games_per_block=5, row_no=16, game_type="Baker", num_baker_games=5, baker_match_distributions=[1, 1, 1]), 4)

        self.assertEqual(getGameGroup(num_baker_games_per_block=3, row_no=5, game_type="Baker", num_baker_games=5, baker_match_distributions=[1, 1, 1]), 2)
        self.assertEqual(getGameGroup(num_baker_games_per_block=3, row_no=10, game_type="Baker", num_baker_games=5, baker_match_distributions=[1, 1, 1]), 4)
        self.assertEqual(getGameGroup(num_baker_games_per_block=3, row_no=15, game_type="Baker", num_baker_games=5, baker_match_distributions=[1, 1, 1]), 5)
        self.assertEqual(getGameGroup(num_baker_games_per_block=3, row_no=16, game_type="Baker", num_baker_games=5, baker_match_distributions=[1, 1, 1]), 6)

        ## FOR Team ##
        self.assertEqual(getGameGroup(num_baker_games_per_block=1, row_no=1, game_type="Team", num_baker_games=5, baker_match_distributions=[1, 1, 1]), 1)
        self.assertEqual(getGameGroup(num_baker_games_per_block=1, row_no=5, game_type="Team", num_baker_games=5, baker_match_distributions=[1, 1, 1]), 1)
        self.assertEqual(getGameGroup(num_baker_games_per_block=1, row_no=9, game_type="Team", num_baker_games=5, baker_match_distributions=[1, 1, 1]), 2)
        self.assertEqual(getGameGroup(num_baker_games_per_block=1, row_no=13, game_type="Team", num_baker_games=5, baker_match_distributions=[1, 1, 1]), 3)
        self.assertEqual(getGameGroup(num_baker_games_per_block=1, row_no=50, game_type="Team", num_baker_games=5, baker_match_distributions=[1, 1, 1]), 10)

        ## FOR Baker MP ##
        self.assertEqual(getGameGroup(num_baker_games_per_block=10, row_no=1, game_type="Baker Match Play", num_baker_games=100, baker_match_distributions=[1, 1, 1]), 1)
        self.assertEqual(getGameGroup(num_baker_games_per_block=10, row_no=2, game_type="Baker Match Play", num_baker_games=100, baker_match_distributions=[1, 1, 1]), 2)
        self.assertEqual(getGameGroup(num_baker_games_per_block=10, row_no=3, game_type="Baker Match Play", num_baker_games=100, baker_match_distributions=[1, 1, 1]), 3)

        self.assertEqual(getGameGroup(num_baker_games_per_block=10, row_no=7, game_type="Baker Match Play", num_baker_games=100, baker_match_distributions=[7, 4, 5]), 1)
        self.assertEqual(getGameGroup(num_baker_games_per_block=10, row_no=7, game_type="Baker Match Play", num_baker_games=100, baker_match_distributions=[4, 5, 7]), 2)
        self.assertEqual(getGameGroup(num_baker_games_per_block=10, row_no=7, game_type="Baker Match Play", num_baker_games=100, baker_match_distributions=[6, 6, 6]), 2)

        self.assertEqual(getGameGroup(num_baker_games_per_block=10, row_no=6, game_type="Baker Match Play", num_baker_games=100, baker_match_distributions=[7, 4, 5]), 1)
        self.assertEqual(getGameGroup(num_baker_games_per_block=10, row_no=6, game_type="Baker Match Play", num_baker_games=100, baker_match_distributions=[4, 5, 7]), 2)
        self.assertEqual(getGameGroup(num_baker_games_per_block=10, row_no=6, game_type="Baker Match Play", num_baker_games=100, baker_match_distributions=[6, 6, 6]), 1)

        self.assertEqual(getGameGroup(num_baker_games_per_block=10, row_no=12, game_type="Baker Match Play", num_baker_games=100, baker_match_distributions=[7, 4, 5]), 3)
        self.assertEqual(getGameGroup(num_baker_games_per_block=10, row_no=12, game_type="Baker Match Play", num_baker_games=100, baker_match_distributions=[4, 5, 7]), 3)
        self.assertEqual(getGameGroup(num_baker_games_per_block=10, row_no=12, game_type="Baker Match Play", num_baker_games=100, baker_match_distributions=[6, 6, 6]), 2)

    def test_correctly_get_current_frame_bowler(self):
        """Bowler should be correctly identified"""
        self.assertEqual(getCurrentFrameBowler(1, frame_bowler_row), "A")
        self.assertEqual(getCurrentFrameBowler(2, frame_bowler_row), "B")
        self.assertEqual(getCurrentFrameBowler(3, frame_bowler_row), "C")
        self.assertEqual(getCurrentFrameBowler(4, frame_bowler_row), "D")
        self.assertEqual(getCurrentFrameBowler(5, frame_bowler_row), "E")
        self.assertEqual(getCurrentFrameBowler(10, frame_bowler_row), "D")
        self.assertEqual(getCurrentFrameBowler(11, frame_bowler_row), "A")
        self.assertEqual(getCurrentFrameBowler(12, frame_bowler_row), "A")

    def test_get_current_frame_first_ball(self):
        """First Ball value should be correctly identified"""
        ### TEST CASE ONE ###
        self.assertEqual(getCurrentFrameFirstBall(1, frame_data_row), 10)
        self.assertEqual(getCurrentFrameFirstBall(2, frame_data_row), 6)
        self.assertEqual(getCurrentFrameFirstBall(3, frame_data_row), 10)
        self.assertEqual(getCurrentFrameFirstBall(4, frame_data_row), 9)
        self.assertEqual(getCurrentFrameFirstBall(10, frame_data_row), 10)
        self.assertEqual(getCurrentFrameFirstBall(11, frame_data_row), 10)
        self.assertEqual(getCurrentFrameFirstBall(12, frame_data_row), 6)

        ### TEST CASE Two ###
        self.assertEqual(getCurrentFrameFirstBall(10, frame_data_row_case_2), 6)
        self.assertEqual(getCurrentFrameFirstBall(11, frame_data_row_case_2), 10)
        self.assertEqual(getCurrentFrameFirstBall(12, frame_data_row_case_2), 0)

        ### TEST CASE Three ###
        self.assertEqual(getCurrentFrameFirstBall(10, frame_data_row_case_3), 6)
        self.assertEqual(getCurrentFrameFirstBall(11, frame_data_row_case_3), 0)
        self.assertEqual(getCurrentFrameFirstBall(12, frame_data_row_case_3), 0)

    def test_get_current_frame_second_ball(self):
        """Second Ball value should be correctly identified"""
        ### TEST CASE ONE ###
        self.assertTrue(math.isnan(getCurrentFrameSecondBall(1, frame_data_row)))
        self.assertTrue(getCurrentFrameSecondBall(2, frame_data_row) == 4)
        self.assertTrue(math.isnan(getCurrentFrameSecondBall(3, frame_data_row)))
        self.assertTrue(getCurrentFrameSecondBall(10, frame_data_row) == 0)
        self.assertTrue(getCurrentFrameSecondBall(11, frame_data_row) == 0)
        self.assertTrue(getCurrentFrameSecondBall(12, frame_data_row) == 0)

        # ### TEST CASE Two ###
        self.assertEqual(getCurrentFrameSecondBall(10, frame_data_row_case_2), 4)
        self.assertEqual(getCurrentFrameSecondBall(11, frame_data_row_case_2), 0)
        self.assertEqual(getCurrentFrameSecondBall(12, frame_data_row_case_2), 0)

        # ### TEST CASE Three ###
        self.assertEqual(getCurrentFrameSecondBall(10, frame_data_row_case_3), 3)
        self.assertEqual(getCurrentFrameSecondBall(11, frame_data_row_case_3), 0)
        self.assertEqual(getCurrentFrameSecondBall(12, frame_data_row_case_3), 0)

    def test_get_is_first_ball_attempt(self):
        """First ball attempt should be correctly identified"""
        ### TEST CASE ONE ###
        self.assertEqual(getFirstBallAttempt(1, frame_data_row), 1)
        self.assertEqual(getFirstBallAttempt(2, frame_data_row), 1)
        self.assertEqual(getFirstBallAttempt(3, frame_data_row), 1)
        self.assertEqual(getFirstBallAttempt(4, frame_data_row), 1)
        self.assertEqual(getFirstBallAttempt(10, frame_data_row), 1)
        self.assertEqual(getFirstBallAttempt(11, frame_data_row), 1)
        self.assertEqual(getFirstBallAttempt(12, frame_data_row), 1)

        # # ### TEST CASE Two ###
        self.assertEqual(getFirstBallAttempt(10, frame_data_row_case_2), 1)
        self.assertEqual(getFirstBallAttempt(11, frame_data_row_case_2), 0)
        self.assertEqual(getFirstBallAttempt(12, frame_data_row_case_2), 1)

        # # ### TEST CASE Three ###
        self.assertEqual(getFirstBallAttempt(10, frame_data_row_case_3), 1)
        self.assertEqual(getFirstBallAttempt(11, frame_data_row_case_3), 0)
        self.assertEqual(getFirstBallAttempt(12, frame_data_row_case_3), 0)

    def test_get_is_spares(self):
        """Is Spares should be correctly identified"""
        ### TEST CASE ONE ###
        self.assertEqual(getIsSpare(1, frame_data_row), 0)
        self.assertEqual(getIsSpare(2, frame_data_row), 1)
        self.assertEqual(getIsSpare(3, frame_data_row), 0)
        self.assertEqual(getIsSpare(4, frame_data_row), 0)
        self.assertEqual(getIsSpare(10, frame_data_row), 0)
        self.assertEqual(getIsSpare(11, frame_data_row), 0)
        self.assertEqual(getIsSpare(12, frame_data_row), 0)

        ### TEST CASE Two ###
        self.assertEqual(getIsSpare(10, frame_data_row_case_2), 1)
        self.assertEqual(getIsSpare(11, frame_data_row_case_2), 0)
        self.assertEqual(getIsSpare(12, frame_data_row_case_2), 0)

        ### TEST CASE Three ###
        self.assertEqual(getIsSpare(10, frame_data_row_case_3), 0)
        self.assertEqual(getIsSpare(11, frame_data_row_case_3), 0)
        self.assertEqual(getIsSpare(12, frame_data_row_case_3), 0)

    def test_get_is_open(self):
        """Is Open should be correctly identified"""
        ### TEST CASE ONE ###
        self.assertEqual(getIsOpen(1, frame_data_row), 0)
        self.assertEqual(getIsOpen(2, frame_data_row), 0)
        self.assertEqual(getIsOpen(3, frame_data_row), 0)
        self.assertEqual(getIsOpen(4, frame_data_row), 1)
        self.assertEqual(getIsOpen(10, frame_data_row), 0)
        self.assertEqual(getIsOpen(11, frame_data_row), 0)
        self.assertEqual(getIsOpen(12, frame_data_row), 0)

        # ### TEST CASE Two ###
        self.assertEqual(getIsOpen(10, frame_data_row_case_2), 0)
        self.assertEqual(getIsOpen(11, frame_data_row_case_2), 0)
        self.assertEqual(getIsOpen(12, frame_data_row_case_2), 0)

        # ### TEST CASE Three ###
        self.assertEqual(getIsOpen(10, frame_data_row_case_3), 1)
        self.assertEqual(getIsOpen(11, frame_data_row_case_3), 0)
        self.assertEqual(getIsOpen(12, frame_data_row_case_3), 0)

    def test_get_is_double(self):
        """Is Double should be correctly identified"""
        ### TEST CASE ONE ###
        self.assertEqual(getIsDouble("Team", 1, frame_data_row), 0)
        self.assertEqual(getIsDouble("Team", 2, frame_data_row), 0)
        self.assertEqual(getIsDouble("Team", 3, frame_data_row), 0)
        self.assertEqual(getIsDouble("Team", 4, frame_data_row), 0)
        self.assertEqual(getIsDouble("Team", 5, frame_data_row), 0)
        self.assertEqual(getIsDouble("Team", 11, frame_data_row), 1)
        self.assertEqual(getIsDouble("Team", 12, frame_data_row), 0)

        ### TEST CASE Two ###
        self.assertEqual(getIsDouble("Team", 1, frame_data_row_case_2), 0)
        self.assertEqual(getIsDouble("Team", 2, frame_data_row_case_2), 1)
        self.assertEqual(getIsDouble("Team", 3, frame_data_row_case_2), 1)
        self.assertEqual(getIsDouble("Team", 4, frame_data_row_case_2), 0)
        self.assertEqual(getIsDouble("Team", 11, frame_data_row_case_2), 0)
        self.assertEqual(getIsDouble("Team", 12, frame_data_row_case_2), 0)

        ## Baker or Baker Match Play always return "-" ###
        self.assertEqual(getIsDouble("Baker", 1, frame_data_row_case_2), "-")
        self.assertEqual(getIsDouble("Baker Match Play", 2, frame_data_row_case_2), "-")

    def test_get_is_double_attempt(self):
        """Is Double attempt should be correctly identified"""
        ### TEST CASE ONE ###
        self.assertEqual(getIsDoubleAttempt("Team", 1, frame_data_row), 0)
        self.assertEqual(getIsDoubleAttempt("Team", 2, frame_data_row), 1)
        self.assertEqual(getIsDoubleAttempt("Team", 3, frame_data_row), 0)
        self.assertEqual(getIsDoubleAttempt("Team", 4, frame_data_row), 1)
        self.assertEqual(getIsDoubleAttempt("Team", 5, frame_data_row), 0)
        self.assertEqual(getIsDoubleAttempt("Team", 11, frame_data_row), 1)
        self.assertEqual(getIsDoubleAttempt("Team", 12, frame_data_row), 1)

        ### TEST CASE Two ###
        self.assertEqual(getIsDoubleAttempt("Team", 1, frame_data_row_case_2), 0)
        self.assertEqual(getIsDoubleAttempt("Team", 2, frame_data_row_case_2), 1)
        self.assertEqual(getIsDoubleAttempt("Team", 3, frame_data_row_case_2), 1)
        self.assertEqual(getIsDoubleAttempt("Team", 4, frame_data_row_case_2), 1)
        self.assertEqual(getIsDoubleAttempt("Team", 5, frame_data_row_case_2), 0)
        self.assertEqual(getIsDoubleAttempt("Team", 11, frame_data_row_case_2), 0)
        self.assertEqual(getIsDoubleAttempt("Team", 12, frame_data_row_case_2), 0)

        ## Baker or Baker Match Play always return "-" ###
        self.assertEqual(getIsDoubleAttempt("Baker", 1, frame_data_row_case_2), "-")
        self.assertEqual(getIsDoubleAttempt("Baker Match Play", 2, frame_data_row_case_2), "-")
