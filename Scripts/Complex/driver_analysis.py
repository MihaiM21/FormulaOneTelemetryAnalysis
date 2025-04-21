import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
from timple.timedelta import strftimedelta
import dirOrg
from matplotlib import font_manager
from ..teamColorPicker import get_driver_color, get_team_color

def _init(y, r, e, d, session):
    dirOrg.checkForFolder(str(y) + "/" + session.event['EventName'] + "/" + e)
    location = "plots/" + str(y) + "/" + session.event['EventName'] + "/" + e
    name = 'Driver Analysis ' + str(y) + " " + session.event['EventName'] + " " + str(d) + ' ' + session.name + ".png"
    return location, name
def get_sector_top_speeds(lap, driver_code):

    # Extrage datele de telemetrie
    telemetry = lap.get_car_data()

    # Convertim timpul telemetriei relativ la startul turului
    telemetry["RelativeTime"] = telemetry["Time"] - telemetry["Time"].min()

    # Obține punctele de sfârșit ale sectoarelor, convertite la același format
    s1_end = lap.Sector1SessionTime - lap.LapStartTime
    s2_end = lap.Sector2SessionTime - lap.LapStartTime
    s3_end = lap.Sector3SessionTime - lap.LapStartTime

    # Verificăm dacă avem valori valide pentru sectoare
    if pd.isna(s1_end) or pd.isna(s2_end) or pd.isna(s3_end):
        return None, None, None

    # Filtrare telemetrie pentru fiecare sector
    s1_data = telemetry[telemetry["RelativeTime"] <= s1_end]
    s2_data = telemetry[(telemetry["RelativeTime"] > s1_end) & (telemetry["RelativeTime"] <= s2_end)]
    s3_data = telemetry[(telemetry["RelativeTime"] > s2_end) & (telemetry["RelativeTime"] <= s3_end)]

    # Obține viteza maximă pe fiecare sector, verificând dacă setul de date e gol
    topSpeedS1 = s1_data["Speed"].max() if not s1_data.empty else None
    topSpeedS2 = s2_data["Speed"].max() if not s2_data.empty else None
    topSpeedS3 = s3_data["Speed"].max() if not s3_data.empty else None

    return topSpeedS1, topSpeedS2, topSpeedS3
def driver_analysis(y,r,e,d):
    # Activează cache-ul pentru FastF1
    fastf1.Cache.enable_cache('cache')

    # Încarcă datele unui Grand Prix (ex: Monza 2023, sesiunea de cursă)
    session = fastf1.get_session(y, r, e)
    session.load()

    # Verifică dacă folderul pentru ploturi există si daca exista si plotul deja generat
    location, name = _init(y,r,e,d,session)
    path = dirOrg.checkForFile(location, name)
    if(path != "NULL"):
        return path
    # Pana aici

    driver_code = d

    # Încarcă imaginea pilotului (modifică path-ul cu imaginea corectă)
    driver_img_path = f"lib/drivers/{driver_code}.png"


    ##############################################################################
    # First, we select the two laps that we want to compare

    driver1_lap = session.laps.pick_driver(d).pick_fastest()
    sector1 = strftimedelta(driver1_lap['Sector1Time'], '%S.%ms')
    sector2 = strftimedelta(driver1_lap['Sector2Time'], '%S.%ms')
    sector3 = strftimedelta(driver1_lap['Sector3Time'], '%S.%ms')
    lapTime = strftimedelta(driver1_lap['LapTime'], '%m:%s.%ms')

    telemetry = driver1_lap.get_car_data()
    topSpeedLap = max(telemetry['Speed'])
    topSpeedS1, topSpeedS2, topSpeedS3 = get_sector_top_speeds(driver1_lap, driver_code)

    # Track Distance
    trackLenght = driver1_lap.get_car_data().add_distance()
    total_distance = trackLenght['Distance'].iloc[-1]
    print(total_distance)

    ##############################################################################
    # Next we get the telemetry data for each lap. We also add a 'Distance' column
    # to the telemetry dataframe as this makes it easier to compare the laps.

    driver1_tel = driver1_lap.get_car_data().add_distance()

    ##############################################################################
    # Finally, we create a plot and plot both speed traces.
    # We color the individual lines with the driver's team colors.

    driver1_color = get_driver_color(d)

    # Creează figura și layout-ul cu GridSpec
    fig = plt.figure(figsize=(13, 13))

    font_path = 'lib/fonts/Formula1-Regular.ttf'  # Your font path goes here
    font_manager.fontManager.addfont(font_path)
    prop = font_manager.FontProperties(fname=font_path)

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = prop.get_name()

    gs = gridspec.GridSpec(2, 2)

    # Grafic viteza vs. distanță
    ax1 = plt.subplot(gs[1, :] )
    ax1.plot(driver1_tel['Distance'], driver1_tel['Speed'], color=driver1_color, label=d)
    ax1.set_xlabel("Distance (m)")
    ax1.set_ylabel("Speed (km/h)")

    #Sectors Distance
    S1_lenght = total_distance/3
    S2_lenght = total_distance/3 + total_distance/3


    ax1.axvline(S1_lenght, color="white", linestyle="--", label="S1 End")
    ax1.axvline(S2_lenght, color="white", linestyle="--", label="S2 End")
    ax1.text(1000, 350, "Sector 1", ha="center", va="center", fontsize=20, weight="bold")
    ax1.text(3000, 350, "Sector 2", ha="center", va="center", fontsize=20, weight="bold")
    ax1.text(5000, 350, "Sector 3", ha="center", va="center", fontsize=20, weight="bold")
    # ax1.set_title(f"{driver_code} Speed vs Distance")

    # Delimitare sectoare
    # s1_end = distance.iloc[-1] / 3
    # s2_end = 2 * (distance.iloc[-1] / 3)
    # ax1.axvline(s1_end, color="black", linestyle="--", label="S1 End")
    # ax1.axvline(s2_end, color="black", linestyle="--", label="S2 End")
    # ax1.legend()
    #
    # Imaginea șoferului
    ax2 = plt.subplot(gs[0, 1])
    img = mpimg.imread(driver_img_path)
    ax2.imshow(img)
    ax2.axis("off")

    # Timpi pe sectoare
    ax3 = plt.subplot(gs[0, 0])
    ax3.axis("off")
    ax3.text(0.56, 0.65, f"Sector Times", fontsize=50, ha="center", weight="bold")

    ax3.text(0.2, 0.5, f"S1: {sector1}s", fontsize=22, ha="center")
    ax3.text(0.2, 0.4, f"S2: {sector2}s", fontsize=22, ha="center")
    ax3.text(0.2, 0.3, f"S3: {sector3}s", fontsize=22, ha="center")

    ax3.text(0.9, 0.5, f"Top Speed: {topSpeedS1} km/h", fontsize=22, ha="center")
    ax3.text(0.9, 0.4, f"Top Speed: {topSpeedS2} km/h", fontsize=22, ha="center")
    ax3.text(0.9, 0.3, f"Top Speed: {topSpeedS3} km/h", fontsize=22, ha="center")

    ax3.text(0.56,0.2,f"Fastest lap: {lapTime}s", fontsize=22, ha="center")
    ax3.text(0.56, 0.1, f"Top speed: {topSpeedLap} km/h", fontsize=22, ha="center")




    # Adding Watermark
    logo = mpimg.imread('lib/logo mic.png')
    fig.figimage(logo, 575, 575, zorder=3, alpha=.6)


    plt.suptitle('Driver Analysis\n' + str(y) + " " + session.event['EventName'] + ' ' + session.name)

    plt.tight_layout(pad = 2)
    #plt.show()


    plt.savefig(location + "/" + name)

    return location + "/" + name
