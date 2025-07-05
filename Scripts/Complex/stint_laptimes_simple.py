import fastf1
import fastf1.plotting
from matplotlib import pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np
import dirOrg
import matplotlib.image as mpimg
from matplotlib.patches import Patch
import matplotlib.colors as mcolors

def _init(y, r, e, session):
    dirOrg.checkForFolder(str(y) + "/" + session.event['EventName'] + "/" + e)
    location = "plots/" + str(y) + "/" + session.event['EventName'] + "/" + e
    name = 'Simple Stint Laptimes ' + str(y) + " " + session.event['EventName'] + ' ' + session.name + " .png"
    return location, name

def generate_shades(base_color, n_shades):
    """Genereaza n nuanțe din culoarea de bază prin ajustarea luminozității."""
    base_rgb = np.array(mcolors.to_rgb(base_color))
    shades = []

    for i in range(n_shades):
        factor = 1 - (i / max(n_shades - 1, 1)) * 0.5  # variaza între 1.0 și 0.5
        shaded_rgb = np.clip(base_rgb * factor, 0, 1)
        shades.append(mcolors.to_hex(shaded_rgb))

    return shades

def stint_laptimes_simple(y, r, e):
    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    fastf1.Cache.enable_cache('./cache')

    # Load session
    session = fastf1.get_session(y, r, e)
    session.load()

    # Verifica dacă plotul exista deja
    location, name = _init(y, r, e, session)
    path = dirOrg.checkForFile(location, name)
    if path != "NULL":
        return path

    # Lista cu piloti
    drivers = ['HAM', 'LEC', 'VER', 'NOR', 'PIA', 'RUS', 'ANT', 'TSU']
    compound_base = fastf1.plotting.COMPOUND_COLORS

    # Determina stinturile per compus
    compound_stints = {'SOFT': set(), 'MEDIUM': set(), 'HARD': set()}
    for drv in drivers:
        laps = session.laps.pick_driver(drv)
        for _, lap in laps.iterrows():
            if pd.notna(lap['Stint']) and pd.notna(lap['Compound']):
                compound_stints[lap['Compound'].upper()].add(int(lap['Stint']))

    # Genereaza nuanțe per compus
    compound_color_map = {}
    for compound in ['SOFT', 'MEDIUM', 'HARD']:
        stints_sorted = sorted(compound_stints[compound])
        shades = generate_shades(compound_base[compound], len(stints_sorted))
        compound_color_map[compound] = {
            stint: shade for stint, shade in zip(stints_sorted, shades)
        }

    # Setup plot
    fig, ax = plt.subplots(figsize=(20, 10))
    xticks, xticklabels = [], []

    for i, drv in enumerate(drivers):
        driver_laps = session.laps.pick_driver(drv)
        driver_laps = driver_laps[driver_laps['LapTime'].notna()]
        x_base = i

        for _, lap in driver_laps.iterrows():
            lap_time = lap['LapTime'].total_seconds()
            stint_number = int(lap['Stint']) if not pd.isna(lap['Stint']) else None
            compound = lap['Compound'].upper() if isinstance(lap['Compound'], str) else None

            if stint_number is None or compound not in compound_color_map:
                continue

            color = compound_color_map[compound].get(stint_number, '#888888')
            x_jittered = x_base + np.random.uniform(-0.2, 0.2)

            ax.scatter(
                x_jittered, lap_time,
                color=color,
                s=200,
                edgecolors='black',
                linewidths=0.5,
                zorder=3
            )

        xticks.append(x_base)
        xticklabels.append(drv)

    # Formatter axa Y
    def format_time(x, _):
        m = int(x // 60)
        s = x % 60
        return f"{m}:{s:05.2f}"

    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_time))
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, fontsize=10)
    ax.set_ylabel("Lap Time [s]")
    ax.set_xlabel("Driver")
    ax.set_title("Laptimes for Multiple Drivers by Stint and Compound", fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()

    # Legend
    # legend_patches = []
    # for compound, stint_colors in compound_color_map.items():
    #     for stint_num, color in stint_colors.items():
    #         label = f"{compound.title()} - Stint {stint_num}"
    #         patch = Patch(facecolor=color, edgecolor='black', label=label)
    #         legend_patches.append(patch)
    #
    # ax.legend(handles=legend_patches, loc='upper right', fontsize=8, title="Stint Colors", ncol=1)

    # Watermark
    logo = mpimg.imread('lib/logo mic.png')
    fig.figimage(logo, 975, 425, zorder=3, alpha=.6)

    # Salvare imagine
    plt.savefig(location + "/" + name)
    return location + "/" + name
