"""Overlaying speed traces of two laps
=====================================
Compare two fastest laps by overlaying their speed traces.
"""


import matplotlib.pyplot as plt
import fastf1.plotting
import matplotlib.image as mpimg
import dirOrg
from ..teamColorPicker import get_driver_color, get_team_color


def SpeedTraceFunc(y,r,e,d1,d2,t1,t2):
    
    # enable some matplotlib patches for plotting timedelta values and load
    # FastF1's default color scheme
    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    fastf1.Cache.enable_cache('./cache')
    # load a session and its telemetry data
    session = fastf1.get_session(y, r, e)
    session.load()

    ##############################################################################
    # First, we select the two laps that we want to compare

    driver1_lap = session.laps.pick_driver(d1).pick_fastest()
    driver2_lap = session.laps.pick_driver(d2).pick_fastest()

    ##############################################################################
    # Next we get the telemetry data for each lap. We also add a 'Distance' column
    # to the telemetry dataframe as this makes it easier to compare the laps.

    driver1_tel = driver1_lap.get_car_data().add_distance()
    driver2_tel = driver2_lap.get_car_data().add_distance()

    ##############################################################################
    # Finally, we create a plot and plot both speed traces.
    # We color the individual lines with the driver's team colors.

    driver1_color = get_driver_color(d1)
    driver2_color = get_driver_color(d2)

    fig, ax = plt.subplots(figsize=(13, 13))
    ax.plot(driver1_tel['Distance'], driver1_tel['Speed'], color=driver1_color, label=d1)
    ax.plot(driver2_tel['Distance'], driver2_tel['Speed'], color=driver2_color, label=d2)

    ax.set_xlabel('Distance in m')
    ax.set_ylabel('Speed in km/h')

    ax.legend()

    # Adding Watermark
    logo = mpimg.imread('lib/logo mic.png')
    fig.figimage(logo, 575, 575, zorder=3, alpha=.6)

    plt.suptitle('Fastest Lap Comparison\n' + str(y) + " " + session.event['EventName'] + ' ' + session.name)

    dirOrg.checkForFolder(str(y) + "/" + session.event['EventName'])
    location = "plots/" + str(y) + "/" + session.event['EventName']
    name = str(y) + " " + session.event['EventName'] + " " + str(d1) + " vs " + str(d2) + " Fastest Lap Comparison.png"
    plt.savefig(location + "/" + name)

    return location + "/" + name
