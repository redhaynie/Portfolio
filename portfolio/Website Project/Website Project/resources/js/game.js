var messages = [
	"Good job!",
	"Bopped that one!",
	"Impressive!",
	"Great work!",
	"Fantastic!",
	"Incredible!",
	"lol gottem",
	"You have most certainly bopped that.",
	"Hot dog!",
	"Great work, sport!",
	"Whomst'd've hath did this?",
	"WhO iS ThIS gUy?",
	"You're rougher than the rest of 'em",
	"That key just got BOPPED!",
	"That was bopped successfully."
];
var score = 0;
var name = "";
var bops = 0;
var startTime = new Date();
var currentKey = "a";
var pressedKey = "";
var interval = 2000;
var running = false;
var keys = ['a', 's', 'd', 'f'];
var si;
var audio;
var ready = true;
var stage = 0;
var latency = .33; // seconds of audio delay, Nate W's bluetooth earbuds are at .34, when submitting final work maybe set to .1

$(document).ready(function() {
	$("#restart").hide();
	$("#score").hide();
	$("#speed").hide();
	$("#letter").hide();
	audio = document.getElementById("audio");
	audio.load();

	$("#latency").click(function() {
		var input = parseFloat(prompt("Enter the amount of audio latency. The more delayed your audio sounds, the higher this should be.", latency));
		if (input >= 0 && input <= 1) {
			latency = input;
			alert("audio latency has been set to " + String(latency) + " seconds");
		}
		else alert("Whoops, that wasn't a decimal between 0 and 1.");
	});

	$("#play").click(function() {
		$("#latency").hide();
		$("#play").hide();
		$("#leave").hide();
		changeText("Ready...", "");
		audio.play();
		setTimeout(function(){si = setInterval(updateKey, 2000);}, 1000*latency + 2000);
	});

	$("#restart").click(function() {location.reload();});
});


function changeText(output, highlight) {
	$("#output").text(output);
	if (highlight == "") {
		$("#highlight").hide();
	} else {
		$("#highlight").show();
		$("#highlight").text(highlight);
	}
}

function endGame(message) {
	clearInterval(si);
	running = false;
	if (message == "Great Job!") {
		$("body").css("background-color", "#f8f8f8");
		$("#highlight").css("color", "hsl(30, 100%, 43%)");
		$("#highlight").css("border", "2px solid hsl(30, 100%, 50%)");
		$("#highlight").css("background-color", "hsla(30, 100%, 50%, 15%)");
		changeText(message, "YOU WIN!");
		$("#speed").html('<a href="https://qph.fs.quoracdn.net/main-raw-161075514-idrkoylvendsmeupjgsozbluzstiskbk.jpeg" target="_blank">Click here to claim your prize!</a>');
		$("#speed").show();
	} else {
		audio.pause();
		changeText(message, "Game Over");
	}
	$("#score").text("score: " + String(score) + "  (" + String(bops) + " bops, " + String(Math.floor(score/bops/10)) + "% accuracy)");
	setInterval(function(){$("#score").show();}, 10);
	$("#restart").show();
	$("#leave").show();
	setTimeout(function(){
		name = prompt("Enter your name to save your score!!!");
		console.log(String(score) + name);
		var data = {};
		data.name = name;
		data.score = score;
		$.ajax({
			type: "POST",
			data: JSON.stringify(data),
			contentType: 'application/json',
			url: '/game/add',
			success: function(data) {
				console.log("success");
			}
		});
	}, 300);

}

function updateKey() {
	if (updateTempo()); // updateTempo returns true if player wins the game
	else if (!ready) {
		endGame("Too slow!");
	} else {
		startTime = new Date();
		currentKey = keys[Math.floor(Math.random() * keys.length)];
		changeText("Press", currentKey);
		running = true;
		ready = false;
	}
}

function changeTempo(newSpeed) {
	$("#score").text("score: " + String(score) + "  (" + String(bops) + " bops, " + String(Math.floor(score/bops/10)) + "% accuracy)");
	$("#score").show();
	$("#speed").show();
	setTimeout(function(){$("#speed").hide(3000);}, 1000);
	setTimeout(function(){$("#score").hide(750);}, 6000);
	clearInterval(si);
	si = setInterval(updateKey, newSpeed);
	interval = newSpeed;

	stage++;
	switch (stage) {
		case 1:
			keys.push('j','k','l',';');
			$("#letter").show();
			setTimeout(function(){$("#letter").hide(3000);}, 1000);
			break;
		case 2:
			$("#highlight").css("--highlight-hue", "210");
			break;
		case 3:
			break;
		case 4:
			keys.push('q','w','e','r','u','i','o','p');
			$("#letter").show();
			setTimeout(function(){$("#letter").hide(3000);}, 1000);

			$("#highlight").css("--highlight-hue", "0");
			$("body").css("background-color", "black");
			$("#output").hide();
			break;
		case 5:
			$("body").css("background-color", "#ffff77");
			$("#output").show();
			$("#highlight").css("color", "black");
			$("#highlight").css("border", "3px solid black");
			$("#highlight").css("background-color", "hsla(0, 0%, 0%, 8%)");
			break;
		case 6:
			keys.push('t','y','g','h','z','x','c','v','b','n','m');
			$("#letter").show();
			setTimeout(function(){$("#letter").hide(3000);}, 1000);
			break;
	}
}

function updateTempo() {
	switch (stage) {
		case 0: // start of song
			if (bops == 24) changeTempo(1600);
			break;
		case 1: // first speedup
			if (bops == 48) changeTempo(1500);
			break;
		case 2: // mellow/emotional
			if (bops == 80) changeTempo(1250);
			break;
		case 3: // mellow/emotional pt 2
			if (bops == 112) changeTempo(1200);
			break;
		case 4: // hellfire (black)
			if (bops == 144) changeTempo(1000);
			break;
		case 5: // pop (yellow)
			if (bops == 184) changeTempo(882); // 882 isn't exact but the drift is negligible
			break;
		case 6: // pop pt 2 (rainbow)
			$("body").css("background-color", "hsl("+String(Math.floor(Math.random() * 360))+", 100%, 60%)");
			if (bops == 246) {
				endGame("Great Job!");
				return true;
			}
	}
	//keys = ['f']; // COMMENT THIS OUT UNLESS YOU'RE TESTING SHIT
	return false;
}

function keyDownHandler(e) {
	pressedKey = e.key;
	if(running) {
		running = false;
		var now = new Date();
		var ms = (now.getSeconds() * 1000 + now.getMilliseconds()) - (startTime.getSeconds() * 1000 + startTime.getMilliseconds());
		if(pressedKey == currentKey) {
			score += 1000-(Math.abs(ms-interval/2))%1000;
			bops += 1;
			changeText(messages[Math.floor(Math.random() * messages.length)], "");
			ready = true;
		} else {
			endGame("Wrong Key!");
		}
	}
}

function keyUpHandler(e) {
	pressedKey = '';
}

document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);
