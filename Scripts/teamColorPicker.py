teams = [
    "Alpine", "Aston Martin", "Ferrari", "Haas", "Kick Sauber",
    "McLaren", "Mercedes", "Racing Bulls", "Red Bull Racing", "Williams"
]

team_colors = {
    "Alpine": "#0093CC",
    "Aston Martin": "#229971",
    "Ferrari": "#E80020",
    "Haas": "#B6BABD",
    "Kick Sauber": "#52E252",
    "McLaren": "#FF8000",
    "Mercedes": "#27F4D2",
    "Racing Bulls": "#6692FF",
    "Red Bull Racing": "#3671C6",
    "Williams": "#64C4FF",
}

def get_team_color(team):

    team_aliases = {
        "Alpine": ["alpine", "alp"],
        "Aston Martin": ["aston martin", "am", "aston"],
        "Ferrari": ["ferrari", "fer"],
        "Haas": ["haas", "has"],
        "Kick Sauber": ["kick sauber", "sauber", "kick"],
        "McLaren": ["mclaren", "mcl"],
        "Mercedes": ["mercedes", "merc"],
        "Racing Bulls": ["racing bulls", "rb", "racingbulls", "visa cash app rb", "vcarb"],
        "Red Bull Racing": ["red bull racing", "redbull", "rbr"],
        "Williams": ["williams", "wil"]
    }

    team_colors = {
        "Alpine": "#0093CC",
        "Aston Martin": "#229971",
        "Ferrari": "#E80020",
        "Haas": "#B6BABD",
        "Kick Sauber": "#52E252",
        "McLaren": "#FF8000",
        "Mercedes": "#27F4D2",
        "Racing Bulls": "#6692FF",
        "Red Bull Racing": "#3671C6",
        "Williams": "#64C4FF",
    }

    team = team.lower().strip()  # Normalizează numele echipei (ignora case sensitivity și spațiile)

    for official_name, aliases in team_aliases.items():
        if team in aliases:
            return team_colors[official_name]

    return "#FFFFFF"  # Default: alb dacă echipa nu este găsită