from django.db import models


class Team(models.Model):
    """Model class for the cricket_app  Teams
    """
    name = models.CharField(max_length=200, primary_key=True)
    logo = models.ImageField(upload_to='media/')


class Playerhistory(models.Model):
    """Model class for the cricket_app  PlayerHistory. This is where the
        extra/miscellaneous information about the player will be stored
        """
    matches = models.IntegerField()
    runs = models.IntegerField()
    highest_score = models.IntegerField()
    fifties = models.IntegerField()
    hundreds = models.IntegerField()


class Players(models.Model):
    """Model class for the cricket_app  Player
       """

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    jersey_number = models.IntegerField()
    logo_player = models.ImageField(upload_to='media/')
    country = models.ForeignKey(Team, on_delete=models.CASCADE)
    player_history = models.OneToOneField(Playerhistory, on_delete=models.CASCADE)


class Matches(models.Model):
    """Model class for the cricket_app Matches
    """
    teams = models.ManyToManyField(Team)
    winning_team = models.CharField(max_length=100)
    match_number = models.PositiveIntegerField(unique=True)
    match_stadium = models.CharField(max_length=255)
    match_location = models.CharField(max_length=255)
    match_tournament = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)


class Points(models.Model):
    """Model class for the cricket_app Points
       """
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    points = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
