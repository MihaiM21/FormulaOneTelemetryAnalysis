import matplotlib.pyplot as plt
import pandas as pd
from timple.timedelta import strftimedelta
import matplotlib.image as mpimg
import fastf1
import fastf1.plotting
from fastf1.core import Laps
from ..teamColorPicker import get_team_color
import dirOrg


def QualiResults(y,r,e):

    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)

    session = fastf1.get_session(y, r, e)
    fastf1.Cache.enable_cache('./cache')
    session.load()


    drivers = pd.unique(session.laps['Driver'])
    print(drivers)



    list_fastest_laps = list()
    for drv in drivers:
        drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
        list_fastest_laps.append(drvs_fastest_lap)
    fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)


    pole_lap = fastest_laps.pick_fastest()
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']


    print(fastest_laps[['Driver', 'LapTime', 'LapTimeDelta']])


    team_colors = list()
    for index, lap in fastest_laps.iterlaps():
        # Removed FF1 color and using ours
        # color = fastf1.plotting.team_color(lap['Team'])
        color = get_team_color(lap['Team'])
        team_colors.append(color)



    fig, ax = plt.subplots(figsize=(13, 13))
    ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'],
        color=team_colors, edgecolor='grey')
    ax.set_yticks(fastest_laps.index)
    ax.set_yticklabels(fastest_laps['Driver'])
    max_value = fastest_laps['LapTimeDelta'].max()
    ax.set_xlim(0, max_value * 1.15)


    # Adding time gaps on the plot
    fastest_lap_time = fastest_laps['LapTime'].min()
    for i, lap in fastest_laps.iterrows():
        lap_time = strftimedelta(lap['LapTime'], '%S.%ms')
        pole_time = strftimedelta(fastest_lap_time, '%S.%ms')
        pole_time_full = strftimedelta(fastest_lap_time, '%m:%s.%ms')
        time_difference = abs(round(float(pole_time) - float(lap_time), 3))
        if i==0:
            ax.text(lap['LapTimeDelta'], i, f" {pole_time_full}s", va='center', fontsize=13, weight='bold')
        else:
            ax.text(lap['LapTimeDelta'], i, f" +{time_difference}s", va='center', fontsize=13, weight='bold')



    # show fastest at the top
    ax.invert_yaxis()

    # draw vertical lines behind the bars
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)
    # sphinx_gallery_defer_figures



    lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')

    plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\n"
             f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")

    # Adding Watermark
    logo = mpimg.imread('lib/logo mic.png')
    fig.figimage(logo, 575, 575, zorder=3, alpha=.6)

    dirOrg.checkForFolder(str(y) + "/" + session.event['EventName'])
    location = "plots/" + str(y) + "/" + session.event['EventName']
    name = str(y) + " " + session.event['EventName'] + ' Quali results.png'
    plt.savefig(location + "/" + name)
    return location + "/" + name

    #plt.show()

    #DONE FOR Serverside
    # working with program.py
