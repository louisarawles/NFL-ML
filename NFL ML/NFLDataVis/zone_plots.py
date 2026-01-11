import numpy as np
from matplotlib import pyplot as plt


def show_zone_performance(game, passer):
    zones = passer.zones
    # make the field
    rows = 4
    yd_zones = ["20Plus", "10To19", "losTo9", "behindLOS",]
    cols = 3
    w_sects = ["leftThird", "middleThird", "rightThird"]
    cbar_kw = {
        "ticks":[0,1,2,3],
    }
    cbarlabel = 'QB Success Rating (Relative to Game Avg)'
    field = np.full((rows, cols),0.0,dtype=float)
    labels = np.full((rows,cols),"",dtype=object)
    for z in zones:
        yd = -1
        sect = -1
        lvl = 0
        qbRating = z.get('qbRating')
        yardzone = z.get('lineOfScrimmageDistance')
        match yardzone:
            case 'behindLOS':
                yd = 3
            case 'losTo9':
                yd = 2
            case '10To19':
                yd = 1
            case _:
                yd = 0

        section = z.get('section')
        match section:
            case 'leftThird':
                sect = 0
            case 'middleThird':
                sect = 1
            case _:
                sect = 2

        success = z.get('qbRatingSuccessLevel')
        match success:
            case 'ABOVE':
                lvl = 3
            case 'AVERAGE':
                lvl = 2
            case 'BELOW':
                lvl = 1
            case _:
                lvl = 0
        field[yd,sect] = lvl
        cell = f"{round(qbRating,2)}"
        labels[yd,sect] = cell
    # plot heat map
    fig, ax = plt.subplots()
    im = ax.imshow(field, cmap='summer_r')
    # create colorbar
    cbar = ax.figure.colorbar(im, ax=ax,**cbar_kw)
    cbar.set_ticklabels(["No Attempts", "BELOW", "AVERAGE", "ABOVE"])
    cbar.set_label(cbarlabel)

    ax.set_xticks(range(cols), labels=w_sects, rotation=45, ha='right', rotation_mode='anchor')
    ax.set_yticks(range(rows), labels=yd_zones)

    for i in range(rows):
        for j in range(cols):
            if labels[i,j] == "":
                labels[i,j] = "N/A"
            ax.text(j, i, labels[i, j],
                           ha='center', va='center', color='black')

    playerName = passer.playerName
    date = game.gameDate
    team = passer.teamAbbr
    comp = game.homeTeamAbbr
    if comp == team:
        comp = game.visitorTeamAbbr
    ax.set_title(f"v. {comp} {date} - {team} {playerName} QB Rating by Passing Zone")
    fig.tight_layout()
    plt.show()