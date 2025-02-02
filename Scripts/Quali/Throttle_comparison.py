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
import fastf1.plotting
from fastf1.core import Laps
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from timple.timedelta import strftimedelta
import sys
import dirOrg

def ThrottleComp(y,r,e):  

    fastf1.plotting.setup_mpl(misc_mpl_mods = False)
    ff1.Cache.enable_cache('./cache')

    #Information needed to be changed every race !!!

    roundnr = r
    event = e
    year = y


    #Loading session info
    session = fastf1.get_session(year, roundnr, event)
    session.load()

    drivers = pd.unique(session.laps['Driver'])

    teams = pd.unique(session.laps['Team'])

    list_telemetry = list()
    string_telemetry = list()
    for drv in drivers:
        telemetry = session.laps.pick_driver(drv).pick_fastest().get_car_data().add_distance()
        average = sum(telemetry['Throttle'])/len(telemetry['Throttle'])
        average = round(average, 2)
        string_telemetry.append(str(average))
        print(drv)
        print(average)
        list_telemetry.append(average)

    list_colors = list()
    for drv in drivers:
        drivercolor = fastf1.plotting.driver_color(drv)
        list_colors.append(drivercolor)


    list_telemetry, drivers, list_colors = (list(t) for t in zip(*sorted(zip(list_telemetry, drivers, list_colors))))
    string_telemetry.sort()
    list_telemetry.reverse()
    drivers.reverse()
    list_colors.reverse()
    string_telemetry.reverse()
    fig, ax = plt.subplots(figsize=(13, 13), layout='constrained')
    ax.bar(drivers, list_telemetry, color = list_colors)
    # ax.set(ylim=(0, 100), yticks=np.linspace(0, 100, 11))
    ax.set_ylim(50, 100)
    plt.yticks(range(50, 101, 5))

    x=0
    for drv in drivers:
        ax.text(drv, list_telemetry[x]+1, string_telemetry[x] + "%", horizontalalignment='center', color='white')
        x=x+1

    plt.suptitle('Throttle comparison\n' + str(y) + " " + session.event['EventName'] + ' ' + session.name)

    dirOrg.checkForFolder(str(y) + "/" + session.event['EventName'])
    location = "plots/" + str(y) + "/" + session.event['EventName']
    name = str(y) + " " + session.event['EventName'] + " Throttle comparison.png"
    plt.savefig(location + "/" + name)

    return location + "/" + name



    # DONE FOR Serverside
    # working with program.py