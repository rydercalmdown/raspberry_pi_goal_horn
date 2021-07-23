import os
import time
import requests
from relay_controller import RelayController


class ScoreManager():
    """Manages the score for an ongoing game"""

    def __init__(self, team_abbreviation):
        self.team = str(team_abbreviation).upper().strip()
        self._set_defaults()
        self.relay_controller = RelayController()

    def _set_defaults(self):
        """Sets the defaults for the application"""
        self.api_protocol = 'https'
        self.api_host = 'nhl-score-api.herokuapp.com'
        self.current_score = 0
        self.sleep_seconds = 30  # Time to sleep after calling the API
        self.desired_game_state = 'LIVE'  # Desired game state is LIVE

    def _get_score_url(self):
        score_endpoint = '/api/scores/latest'
        return self.api_protocol + '://' + self.api_host + score_endpoint

    def _get_live_games(self):
        """Returns any live games currently happening with the API"""
        response = requests.get(self._get_score_url())
        if response.status_code == 200:
            return [g for g in response.json()['games'] if g['status']['state'] == self.desired_game_state]

    def _get_current_teams_score(self):
        """Gets the current team's score from the API"""
        for game in self._get_live_games():
            teams_playing = [x['abbreviation'] for index, x in game['teams'].items()]
            if self.team in teams_playing:
                # Our team is playing in this game, get the score                
                return int(game['scores'][self.team])

    def _score_has_changed(self):
        """A callback for when the score has changed"""
        print('The score for {} has changed'.format(self.team))
        self.relay_controller.activate_solenoid()

    def run(self):
        """Run the app and watch for changes"""
        try:
            while True:
                print('Getting score from API...')
                latest_score = self._get_current_teams_score()
                if latest_score is None:
                    print('No score available, waiting')
                else:
                    print('Current score for {}: {}'.format(self.team, latest_score))
                    if latest_score > self.current_score:
                        self._score_has_changed()
                        self.current_score = latest_score
                print('Sleeping for {} seconds'.format(self.sleep_seconds))
                time.sleep(self.sleep_seconds)
        except KeyboardInterrupt:
            print('Exiting')
