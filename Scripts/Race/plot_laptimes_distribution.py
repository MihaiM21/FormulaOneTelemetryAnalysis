"""Driver Laptimes Distribution Visualization
=============================================
Visualizae different drivers' laptime distributions.
"""

import fastf1
import fastf1.plotting
import seaborn as sns
from matplotlib import pyplot as plt
import dirOrg

def LaptimesDistributionFunc(y,r,e):


    # enabling misc_mpl_mods will turn on minor grid lines that clutters the plot
    fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False)

    ################################################################################ Load the race session

    session = fastf1.get_session(y, r, e)
    fastf1.Cache.enable_cache('./cache')
    session.load()

    ###############################################################################
    # Get all the laps for the point finishers only.
    # Filter out slow laps (yellow flag, VSC, pitstops etc.)
    # as they distort the graph axis.
    point_finishers = session.drivers[:10]
    print(point_finishers)
    driver_laps = session.laps.pick_drivers(point_finishers).pick_quicklaps()
    driver_laps = driver_laps.reset_index()

    ###############################################################################
    # To plot the drivers by finishing order,
    # we need to get their three-letter abbreviations in the finishing order.
    finishing_order = [session.get_driver(i)["Abbreviation"] for i in point_finishers]
    print(finishing_order)

    ###############################################################################
    # We need to modify the DRIVER_COLORS palette.
    # Its keys are the driver's full names but we need the keys to be the drivers'
    # three-letter abbreviations.
    # We can do this with the DRIVER_TRANSLATE mapping.
    driver_colors = {abv: fastf1.plotting.DRIVER_COLORS[driver] for abv,
                    driver in fastf1.plotting.DRIVER_TRANSLATE.items()}
    print(driver_colors)

    ###############################################################################
    # First create the violin plots to show the distributions.
    # Then use the swarm plot to show the actual laptimes.

    # create the figure
    fig, ax = plt.subplots(figsize=(10, 10))

    # Seaborn doesn't have proper timedelta support
    # so we have to convert timedelta to float (in seconds)
    driver_laps["LapTime(s)"] = driver_laps["LapTime"].dt.total_seconds()

    sns.violinplot(data=driver_laps,
                    x="Driver",
                    y="LapTime(s)",
                    inner=None,
                    scale="area",
                    order=finishing_order,
                    palette=driver_colors
                    )

    sns.swarmplot(data=driver_laps,
                  x="Driver",
                  y="LapTime(s)",
                  order=finishing_order,
                  hue="Compound",
                  palette=fastf1.plotting.COMPOUND_COLORS,
                  hue_order=["SOFT", "MEDIUM", "HARD"],
                  linewidth=0,
                  size=5,
                  )
    # sphinx_gallery_defer_figures

    ###############################################################################
    # Make the plot more aesthetic
    ax.set_xlabel("Driver")
    ax.set_ylabel("Lap Time (s)")
    plt.suptitle("Lap Time Distributions")
    sns.despine(left=True, bottom=True)

    plt.suptitle('Laptimes distribution\n' + str(y) + " " + session.event['EventName'] + ' ' + session.name)

    dirOrg.checkForFolder(str(y) + "/" + session.event['EventName'])
    location = "plots/" + str(y) + "/" + session.event['EventName']
    name = str(y) + " " + session.event['EventName'] + " Laptimes distribution.png"
    plt.savefig(location + "/" + name)

    return location + "/" + name

    #plt.tight_layout()
    #plt.show()

    #DONE
