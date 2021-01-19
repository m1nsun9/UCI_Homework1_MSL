// All Earthquakes from Past 7 days
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson";

d3.json(url, function(response) {
    createFeatures(response.features);

    // use SVG to create earthquake depth legend's linear gradient color scale
    var svg = d3.select(".legend")
                    .append("svg")
                    .attr("height", 10);

    var defs = svg.append("defs");
    
    var linearGradient = defs.append("linearGradient")
            .attr("id", "linear-gradient")
            .attr("x1", "0%")
            .attr("y1", "0%")
            .attr("x2", "100%")
            .attr("y2", "0%");

    //Set the color for the start (0%)
    linearGradient.append("stop")
            .attr("offset", "0%")
            .attr("stop-color", "rgb(182, 242, 76)");

    linearGradient.append("stop")
            .attr("offset", "50%")
            .attr("stop-color", "rgb(230, 53, 128)");
    
    //Set the color for the end (100%)      
    linearGradient.append("stop")
            .attr("offset", "100%")
            .attr("stop-color", "rgb(255, 0, 255)");

    svg.append("rect")
            .attr("width", 300)
            .attr("height", 10)
            .style("fill", "url(#linear-gradient)");
});

// function to create all features on map
// call createMap in this function
function createFeatures(data) {
    // create onEachFeature function that creates circle for each datapoint
    function onEachFeature(feature, layer) {
        layer.bindPopup(`<strong>Location: ${feature.properties.place}<strong> 
        <br> Depth: ${feature.geometry.coordinates[2]}
        <br> Magnitude: ${feature.properties.mag}`)
    };

    var depths = [];
    data.forEach((feature) => {
        depths.push(feature.geometry.coordinates[2]);
    });

    var colorScale = d3.scaleLinear()
            .domain([Math.min(... depths), 90])
            .range(["rgb(182, 242, 76)", "rgb(237, 106, 106)"]);

    // create circle with colors dependent on earthquake depth
    function createCircle(feature) {

        return L.circle([feature.geometry.coordinates[1], feature.geometry.coordinates[0]], {
            // change color to depend on depth (third coordinate)
            stroke: false,
            fillOpacity: 0.5,
            color: colorScale(feature.geometry.coordinates[2]),
            radius: feature.properties.mag * 20000
        })
    };

    // earthquakes layer that creates circles and popup for each earthquake
    var earthquakes = L.geoJSON(data, {
        pointToLayer: createCircle,
        onEachFeature: onEachFeature
    });

    createMap(earthquakes);
};

function createMap(earthquakes) {

    var streetmap = L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
        tileSize: 512,
        maxZoom: 18,
        zoomOffset: -1,
        id: "mapbox/streets-v11",
        accessToken: API_KEY
    });
        
    var darkmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "dark-v10",
        accessToken: API_KEY
    });

    var baseMaps = {
        "Street Map": streetmap,
        "Dark Map": darkmap
    };

    var overlayMaps = {
        "Earthquakes": earthquakes
    };

    var myMap = L.map("mapid", {
        center: [39.8283, -98.5795],
        zoom: 5,
        layers: [darkmap, earthquakes]
    });

    L.control.layers(baseMaps, overlayMaps, {
        collapsed: false
    }).addTo(myMap);

    // create a legend on bottom right corner for colors of earthquake depths
    var legend = L.control({position: "bottomright"});

    // create legend and add to innerHTML
    legend.onAdd = function() {
        var div = L.DomUtil.create("div", "info legend");
        var limits = [-10, 500];

        var legendInfo = "<h3>Earthquake Depth</h3>" +
            "<div class=\"labels\">" +
                "<div class=\"min\">" + limits[0] + "</div>" +
                "<div class=\"max\">" + `${limits[limits.length - 1]}+` + "</div>" +
            "</div>";

        div.innerHTML = legendInfo;
        return div;
    };

    // add legend to map
    legend.addTo(myMap);
};