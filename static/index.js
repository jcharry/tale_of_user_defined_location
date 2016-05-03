/*
 * index.js
 * Copyright (C) 2016 jamiecharry <jamiecharry@Jamies-Air-2.home>
 *
 * Distributed under terms of the MIT license.
 */
(function(){
    'use strict';

    var dev = false;
    var dummyPlace = {"type":"FeatureCollection","query":[-73.989,40.733],"features":[{"id":"poi.17803065968973360","type":"Feature","text":"Atlas Installation","place_name":"Atlas Installation, 124 E 13th St, New York, New York 10003, United States","relevance":1,"properties":{"maki":"mobilephone","tel":"(212) 598-0256","address":"124 E 13th St","category":"computer, electronic"},"center":[-73.989015,40.732984],"geometry":{"type":"Point","coordinates":[-73.989015,40.732984]},"context":[{"id":"neighborhood.13193176554088160","text":"Gramercy-Flatiron"},{"id":"place.40071","text":"New York"},{"id":"postcode.17946862605296810","text":"10003"},{"id":"region.10680295328053660","text":"New York"},{"id":"country.12862386939497690","text":"United States","short_code":"us"}]},{"id":"neighborhood.13193176554088160","type":"Feature","text":"Gramercy-Flatiron","place_name":"Gramercy-Flatiron, New York, 10003, New York, United States","relevance":1,"properties":{},"bbox":[-73.9903760094056,40.7323331488558,-73.9819335937874,40.740330387996],"center":[-73.9882,40.735],"geometry":{"type":"Point","coordinates":[-73.9882,40.735]},"context":[{"id":"place.40071","text":"New York"},{"id":"postcode.17946862605296810","text":"10003"},{"id":"region.10680295328053660","text":"New York"},{"id":"country.12862386939497690","text":"United States","short_code":"us"}]},{"id":"place.40071","type":"Feature","text":"New York","place_name":"New York, New York, United States","relevance":1,"properties":{},"bbox":[-74.0472850075116,40.6839279901504,-73.9105869900014,40.8776450076585],"center":[-73.9808,40.7648],"geometry":{"type":"Point","coordinates":[-73.9808,40.7648]},"context":[{"id":"postcode.17946862605296810","text":"10003"},{"id":"region.10680295328053660","text":"New York"},{"id":"country.12862386939497690","text":"United States","short_code":"us"}]},{"id":"postcode.17946862605296810","type":"Feature","text":"10003","place_name":"10003, New York, United States","relevance":1,"properties":{},"bbox":[-73.999604,40.722933,-73.979864,40.739673],"center":[-73.991023,40.731226],"geometry":{"type":"Point","coordinates":[-73.991023,40.731226]},"context":[{"id":"region.10680295328053660","text":"New York"},{"id":"country.12862386939497690","text":"United States","short_code":"us"}]},{"id":"region.10680295328053660","type":"Feature","text":"New York","place_name":"New York, United States","relevance":1,"properties":{},"bbox":[-79.762418,40.4205279464,-71.6780244384,45.015865],"center":[-76.182169,42.773969],"geometry":{"type":"Point","coordinates":[-76.182169,42.773969]},"context":[{"id":"country.12862386939497690","text":"United States","short_code":"us"}]},{"id":"country.12862386939497690","type":"Feature","text":"United States","place_name":"United States","relevance":1,"properties":{"short_code":"us"},"bbox":[-179.330950579,18.765563302,179.959578044,71.540723637],"center":[-97.922211,39.381266],"geometry":{"type":"Point","coordinates":[-97.922211,39.381266]}}],"attribution":"NOTICE: © 2016 Mapbox and its suppliers. All rights reserved. Use of this data is subject to the Mapbox Terms of Service (https://www.mapbox.com/about/maps/). This response and the information it contains may not be retained."};
    
    window.addEventListener('load', function() {

        document.getElementById('dismissOverlay').addEventListener('click', function() {
            toggleOverlay();
        });
        document.getElementById('infoButton').addEventListener('click', function() {
            document.getElementById('map').classList.add('blurred');
            document.getElementById('infopane').style.display = 'block';
        });
        document.getElementById('closeInfopane').addEventListener('click', function() {
            document.getElementById('map').classList.remove('blurred');
            document.getElementById('infopane').style.display = 'none';
        });
        document.getElementById('savePoem').addEventListener('click', function() {
            $.ajax({
                type: 'POST',
                url: '/save',
                data: JSON.stringify({
                    title: document.getElementById('poemTitle').innerHTML, 
                    poem: document.getElementById('poem').innerHTML}),
                contentType: 'application/json;charset=UTF-8',
                success: function(res) {
                    console.log(res);
                },
                error: function(err) {
                    console.log(err);
                }

            });
        });

        document.getElementById('poemContainer').style.display = 'none';

    });
    // NYC LatLon - 40.7340314,-74.0146958
    var map = L.map('map').setView([40.7340314,-74.0146958], 13);

    L.accessToken = 'pk.eyJ1IjoiamNoYXJyeSIsImEiOiJjaW10ZW95dzEwMXl4dXdtNHRtMGk4azJhIn0.E3mtcvu7db6UCAFTgHOsyQ';
    /*    
    mapbox.streets
    mapbox.light
    mapbox.dark
    mapbox.satellite
    mapbox.streets-satellite
    mapbox.wheatpaste
    mapbox.streets-basic
    mapbox.comic
    mapbox.outdoors
    mapbox.run-bike-hike
    mapbox.pencil
    mapbox.pirates
    mapbox.emerald
    mapbox.high-contrast
    */
    var mapboxtype = 'mapbox.light';
    L.tileLayer('https://api.tiles.mapbox.com/v4/'+mapboxtype+'/{z}/{x}/{y}.png?access_token='+L.accessToken, {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'tale_of_user_defined_location',
        accessToken: 'pk.eyJ1IjoiamNoYXJyeSIsImEiOiJjaW10ZW95dzEwMXl4dXdtNHRtMGk4azJhIn0.E3mtcvu7db6UCAFTgHOsyQ'
    }).addTo(map);


    var popup = L.popup({closeButton: true});
    map.on('click', function(e) {

        // Convert coords into list of places
        getPlaces(e.latlng.lat, e.latlng.lng, function(places) {
            displayPopup(places.features[0], e.latlng);
            document.getElementById('postlocation').addEventListener('click', function() {
                postLocation(places.features[0]);
            });
        });
    });

    var overlay = false;
    function toggleOverlay() {
        if (overlay === false) {
            document.getElementById('overlay').style.display = 'block';
            document.getElementsByClassName('columnContainer')[0].classList.add('blurred');
            document.getElementById('infoButton').classList.add('blurred');
            document.getElementById('pageTitle').classList.add('blurred');
            overlay = true;
        }
        else {
            document.getElementById('overlay').style.display = 'none';
            document.getElementsByClassName('columnContainer')[0].classList.remove('blurred');
            document.getElementById('pageTitle').classList.remove('blurred');
            document.getElementById('infoButton').classList.remove('blurred');
            document.getElementById('poemContainer').style.display = 'none';
            document.getElementsByClassName('spinner')[0].style.display = 'block';
            overlay = false;
        }
    }

    function displayPopup(place, latlng) {
        console.log(place);

        var placeTitle = place.text;
        var placeCat = place.category;
        var placeProps = place.properties;
        // Display Popup
        popup.setLatLng(latlng)
        .setContent(
            
            "<p>Would you like to generate a summary for " + (placeProps.address || placeTitle)  + "?</p><p style='font-size:8pt'>Note: summary may take a few minutes to generate</p> <button id='postlocation' style='width:100%'>Post Location</button>"
        )
            .openOn(map);
    }


    function getPlaces(lat, lng, cb) {
        if (dev) {
            cb(dummyPlace);
        } else {
            $.ajax({
                type: "GET",
                url: 'https://api.mapbox.com/geocoding/v5/mapbox.places/'+lng+ ','+lat+'.json?access_token=pk.eyJ1IjoiamNoYXJyeSIsImEiOiJjaW10ZW95dzEwMXl4dXdtNHRtMGk4azJhIn0.E3mtcvu7db6UCAFTgHOsyQ',
                success: function(data) {
                    cb(data);
                },
                error: function(err) {
                    console.error(err);
                }
            });
        }
    }
    
    function postLocation(place) {

        // Show loading overlay
        toggleOverlay();

        var loadingMessages = ['Assessing nearby culture', 'Digging through old attics', 'Isolating weather patterns', 'Classifying archival footage', 'Converting meaningless data', 'Applying machine learning', 'Transcribing local stories', 'Making a pot of coffee','Sending drones to location', 'Sampling native food', 'Constructing Geocity webpage'];

        var counter = 0;
        var messageElt = document.getElementById('loadingMessage');
        var timer = setInterval(function() {
            if (counter >= loadingMessages.length) { counter = 0; }
            messageElt.innerHTML = loadingMessages[counter];
            counter++;
        }, 800);

        console.log(place);
        var city;
        var neighborhood;
        var region;
        var country;
        place.context.forEach(function(ctx) {
            console.log(ctx);
            if (ctx.id.search('place') !== -1) {
                // This should point to a city or town
                city = ctx.text;
            }
            if (ctx.id.search('neighborhood') !== -1) {
                neighborhood = ctx.text;
            }
            if (ctx.id.search('region') !== -1) {
                region = ctx.text;
            }
            if (ctx.id.search('country') !== -1) {
                country = ctx.text;
            }
        });
        var params = $.param({
            lat: place.geometry.coordinates[1],
            lng: place.geometry.coordinates[0],
            title: place.text,
            name: place.name,
            addr: place.properties.addr,
            cat: place.properties.category,
            country: country,
            phone: place.properties.tel,
            maki: place.properties.maki,
            place_name: place.place_name,
            city: city,
            neighborhood: neighborhood,
            region: region,
            dev: dev
        });
        $.get('/location', params, function(data) {
            var parsedData = JSON.parse(data);
            handleData(parsedData, timer);
        }).fail(function(error) {
            console.log(error);
            stopSpinner(timer);
            document.getElementById('poem').innerHTML = 'We searched and we searched\nbut up empty we came.\nFor a different refrain\nplease try again\nperhaps in a different\ngeological domain';
        });
    }
    function stopSpinner(timer) {
        clearInterval(timer);
        document.getElementById('loadingMessage').innerHTML = '';
        document.getElementsByClassName('spinner')[0].style.display = 'none';
        document.getElementById('poemContainer').style.display = 'flex';

    }

    function handleData(data, timer) {
        console.log(data);
        document.getElementById('poemTitle').innerHTML = 'tale of ' + data.title;

        stopSpinner(timer);
        document.getElementById('poem').innerHTML = data.allLines;

        for (var i = 0; i < data.imgUrls.length; i++) {
            var imgurl = data.imgUrls[i];

            var imgElt = document.createElement('img');
            imgElt.src = imgurl;
            document.getElementById('');
            console.log(imgurl);
        }
    }
})();
