const url = "/api/v1.0/covid-all";

var selected_state = "";
var selected_county = "";
var dataset = [];



// Display wait message while JSON loads into the dropdown
function show_initial(ele) {

    // Show a message to the user
    var msg = document.getElementById('msg');
    var chart = document.getElementById('chart');
    msg.innerHTML = 'Please wait while the state menu loads...';

    d3.json(url).then((data) => {
        dataset = data;
        //console.log(dataset);

        // Pass the dataset to be used elsewhere
        states_dropdown(dataset);
    });
  
};

function states_dropdown(d){    
    
    // Build a list of unique states
    var u1 = {}, a1 = [];
    
    for(var i = 0, l = d.length; i < l; ++i){
        if(!u1.hasOwnProperty(d[i]['state'])) {
            a1.push(d[i]['state']);
            u1[d[i]['state']] = 1;
        }
    };
    
    // Sort the list alphabetically
    a1.sort();
    //console.log('State list loaded successfully.');

    // Populate the dropdown
    // Adapted from: https://www.encodedna.com/javascript/populate-select-dropdown-list-with-json-data-using-javascript.htm
    var ele = document.getElementById('sel_state');
    
    for (var i = 0; i < a1.length; i++) {
        ele.innerHTML = ele.innerHTML + '<option value="' + a1[i] + '">' + a1[i] + '</option>';
    };
    
    // Change the message to say dropdown is ready
    msg.innerHTML = 'Select a state.';
    
};    

// Populates the county dropdown
function show_county(ele) {  
    
    selected_state = ele.value;
     
    // Build a list of unique counties
    var u2 = {}, a2 = [];

    for(var i = 0, l = dataset.length; i < l; ++i){
        if(dataset[i]['state'] === ele.value){
            
            if(!u2.hasOwnProperty(dataset[i]['county'])) {
                a2.push(dataset[i]['county']);
                u2[dataset[i]['county']] = 1;
            }
        }
    };

    // Sort the list alphabetically
    a2.sort();
    //console.log('County list loaded successfully.');

    // Populate the dropdown
    // Adapted from: https://www.encodedna.com/javascript/populate-select-dropdown-list-with-json-data-using-javascript.htm
    var ele2 = document.getElementById('sel_county');
    
    ele2.innerHTML = '<option value="">-- Select county--</option>'; 
    
    for (var i = 0; i < a2.length; i++) {
        ele2.innerHTML = ele2.innerHTML +
            '<option value="' + a2[i] + '">' + a2[i] + '</option>';
    };
    // Change the message to say dropdown is ready
    msg.innerHTML = 'Select a county.';

};

// Build a plot using the state and county data selected by user
function selections_made(ele){
    
    // Get the selected county
    selected_county = ele.value;

    // Display message to user while the data is filtered
    //msg.innerHTML = `Please wait while the graph builds based on your selections`;
    msg.innerHTML = `The blue line represents cases. The red line represents deaths.`;

    var selection_msg = document.getElementById('selection_msg');

    plot();
};

function plot(){
    chart.innerHTML = "";

    // Filter the data by user selection
    var state_filtered = dataset.filter(x => ((x.state == selected_state) && (x.county == selected_county)) );        
    
    // Print out confirmation to the console
    //console.log(state_filtered);
    //console.log(`Number of records: ${state_filtered.length}`);
    //console.log(state_filtered[0].date);

    var margin = {top: 20, right: 20, bottom: 50, left: 60},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

    // parse the date / time
    var parseTime = d3.timeParse("%Y-%m-%d");

    // set the ranges
    var x = d3.scaleTime().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    // define the line
    var valueline = d3.line()
        .x(function(d) { 
            return x(d.date);
        })
        .y(function(d) {
            return y(d.cases);
        });
    // define the line
    var valueline2 = d3.line()
        .x(function(d) {
            return x(d.date);
        })
        .y(function(d) {
            return y(d.deaths);
        });
    
    // append the svg obgect to the body of the page
    // appends a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    var svg = d3.select("#chart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    function draw(data) {
    
        // format the data
        data.forEach(function(d) {
            d.date = parseTime(d.date);
            d.cases = +d.cases;
            d.deaths = +d.deaths;
        });
        //console.log(data);
        
        // Scale the range of the data
        x.domain(d3.extent(data, function(d) { return d.date; }));
        y.domain([0, d3.max(data, function(d) {
            return Math.max(d.cases, d.deaths); })]);
        
        // Add the valueline path.
        svg.append("path")
            .attr("fill", "none")
            .attr("stroke","blue")
            .attr("d", valueline(data));
        // Add the valueline path.
        svg.append("path")
            .attr("fill", "none")
            .attr("stroke","red")
            .attr("d", valueline2(data));  
        // Add the X Axis
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));
        // Add the Y Axis
        svg.append("g")
            .call(d3.axisLeft(y));
            svg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 1 - margin.left)
            .attr("x", 0 - (height / 2))
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .text("Number of Cases and Deaths");

        svg.append("text")             
        .attr("transform", "translate(" + (width/2) + " ," + (height + margin.top + 20) + ")")
        .style("text-anchor", "middle")
        .text("Date");
    }    
    
    // trigger render
    draw(state_filtered);
};