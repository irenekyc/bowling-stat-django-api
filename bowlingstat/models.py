from django.db import models


class Team(models.Model):
    team_id = models.CharField(max_length=250, primary_key=True)
    team_name = models.CharField(max_length=250)
    bowlers = models.CharField(max_length=500)
    events = models.CharField(max_length=500)


class EventData(models.Model):
    event_id = models.CharField(max_length=250)
    team_id = models.CharField(max_length=250)
    team_name = models.CharField(max_length=250)
    event_season = models.CharField(max_length=250)
    event_location = models.CharField(max_length=250)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    event_name = models.CharField(max_length=250)
    game_type = models.CharField(max_length=250)
    game_group = models.CharField(max_length=250)
    bowler = models.CharField(max_length=250)
    first_balls = models.CharField(max_length=250, null=True)
    first_ball_average = models.CharField(max_length=250, null=True)
    frames = models.CharField(max_length=250, null=True)
    frame_average = models.CharField(max_length=250, null=True)
    num_strikes = models.CharField(max_length=250, null=True)
    num_spares = models.CharField(max_length=250, null=True)
    num_opens = models.CharField(max_length=250, null=True)
    num_doubles = models.CharField(max_length=250, null=True)
    num_double_attempts = models.CharField(max_length=250, null=True)
    score = models.CharField(max_length=250, null=True)
    fill_balls = models.CharField(max_length=250, null=True)
    fill_ball_strikes = models.CharField(max_length=250, null=True)
    fill_ball_non_strikes = models.CharField(max_length=250, null=True)
    spares_per_game = models.CharField(max_length=250, null=True)
    opens_per_game = models.CharField(max_length=250, null=True)
    strikes_per_game = models.CharField(max_length=250, null=True)
    double_percentage = models.CharField(max_length=250, null=True)
    strikes_percentage = models.CharField(max_length=250, null=True)
    fill_ball_strikes_percentage = models.CharField(max_length=250, null=True)


class EventSummaryData(models.Model):
    event_id = models.CharField(max_length=250)
    team_id = models.CharField(max_length=250)
    team_name = models.CharField(max_length=250)
    event_name = models.CharField(max_length=250)
    event_season = models.CharField(max_length=250)
    event_location = models.CharField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()
    bowler = models.CharField(max_length=250)
    baker_num_frames = models.CharField(max_length=250, null=True)
    baker_frame_ave = models.CharField(max_length=250, null=True)
    baker_num_strikes = models.CharField(max_length=250, null=True)
    baker_num_strikes_attempt = models.CharField(max_length=250, null=True)
    baker_strikes_percentage = models.CharField(max_length=250, null=True)
    baker_first_ball_average = models.CharField(max_length=250, null=True)
    baker_fill_balls = models.CharField(max_length=250, null=True)
    baker_fill_ball_strikes = models.CharField(max_length=250, null=True)
    baker_fill_ball_non_strikes = models.CharField(max_length=250, null=True)
    baker_fill_ball_strikes_percentage = models.CharField(max_length=250, null=True)
    team_num_frames = models.CharField(max_length=250, null=True)
    team_frame_ave = models.CharField(max_length=250, null=True)
    team_num_strikes = models.CharField(max_length=250, null=True)
    team_num_strikes_attempt = models.CharField(max_length=250, null=True)
    team_strikes_percentage = models.CharField(max_length=250, null=True)
    team_first_ball_average = models.CharField(max_length=250, null=True)
    team_doubles = models.CharField(max_length=250, null=True)
    team_doubles_attempt = models.CharField(max_length=250, null=True)
    team_double_percentage = models.CharField(max_length=250, null=True)
    team_fill_balls = models.CharField(max_length=250, null=True)
    team_fill_ball_strikes = models.CharField(max_length=250, null=True)
    team_fill_ball_non_strikes = models.CharField(max_length=250, null=True)
    team_fill_ball_strikes_percentage = models.CharField(max_length=250, null=True)
    baker_mp_num_frames = models.CharField(max_length=250, null=True)
    baker_mp_frame_ave = models.CharField(max_length=250, null=True)
    baker_mp_num_strikes = models.CharField(max_length=250, null=True)
    baker_mp_num_strikes_attempt = models.CharField(max_length=250, null=True)
    baker_mp_strikes_percentage = models.CharField(max_length=250, null=True)
    baker_mp_first_ball_average = models.CharField(max_length=250, null=True)
    baker_mp_fill_balls = models.CharField(max_length=250, null=True)
    baker_mp_fill_ball_strikes = models.CharField(max_length=250, null=True)
    baker_mp_fill_ball_non_strikes = models.CharField(max_length=250, null=True)
    baker_mp_fill_ball_strikes_percentage = models.CharField(max_length=250, null=True)
    all_num_frames = models.CharField(max_length=250, null=True)
    all_frame_ave = models.CharField(max_length=250, null=True)
    all_num_strikes = models.CharField(max_length=250, null=True)
    all_num_strikes_attempt = models.CharField(max_length=250, null=True)
    all_strikes_percentage = models.CharField(max_length=250, null=True)
    all_first_ball_average = models.CharField(max_length=250, null=True)
