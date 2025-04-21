import fastf1
import fastf1.plotting
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import dirOrg

def _init(y, r, e, session):
    dirOrg.checkForFolder(str(y) + "/" + session.event['EventName'] + "/" + e)
    location = "plots/" + str(y) + "/" + session.event['EventName'] + "/" + e
    name = str(y) + " " + session.event['EventName'] + " Tyre strategy.png"
    return location, name

def StrategyFunc(y,r,e):

    session = fastf1.get_session(y, r, e)
    fastf1.Cache.enable_cache('./cache')
    session.load()
    laps = session.laps

    # Verifică dacă folderul pentru ploturi există si daca exista si plotul deja generat
    location, name = _init(y, r, e, session)
    path = dirOrg.checkForFile(location, name)
    if (path != "NULL"):
        return path
    # Pana aici

    drivers = session.drivers
    print(drivers)


    drivers = [session.get_driver(driver)["Abbreviation"] for driver in drivers]
    print(drivers)


    stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
    stints = stints.groupby(["Driver", "Stint", "Compound"])
    stints = stints.count().reset_index()


    stints = stints.rename(columns={"LapNumber": "StintLength"})
    print(stints)


    fig, ax = plt.subplots(figsize=(13, 13))

    for driver in drivers:
        driver_stints = stints.loc[stints["Driver"] == driver]

        previous_stint_end = 0
        for idx, row in driver_stints.iterrows():
            # each row contains the compound name and stint length
            # we can use these information to draw horizontal bars
            plt.barh(
                y=driver,
                width=row["StintLength"],
                left=previous_stint_end,
                color=fastf1.plotting.COMPOUND_COLORS[row["Compound"]],
                edgecolor="black",
                fill=True
            )

            previous_stint_end += row["StintLength"]

    # sphinx_gallery_defer_figures

    ###############################################################################
    # Make the plot more readable and intuitive
    # plt.title("Strategy")
    plt.xlabel("Lap Number")
    plt.grid(False)
    # invert the y-axis so drivers that finish higher are closer to the top
    ax.invert_yaxis()

    # sphinx_gallery_defer_figures

    ###############################################################################
    # Plot aesthetics
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tight_layout()
    #plt.show()

    plt.suptitle('Tyre strategy\n' + str(y) + " " + session.event['EventName'] + ' ' + session.name)

    # Adding the Watermark
    logo = mpimg.imread('lib/logo mic.png')
    fig.figimage(logo, 575, 575, zorder=3, alpha=.6)


    plt.savefig(location + "/" + name)

    return location + "/" + name
