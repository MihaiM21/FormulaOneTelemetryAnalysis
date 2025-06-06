import fastf1 as ff1
import fastf1
from fastf1 import plotting
import pandas as pd
import matplotlib.pyplot as plt
import fastf1.plotting
import matplotlib.image as mpimg
import dirOrg
from ..teamColorPicker import get_driver_color

def _init(y, r, e, session):
    dirOrg.checkForFolder(str(y) + "/" + session.event['EventName'] + "/" + e)
    location = "plots/" + str(y) + "/" + session.event['EventName'] + "/" + e
    name = str(y) + " " + session.event['EventName'] + " Throttle comparison.png"
    return location, name
def ThrottleComp(y,r,e):  

    fastf1.plotting.setup_mpl(misc_mpl_mods = False)
    ff1.Cache.enable_cache('./cache')

    roundnr = r
    event = e
    year = y


    #Loading session info
    session = fastf1.get_session(year, roundnr, event)
    session.load()

    # Verifică dacă folderul pentru ploturi există si daca exista si plotul deja generat
    location, name = _init(y, r, e, session)
    path = dirOrg.checkForFile(location, name)
    if (path != "NULL"):
        return path
    # Pana aici

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
        # Removed the FF1 driver color and using ours from now on.
        # drivercolor = fastf1.plotting.driver_color(drv)
        drivercolor = get_driver_color(drv)
        print(drivercolor)
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

    # Adding Watermark
    logo = mpimg.imread('lib/logo mic.png')
    fig.figimage(logo, 575, 575, zorder=3, alpha=.6)


    plt.savefig(location + "/" + name)

    return location + "/" + name



    # DONE FOR Serverside
    # working with program.py