// Constants
// =========

// how often should the scoreboard update?
const update_interval = 2000;

// path to the json containing scoreboard data
const sb_path = "/output/sb_data.json";

// stores the last read scoreboard data, used to check for changes
var sb_data = null;

/**
 * Shortcut method to getting an element by ID in the HTML.
 */
function get_elm(id) {
	return document.getElementById(id);
}

function get_portrait_path(character) {
	if (character === "") {
		return `/assets/portraits/Random CPU.png`;
	}
	return `/assets/portraits/${character}/Default.png`;
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
		sb_data = this.json;
	}

	/**
	 * Return true if this key is different between this data
	 * and the last saved data.
	 *
	 * @param {string} key a period seperated list of json keys
	 * @param {function} callback a callback function
	 */
	on_modified(key, callback) {
		var keys = key.split(".");

		// check if saved data is null
		if (sb_data === null) {
			var curr_obj = this.json;
			keys.forEach((key) => (curr_obj = curr_obj[key]));
			callback(curr_obj);
			return;
		}

		// find element in current data and saved data
		var curr_obj = this.json;
		var last_obj = sb_data;

		keys.forEach((key) => {
			curr_obj = curr_obj[key];
			last_obj = last_obj[key];
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
async function fetch_sb_data() {
	var res = await fetch(sb_path);
	var json = await res.json();
	return new ScoreboardData(json);
}

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
 * Updates the scoreboard.
 */
async function sb_update() {
	console.log("fetching data...");
	data = await fetch_sb_data();

	// WIN COUNT

	data.on_modified("round_games", (games) => {
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

		sb_update_wins(0, data.json["p1"]["wins"]);
		sb_update_wins(0, data.json["p2"]["wins"]);
	});

	// WIN COUNTER

	data.on_modified("p1.wins", (wins) => {
		sb_update_wins(0, wins);
	});

	data.on_modified("p2.wins", (wins) => {
		sb_update_wins(1, wins);
	});

	// PLAYER NAME

	data.on_modified("p1.name", (name) => {
		console.log("updating p1 name");
		get_elm("p1_name").textContent = name;
	});

	data.on_modified("p2.name", (name) => {
		console.log("updating p2 name");
		get_elm("p2_name").textContent = name;
	});

	// PLAYER CHARACTER PORTRAIT

	data.on_modified("p1.character", (character) => {
		var path = get_portrait_path(character);
		get_elm("p1_portrait").style.backgroundImage = `url("${path}")`;
	});

	data.on_modified("p2.character", (character) => {
		var path = get_portrait_path(character);
		get_elm("p2_portrait").style.backgroundImage = `url("${path}")`;
	});

	data.on_modified("round_title", (title) => {
		get_elm("sb_roundtitle").textContent = title;
	});

	data.on_modified("round_games", (games) => {
		get_elm("sb_roundtype").textContent = `Best of ${games}`;
	});

	data.update_cache();
}

// the main function

window.onload = () => {
	setInterval(() => sb_update(), 1000);
};
