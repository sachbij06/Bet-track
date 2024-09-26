from flask import Flask, render_template, Blueprint, request, redirect, url_for

bet = Blueprint("bet", __name__, template_folder="templates")


# BetTracker class from the previous code
class BetTracker:
    def __init__(self):
        self.bets = []

    def add_bet(self, odds: int, stake: float, return_amount: float, over_under: str, play_type: str):
        """Adds a new bet to the tracker with additional details for over/under and play type."""
        bet_result = {
            "odds": odds,
            "stake": stake,
            "return": return_amount,
            "over_under": over_under,
            "play_type": play_type
        }
        self.bets.append(bet_result)

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
        total_stake = sum(bet['stake'] for bet in self.bets)
        return total_return - total_stake

    def get_bets(self):
        """Retrieve the list of all bets."""
        return self.bets
    
    def total_bets(self):
        return len(self.bets)
    
    # Update add_bet to include win/loss flag
    def add_bet(self, odds: int, stake: float, return_amount: float, over_under: str, play_type: str):
        """Adds a new bet to the tracker with win/loss flag."""
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