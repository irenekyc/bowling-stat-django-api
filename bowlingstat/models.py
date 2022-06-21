from django.db import models

class Team(models.Model):
  team_id = models.CharField(max_length=250, primary_key=True)
  team_name = models.CharField(max_length=250)
  bowlers = models.CharField(max_length=500)
  events = models.CharField(max_length=500)


class EventData(models.Model):
        event_id = models.CharField(max_length=250, null=True)
        team_id = models.CharField(max_length=250, null=True)
        team_name = models.CharField(max_length=250, null=True)
        season = models.CharField(max_length=250)
        location = models.CharField(max_length=250)
        start_date = models.DateField()
        end_date =  models.DateField()
        event_name = models.CharField(max_length=250)
        game_type = models.CharField(max_length=250)
        game_group =models.CharField(max_length=250)
        bowler = models.CharField(max_length=250)
        first_balls = models.CharField(max_length=250)
        first_ball_average = models.CharField(max_length=250)
        frames = models.CharField(max_length=250)
        frame_average = models.CharField(max_length=250)
        num_strikes = models.CharField(max_length=250)
        num_spares = models.CharField(max_length=250)
        num_opens = models.CharField(max_length=250)
        num_doubles = models.CharField(max_length=250)
        num_double_attempts = models.CharField(max_length=250)
        score = models.CharField(max_length=250)

        fill_balls = models.CharField(max_length=250)
        fill_ball_strikes = models.CharField(max_length=250)
        fill_ball_non_strikes = models.CharField(max_length=250)
        spares_per_game = models.CharField(max_length=250)
        opens_per_game = models.CharField(max_length=250)

        strikes_per_game = models.CharField(max_length=250)
        double_percentage = models.CharField(max_length=250)
        sitrkes_percentage = models.CharField(max_length=250)
        fill_ball_strikes_percentage = models.CharField(max_length=250)