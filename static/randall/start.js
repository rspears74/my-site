function showDate () {
    const days = {
        0: 'Sunday',
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday'
    }

    var now = new Date();

    var day = days[now.getDay()];
    var month = now.getMonth() + 1;
    var date = now.getDate();
    var year = now.getFullYear();
    var currentHours = now.getHours();
    var currentMinutes = now.getMinutes();
    var currentSeconds = now.getSeconds();

    var currentDateString = day + ", " + month + "/" + date + "/" + year; 

    currentMinutes = (currentMinutes < 10 ? "0" : "") + currentMinutes;
    currentSeconds = (currentSeconds < 10 ? "0" : "") + currentSeconds;

    var timeOfDay = (currentHours < 12) ? "AM" : "PM";

    currentHours = (currentHours > 12) ? currentHours - 12 : currentHours;
    currentHours = (currentHours == 0) ? 12 : currentHours;

    var currentTimeString = currentHours + ":" + currentMinutes + ":" + currentSeconds + " " + timeOfDay;

    var dtString = currentDateString + " - " + currentTimeString;
    return dtString;
};


Vue.component('list-item', {
    props: ['site'],
    template: '<div class="list-item"><a :href="site.link" class="list-link">{{ site.name }}</a><br/></div>'
});

Vue.component('tab', {
    props: ['listtype'],
    template: '<div><a :class="listtype.isActive ? \'tabname-active\' : \'tabname\'" href="javascript:void(0)" @click="showList">{{listtype.name.toUpperCase()}}</a><br/></div>',
    methods: {
        showList: function () {
            for (x in lists) {
                lists[x].isActive = false;
            }
            this.listtype.isActive = true;
        }
    }
});

Vue.component('list', {
    props: ['listtype'],
    template: '<div><list-item v-for="item in listtype.links" v-if="listtype.isActive" :site="item" :key="item.id"></list-item></div>',
});

Vue.component('weather', {
    template: '<div id="weather"><a href="https://www.wunderground.com/weather/us/co/englewood">{{weatherString}}</a></div>',
    data: function () {
        return {weatherString: ''}
    },
    mounted: function () {
        var me = this;
        var location = {city: "Englewood", state: "CO"};
        var wgAPIKey = "e64c663775a23710";
        var wunderURL = "https://api.wunderground.com/api/" + wgAPIKey + "/conditions/q/" + location.state + "/" + location.city + ".json";
        xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var data = JSON.parse(xhttp.responseText);
                var currTemp = data.current_observation.temp_f;
                var currConditions = data.current_observation.weather;
                var currCity = data.current_observation.display_location.full;
                me.weatherString = currCity + ": " + currConditions + ", " + Math.round(currTemp) + "\u00B0" + "F";
                }
            };
        xhttp.open('GET', wunderURL, true);
        xhttp.send();
    }
});

Vue.component('datetime', {
    template: '<div id="date">{{time}}</div>',
    data: function () {
        return {
            time: showDate(),
        }
    },
    methods: {
        showDate: function () {
            this.time = showDate();
        }
    },
    mounted: function () {
        setInterval(this.showDate, 1000);
    }
});

var lists = {
                stuff: {
                    name: 'stuff',
                    links: [
                        {
                            name: 'jriver',
                            link: 'http://music.rspears.me',
                            id: 1
                        },
                        {
                            name: 'jupyter',
                            link: 'https://jupyter.rspears.me',
                            id: 2
                        },
                        {
                            name: 'spotify',
                            link: 'https://open.spotify.com',
                            id: 3
                        },
                        {
                            name: 'gmail',
                            link: 'https://mail.google.com',
                            id: 4
                        },
                        {
                            name: 'home',
                            link: 'https://hass.rspears.me',
                            id: 5
                        },
                        {
                            name: 'riot',
                            link: 'https://riot.im/app',
                            id: 6
                        },
			{
	  		    name: 'messages',
			    link: 'https://messages.android.com',
		            id: 7
		        },
                        {
                            name: 'dropbox',
                            link: 'https://www.dropbox.com',
                            id: 8
                        },
                        {
                            name: 'amazon',
                            link: 'https://www.amazon.com',
                            id: 9
                        },
                        {
                            name: 'weather',
                            link: 'https://www.wunderground.com',
                            id: 10
                        },
                        {
                            name: 'last fm',
                            link: 'https://www.last.fm/user/randeezydizzle',
                            id: 11
                        }
                    ],
                    isActive: true
                },
                googleStuff: {
                    name: 'google',
                    links: [
                        {
                            name: 'gmail',
                            link: 'https://mail.google.com',
                            id: 1
                        },
                        {
                            name: 'calendar',
                            link: 'https://calendar.google.com/calendar/render#main_7%7Cmonth',
                            id: 2
                        },
                        {
                            name: 'maps',
                            link: 'https://www.google.com/maps',
                            id: 3
                        },
                        {
                            name: 'drive',
                            link: 'https://drive.google.com/drive/my-drive',
                            id: 4
                        },
                        {
                            name: 'sheets',
                            link: 'https://docs.google.com/spreadsheets/u/0/',
                            id: 5
                        },
                        {
                            name: 'youtube',
                            link: 'https://www.youtube.com',
                            id: 6
                        }
                    ],
                    isActive: false
                },
                money: {
                    name: 'money',
                    links: [
                        {
                            name: 'wells fargo',
                            link: 'https://www.wellsfargo.com',
                            id: 1
                        },
                        {
                            name: 'amex',
                            link: 'https://www.americanexpress.com',
                            id: 2
                        },
                        {
                            name: 'stocks',
                            link: 'https://invest.ameritrade.com/grid/p/site#r=home',
                            id: 3
                        },
                        {
                            name: 'plains capital',
                            link: 'https://www.plainscapital.com/',
                            id: 4
                        },
                        {
                            name: 'mint',
                            link: 'https://wwws.mint.com/overview.event',
                            id: 5
                        },
                    ],
                    isActive: false
                },
                social: {
                    name: 'social',
                    links: [
                        {
                            name: 'twitter',
                            link: 'https://www.twitter.com',
                            id: 1
                        },
                        {
                            name: 'facebook',
                            link: 'https://www.facebook.com',
                            id: 2
                        },
                        {
                            name: 'reddit',
                            link: 'https://www.reddit.com',
                            id: 3
                        },
                        {
                            name: 'linkedin',
                            link: 'https://www.linkedin.com/',
                            id: 4
                        },
                        {
                            name: 'untappd',
                            link: 'https://untappd.com',
                            id: 5
                        },
                    ],
                    isActive: false
                },
                bills: {
                    name: 'bills',
                    links: [
                        {
                            name: 'wm',
                            link: 'https://www.wm.com/',
                            id: 1
                        },
                        {
                            name: 'xcel',
                            link: 'https://www.xcelenergy.com/',
                            id: 2
                        },
                        {
                            name: 'xfinity',
                            link: 'http://my.xfinity.com/?cid=cust',
                            id: 3
                        },
                        {
                            name: 'mortgage',
                            link: 'https://www.myloancare.com/pub/index.html#/Login?ReturnUrl=%2f',
                            id: 4
                        },
                        {
                            name: 'water',
                            link: 'https://ipn.paymentus.com/cp/engl',
                            id: 5
                        }
                    ],
                    isActive: false
                },
                programming: {
                    name: 'programming',
                    links: [
                        {
                            name: 'github',
                            link: 'https://github.com',
                            id: 1
                        },
                        {
                            name: 'google developer console',
                            link: 'https://console.developers.google.com/',
                            id: 2
                        },
                        {
                            name: 'stack overflow',
                            link: 'https://www.stackoverflow.com',
                            id: 3
                        },
                        {
                            name: 'namecheap',
                            link: 'https://ap.www.namecheap.com/dashboard',
                            id: 4
                        },
                        {
                            name: 'digitalocean',
                            link: 'https://cloud.digitalocean.com/dashboard?i=1de60c',
                            id: 5
                        }
                    ],
                    isActive: false
                },
}

var app = new Vue({
    el: '#app',
    data: lists,
});
