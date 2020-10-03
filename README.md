
Octogon Panel
=============

super early stuff

![Preview Screenshot](preview.png)

## what is this?

this is an all-purpose streaming tool for esports tournaments.
while this was made for SSBM specifically, the codebase is being modeled such that supporting other games later is possible.

this program currently features:

- various smash.gg overlays
- a scoreboard overlay
- a scoreboard control GUI

curious about how some of this stuff works? i've made some writeups on the wiki [here](https://github.com/branden-akana/octogon-panel/wiki/Interfaces).

## running

requires Python 3.

the smash.gg overlays require a smash.gg API key in order to retrieve information. this key should be saved to a file named `dev-key.txt`.

```cmd
pip install -r requirements.txt
python src/main.py
```

serves to localhost at port 8000.

## usage

this program runs a server that serves HTML when connecting to certain paths. intended for use with the "browser source" source in OBS.

current source URLs:
```bash
# scoreboard source (to be used with the background source)
localhost:8000/scoreboard
localhost:8000/background

# smash.gg sources
localhost:8000/standings
localhost:8000/countdown
localhost:8000/bracket
```

## customization

### custom backgrounds

backgrounds can be added into the `assets/bgs/` folder. at this time, only `assets/bgs/1.png` is loaded.

### custom html/stylesheet

HTML templates are located in `templates/`, which are rendered using Jinja2 when serving overlays.
SCSS files are used for styling, and can be found in `style/`. These files are rendered automatically when they are modified.
