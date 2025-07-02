from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from app.extensions import mongo
import logging

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def format_timestamp():
    """Format timestamp exactly as specified: 1st April 2021 - 9:30 PM UTC"""
    dt = datetime.utcnow()
    
   
    day = dt.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    
    
    hour = dt.hour
    if hour == 0:
        hour_12 = 12
        am_pm = "AM"
    elif hour < 12:
        hour_12 = hour
        am_pm = "AM"
    elif hour == 12:
        hour_12 = 12
        am_pm = "PM"
    else:
        hour_12 = hour - 12
        am_pm = "PM"
    
    return f"{day}{suffix} {dt.strftime('%B %Y')} - {hour_12}:{dt.strftime('%M')} {am_pm} UTC"


@webhook.route('/', methods=["GET"])
def dashboard():
    """Serve the events dashboard"""
    return render_template('index.html')


@webhook.route('/receiver', methods=["POST"])
def receiver():
    try:
        if not request.is_json:
            return {"error": "Invalid content type"}, 400
        
        data = request.json
        if not data:
            return {"error": "Empty request body"}, 400
        
        logger.info("Webhook received successfully")

       
        if "pusher" in data and "ref" in data:
            try:
                author = data["pusher"]["name"]
                to_branch = data["ref"].split("/")[-1]
                timestamp = format_timestamp()
                
              
                message = f'"{author}" pushed to "{to_branch}" on {timestamp}'

                event = {
                    "type": "push",
                    "message": message,
                    "timestamp": timestamp,
                    "author": author,
                    "branch": to_branch,
                    "created_at": datetime.utcnow()
                }
                
                result = mongo.db.events.insert_one(event)
                logger.info(f"Push event stored: {message}")
                
            except KeyError as e:
                logger.error(f"Missing field for push event: {e}")
                return {"error": f"Missing field: {e}"}, 400

       
        elif "pull_request" in data and "action" in data:
            try:
                pr = data["pull_request"]
                action = data["action"]
                from_branch = pr["head"]["ref"]
                to_branch = pr["base"]["ref"]
                author = pr["user"]["login"]
                timestamp = format_timestamp()

                if action == "opened":
                   
                    message = f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}'
                    
                    event = {
                        "type": "pull_request",
                        "message": message,
                        "timestamp": timestamp,
                        "author": author,
                        "from_branch": from_branch,
                        "to_branch": to_branch,
                        "created_at": datetime.utcnow()
                    }
                    
                    result = mongo.db.events.insert_one(event)
                    logger.info(f"Pull request event stored: {message}")

                elif action == "closed" and pr.get("merged", False):
                   
                    message = f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}'
                    
                    event = {
                        "type": "merge",
                        "message": message,
                        "timestamp": timestamp,
                        "author": author,
                        "from_branch": from_branch,
                        "to_branch": to_branch,
                        "created_at": datetime.utcnow()
                    }
                    
                    result = mongo.db.events.insert_one(event)
                    logger.info(f"Merge event stored: {message}")
                
            except KeyError as e:
                logger.error(f"Missing field for pull request event: {e}")
                return {"error": f"Missing field: {e}"}, 400

        return {"message": "Webhook processed successfully"}, 200

    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return {"error": "Internal server error"}, 500


@webhook.route('/events', methods=["GET"])
def get_events():
    try:
        
        events = list(mongo.db.events.find({}, {"_id": 0}).sort("created_at", -1))
        logger.info(f"Retrieved {len(events)} events")
        return jsonify(events)
    
    except Exception as e:
        logger.error(f"Error retrieving events: {str(e)}")
        return {"error": "Failed to retrieve events"}, 500


@webhook.route('/events/latest', methods=["GET"])
def get_latest_events():
    """Get the latest N events (default 20 for UI)"""
    try:
        limit = request.args.get('limit', 20, type=int)
        events = list(mongo.db.events.find({}, {"_id": 0}).sort("created_at", -1).limit(limit))
        return jsonify(events)
    
    except Exception as e:
        logger.error(f"Error retrieving latest events: {str(e)}")
        return {"error": "Failed to retrieve latest events"}, 500