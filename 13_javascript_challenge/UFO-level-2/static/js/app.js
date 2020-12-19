// from data.js
var tableData = data;

// assign table body where table rows will go to a variable
var tableBody = d3.select("tbody");

// assign variable to form for event listener "submit"
var form = d3.select(".form-group");

// for each data entry object in data list
data.forEach((sighting) => {
    // create a table row in the html table
    var row = tableBody.append("tr");
    // for each item in object
    Object.entries(sighting).forEach(([key, value]) => {
        // append data cell to row and change text 
        var cell = row.append("td");
        cell.text(value);
    })
});

// use date form and listen for events that will search through the 
// datetime column and find matching events

// assign variable to filter table button
var filterButton = d3.select("#filter-btn");

// run filter and present only data that matches description
function runFilter() {

    // prevent page from refreshing
    d3.event.preventDefault();
    
    // assign input boxes to variables and get text value of inputs
    var inputFields = {
        datetimeInputField: d3.select("#datetime"),
        cityInputField: d3.select("#city"),
        stateInputField: d3.select("#state"),
        countryInputField: d3.select("#country"),
        shapeInputField: d3.select("#shape")
    };

    var inputValues = {
        datetime: inputFields.datetimeInputField.property("value"),
        city: inputFields.cityInputField.property("value"),
        state: inputFields.stateInputField.property("value"),
        country: inputFields.countryInputField.property("value"),
        shape: inputFields.shapeInputField.property("value")
    };

    var filterValues = {};

    // iterate through each filter value
    Object.entries(inputValues).forEach(([key, value]) => {
        if (value != "") {
            filterValues[key] = value.toLowerCase();
        };
    });

    // assign list of filtered data to new variable
    var filteredData = tableData.filter(function(sighting) {
        // for each sighting, if the filter values are a match, return
        var match = true;
        Object.entries(filterValues).forEach(([key, value]) => {
            if (sighting[key] != value) {
                match = false;
            };
        });
        
        if (match === true) {
            return sighting;
        };
    });

    // if the input is not empty, run filter
    if (Object.keys(filterValues).length > 0) {
        // remove all rows from before filter
        tableBody.selectAll("td").remove();

        // add the new filtered data
        filteredData.forEach((sighting) => {
            var row = tableBody.append("tr");

            Object.entries(sighting).forEach(([key, value]) => {
                // append data cell to row and change text
                var cell = row.append("td");
                cell.text(value);
            });
        });
    }
    // if filter is cleared, return all sightings
    else {
        // remove all rows from before filter
        tableBody.selectAll("td").remove();
        
        // for each data entry object in data list
        data.forEach((sighting) => {
            // create a table row in the html table
            var row = tableBody.append("tr");
            // for each item in object
            Object.entries(sighting).forEach(([key, value]) => {
                // append data cell to row and change text 
                var cell = row.append("td");
                cell.text(value);
            });
        });
    };
};

filterButton.on("click", runFilter);
form.on("change", runFilter);