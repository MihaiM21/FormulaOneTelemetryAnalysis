
import fastf1 as ff1
from fastf1 import plotting
import matplotlib.pyplot as plt
import dirOrg
import matplotlib.image as mpimg

def throttle_graph(y,r,e,d1,d2):
    # Setup plotting
    plotting.setup_mpl()
    # Enable the cache


    driver1 = d1
    driver2 = d2
    year = y
    round = r
    event = e

    # Load the session data
    session = ff1.get_session(year, round, event)
    ff1.Cache.enable_cache('./cache')

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
    fig, ax = plt.subplots(3 ,figsize=(13, 13), clear = "True")
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

    # Obține datele de timp pentru cel mai rapid tur
    telemetry_driver1['LapTime(s)'] = (telemetry_driver1['Time'] - telemetry_driver1['Time'].iloc[0]).dt.total_seconds()
    telemetry_driver2['LapTime(s)'] = (telemetry_driver2['Time'] - telemetry_driver2['Time'].iloc[0]).dt.total_seconds()

    # Plot pentru timpul pe tur în funcție de distanță
    # ax[3].plot(telemetry_driver1['Distance'], telemetry_driver1['LapTime(s)'], label=driver1)
    # ax[3].plot(telemetry_driver2['Distance'], telemetry_driver2['LapTime(s)'], label=driver2)
    #
    # ax[3].set(ylabel='Lap Time (s)', xlabel='Distance (m)')
    # ax[3].legend(loc="lower right")

    # NO NEED
    #ax[3].plot(telemetry_driver1['Distance'], telemetry_driver1['Brake'], label=driver1)
    #ax[3].plot(telemetry_driver1['Distance'], telemetry_driver1['Throttle'], label=driver1)
    #ax[3].set(ylabel='Comparison')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for a in ax.flat:
        a.label_outer()

    # Adding Watermark
    logo = mpimg.imread('lib/logo mic.png')
    fig.figimage(logo, 575, 575, zorder=3, alpha=.6)

    plt.suptitle('Throttle graph\n' + str(y) + " " + session.event['EventName'] + ' ' + session.name)

    dirOrg.checkForFolder(str(y) + "/" + session.event['EventName'] + "/" + e)
    location = "plots/" + str(y) + "/" + session.event['EventName'] + "/" + e
    name = str(y) + " " + session.event['EventName'] + " " + driver1 + " vs " + driver2 + " Throttle graph.png"
    plt.savefig(location + "/" + name)

    plt.close()

    return location + "/" + name