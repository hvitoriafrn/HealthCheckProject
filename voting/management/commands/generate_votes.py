import random
from datetime import datetime, timedelta

# Example data structure
teams = ["Team A", "Team B", "Team C", "Team D"]
questions = [
    "Question 1",
    "Question 2",
    "Question 3",
    "Question 4"
]

# Function to generate random vote for each team and question
def generate_vote():
    return random.choice(['red', 'amber', 'green'])

# Function to generate trends (random: up, down, flat)
def generate_trend():
    return random.choice(['↑', '↓', '→'])

# Generate random votes for each team
def generate_votes():
    votes_data = []
    trends_data = []
    for team in teams:
        team_votes = []
        team_trends = []
        for question in questions:
            # Generate random vote for the question
            vote = generate_vote()
            trend = generate_trend()  # Get trend for this vote
            
            team_votes.append(vote)
            team_trends.append(trend)
        votes_data.append({
            'team': team,
            'votes': team_votes,
            'trends': team_trends
        })
    return votes_data

# Generate the pie chart and line chart data
def generate_chart_data():
    # Example values, you'd likely want to process your votes_data here
    # Pie chart data (example: 30% Red, 40% Amber, 30% Green)
    pie_data = {
        'labels': ['Red', 'Amber', 'Green'],
        'data': [30, 40, 30]
    }
    
    # Line chart data (example: 5 data points over time)
    line_data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        'data': [60, 70, 65, 80, 75]  # Example percentage of Green votes
    }
    
    return pie_data, line_data

# Sample function to convert the data into a format that can be used by the front-end
def prepare_frontend_data():
    votes_data = generate_votes()
    pie_data, line_data = generate_chart_data()
    
    # Format the votes data to be suitable for rendering in your template
    rows = []
    for vote in votes_data:
        row = {
            'team': vote['team'],
            'cells': []
        }
        for i, vote_value in enumerate(vote['votes']):
            trend = vote['trends'][i]
            row['cells'].append({
                'cur': (vote_value, trend)
            })
        rows.append(row)
    
    # Prepare chart data for template rendering
    pie_labels = pie_data['labels']
    pie_data_values = pie_data['data']
    line_labels = line_data['labels']
    line_data_values = line_data['data']
    
    return rows, pie_labels, pie_data_values, line_labels, line_data_values

# Call this function and use the returned data in your view logic
if __name__ == "__main__":
    rows, pie_labels, pie_data_values, line_labels, line_data_values = prepare_frontend_data()
    
    # Example output, this can be passed to the template rendering logic
    print(f"Rows: {rows}")
    print(f"Pie Labels: {pie_labels}")
    print(f"Pie Data: {pie_data_values}")
    print(f"Line Labels: {line_labels}")
    print(f"Line Data: {line_data_values}")
