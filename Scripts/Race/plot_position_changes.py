"""
Position changes during a race
==============================

Plot the position of each driver at the end of each lap.
"""

import fastf1.plotting
import matplotlib.pyplot as plt
import dirOrg


def position_changes(y,r,e):

    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    fastf1.Cache.enable_cache('./cache')

    ##############################################################################
    # Load the session and create the plot
    session = fastf1.get_session(y, r, e)
    session.load(telemetry=False, weather=False)

    fig, ax = plt.subplots(figsize=(10.0, 10.0))
    # sphinx_gallery_defer_figures

    ##############################################################################
    # For each driver, get their three letter abbreviation (e.g. 'HAM') by simply
    # using the value of the first lap, get their color and then plot their
    # position over the number of laps.
    for drv in session.drivers:
        drv_laps = session.laps.pick_driver(drv)

        abb = drv_laps['Driver'].iloc[0]
        color = fastf1.plotting.driver_color(abb)

        ax.plot(drv_laps['LapNumber'], drv_laps['Position'],
                label=abb, color=color)
    # sphinx_gallery_defer_figures

    ##############################################################################
    # Finalize the plot by setting y-limits that invert the y-axis so that position
    # one is at the top, set custom tick positions and axis labels.
    ax.set_ylim([20.5, 0.5])
    ax.set_yticks([1, 5, 10, 15, 20])
    ax.set_xlabel('Lap')
    ax.set_ylabel('Position')
    # sphinx_gallery_defer_figures

    ##############################################################################
    # Because this plot is very crowed, add the legend outside the plot area.
    ax.legend(bbox_to_anchor=(1.0, 1.02))
    #plt.tight_layout()

    plt.suptitle('Position changes\n' + str(y) + " " + session.event['EventName'] + ' ' + session.name)

    dirOrg.checkForFolder(str(y) + "/" + session.event['EventName'])
    location = "plots/" + str(y) + "/" + session.event['EventName']
    name = str(y) + " " + session.event['EventName'] + " Position changes.png"
    plt.savefig(location + "/" + name)

    return location + "/" + name