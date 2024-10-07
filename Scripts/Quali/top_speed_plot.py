
import fastf1
from fastf1 import plotting
import pandas as pd
import matplotlib.pyplot as plt
import fastf1.plotting
import dirOrg

def TopSpeedFunc(y, r, e):
    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    fastf1.Cache.enable_cache('cache')
    roundnr = r
    event = e
    year = y

    session = fastf1.get_session(year, roundnr, event)
    session.load()

    teams = pd.unique(session.laps['Team'])
    session.laps.pick_driver('VER').pick_fastest().get_car_data()

    list_top_speed = list()
    string_top_speed = list()
    for tms in teams:
        telemetry = session.laps.pick_team(tms).pick_fastest().get_car_data()
        speed = max(telemetry['Speed'])
        list_top_speed.append(speed)
        string_top_speed.append(str(speed))


    list_colors = list()
    for tms in teams:
        teamcolor = fastf1.plotting.team_color(tms)
        list_colors.append(teamcolor)

    list_top_speed, teams, list_colors = (list(t) for t in zip(*sorted(zip(list_top_speed, teams, list_colors))))


    string_top_speed.sort()
    list_top_speed.reverse()
    teams.reverse()
    list_colors.reverse()
    string_top_speed.reverse()
    print(list_top_speed)
    print(teams)

    fig, ax = plt.subplots(figsize=(13, 13), layout='constrained')
    ax.bar(teams, list_top_speed, color=list_colors)

    # Set Y-axis limits and ticks
    ax.set_ylim(0, 400)  # Optional, ensures Y-axis goes from 0 to 350
    plt.yticks(range(0, 401, 50))  # Set Y-axis ticks from 0 to 350 in increments of 50


    x = 0
    for tms in teams:
        telemetry2 = session.laps.pick_team(tms).pick_fastest().get_car_data()
        speed2 = max(telemetry['Speed'])

        ax.text(tms, list_top_speed[x] + 1, str(list_top_speed[x]) + 'km/h', verticalalignment='bottom',
                horizontalalignment='center', color='white', fontsize = 16, fontweight = "bold")
        x += 1


    plt.suptitle(f"Top speed comparison {session.event['EventName']} {session.event.year}")

    dirOrg.checkForFolder(session.event['EventName'])
    plt.savefig("plots/" + session.event['EventName'] + "/" + "Top speed comparison " + session.name + '.png')

    return "plots/" + session.event['EventName'] + "/" + "Top speed comparison " + session.name + '.png'
