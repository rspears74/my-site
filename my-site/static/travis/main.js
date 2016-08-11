function updateClock () {
    var currentTime = new Date();

    var currentHours = currentTime.getHours();
    var currentMinutes = currentTime.getMinutes();
    var currentSeconds = currentTime.getSeconds();

    currentMinutes = (currentMinutes < 10 ? "0" : "") + currentMinutes;
    currentSeconds = (currentSeconds < 10 ? "0" : "") + currentSeconds;

    var timeOfDay = (currentHours < 12) ? "AM" : "PM";

    currentHours = (currentHours > 12) ? currentHours - 12 : currentHours;
    currentHours = (currentHours == 0) ? 12 : currentHours;

    var currentTimeString = currentHours + ":" + currentMinutes + " " + timeOfDay;

    document.getElementById("clock").firstChild.nodeValue = currentTimeString;
}

function getWeather () {
    var location = {city: "Lubbock", state: "TX"};
    var wgAPIKey = "e64c663775a23710";
    var wunderURL = "http://api.wunderground.com/api/" + wgAPIKey + "/conditions/q/" + location.state + "/" + location.city + ".json";
    $.getJSON(wunderURL, function(data) {
      var currTemp = data.current_observation.temp_f;
      var currConditions = data.current_observation.weather;
      var currCity = data.current_observation.display_location.full;
      var weatherString = currConditions + ", " + Math.round(currTemp) + "\u00B0" + "F"
      document.getElementById("weather").firstChild.nodeValue = currCity + ": " + weatherString
    });
}
