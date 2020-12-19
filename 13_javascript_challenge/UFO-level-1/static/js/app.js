// from data.js
var tableData = data;

// assign table body where table rows will go to a variable
var tableBody = d3.select("tbody");

// assign variable to form for event listener "submit"
var form = d3.select("form");

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
    var dateInputField = d3.select("#datetime");
    var dateInputValue = dateInputField.property("value");

    // assign list of filtered data to new variable
    var filteredData = tableData.filter(sighting => sighting.datetime === dateInputValue);

    // if the input is not empty, run filter
    if (dateInputValue.length > 0) {
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
form.on("submit", runFilter);