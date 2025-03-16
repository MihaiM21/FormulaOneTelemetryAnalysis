
import fastf1
from fastf1 import plotting
import pandas as pd
import matplotlib.pyplot as plt
import fastf1.plotting
import dirOrg
from ..teamColorPicker import team_colors, teams
def TopSpeedFunc(y, r, e):
    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    fastf1.Cache.enable_cache('./cache')
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
    # for tms in teams:
    #     teamcolor = fastf1.plotting.team_color(tms)
    #     list_colors.append(teamcolor)


    list_colors = [team_colors[tms] for tms in teams if tms in team_colors]


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
    # 400 is the best for now, check for 380
    ax.set_ylim(290, 390)
    plt.yticks(range(290, 391, 10))


    x = 0
    for tms in teams:

        ax.text(tms, list_top_speed[x] + 1, str(list_top_speed[x]) + 'km/h', verticalalignment='bottom',
                horizontalalignment='center', color='white', fontsize = 16, fontweight = "bold")
        x += 1




    plt.suptitle('Top speed comparison\n' + str(y) + " " + session.event['EventName'] + ' ' + session.name)

    dirOrg.checkForFolder(str(y) + "/" + session.event['EventName'])
    location = "plots/" + str(y) + "/" + session.event['EventName']
    name = 'Top speed comparison ' + str(y) + " " + session.event['EventName'] + ' ' + session.name + " .png"
    plt.savefig(location + "/" + name)

    return location + "/" + name
