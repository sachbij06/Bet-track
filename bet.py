from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# BetTracker class from the previous code
class BetTracker:
    def __init__(self):
        self.bets = []

    def add_bet(self, odds: int, stake: float, return_amount: float):
        bet_result = {
            "odds": odds,
            "stake": stake,
            "return": return_amount
        }
        self.bets.append(bet_result)

    def average_bet_size(self):
        if not self.bets:
            return 0.0
        total_stake = sum(bet['stake'] for bet in self.bets)
        return total_stake / len(self.bets)

    def average_odds_taken(self):
        if not self.bets:
            return 0.0
        total_odds = sum(bet['odds'] for bet in self.bets)
        return total_odds / len(self.bets)

    def win_percentage(self):
        if not self.bets:
            return 0.0
        wins = sum(1 for bet in self.bets if bet['return'] > 0)
        return (wins / len(self.bets)) * 100

    def total_win_loss(self):
        if not self.bets:
            return 0.0
        total_return = sum(bet['return'] for bet in self.bets)
        total_stake = sum(bet['stake'] for bet in self.bets)
        return total_return - total_stake

    def get_bets(self):
        return self.bets

# Create an instance of the BetTracker
tracker = BetTracker()

@app.route('/')
def index():
    # Display the home page with form and bet data
    bets = tracker.get_bets()
    summary = {
        "avg_bet_size": tracker.average_bet_size(),
        "avg_odds": tracker.average_odds_taken(),
        "win_percentage": tracker.win_percentage(),
        "total_win_loss": tracker.total_win_loss()
    }
    return render_template('index.html', bets=bets, summary=summary)

@app.route('/add_bet', methods=['POST'])
def add_bet():
    # Get form data from the POST request
    odds = int(request.form.get('odds'))
    stake = float(request.form.get('stake'))
    return_amount = float(request.form.get('return'))

    # Add the new bet to the tracker
    tracker.add_bet(odds, stake, return_amount)

    # Redirect back to the index page to display updated results
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
