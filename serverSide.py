from flask import Flask, request, jsonify, send_file
import os
import logging
from Scripts.Quali.Throttle_comparison import ThrottleComp
from Scripts.Quali.plot_qualifying_results import QualiResults
from Scripts.Quali.top_speed_plot import TopSpeedFunc
from Scripts.Race.plot_strategy import StrategyFunc
from Scripts.Quali.Track_comparison import TrackCompFunc
from Scripts.Quali.plot_speed_traces import SpeedTraceFunc
from Scripts.Race.plot_team_pace_ranking import TeamPaceRankingFunc
from Scripts.Race.plot_driver_laptimes import DriverLaptimesFunc
from Scripts.Race.plot_laptimes_distribution import LaptimesDistributionFunc
from Scripts.Throttle_graph import throttle_graph
from Scripts.Race.plot_position_changes import position_changes
from Scripts.tokenFolder.token_checker import verify_token
from Scripts.tokenFolder.token_checker import delete_token
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['https://www.t1f1.com'])

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/generate_plot', methods=['POST'])
def generate_plot():
    try:
        data = request.json
        logging.info(f"Received request: {data}")

        # Extract parameters
        plot_type = data.get("plot_type")
        year = data.get("year")
        round_number = data.get("round")
        event_type = data.get("eventType")
        driver1 = data.get("driver1", "")
        driver2 = data.get("driver2", "")
        team1 = data.get("team1", "")
        team2 = data.get("team2", "")
        token = data.get("token", "")

        # Validate required parameters
        if not all([plot_type, year, round_number, event_type]):
            logging.warning("Missing required parameters")
            return jsonify({"error": "Missing required parameters"}), 400

        # Validate Token
        if not verify_token(token):
            img_path = "lib/WRONG TOKEN.png"
            logging.warning("Wrong Token")
            #return jsonify({"error": "Wrong Token"})
            return send_file(img_path, mimetype='image/png')
        # Generate the plot based on plot_type
        if plot_type == 'Throttle comparison':
            img_path = ThrottleComp(int(year), int(round_number), event_type)
        elif plot_type == 'Qualifying Results':
            img_path = QualiResults(int(year), int(round_number), event_type)
        elif plot_type == 'TopSpeed':
            img_path = TopSpeedFunc(int(year), int(round_number), event_type)
        elif plot_type == 'Strategy':
            img_path = StrategyFunc(int(year), int(round_number), event_type)
        elif plot_type == 'DriversTrackComparison':
            img_path = TrackCompFunc(int(year), int(round_number), event_type, driver1, driver2, team1, team2)
        elif plot_type == 'Speed Trace(2 drivers)':
            img_path = SpeedTraceFunc(int(year), int(round_number), event_type, driver1, driver2, team1, team2)
        elif plot_type == 'TeamPace':
            img_path = TeamPaceRankingFunc(int(year), int(round_number), event_type)
        elif plot_type == 'DriversLaptimesDistribution':
            img_path = LaptimesDistributionFunc(int(year), int(round_number), event_type)
        elif plot_type == 'OneDriverLaptimes':
            img_path = DriverLaptimesFunc(int(year), int(round_number), event_type, driver1)
        elif plot_type == 'ThrottleGraph':
            img_path = throttle_graph(int(year), int(round_number), event_type, driver1, driver2)
        elif plot_type == 'PositionChanges':
            img_path = position_changes(int(year), int(round_number), event_type)
        elif plot_type == 'SpeedTraces':
            img_path = SpeedTraceFunc(int(year), int(round_number), event_type, driver1, driver2, team1, team2)
        else:
            logging.warning("Invalid plot type")
            return jsonify({"error": "Invalid plot type"}), 400

        # Check if the file exists
        if not os.path.exists(img_path):
            logging.error(f"File not found: {img_path}")
            return jsonify({"error": "File not generated or missing (Token remains valid)"}), 500

        # Return the image file
        logging.info(f"Successfully generated plot: {img_path}")
        delete_token(token)
        return send_file(img_path, mimetype='image/png')

    except Exception as e:
        logging.exception("Error generating plot")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# TopSpeed
# ThrottleGraph
# Strategy
# DriversTrackComparison
# TeamPace
#  PositionChanges
# OneDriverLaptimes
# DriversLaptimesDistribution
#  SpeedTraces