import fastf1 as ff1
import fastf1
from fastf1 import plotting
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import matplotlib.patches as mpatches
import dirOrg
from ..teamColorPicker import get_team_color, get_driver_color


def print_sector_times(lap, driver_code):
    print(f"Sector times for {driver_code}:")
    lap_number = lap['LapNumber']
    sector1 = lap['Sector1Time']
    sector2 = lap['Sector2Time']
    sector3 = lap['Sector3Time']
    telemetry = lap.get_car_data()
    speed = max(telemetry['Speed'])
    print(f"Lap {lap_number}: Sector 1: {sector1}, Sector 2: {sector2}, Sector 3: {sector3}, Speed: {speed}")
    print("\n")

def _init(y, r, e, d1, d2, session):
    dirOrg.checkForFolder(str(y) + "/" + session.event['EventName'] + "/" + e)
    location = "plots/" + str(y) + "/" + session.event['EventName'] + "/" + e
    # name = str(year) + " " + session.event['EventName'] + " " +str(d1) + " vs " + str(d2) +".png"
    name = session.event['EventName'] + " " + str(session.name) + " " + str(session.event.year) + " " + str(
        d1) + " vs " + str(d2) + ".png"
    return location, name

def TrackCompFunc(y, r, e, d1, d2, t1, t2):
    # Enable the cache
    ff1.Cache.enable_cache('cache')

    # Setup plotting
    plotting.setup_mpl()


    # Data for the event
    year = y
    race = r
    event = e
    driver1 = d1
    team1 = t1
    team2 = t2
    driver2 = d2
    # Importing team colors
    # color_team1 = fastf1.plotting.team_color(team1)
    # color_team2 = fastf1.plotting.team_color(team2)
    color_team1 = get_driver_color(driver1)
    color_team2 = get_driver_color(driver2)
    # Load the session data
    session = ff1.get_session(year, race, event)
    fastf1.Cache.enable_cache('./cache')

    # Get the laps
    session.load()
    laps = session.laps

    # Verifică dacă folderul pentru ploturi există si daca exista si plotul deja generat
    location, name = _init(y, r, e,d1, d2, session)
    path = dirOrg.checkForFile(location, name)
    if (path != "NULL"):
        return path
    # Pana aici

    # Select the laps from drivers
    laps_driver1 = laps.pick_driver(driver1)
    laps_driver2 = laps.pick_driver(driver2)

    # Get the telemetry data from their fastest lap
    fastest_driver1 = laps_driver1.pick_fastest().get_telemetry().add_distance()
    fastest_driver2 = laps_driver2.pick_fastest().get_telemetry().add_distance()

    # Since the telemetry data does not have a variable that indicates the driver, 
    # we need to create that column
    fastest_driver1['Driver'] = driver1
    fastest_driver2['Driver'] = driver2

    # Merge both lap telemetries so we have everything in one DataFrame
    telemetry = fastest_driver1._append(fastest_driver2)

    # 25 mini-sectors (this can be adjusted)
    num_minisectors = 25

    # Grab the maximum value of distance that is known in the telemetry
    total_distance = total_distance = max(telemetry['Distance'])

    # Generate equally sized mini-sectors 
    minisector_length = total_distance / num_minisectors

    # Initiate minisector variable, with 0 (meters) as a starting point.
    minisectors = [0]

    # Add multiples of minisector_length to the minisectors
    for i in range(0, (num_minisectors - 1)):
        minisectors.append(minisector_length * (i + 1))

    telemetry['Minisector'] = telemetry['Distance'].apply(
        lambda dist: (
            int((dist // minisector_length) + 1)
        )
    )

    # Calculate avg. speed per driver per mini sector
    average_speed = telemetry.groupby(['Minisector', 'Driver'])['Speed'].mean().reset_index()

    # Select the driver with the highest average speed
    fastest_driver = average_speed.loc[average_speed.groupby(['Minisector'])['Speed'].idxmax()]

    # Get rid of the speed column and rename the driver column
    fastest_driver = fastest_driver[['Minisector', 'Driver']].rename(columns={'Driver': 'Fastest_driver'})

    # Join the fastest driver per minisector with the full telemetry
    telemetry = telemetry.merge(fastest_driver, on=['Minisector'])

    # Order the data by distance to make matploblib does not get confused
    telemetry = telemetry.sort_values(by=['Distance'])

    # Convert driver name to integer
    telemetry.loc[telemetry['Fastest_driver'] == driver1, 'Fastest_driver_int'] = 1
    telemetry.loc[telemetry['Fastest_driver'] == driver2, 'Fastest_driver_int'] = 2

    x = np.array(telemetry['X'].values)
    y = np.array(telemetry['Y'].values)

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    fastest_driver_array = telemetry['Fastest_driver_int'].to_numpy().astype(float)


    # cmap = cm.get_cmap('Paired', 2)
    cmap = ListedColormap([color_team1, color_team2])
    lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N + 1), cmap=cmap)
    lc_comp.set_array(fastest_driver_array)
    lc_comp.set_linewidth(5)

    # Setting the size of the image
    fig, ax = plt.subplots(figsize=(13, 13))
    #plt.rcParams['figure.figsize'] = [13, 13]


    plt.gca().add_collection(lc_comp)
    plt.axis('equal')
    plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

    # Removed because of errors
    # cbar = plt.colorbar(mappable=lc_comp, boundaries=np.arange(1, 4))
    # cbar.set_ticks(np.arange(1.5, 3.5))
    # cbar.set_ticklabels([driver1, driver2])

    # New legend model
    legend_patches = [mpatches.Patch(color=color_team1, label=driver1),
                      mpatches.Patch(color=color_team2, label=driver2)]

    plt.legend(handles=legend_patches, loc='upper right')


    plt.suptitle(str(d1) + " vs " + str(d2) + " " + str(year) + " " + session.event['EventName'] + ' ' + session.name)

    # Adding Watermark
    logo = mpimg.imread('lib/logo mic.png')
    plt.figimage(logo, 575, 575, zorder=3, alpha=.6)


    plt.savefig(location + "/" + name)
    plt.close()

    return location + "/" + name
# WORKING WITH PROGRAM and image view