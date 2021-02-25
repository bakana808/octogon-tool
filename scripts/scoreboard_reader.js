/**
 * Handles automatic updating of scoreboard elements.
 */

// Constants
// =============================================================================

// how often should the scoreboard update?
const update_interval = 1000;

// path to the json containing scoreboard data
const sb_path = "scoreboard.json";

// =============================================================================

// stores the last read scoreboard data, used to check for changes
var scoreboard_cache = null;


function http_post(url, data, mimetype = "application/json") {

	if(typeof(data) === "object") { data = JSON.stringify(data); }

	var xhr = new XMLHttpRequest();
	xhr.open("POST", url, true);
	xhr.setRequestHeader('Content-Type', mimetype);
	xhr.send(data);
}

function http_get(url) {
	return new Promise(resolve => {
		var xhr = new XMLHttpRequest();
		xhr.onreadystatechange = function() {
			if (this.readyState != 4) return;
			if (this.status == 200) {
				var data = JSON.parse(this.responseText);
				resolve(data);
			}
		};
		xhr.open("GET", url, true);
		xhr.send();
	});
}

/**
 * POSTs a message to Octogon to print a message to the console.
 *
 * @param {string} msg the message to print
 */
function print(msg) {
	http_post("http://localhost:8000/debug", { message: "JS: " + msg });
}

async function fetch_scoreboard() {
	return await http_get("http://localhost:8000/scoreboard/data");
}

/**
 * Shortcut method to getting an element by ID in the HTML.
 *
 * @param {string} id ID of the element
 */
function get_elm(id) {
	return document.getElementById(id);
}

/**
 * Gets the path to a character portrait from its name.
 *
 * @param {string} character the name of the character
 * @return {string} the path to the character's portrait
 */
function get_portrait_path(character, color = "") {
	if (character === "") {
		return `/assets/portraits/Random CPU.png`;
	}
	if (color === "") {
		return `/assets/portraits/${character}/Default.png`;
	} else {
		return `/assets/portraits/${character}/${color}.png`;
	}
}

class ScoreboardData {
	constructor(json) {
		/** @type {object} */
		this.json = json;

		console.log(this.json);
	}

	/**
	 * Update the cached data with this one.
	 */
	update_cache() {
		scoreboard_cache = this.json;
	}

	/**
	 * Calls the callback function if the value at this key is
	 * different than the value in the cached data.
	 *
	 * @param {string} key a period seperated list of json keys
	 * @param {function} callback a callback function
	 */
	if_modified(key, callback) {
		var keys = key.split(".");

		// find target value in current data and saved data
		var curr_obj = this.json;
		var last_obj = scoreboard_cache;

		keys.forEach((key) => {
			curr_obj = curr_obj[key];
			if(last_obj !== null) { last_obj = last_obj[key]; }
		});

		// then compare the two objects
		if (curr_obj !== last_obj) {
			callback(curr_obj);
		}
	}
}

/**
 * Reads the JSON file containing the scoreboard data
 * and parses it as an object.
 *
 * The callback function will be called with the
 * object as the first paramater.
 *
 * TODO: check if the file doesn't exist
 *
 * @return {Promise<ScoreboardData>} a promise that resolves with the object
 */
//async function fetch_scoreboard() {
//    var res = await fetch(sb_path);
//    var json = await res.json();
//    return new ScoreboardData(json);
//}

/**
 * Updates the win count for the given player.
 *
 * 0: Player 1
 * 1: Player 2
 */
async function sb_update_wins(player, wins) {
	var id;
	if (player === 0) {
		id = "p1_wincounter";
	} else {
		id = "p2_wincounter";
	}

	var elm = get_elm(id);
	var children = elm.childNodes;

	// reverse order of filled icons for P1 side
	// TODO: change into setting
	if (player === 0) {
		children = Array.from(children).reverse();
	}

	children.forEach((child) => {
		if (wins > 0) child.classList.add("sb_winicon_filled");
		else child.classList.remove("sb_winicon_filled");
		wins--;
	});
}

/**
 * Checks if there is a change in the scoreboard data.
 */
async function check_scoreboard_changes() {

	data = await fetch_scoreboard();
	//print(JSON.stringify(data));
	if (scoreboard_cache !== null && data.is_modified === false) { return; }

	scoreboard = new ScoreboardData(data.scoreboard);
	//print("detected change in scoreboard");

	// WIN COUNT

	scoreboard.if_modified("round_games", (games) => {
		var num_icons = 2;
		if (games == 5) {
			num_icons = 3;
		}

		var p1_wincounter = get_elm("p1_wincounter");
		// clear all child nodes
		while (p1_wincounter.firstChild) {
			p1_wincounter.removeChild(p1_wincounter.lastChild);
		}

		for (var i = 0; i < num_icons; i++) {
			var win_elm = document.createElement("div");
			win_elm.id = "p1_w" + i;
			win_elm.className = "sb_winicon";
			win_elm.appendChild(document.createElement("span"));
			p1_wincounter.appendChild(win_elm);
		}

		var p2_wincounter = get_elm("p2_wincounter");
		while (p2_wincounter.firstChild) {
			p2_wincounter.removeChild(p2_wincounter.lastChild);
		}

		for (var i = 0; i < num_icons; i++) {
			var win_elm = document.createElement("div");
			win_elm.id = "p2_w" + i;
			win_elm.className = "sb_winicon";
			win_elm.appendChild(document.createElement("span"));
			p2_wincounter.appendChild(win_elm);
		}

		sb_update_wins(0, scoreboard.json["p1"]["wins"]);
		sb_update_wins(1, scoreboard.json["p2"]["wins"]);
	});

	// WIN COUNTER

	scoreboard.if_modified("p1.wins", (wins) => {
		sb_update_wins(0, wins);
	});

	scoreboard.if_modified("p2.wins", (wins) => {
		sb_update_wins(1, wins);
	});

	// PLAYER NAME

	scoreboard.if_modified("p1.name", (name) => {
		//console.log("updating p1 name");
		get_elm("p1_name").textContent = name;
	});

	scoreboard.if_modified("p2.name", (name) => {
		//console.log("updating p2 name");
		get_elm("p2_name").textContent = name;
	});

	// PLAYER CHARACTER PORTRAIT
	
	function update_portrait(player) {
		if (player == 0) {
			var id = "p1_portrait";
			var character = scoreboard.json["p1"]["character"];
			var color = scoreboard.json["p1"]["color"];
		} else {
			var id = "p2_portrait";
			var character = scoreboard.json["p2"]["character"];
			var color = scoreboard.json["p2"]["color"];
		}

		var path = get_portrait_path(character, color);
		//print(`portrait path => ${ path }`);
		get_elm(id).style.backgroundImage = `url("${path}")`;
	}

	scoreboard.if_modified("p1.character", (_) => { update_portrait(0) });
	scoreboard.if_modified("p1.character", (_) => { update_portrait(0) });
	scoreboard.if_modified("p1.color", (_) => { update_portrait(0) });
	scoreboard.if_modified("p2.color", (_) => { update_portrait(1) });

	// PLAYER CONTROLLER PORT
	
	scoreboard.if_modified("p1.port", (port) => {
		elm = get_elm("p1_name")
		elm.classList.remove("port_0", "port_1", "port_2", "port_3");
		elm.classList.add(`port_${port}`);
	});

	scoreboard.if_modified("p2.port", (port) => {
		elm = get_elm("p2_name")
		elm.classList.remove("port_0", "port_1", "port_2", "port_3");
		elm.classList.add(`port_${port}`);
	});

	// ROUND TITLE

	scoreboard.if_modified("round_title", (title) => {
		get_elm("sb_roundtitle").textContent = title;
	});

	// ROUND NUM OF GAMES

	scoreboard.if_modified("round_games", (games) => {
		get_elm("sb_roundtype").textContent = `Best of ${games}`;
	});

	scoreboard.update_cache();
}

// the main function

window.onload = () => {
	setInterval(() => check_scoreboard_changes(), update_interval);
};
