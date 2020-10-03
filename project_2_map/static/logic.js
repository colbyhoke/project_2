// Access Token to MapBox
mapboxgl.accessToken = 'pk.eyJ1IjoiY2pyZXNpZGUiLCJhIjoiY2tmN2R6bDVmMDFndDJybGtvZGdnZWV3ZCJ9.tYi9cIPcH18ZWKlrS7MOdA';

// Create our initial map object, longitude, latitude, and the starting zoom level
var map = new mapboxgl.Map({
  container: 'map', 
  style: 'mapbox://styles/mapbox/light-v10',
  center: [-100.0, 40.0], 
  zoom: 3.8
});

map.on('load', function () {
  var filterDate = ['==', ['number', ['get', 'Date'], 12];

// On load add the source which we will pull and reference our data from
  map.addLayer({
    id: 'deaths',
    type: 'circle',
    source: { // Input Source, and accomodate code to read data
      type: '', 
      data: '' 
    },
    paint: {
      'circle-radius': [
        'interpolate',
        ['linear'],
        ['number', ['get', 'deaths']],
        0, 4,
        5, 24
      ],
      'circle-color': [
        'interpolate',
        ['linear'],
        ['number', ['get', 'deaths']],
        0, '#2DC4B2',
        1000, '#3BB3C3',
        50000, '#669EC4',
        100000, '#8B88B6',
        150000, '#A2719B',
        200000, '#AA5E79'
      ],
      'circle-opacity': 0.8
    },
    'filter': ['all', filterDate]
  });

  // Update Date filter when slider is dragged
  document.getElementById('slider').addEventListener('input', function(e) {
    var date = parseInt(e.target.value);
    // update the map
    filterDate = ['==', ['number', ['get', 'Date']], date];
    map.setFilter('deaths', ['all', filterDate]);
  
    // update text in the UI
    document.getElementById('active-date').innerText = date;
   });

  document.getElementById('filters').addEventListener('change', function(e) {
  var date = e.target.value;
  // update the map filter
  if (date === 'deaths') {
    filterDate = ['!=', ['string', ['get', 'Date']], 'placeholder'];
  } else if (date === 'cases') {
    filterDate = ['!=', ['string'], ['get', 'Date'], 'placeholder'];
  } else {
    console.log('error');
  }
  map.setFilter('collisions', ['all', filterDay]);
});
});


