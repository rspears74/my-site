var checkLights = function () {
  $.getJSON('/check-all-lights', function (data) {
    lightStates=[];
    // check each light to see if its on and add to
    // lightStates array
    var lights_nums = ['4','5','6','7','8']
    for (var i=0; i<lights_nums.length; i++) {
      lightStates.push(data[lights_nums[i]].state.on);
    }
    // if all lights are on, set all switches to on
    if (lightStates.every(elem => elem == true)) {
      $('.switch input').prop('checked', true);
      // if not, but the first 3 are on, set the group
      // switch on, all lights switch off
    } else if (lightStates[0] == true && lightStates[1] == true && lightStates[2] == true) {
      $('.switch#all input').prop('checked', false);
      $('.switch#g-1 input').prop('checked', true);
      // if not all first 3 lights are on, set both the
      // all lights and group 1 switches off
    } else {
      $('.switch#all input').prop('checked', false);
      $('.switch#g-1 input').prop('checked', false);
    }
    // finally, for each light that is on, set its corresponding
    // switch on
    for (var i=0; i<lights_nums.length; i++) {
      if (lightStates[i]) {
        $('.switch#l-'+lights_nums[i]+' input').prop('checked', true);
      } else {
        $('.switch#l-'+lights_nums[i]+' input').prop('checked', false);
      }
    }
  });
}

// load checkLights function at page load, and...
$(checkLights)
// make checkLights function fire every 5 seconds
$(setInterval(checkLights, 5000))


var setLights = function () {
  // actions for 'All Lights' switch
  $('.switch#all input').click(function () {
    // if the click turns the switch on, turn all lights on
    if ($(this).is(':checked')) {
      $.ajax({
        method: 'PUT',
        url: '/set-lights',
        data: JSON.stringify({
          lights: ['5', '6', '7', '8', '4'],
          on_off: true
        })
      }).success(function () {
        // if the request is successful, turn all switches on
        $('.switch input').prop('checked', true);
      });
      // if the check turns the switch off, turn all lights off
    } else {
      $.ajax({
        method: 'PUT',
        url: '/set-lights',
        data: JSON.stringify({
          lights: ['5', '6', '7', '8', '4'],
          on_off: false
        })
      }).success(function () {
        // if the request is successful, turn all switches off
        $('.switch input').prop('checked', false);
      });
    }
  });
  // actions for 'Living Room' switch
  $('.switch#g-1 input').click(function () {
    // if the click turns on the living room switch, set lights 1,2,3 on
    if ($(this).is(':checked')) {
      $.ajax({
        method: 'PUT',
        url: '/set-lights',
        data: JSON.stringify({
          lights: ['5','6','7','8'],
          on_off: true
        })
      }).success(function () {
        // if the request is successful, turn on the group switch and all
        // members of the group
        $('.switch#g-1 input').prop('checked', true);
        for (var i=5; i<=8; i++) {
          $('.switch#l-'+i+' input').prop('checked', true);
        }
        // if light 4 is on, turn on the all lights switch
        if ($('.switch#l-4 input').is(':checked')) {
          $('.switch#all input').prop('checked', true);
        }
      });
    } else {
      // if the click turns off the group 1 switch, turn off lights 1,2,3
      $.ajax({
        method: 'PUT',
        url: '/set-lights',
        data: JSON.stringify({
          lights: ['5','6','7','8'],
          on_off: false
        })
      }).success(function () {
        // if the request is successful, turn off the group switch,
        // all members, and the all lights switch
        $('.switch#g-1 input').prop('checked', false);
        for (var i=5; i<=8; i++) {
          $('.switch#l-'+i+' input').prop('checked', false);
        }
        $('.switch#all input').prop('checked', false);
      });
    }
  });
  // actions for Light 1 switch
  $('.switch#l-5 input').click(function () {
    if ($(this).is(':checked')) {
      $.ajax({
        method: 'PUT',
        url: '/set-lights',
        data: JSON.stringify({
          lights: ['5'],
          on_off: true
        })
      }).success(function () {
        var otherLights = [];
        for (var i=4; i<=8; i++) {
          otherLights.push($('.switch#l-'+i+' input').is(':checked'));
        }
        if (otherLights.every(elem => elem == true)) {
          $('.switch#all input').prop('checked', true);
          $('.switch#g-1 input').prop('checked', true);
        } else if (otherLights.slice(1,5).every(elem => elem == true)) {
          $('.switch#g-1 input').prop('checked', true);
        }
      });
    } else {
      $.ajax({
        method: 'PUT',
        url: '/set-lights',
        data: JSON.stringify({
          lights: ['5'],
          on_off: false
        })
      }).success(function () {
        $('.switch#all input').prop('checked', false);
        $('.switch#g-1 input').prop('checked', false);
      });
    }
  });
  // actions for Light 2 switch
  $('.switch#l-6 input').click(function () {
    if ($(this).is(':checked')) {
      $.ajax({
        method: 'PUT',
        url: '/set-lights',
        data: JSON.stringify({
          lights: ['6'],
          on_off: true
        })
      }).success(function () {
        var otherLights = [];
        for (var i=4; i<=8; i++) {
          otherLights.push($('.switch#l-'+i+' input').is(':checked'));
        }
        if (otherLights.every(elem => elem == true)) {
          $('.switch#all input').prop('checked', true);
          $('.switch#g-1 input').prop('checked', true);
        } else if (otherLights.slice(1,5).every(elem => elem == true)) {
          $('.switch#g-1 input').prop('checked', true);
        }
      });
    } else {
      $.ajax({
        method: 'PUT',
        url: '/set-lights',
        data: JSON.stringify({
          lights: ['6'],
          on_off: false
        })
      }).success(function () {
        $('.switch#all input').prop('checked', false);
        $('.switch#g-1 input').prop('checked', false);
      });
    }
  });
  // actions for Light 3 swtich
  $('.switch#l-7 input').click(function () {
    if ($(this).is(':checked')) {
      $.ajax({
        method: 'PUT',
        url: '/set-lights',
        data: JSON.stringify({
          lights: ['7'],
          on_off: true
        })
      }).success(function () {
        var otherLights = [];
        for (var i=4; i<=8; i++) {
          otherLights.push($('.switch#l-'+i+' input').is(':checked'));
        }
        if (otherLights.every(elem => elem == true)) {
          $('.switch#all input').prop('checked', true);
          $('.switch#g-1 input').prop('checked', true);
        } else if (otherLights.slice(1,5).every(elem => elem == true)) {
          $('.switch#g-1 input').prop('checked', true);
        }
      });
    } else {
      $.ajax({
        method: 'PUT',
        url: '/set-lights',
        data: JSON.stringify({
          lights: ['7'],
          on_off: false
        })
      }).success(function () {
        $('.switch#all input').prop('checked', false);
        $('.switch#g-1 input').prop('checked', false);
      });
    }
  });
  // actions for Light 3 swtich
  $('.switch#l-8 input').click(function () {
    if ($(this).is(':checked')) {
      $.ajax({
        method: 'PUT',
        url: '/set-lights',
        data: JSON.stringify({
          lights: ['8'],
          on_off: true
        })
      }).success(function () {
        var otherLights = [];
        for (var i=4; i<=8; i++) {
          otherLights.push($('.switch#l-'+i+' input').is(':checked'));
        }
        if (otherLights.every(elem => elem == true)) {
          $('.switch#all input').prop('checked', true);
          $('.switch#g-1 input').prop('checked', true);
        } else if (otherLights.slice(1,5).every(elem => elem == true)) {
          $('.switch#g-1 input').prop('checked', true);
        }
      });
    } else {
      $.ajax({
        method: 'PUT',
        url: '/set-lights',
        data: JSON.stringify({
          lights: ['8'],
          on_off: false
        })
      }).success(function () {
        $('.switch#all input').prop('checked', false);
        $('.switch#g-1 input').prop('checked', false);
      });
    }
  });
  // actions for Light 4 swtich
  $('.switch#l-4 input').click(function () {
    if ($(this).is(':checked')) {
      $.ajax({
        method: 'PUT',
        url: '/set-lights',
        data: JSON.stringify({
          lights: ['4'],
          on_off: true
        })
      }).success(function () {
        var otherLights = [];
        for (var i=4; i<=8; i++) {
          otherLights.push($('.switch#l-'+i+' input').is(':checked'));
        }
        if (otherLights.every(elem => elem == true)) {
          $('.switch#all input').prop('checked', true);
        }
      });
    } else {
      $.ajax({
        method: 'PUT',
        url: '/set-lights',
        data: JSON.stringify({
          lights: ['4'],
          on_off: false
        })
      }).success(function () {
        $('.switch#all input').prop('checked', false);
      });
    }
  });
}


$(setLights)
