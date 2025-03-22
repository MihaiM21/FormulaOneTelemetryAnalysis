"""Driver Laptimes Scatterplot
==============================

Plot a driver's lap times in a race, with color coding for the compounds.
"""

import fastf1
import fastf1.plotting
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import dirOrg

def DriverLaptimesFunc(y,r,e,d):


    # The misc_mpl_mods option enables minor grid lines which clutter the plot
    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    fastf1.Cache.enable_cache('./cache')

    # Load the race session.

    session = fastf1.get_session(y, r, e)
    session.load()

    # Get all the laps for a single driver.
    # Filter out slow laps as they distort the graph axis.

    driver_laps = session.laps.pick_driver(d).pick_quicklaps().reset_index()

    # Make the scattterplot using lap number as x-axis and lap time as y-axis.
    # Marker colors correspond to the compounds used.
    # Note: as LapTime is represented by timedelta, calling setup_mpl earlier
    # is required.

    fig, ax = plt.subplots(figsize=(13, 13))

    sns.scatterplot(data=driver_laps,
                    x="LapNumber",
                    y="LapTime",
                    ax=ax,
                    hue="Compound",
                    palette=fastf1.plotting.COMPOUND_COLORS,
                    s=80,
                    linewidth=0,
                    legend='auto')
    # sphinx_gallery_defer_figures

    # Make the plot more aesthetic.
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")

    # The y-axis increases from bottom to top by default
    # Since we are plotting time, it makes sense to invert the axis
    ax.invert_yaxis()
    plt.suptitle(d+"Laptimes")

    # Turn on major grid lines
    plt.grid(color='w', which='major', axis='both')
    sns.despine(left=True, bottom=True)

    plt.suptitle(d + ' Laptimes\n' + session.event['EventName'] + ' ' + session.name)

    # Adding Watermark
    logo = mpimg.imread('lib/logo mic.png')
    fig.figimage(logo, 575, 575, zorder=3, alpha=.6)

    dirOrg.checkForFolder(str(y) + "/" + session.event['EventName'])
    location = "plots/" + str(y) + "/" + session.event['EventName']
    name = str(y) + " " + session.event['EventName'] + " " + d + " Laptimes.png"
    plt.savefig(location + "/" + name)

    return location + "/" + name

    #DONE
