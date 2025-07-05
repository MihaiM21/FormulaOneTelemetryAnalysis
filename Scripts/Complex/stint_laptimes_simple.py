import fastf1
import fastf1.plotting
from matplotlib import pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np
import dirOrg
import matplotlib.image as mpimg
def _init(y, r, e, session):
    dirOrg.checkForFolder(str(y) + "/" + session.event['EventName'] + "/" + e)
    location = "plots/" + str(y) + "/" + session.event['EventName'] + "/" + e
    name = 'Simple Stint Laptimes ' + str(y) + " " + session.event['EventName'] + ' ' + session.name + " .png"
    return location, name


def stint_laptimes_simple(y, r, e):

    # Setup
    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    #plt.style.use('dark_background')
    fastf1.Cache.enable_cache('./cache')

    # Load session
    year = y
    race = r
    session = fastf1.get_session(year, race, e)
    session.load()

    # Verifică dacă folderul pentru ploturi există si daca exista si plotul deja generat
    location, name = _init(y, r, e, session)
    path = dirOrg.checkForFile(location, name)
    if (path != "NULL"):
        return path
    # Pana aici

    # Lista cu piloți
    drivers = ['HAM', 'LEC', 'VER', 'NOR', 'PIA', 'RUS', 'ANT', 'TSU']
    compound_colors = fastf1.plotting.COMPOUND_COLORS

    # Setup plot
    fig, ax = plt.subplots(figsize=(20, 10))

    xticks = []
    xticklabels = []

    for i, drv in enumerate(drivers):
        driver_laps = session.laps.pick_driver(drv)
        driver_laps = driver_laps[driver_laps['LapTime'].notna()]
        x_base = i

        for idx, lap in driver_laps.iterrows():
            lap_time = lap['LapTime'].total_seconds()
            stint_number = int(lap['Stint']) if not pd.isna(lap['Stint']) else '?'
            compound = lap['Compound']
            color = compound_colors.get(compound, 'gray')

            # Offset aleatoriu pentru spațiere vizuală
            x_jittered = x_base + np.random.uniform(-0.2, 0.2)

            # Bulina
            ax.scatter(
                x_jittered, lap_time,
                color=color,
                s=200,
                edgecolors='black',
                linewidths=0.5,
                zorder=3
            )

            # Text cu numărul stintului
            ax.text(
                x_jittered, lap_time,
                str(stint_number),
                color='black',
                fontsize=9,
                ha='center',
                va='center',
                zorder=4
            )

        xticks.append(x_base)
        xticklabels.append(drv)

    # Formatter axa Y
    def format_time(x, _):
        m = int(x // 60)
        s = x % 60
        return f"{m}:{s:05.2f}"

    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_time))
    # ax.invert_yaxis()
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, fontsize=10)
    ax.set_ylabel("Lap Time [s]")
    ax.set_xlabel("Driver")
    ax.set_title("Laptimes for Multiple Drivers by Stint and Compound", fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()

    # Adding Watermark
    logo = mpimg.imread('lib/logo mic.png')
    fig.figimage(logo, 575, 575, zorder=3, alpha=.6)

    plt.savefig(location + "/" + name)

    return location + "/" + name

    plt.show()

stint_laptimes_simple(2025, 12 ,"FP1")


