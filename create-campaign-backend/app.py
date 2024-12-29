#the main flask app
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campaigns.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    audience = db.Column(db.Text, nullable=True)
    goals = db.Column(db.String(50), nullable=False)

class SelectedInfluencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.String(100), nullable=False)

# Matching Algorithm (Mock for now)
def recommend_influencers(campaign):
    # Replace with TikTok API integration
    influencers = [
        {"id": "influencer_1", "name": "Influencer A", "match_score": 0.9},
        {"id": "influencer_2", "name": "Influencer B", "match_score": 0.85},
        {"id": "influencer_3", "name": "Influencer C", "match_score": 0.8},
    ]
    return influencers

# API Endpoints
@app.route('/campaigns', methods=['POST'])
def create_campaign():
    data = request.json
    campaign = Campaign(
        name=data['campaign_name'],
        budget=data['budget'],
        duration=data['duration'],
        audience=data.get('audience'),
        goals=data['goals']
    )
    db.session.add(campaign)
    db.session.commit()

    # Recommend influencers
    influencers = recommend_influencers(data)
    return jsonify({
        "message": "Campaign created successfully!",
        "campaign_id": campaign.id,
        "recommended_influencers": influencers
    })

@app.route('/campaigns', methods=['GET'])
def get_campaigns():
    campaigns = Campaign.query.all()
    return jsonify([{
        "id": campaign.id,
        "name": campaign.name,
        "budget": campaign.budget,
        "duration": campaign.duration,
        "audience": campaign.audience,
        "goals": campaign.goals
    } for campaign in campaigns])

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
