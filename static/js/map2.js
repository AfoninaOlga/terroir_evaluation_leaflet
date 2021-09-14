var color_expanded = false;
var clicked_id = 1;
var is_white, is_red, is_pink, is_black = false;

const checkbox = document.getElementsByName('color')
var i;
for (i = 0; i<checkbox.length; i++) {
	checkbox[i].addEventListener('change', (event) => {
		if (event.target.checked) {
			if (event.target.id == 'white') {
				is_white = true;
				console.log(event.target.id, is_white);
				console.log(white_cantons)
			} else if (event.target.id == 'pink') {
				is_pink = true;
				console.log(event.target.id, is_pink);
			} else if (event.target.id == 'red') {
				is_red = true;
				console.log(event.target.id, is_red);
			} else if (event.target.id == 'black') {
				is_black = true;
				console.log(event.target.id, is_black);
			}
			geojson.setStyle(style);
		} else {
			if (event.target.id == 'white') {
				is_white = false;
				console.log(event.target.id, is_white);
			} else if (event.target.id == 'pink') {
				is_pink = false;
				console.log(event.target.id, is_pink);
			} else if (event.target.id == 'red') {
				is_red = false;
				console.log(event.target.id, is_red);
			} else if (event.target.id == 'black') {
				is_black = false;
				console.log(event.target.id, is_black);
			}
			geojson.setStyle(style);
		}
	});
}


function get_color(code) {
	let colour;
	if (code == clicked_id) {
		return 'red';
	}
	code = parseInt(code);
	console.log(code, white_cantons.includes(code));
	if ((is_white && white_cantons.includes(code)) || (is_pink && pink_cantons.includes(code))
		|| (is_red && red_cantons.includes(code)) || (is_black && black_cantons.includes(code))) {
		return 'darkred';
	}
	return 'white';
}


function showCheckboxes() {
  var checkboxes = document.getElementById("checkboxes");
  if (!color_expanded) {
    checkboxes.style.display = "block";
    color_expanded = true;
  } else {
    checkboxes.style.display = "none";
    color_expanded = false;
  }
}

function get_suitability(url) {
    var res = ""
    $.getJSON({
            url: url,
            async: false,
            success: function(data) {
                var items = [];
                $.each( data, function( key, val ) {
                    items.push( key + ": " + "<i>" + val + "</i>" + "<br>" );
                });
                res = items.join( "" )
            }
        });
    return res;
}

function get_grape(url) {
    var res = ""
    $.getJSON({
            url: url,
            async: false,
            success: function(data) {
                var items = [];
				items.push("Best grape varieties:<ul class='grapes'>")
                $.each( data, function( key, val ) {
                    items.push(`<li> ${val.name} (${val.berry_color}, ${val.disease_resistance.toLowerCase()}, ${val.origin})</li>`);
                });
				items.push("</ul>");
                res = items.join( "" );
            }
        });
    return res;
}

function get_canton_data(url) {
    var res = ""
    $.getJSON({
            url: url,
            async: false,
            success: function(data) {
                var items = [];
                $.each( data, function( key, val ) {
                    let  row = key + ": " + val + "<br>";
                    if (key == "name") {
                        row = "<b>" + val + "</b><br>";
                    }
                    items.push(row);
                });
                res = items.join( "" )
            }
        });
    return res;
}

var map = L.map('map', { zoomControl: false }).setView([48.091, -2.8], 8.75)

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoicXVvcXFhIiwiYSI6ImNrc3N6YTNuYTA3ZncydmxzMmE0azA5MnoifQ.I_BvYr1t2cnV2xqyWpkZrw', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		id: 'mapbox/dark-v10',
		tileSize: 512,
		zoomOffset: -1
	}).addTo(map);

L.control.zoom({
    position: 'bottomleft'
}).addTo(map);

var info = L.control();

info.onAdd = function (map) {
		this._div = L.DomUtil.create('div', 'info');
		this.update();
		return this._div;
};

info.smallUpdate = function (props) {
	let html = '<b>Canton name</b><br/> Hover over a canton';
	if (props) {
		code = props.code_canton;
		let url_canton = window.location.href + 'canton/' + code;
    	html = get_canton_data(url_canton) + 'Click for more information<br>';
	}

	this._div.innerHTML = '<h4>Bretagne canton data</h4>' +  html;
};

info.update = function (props) {
	let html = '<b>Canton name</b><br/> Hover over a canton';
	if (props) {
		code = props.code_canton;
		let url_canton = window.location.href + 'canton/' + code;
    	let url_suitability = window.location.href + 'suitability/' + code;
    	let url_grape = window.location.href + 'grape/' + code;
    	html = get_canton_data(url_canton) + get_grape(url_grape) + get_suitability(url_suitability);
	}
	this._div.innerHTML = '<h4>Bretagne canton data</h4>' +  html;
};

info.addTo(map);

function style(feature) {
	return {
		weight: 1,
		opacity: 1,
		color: 'white',
		dashArray: '',
		fillOpacity: 0.4,
		fillColor: get_color(feature.properties.code_canton)
	};
}

function highlightOnClick(e) {
	var layer = e.target;
	clicked_id = layer.feature.properties.code_canton;
	geojson.resetStyle();
	layer.setStyle({
		weight: 4,
       	color: 'darkred',
		fillColor: 'red',
       	dashArray: ''
	});

	if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
		layer.bringToFront();
	}
}

function resetHighlight(e)  {
    geojson.resetStyle(e.target);
}

function mouseOut(e) {
	var layer = e.target;

	layer.setStyle({
		weight: 1,
		fillOpacity: 0.4,
       	color: 'white',
       	dashArray: ''
	});

	if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
		layer.bringToFront();
	}
}

function highlightOnMouseOver(e) {
	var layer = e.target;

	layer.setStyle({
		weight: 4,
		fillOpacity: 0.6,
       	color: 'darkred',
       	dashArray: ''
	});

	if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
		layer.bringToFront();
	}
	info.smallUpdate(layer.feature.properties);
}


var geojson;

function zoomToFeature(e) {
	map.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
	let html = '<b>Canton name</b><br/> Hover over a canton';
	if (feature.properties) {
		code = feature.properties.code_canton;
		let url_canton = window.location.href + 'canton/' + code;
    	let url_suitability = window.location.href + 'suitability/' + code;
    	let url_grape = window.location.href + 'grape/' + code;
    	html = get_canton_data(url_canton) + get_grape(url_grape) + get_suitability(url_suitability);
	}
	layer.bindPopup(html);
	layer.on({
		mouseover: highlightOnMouseOver,
		mouseout: mouseOut,
		click: highlightOnClick
	});
}

$.getJSON("static/bretagne.json",function(data){
	geojson = L.geoJson(data, {
		style: style,
		onEachFeature: onEachFeature
	}).addTo(map);
});
