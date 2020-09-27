
Octogon Panel
=============

super early stuff

![Preview Screenshot](preview.png)

## features

###

- 
### displays

- smash.gg bracket: shows all upcoming matches
- standings: shows the top 10 players in a tournament
- countdown: shows a countdown timer to the start of a tournament
- scoreboard: shows a scoreboard overlay used for tournament matches (in 4:3)




## running

requires Python 3.

some displays require a smash.gg API key to be saved to a file named `dev-key.txt`
to be able to query the smash.gg API for event and tournament information.

```cmd
pip install -r requirements.txt
python main.py
```

serves to localhost at port 8000.

## usage

intended for use with the "browser source" source in OBS:
- connect to `localhost:8000` for a matchmaking display
- connect to `localhost:8000/countdown` for a countdown display
- connect to `localhost:8000/bracket` for a bracket display
- connect to `localhost:8000/scoreboard` for a scoreboard display

## customization

### custom layout/stylesheet

HTML templates are located in `templates/` and the SCSS files used are located in `style/`.

### custom 
