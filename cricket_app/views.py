from django.shortcuts import render, redirect
from .models import *
from django.views.generic import View
from django.contrib import messages


class Show_Team(View):
    """View method for 'cricket_app' app front page.

      :param request:
      :return: HttpResponse
      """

    def get(self, request):
        team = Team.objects.all()
        print(team)
        return render(request, 'show.html', {'team': team})


class Show_palyer(View):
    """View method for 'cricket_app' app front page.

         :param request:
         :return: HttpResponse
         """

    def get(self, request):
        name = request.GET['name']
        players_info = list(Players.objects.filter(country_id=name).select_related("player_history"))
        response = {}
        for player in players_info:
            response[player.id] = [player.first_name, player.last_name, player.jersey_number,player.logo_player.url,
                                   player.player_history.matches, player.player_history.runs,
                                   player.player_history.highest_score,
                                   player.player_history.fifties, player.player_history.hundreds]

        return render(request, 'player.html', {'players_info': response})


class Match(View):
    def post(self, request):
        """View method for 'cricket_app' app's matches' details page.

            :param request:
            :param match_id:
            :return: HttpResponse
            """
        team1 = request.POST['team1']
        team2 = request.POST['team2']
        try:
            team_1 = Team.objects.get(name__exact=team1)
            team_2 = Team.objects.get(name__exact=team2)
            match_number = request.POST['match_number']
            print(team_1.name, team_2.name)
            winning_team = request.POST['winning_team']
            match_location = request.POST['match_location']
            match_stadium = request.POST['match_stadium']
            match_tournament = request.POST['match_tournament']
            if int(match_number) >= 1 and winning_team in [team_1.name, team_2.name]:
                match = Matches.objects.create(match_number=match_number, match_location=match_location,
                                               winning_team=winning_team,
                                               match_stadium=match_stadium,
                                               match_tournament=match_tournament)
                match.save()
                match.teams.set([team_1, team_2])
                match.save()
                team = Team.objects.all()
                for teams in team:
                    match = Matches.objects.filter(winning_team=teams.name).count()
                    print(match)
                    team_points = Points.objects.filter(team_id=teams.name)
                    if team_points:
                        team_points.update(points=match)
                    else:
                        Points(team_id=teams.name, points=match).save()
                messages.success(request, 'data saved')
                return redirect('match')
            else:
                messages.error(request, 'no of matches>=1 and winning team must be in team1 and team2')
                return redirect('match')
        except Team.DoesNotExist:
            messages.error(request, 'team must be in tournament')
            return redirect('match')

    def get(self, request):
        query_set = Team.objects.all()
        return render(request, 'match.html', {'query_set': query_set})


class Show_Points(View):
    """View method for 'cricket_app' app front page.

    :param request:
    :return: HttpResponse
    """

    def get(self, request):
        point = Points.objects.all()
        return render(request, 'points.html', {'point': point})
