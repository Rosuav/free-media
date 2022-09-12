import choc, {set_content, DOM, on} from "https://rosuav.github.io/choc/factory.js";
const {A, AUDIO, BR, DIV, FIGCAPTION, FIGURE, H2, P, SECTION, VIDEO} = choc; //autoimport
const FREEMEDIA_ROOT = "https://rosuav.github.io/free-media/"; //Canonical home
//const FREEMEDIA_ROOT = "http://localhost:8000/"; //Browse local files before uploading
//const FREEMEDIA_ROOT = "/"; //Whatever place this page came from

function THUMB(file, noautoplay) {
	if (file.mimetype.startsWith("audio/")) return DIV({class: "thumbnail"}, AUDIO({src: file.url, controls: true}));
	if (file.mimetype.startsWith("video/")) {
		const elem = VIDEO({class: "thumbnail", src: file.url, loop: true, ".muted": true});
		if (file.previewtime) elem.currentTime = file.previewtime;
		return elem;
	}
	return DIV({class: "thumbnail", style: "background-image: url(" + file.url + ")"});
}

async function populate_freemedia() {
	const data = await (await fetch(FREEMEDIA_ROOT + "filelist.json")).json();
	console.log("Got free media", data);
	set_content("#freemedialibrary", data.files.map(file => SECTION([
		FIGURE([
			THUMB(file, true),
			FIGCAPTION([
				A({href: file.url, target: "_blank"}, file.filename),
				BR(),
			]),
		]),
		file.description.split("\n").map(para => P({class: "descr"}, para)),
		file.creator && P({class: "descr"}, [
			"Created by ",
			file.creator, " ",
			file.creatorlink && A({href: file.creatorlink, target: "_blank"}, file.creatorlink),
			BR(),
			"License: ", file.license, //TODO: Link?
		]),
	])));
}
populate_freemedia();

on("pointerover", "video", e => e.match.play());
on("pointerout", "video", e => {
	//For dev use, show the timestamp when you moused out. This will allow selection
	//of a previewtime for both this display and StilleBot's library selector.
	console.log("Out", e.match.src, e.match.currentTime);
	e.match.pause();
});
