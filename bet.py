import json
import os
from flask import Flask, render_template, Blueprint, request, redirect, url_for

bet = Blueprint("bet", __name__, template_folder="templates")

# BetTracker class
class BetTracker:
    def __init__(self, json_file='bets_data.json'):
        self.bets = []
        self.json_file = json_file
        self.load_bets()  # Load bets from the JSON file when the app starts

    def add_bet(self, odds: int, stake: float, return_amount: float, over_under: str, play_type: str):
        """Adds a new bet to the tracker with win/loss flag and saves to the JSON file."""
        win_or_loss = "WIN" if return_amount > 0 else "LOSS"  # Determine if it's a win or loss
        bet_result = {
            "odds": odds,
            "stake": stake,
            "return": return_amount,
            "over_under": over_under,
            "play_type": play_type,
            "win_or_loss": win_or_loss  # Add win/loss flag
        }
        self.bets.append(bet_result)
        self.save_bets()  # Save bets to JSON after adding

    def average_bet_size(self):
        """Calculate average stake size."""
        if not self.bets:
            return 0.0
        total_stake = sum(bet['stake'] for bet in self.bets)
        return total_stake / len(self.bets)

    def average_odds_taken(self):
        """Calculate average odds taken."""
        if not self.bets:
            return 0.0
        total_odds = sum(bet['odds'] for bet in self.bets)
        return total_odds / len(self.bets)

    def win_percentage(self):
        """Calculate win percentage."""
        if not self.bets:
            return 0.0
        wins = sum(1 for bet in self.bets if bet['return'] > 0)
        return (wins / len(self.bets)) * 100

    def total_win_loss(self):
        """Calculate total net win/loss."""
        if not self.bets:
            return 0.0
        total_return = sum(bet['return'] for bet in self.bets)
        return total_return

    def get_bets(self):
        """Retrieve the list of all bets."""
        return self.bets

    def total_bets(self):
        return len(self.bets)

    def save_bets(self):
        """Save bets to a JSON file."""
        try:
            with open(self.json_file, 'w') as file:
                json.dump(self.bets, file, indent=4)
        except IOError as e:
            print(f"Error saving bets to {self.json_file}: {e}")

    def load_bets(self):
        """Load bets from a JSON file if it exists."""
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r') as file:
                    self.bets = json.load(file)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading bets from {self.json_file}: {e}")
                self.bets = []

# Create an instance of the BetTracker
tracker = BetTracker()

@bet.route('/')
def index():
    """Display the home page with form and bet data."""
    bets = tracker.get_bets()
    summary = {
        "avg_odds": tracker.average_odds_taken(),
        "win_percentage": tracker.win_percentage(),
        "total_win_loss": tracker.total_win_loss(),
        "total_bets": tracker.total_bets()
    }
    return render_template('index.html', bets=bets, summary=summary)

@bet.route('/add_bet', methods=['POST'])
def add_bet():
    """Handle POST request to add a new bet."""
    # Get form data from the POST request
    odds = int(request.form.get('odds'))
    stake = float(request.form.get('stake'))
    return_amount = float(request.form.get('return'))
    over_under = request.form.get('over_under')  # Get Over/Under selection
    play_type = request.form.get('play_type')    # Get Play Type selection

    # Add the new bet to the tracker with over/under and play type
    tracker.add_bet(odds, stake, return_amount, over_under, play_type)

    # Redirect back to the index page to display updated results
    return redirect(url_for('bet.index'))  # Use 'bet.index' to reference the correct route in the blueprint
