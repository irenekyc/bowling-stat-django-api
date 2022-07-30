from django.test import TestCase
from .transform_to_table import transform_to_table
from .testcase import *


class TestTransformToFrames(TestCase):
    def test_transform_to_frames_analysized_data(self):
        #     """This is the function aggregate the 12 frames data to analytical data
        #     data should be correctly caclcaulte"""
        (analysized_data, summary_data) = transform_to_table([df_baker_12_frames, df_team_12_frames, df_baker_mp_12_frames])
        result_analysized_data = analysized_data.to_dict("records")

        for row in result_analysized_data:
            first_ball_average = row["first_ball_average"]
            first_balls = row["first_balls"]
            num_strikes = row["num_strikes"]
            num_spares = row["num_spares"]
            num_opens = row["num_opens"]
            fill_balls = row["fill_balls"]
            bowler_data = pd.DataFrame()

            if row["game_type"] == "Baker":
                if row["bowler"] == "Test BowlerA":
                    bowler_data = bakerBowlerA
                if row["bowler"] == "Test BowlerB":
                    bowler_data = bakerBowlerB
                if row["bowler"] == "Test BowlerC":
                    bowler_data = bakerBowlerC
                if row["bowler"] == "Test BowlerD":
                    bowler_data = bakerBowlerD
                if row["bowler"] == "Test BowlerE":
                    bowler_data = bakerBowlerE
            if row["game_type"] == "Team":
                if row["bowler"] == "Test BowlerD":
                    bowler_data = teamBowlerD
                if row["bowler"] == "Test BowlerE":
                    bowler_data = teamBowlerE
            if row["game_type"] == "Baker Match Play":
                if row["bowler"] == "Test BowlerA":
                    bowler_data = bakerMPBowlerA
                if row["bowler"] == "Test BowlerB":
                    bowler_data = bakerMPBowlerB
                if row["bowler"] == "Test BowlerC":
                    bowler_data = bakerMPBowlerC
                if row["bowler"] == "Test BowlerD":
                    bowler_data = bakerMPBowlerD
                if row["bowler"] == "Test BowlerE":
                    bowler_data = bakerMPBowlerE

            if len(bowler_data) > 0:
                expected_first_ball_average = bowler_data[bowler_data["first_ball_attempt"] == 1]["first_ball"].mean()
                self.assertEqual(expected_first_ball_average, first_ball_average)
                expected_num_first_balls = bowler_data["first_ball_attempt"].sum()
                self.assertEqual(expected_num_first_balls, first_balls)
                expected_num_strikes = bowler_data["strike"].sum()
                self.assertEqual(expected_num_strikes, num_strikes)

                expected_num_spares = bowler_data["spare"].sum()
                self.assertEqual(expected_num_spares, num_spares)
                expected_num_opens = bowler_data["open"].sum()
                self.assertEqual(expected_num_opens, num_opens)
                expected_num_fill_balls = bowler_data["is_fill_ball"].sum()
                self.assertEqual(expected_num_fill_balls, fill_balls)

    def test_transform_to_frames_summary_data(self):
        #     """This is the function aggregate the 12 frames data to analytical data
        #     data should be correctly caclcaulte"""
        (analysized_data, summary_data) = transform_to_table([df_baker_12_frames, df_team_12_frames, df_baker_mp_12_frames])

        result_summary_data = summary_data.to_dict("records")

        ## General ##
        self.assertEqual(len(summary_data.columns), 40)

        for record in result_summary_data:
            bakerBowlerData = pd.DataFrame()
            bakerMPBowlerData = pd.DataFrame()
            teamBowlerData = pd.DataFrame()
            if record["bowler"] == "Test BowlerD":
                bakerBowlerData = bakerBowlerD
                bakerMPBowlerData = bakerMPBowlerD
                teamBowlerData = teamBowlerD

            if record["bowler"] == "Test BowlerE":
                bakerBowlerData = bakerBowlerE
                bakerMPBowlerData = bakerMPBowlerE
                teamBowlerData = teamBowlerE

            if len(bakerBowlerData) > 0 and len(bakerMPBowlerData) > 0 and len(teamBowlerData) > 0:

                ## First ball average ##
                baker_first_ball_average = record["baker_first_ball_average"]
                team_first_ball_average = record["team_first_ball_average"]
                bakerMP_first_ball_average = record["baker_mp_first_ball_average"]
                all_first_ball_average = record["all_first_ball_average"]

                bowler_baker_first_ball_average = bakerBowlerData[bakerBowlerData["first_ball_attempt"] == 1]["first_ball"].mean()
                bowler_team_first_ball_average = teamBowlerData[teamBowlerData["first_ball_attempt"] == 1]["first_ball"].mean()
                bowler_bakerMP_first_ball_average = bakerMPBowlerData[bakerMPBowlerData["first_ball_attempt"] == 1]["first_ball"].mean()
                bowler_all_first_ball_average = (bowler_baker_first_ball_average + bowler_team_first_ball_average + bowler_bakerMP_first_ball_average) / 3

                self.assertEqual(baker_first_ball_average, bowler_baker_first_ball_average)
                self.assertEqual(team_first_ball_average, bowler_team_first_ball_average)
                self.assertEqual(bakerMP_first_ball_average, bowler_bakerMP_first_ball_average)
                self.assertEqual(all_first_ball_average, bowler_all_first_ball_average)

                ## Fill Ball ##
                baker_fill_balls = record["baker_fill_balls"]
                team_fill_balls = record["team_fill_balls"]
                bakerMP_fill_balls = record["baker_mp_fill_balls"]

                self.assertEqual(baker_fill_balls, bakerBowlerData["is_fill_ball"].sum())
                self.assertEqual(team_fill_balls, teamBowlerData["is_fill_ball"].sum())
                self.assertEqual(bakerMP_fill_balls, bakerMPBowlerData["is_fill_ball"].sum())
