import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import fastf1 as ff1
import fastf1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.collections import LineCollection
from matplotlib import cm
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import dirOrg

def throttle_graph(y,r,e,d1,d2):
    # Setup plotting
    plotting.setup_mpl()
    # Enable the cache
    # ff1.Cache.enable_cache('cache')


    driver1 = d1
    driver2 = d2
    year = y
    round = r
    event = e

    # Load the session data
    session = ff1.get_session(year, round, event)

    # Collect all race laps
    session.load()
    laps = session.laps

    # Getting laps from the drivers
    laps_driver1 = laps.pick_driver(driver1)
    laps_driver2 = laps.pick_driver(driver2)

    # Extract the fastest laps
    fastest_driver1 = laps_driver1.pick_fastest()
    fastest_driver2 = laps_driver2.pick_fastest()

    # Get telemetry from fastest laps
    telemetry_driver1 = fastest_driver1.get_car_data().add_distance()
    telemetry_driver2 = fastest_driver2.get_car_data().add_distance()

    # 4 subplots in the same image
    fig, ax = plt.subplots(3)
    fig.suptitle("Fastest Lap Telemetry Comparison")

    # Plot for Speed and Distance (axis)
    ax[0].plot(telemetry_driver1['Distance'], telemetry_driver1['Speed'], label=driver1)
    ax[0].plot(telemetry_driver2['Distance'], telemetry_driver2['Speed'], label=driver2)
    ax[0].set(ylabel='Speed')
    ax[0].legend(loc="lower right")

    ax[1].plot(telemetry_driver1['Distance'], telemetry_driver1['Throttle'], label=driver1)
    ax[1].plot(telemetry_driver2['Distance'], telemetry_driver2['Throttle'], label=driver2)
    ax[1].set(ylabel='Throttle')

    ax[2].plot(telemetry_driver1['Distance'], telemetry_driver1['Brake'], label=driver1)
    ax[2].plot(telemetry_driver2['Distance'], telemetry_driver2['Brake'], label=driver2)
    ax[2].set(ylabel='Brakes')

    # NO NEED
    #ax[3].plot(telemetry_driver1['Distance'], telemetry_driver1['Brake'], label=driver1)
    #ax[3].plot(telemetry_driver1['Distance'], telemetry_driver1['Throttle'], label=driver1)
    #ax[3].set(ylabel='Comparison')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for a in ax.flat:
        a.label_outer()


    plt.suptitle('Throttle graph\n' + str(y) + " " + session.event['EventName'] + ' ' + session.name)

    dirOrg.checkForFolder(str(y) + "/" + session.event['EventName'])
    location = "plots/" + str(y) + "/" + session.event['EventName']
    name = str(y) + " " + session.event['EventName'] + "Throttle graph.png"
    plt.savefig(location + "/" + name)

    return location + "/" + name