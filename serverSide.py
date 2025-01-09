from flask import Flask, request, jsonify, send_file
import os
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

app = Flask(__name__)

@app.route('/generate_plot', methods=['POST'])
def generate_plot():
    data = request.json
    plot_type = data.get("plot_type")
    year = data.get("year")
    round_number = data.get("round")
    event_type = data.get("event")
    driver1 = data.get("driver1", "")
    driver2 = data.get("driver2", "")
    team1 = data.get("team1", "")
    team2 = data.get("team2", "")

    if not all([plot_type, year, round_number, event_type]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        # Apelează funcția corectă și obține adresa imaginii generate
        if plot_type == 'Throttle comparison':
            img_path = ThrottleComp(int(year), int(round_number), event_type)
        elif plot_type == 'Qualifying Results':
            img_path = QualiResults(int(year), int(round_number), event_type)
        elif plot_type == 'Top Speed':
            img_path = TopSpeedFunc(int(year), int(round_number), event_type)
        elif plot_type == 'Strategy':
            img_path = StrategyFunc(int(year), int(round_number), event_type)
        elif plot_type == '2 Drivers track comparison':
            img_path = TrackCompFunc(int(year), int(round_number), event_type, driver1, driver2, team1, team2)
        elif plot_type == 'Speed Trace(2 drivers)':
            img_path = SpeedTraceFunc(int(year), int(round_number), event_type, driver1, driver2, team1, team2)
        elif plot_type == 'Team Pace':
            img_path = TeamPaceRankingFunc(int(year), int(round_number), event_type)
        elif plot_type == 'Drivers laptimes distribution':
            img_path = LaptimesDistributionFunc(int(year), int(round_number), event_type)
        elif plot_type == 'Driver Laptimes':
            img_path = DriverLaptimesFunc(int(year), int(round_number), event_type, driver1)
        elif plot_type == 'Throttle Graphs':
            img_path = throttle_graph(int(year), int(round_number), event_type, driver1, driver2)
        else:
            return jsonify({"error": "Invalid plot type"}), 400

        # Verifică dacă fișierul există
        if not os.path.exists(img_path):
            return jsonify({"error": "File not generated or missing"}), 500

        # Returnează imaginea generată
        return send_file(img_path, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
