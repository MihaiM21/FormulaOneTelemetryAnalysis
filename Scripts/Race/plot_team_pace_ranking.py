

import fastf1
import fastf1.plotting
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from ..teamColorPicker import get_team_color
import dirOrg
from ..teamColorPicker import team_colors, teams

fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False)

def _init(y, r, e, session):
    dirOrg.checkForFolder(str(y) + "/" + session.event['EventName'] + "/" + e)
    location = "plots/" + str(y) + "/" + session.event['EventName'] + "/" + e
    name = str(y) + " " + session.event['EventName'] + " Team pace.png"
    return location, name

def TeamPaceRankingFunc(y,r,e):


    year = y
    event = r
    tip = e



    session = fastf1.get_session(year, event, tip)
    fastf1.Cache.enable_cache('./cache')
    session.load()
    laps = session.laps.pick_quicklaps()

    # Verifică dacă folderul pentru ploturi există si daca exista si plotul deja generat
    location, name = _init(y, r, e, session)
    path = dirOrg.checkForFile(location, name)
    if (path != "NULL"):
        return path
    # Pana aici

    ###############################################################################
    # Convert the lap time column from timedelta to integer.
    # This is a seaborn-specific modification.
    # If plotting with matplotlib, set mpl_timedelta_support to true
    # with plotting.setup_mpl.
    transformed_laps = laps.copy()
    transformed_laps.loc[:, "LapTime (s)"] = laps["LapTime"].dt.total_seconds()

    # order the team from the fastest (lowest median lap time) tp slower
    team_order = (
        transformed_laps[["Team", "LapTime (s)"]]
        .groupby("Team")
        .median()["LapTime (s)"]
        .sort_values()
        .index
    )
    print(team_order)

    # make a color palette associating team names to hex codes
    team_palette = {team: get_team_color(team) for team in team_order}



    #   ##############################################################################
    fig, ax = plt.subplots(figsize=(13, 13))
    sns.boxplot(
        data=transformed_laps,
        x="Team",
        y="LapTime (s)",
        order=team_order,
        palette=team_palette,
        whiskerprops=dict(color="white"),
        boxprops=dict(edgecolor="white"),
        medianprops=dict(color="grey"),
        capprops=dict(color="white"),
    )

    #plt.title("2023 US Grand Prix")
    plt.grid(visible=False)

    # x-label is redundant
    ax.set(xlabel=None)
    plt.tight_layout()
    plt.suptitle('Team pace\n' + str(y) + " " + session.event['EventName'] + ' ' + session.name)

    # Adding the Watermark
    logo = mpimg.imread('lib/logo mic.png')
    fig.figimage(logo, 575, 575, zorder=3, alpha=.6)


    plt.savefig(location + "/" + name)

    return location + "/" + name
