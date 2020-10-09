// Mapbox access. We used Mapbox GL to "construct" the map in order to join data on a a county level variable.
mapboxgl.accessToken = 'pk.eyJ1IjoiY2pyZXNpZGUiLCJhIjoiY2tmN2R6bDVmMDFndDJybGtvZGdnZWV3ZCJ9.tYi9cIPcH18ZWKlrS7MOdA';
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/cjreside/ckfo8p10m1hh319ogptxg584j', // Developed style that utilizes the ALBERS geographic projections.
  maxZoom: 18,
  zoom: 3.8,
  center: [-1, 0.339]
});

// Will only populate "data" when the cursor is over an object with data, outside of the mape is "intentionally absent".
let hoveredStateId = null;

// Construct "Pop Up" to showcase mask use data over the map.
const popup = new mapboxgl.Popup({
  closeButton: false,
  closeOnClick: false
});

// When the map loads, it calls the mask api and pulls in that specific data.
map.on('load', () => {
  d3.json("/api/v1.0/masks").then((data) => {
    initFeatureState(data)
  });

// Construct a "Feature State" that pulls in the data, and overlays vectors on the map based on the county fips code.
  const initFeatureState = (data) => {
    map.addSource('albersusa', {
      type: 'vector',
      url: 'mapbox://lobenichou.albersusa', // The developer of the ALBERS style integrated by Mapbox.
      promoteId: 'county_fips'
    });

// Add a Layer that will fill the county vectors based on a value from our Data
    map.addLayer({
      'id': 'albersusa-fill',
      'type': 'fill',
      'source': 'albersusa',
      'source-layer': 'albersusa',
      'paint': {
        'fill-color': ['case', // Using "Case" will return the input string (mask_always) as is.
          ['!=', ['feature-state', 'mask_always'], null],
          ['interpolate',
            ['linear'],
            ['to-number', ['feature-state', 'mask_always']],
            .1, '#B80C09',
            .3, '#8B3843',
            .5, '#5D637C',
            .7, '#2F8FB6',
            .9, '#01BAEF'],
          'rgb(245,245,245)']
      },
      'filter': ['==', ['get', 'type'], 'county']
    });

// Create a layer that outlines the county as you move your cursor over the map.
    map.addLayer({
      'id': 'albersusa-line',
      'type': 'line',
      'source': 'albersusa',
      'source-layer': 'albersusa',
      'layout': {
        'line-join': 'round',
        'line-cap': 'round'
      },
      'paint': {
        'line-color': '#2EBFA5',
        'line-width': [
          'case',
          ['boolean', ['feature-state', 'hover'], false],
          2,
          0
        ]
      },
      'filter': ['==', ['get', 'type'], 'county']
    });

// As you move your cursor over the map, and hover over a county, it will check to see if any "features" exist.
    map.on('mousemove', 'albersusa-fill', (e) => {
      if (e.features.length > 0) {
        if (hoveredStateId) {
          map.setFeatureState({
            source: 'albersusa',
            'sourceLayer': 'albersusa',
            id: hoveredStateId
          }, {
            hover: false
          });
        }
        hoveredStateId = e.features[0].id;
        map.setFeatureState({
          source: 'albersusa',
          'sourceLayer': 'albersusa',
          id: hoveredStateId
        }, {
          hover: true
        });
      }
    });

// Populate the pop-up with text, data, etc... as you hover over a county
      map.on('mousemove', 'albersusa-fill', (e) => {
        map.getCanvas().style.cursor = 'pointer';
        const description = 
        `<p>${d3.format("")(e.features[0].state.mask_always*100)}% of the people in ${e.features[0].properties.county_name}
        always wears a mask</p>`;
        popup // Determines where, what, and how the pop up reacts
          .setLngLat(e.lngLat)
          .setHTML(description)
          .addTo(map);
      });

// Closes pop-up as you move from one county to another
      map.on('mouseleave', 'albersusa-fill', () => {
        if (hoveredStateId) {
          map.setFeatureState({
            source: 'albersusa',
            'sourceLayer': 'albersusa',
            id: hoveredStateId
          }, 
          {hover: false
          });
        }
        hoveredStateId = null;
        map.getCanvas().style.cursor = '';
        popup.remove();
      });

    const setStates = (data) => {
      data.forEach((row) => {
        map.setFeatureState({
          source: 'albersusa',
          'sourceLayer': 'albersusa',
          id: row.fips
        }, {
          mask_always: row.mask_always
        })
      })
    }

    const setAfterLoad = (e) => {
      if (e.sourceId === 'albersusa' && e.isSourceLoaded) {
        setStates(data);
        map.off('sourcedata', setAfterLoad);
      }
    }

    if (map.isSourceLoaded('albersusa')) {
      setStates(data);
    } else {
      map.on('sourcedata', setAfterLoad);
    }
  }
});
