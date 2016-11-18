var resultsButtons = function() {
  $('button#reset').click(function(){
    $('.value-input').val("");
    $('#results').hide();
    $('#error-container').hide();
    $('#showmpos-container').empty();
    $('#showvpos-container').empty();
    $('#mplot-container').empty();
    $('#vplot-container').empty();
    $('#showvreact-container').empty();
    $('.value-input').first().focus();
  });
  $('button#calculate').click(function(){
    $.getJSON($SCRIPT_ROOT + '/api/mvbridge', {
      spanLength: $('input[name="span-length"]').val(),
      xLoc: $('input[name="x-loc"]').val(),
      feetOrFrac: $('input[name="feet-or-frac"]:checked').val(),
      increment: $('input[name="increment"]').val(),
      impactFactor: $('input[name="impact-factor"]').val(),
      distFactor: $('input[name="dist-factor"]').val()
    }, function(data) {
      if(data.data == null){
        $('#error-container').show();
        $('#error').text(data.error);
      }
      else {
      $('#error-container').hide();
      $('#results').show();
      $('#mmax').text(data.data.mmax);
      $('#mmaxloc').text(data.data.mmaxloc);
      $('#vmax').text(data.data.vmax);
      $('#vmaxloc').text(data.data.vmaxloc);
      }
    });
  });
}

$(resultsButtons)


var showPositionPlotsButtons = function() {
  $('button#showpos').click(function(){
    $.getJSON($SCRIPT_ROOT + '/api/mposplot', {
      spanLength: $('input[name="span-length"]').val(),
      xLoc: $('input[name="x-loc"]').val(),
      feetOrFrac: $('input[name="feet-or-frac"]:checked').val(),
      maxMomentLoc: $('span#mmaxloc').text()
    }, function(data){
      if ($('#showmpos-container').is(':empty')) {
        mpld3.draw_figure("showmpos-container", data);
      }
    });
    $.getJSON($SCRIPT_ROOT + '/api/vposplot', {
      spanLength: $('input[name="span-length"]').val(),
      xLoc: $('input[name="x-loc"]').val(),
      feetOrFrac: $('input[name="feet-or-frac"]:checked').val(),
      maxShearLoc: $('span#vmaxloc').text()
    }, function(data){
      if ($('#showvpos-container').is(':empty')) {
        mpld3.draw_figure("showvpos-container", data);
      }
    });
  });
}

$(showPositionPlotsButtons)


var showMVPlots = function () {
  $('button#generate-plots').click(function () {
    $.getJSON($SCRIPT_ROOT + '/api/mplot', {
      spanLength: $('input[name="span-length"]').val(),
      numPoints: $('input[name="n-points"]').val(),
      increment: $('input[name="increment"]').val(),
      impactFactor: $('input[name="impact-factor"]').val(),
      distFactor: $('input[name="dist-factor"]').val()
    }, function(data) {
      if (data.data == null) {
        $('#error-container').show();
        $('#error').text(data.error);
      } else {
        if ($('#mplot-container').is(':empty')) {
          mpld3.draw_figure("mplot-container", data.data);
        }
      }
    });
    $.getJSON($SCRIPT_ROOT + '/api/vplot', {
      spanLength: $('input[name="span-length"]').val(),
      numPoints: $('input[name="n-points"]').val(),
      increment: $('input[name="increment"]').val(),
      impactFactor: $('input[name="impact-factor"]').val(),
      distFactor: $('input[name="dist-factor"]').val()
    }, function (data) {
      if (data.data != null) {
        if ($('#vplot-container').is(':empty')) {
          mpld3.draw_figure("vplot-container", data.data);
        }
        $('#results').show();
      }
    });
  });
}

$(showMVPlots)


var headerAnimation = function () {
  $('.header-link').hover(function () {
    $(this).toggleClass('selected');
  });
}

$(headerAnimation)


var dropDownMenu = function () {
  $('#modules').hover(function () {
    $('#module-drop-down').toggle();
  });
  $('#module-drop-down').hover(function () {
    $(this).toggle();
  });
  $('.module-drop-down-entry').hover(function () {
    $(this).toggleClass('selected');
  });
}

$(dropDownMenu)


var buttonAnimate = function () {
  $('button').hover(function () {
    $(this).toggleClass('button-selected');
  });
  $('select').hover(function () {
    $(this).toggleClass('button-selected');
  });
}

$(buttonAnimate)


var resultsButtonsVReact = function() {
  $('button#calculate-vreact').click(function(){
    $.getJSON($SCRIPT_ROOT + '/api/vreact', {
      spanLength1: $('input[name="span-length-1"]').val(),
      spanLength2: $('input[name="span-length-2"]').val(),
      increment: $('input[name="increment"]').val(),
      impactFactor: $('input[name="impact-factor"]').val(),
      distFactor: $('input[name="dist-factor"]').val()
    }, function(data) {
      if(data.data == null){
        $('#error-container').show();
        $('#error').text(data.error);
      } else {
        $('#error-container').hide();
        $('#results').show();
        $('#vreact-max').text(data.data.maxPierReact);
        $('#vreact-loc').text(data.data.location);
        $('#span-1-contrib').text(data.data.span1);
        $('#span-2-contrib').text(data.data.span2);
        if ($('#showvreact-container').is(':empty')) {
          mpld3.draw_figure("showvreact-container", data.data.locPlot);
        }
      }
    });
  });
}

$(resultsButtonsVReact)


var beamNodes = {};
var beamLoads = {};
var beamProperties = {};
var usedLocations = [];

$( function () {
  p = document.getElementById('plotly-container');
  initPlot(p);
});


var numNode = 1;
var nodesInput = function () {
  $('button#add-node').click(function () {
    if ($.isNumeric($('input[name=node-loc]').val()) && $.inArray($('input[name=node-loc]').val(), usedLocations) == -1) {
      beamNodes[numNode] = {
        location:parseFloat($('input[name=node-loc]').val()),
        rotation: 0,
        displacement: 0
      };
      $('#node-select').append($('<option>', {
        value: numNode,
        text: numNode
      }));
      var currNode = parseInt($('select#node-select').find('option:selected').val());
      $('#node-select-location').text(beamNodes[currNode].location);
      $('#node-select-location-wrap').show()
      $('#node-num').text(numNode);
      plotNode(p, beamNodes[numNode].location);
      if (numNode == 2) {
        plotElement(p, beamNodes[1].location, beamNodes[numNode].location);
      } else if (numNode > 2) {
        updateElement(p, 3, beamNodes[numNode].location)
      }
      numNode = numNode + 1;
      $('#input-error').hide();
      $('input[name=node-loc]').val("");
      $('#message-box').stop(true, true).show().fadeOut(2500);
      $('#node-input-success').stop(true, true).show().fadeOut(2500);
      usedLocations.push($('input[name=node-loc]').val())
    } else {
      $('#message-box').stop(true, true).show().fadeOut(2500);
      $('#input-error').stop(true, true).show().fadeOut(2500);
    }
  });
}

$(nodesInput)


var boundInput = function () {
  $('select#node-select').change(function () {
    var currNode = parseInt($('select#node-select').find('option:selected').val());
    $('#node-select-location').text(beamNodes[currNode].location);
    $('#node-select-location-wrap').show();
  });
  $('button#apply-bound').click(function () {
    var currNode = parseInt($('select#node-select').find('option:selected').val());
    if ($('input[name=displacement]').is(':checked')) {
      beamNodes[currNode].displacement = 1;
    } else {
      beamNodes[currNode].displacement = 0;
    }
    if ($('input[name=rotation]').is(':checked')) {
      beamNodes[currNode].rotation = 1;
    } else {
      beamNodes[currNode].rotation = 0;
    }
    var nodeLoc = beamNodes[currNode].location
    var usedBounds = []
    for (var i = 0; i < p.data.length; i++) {
      if (p.data[i].name.includes("Boundary")) {
        usedBounds.push(p.data[i].x[0]);
      }
    }
    if (beamNodes[currNode].displacement == 1 && beamNodes[currNode].rotation == 1) {
      if (usedBounds.indexOf(nodeLoc) >= 0) {
        updateSupport(p, nodeLoc, 'fixed');
      } else {
        plotSupport(p, nodeLoc, 'fixed');
      }
    } else if (beamNodes[currNode].displacement == 1) {
      if (usedBounds.indexOf(nodeLoc) >= 0) {
        updateSupport(p, nodeLoc, 'simple');
      } else {
        plotSupport(p, nodeLoc, 'simple');
      }
    } else {
      deleteSupport(p, nodeLoc);
    }
    $('#message-box').stop(true, true).show().fadeOut(2500);
    $('#apply-bound-message').stop(true, true).show().fadeOut(2500);
  });
}

$(boundInput)

var loadId = 1;
var loadsInput = function () {
  $('select#load-type-select').change(function () {
    $('#point-load-input').hide();
    $('#distributed-load-input').hide();
    var loadTypeSelected = $(this).find('option:selected').val();
    $('#'+loadTypeSelected+'-load-input').show();
  });
  $('button#add-load').click(function () {
    if ($('select#load-type-select').find('option:selected').val() == "point") {
      if ($.isNumeric($('#point-load-input input[name=load-value]').val()) && $.isNumeric($('#point-load-input input[name=load-loc]').val())) {
        beamLoads[loadId] = {
          type: "point",
          loc: parseFloat($('#point-load-input input[name=load-loc]').val()),
          load: parseFloat($('#point-load-input input[name=load-value]').val())
        }
        $('#point-load-input input').val("");
        $('#message-box').stop(true, true).show().fadeOut(2500);
        $('#load-added-message').stop(true, true).show().fadeOut(2500);
        plotPointLoad(p, beamLoads[loadId].loc, beamLoads[loadId].load);
        loadId = loadId + 1;
      } else {
        $('#message-box').stop(true, true).show().fadeOut(2500);
        $('#input-error').stop(true, true).show().fadeOut(2500);
      }
    }
    if ($('select#load-type-select').find('option:selected').val() == "distributed") {
      if ($.isNumeric($('#distributed-load-input input[name=load-value]').val()) && $.isNumeric($('#distributed-load-input input[name=load-loc1]').val()) && $.isNumeric($('#distributed-load-input input[name=load-loc2]').val())) {
        beamLoads[loadId] = {
          type: "distributed",
          loc1: parseFloat($('#distributed-load-input input[name=load-loc1]').val()),
          loc2: parseFloat($('#distributed-load-input input[name=load-loc2]').val()),
          load: parseFloat($('#distributed-load-input input[name=load-value]').val())
        }
        $('#distributed-load-input input').val("");
        $('#message-box').stop(true, true).show().fadeOut(2500);
        $('#load-added-message').stop(true, true).show().fadeOut(2500);
        plotDistLoad(p, beamLoads[loadId].loc1, beamLoads[loadId].loc2, beamLoads[loadId].load);
        loadId = loadId + 1;
      } else {
        $('#message-box').stop(true, true).show().fadeOut(2500);
        $('#input-error').stop(true, true).show().fadeOut(2500);
      }
    }
  });
}

$(loadsInput)

var beamCalcButtons = function () {
  $('button#reset-beam').click(function () {
    $('.value-input').val("");
    $('.value-select').val("");
    beamNodes = {};
    beamLoads = {};
    beamProperties = {};
    usedLocations = [];
    numNode = 1;
    loadCounter = 1;
    nodeCounter = 1;
    boundCounter = 1;
    Plotly.purge(p);
    initPlot(p);
    $('select#node-select').empty();
    $('#node-select-location').empty();
    $('#node-select-location-wrap').hide();
    $('#point-load-input').hide();
    $('#distributed-load-input').hide();
    $('input[type=checkbox]').prop('checked', false);
  });
  $('button#calculate-beam').click(function () {
    $.ajax({
    url: $SCRIPT_ROOT + '/api/beam',
    type: "POST",
    data: JSON.stringify({
      loads: beamLoads,
      nodes: beamNodes,
      properties: {
        momentOfInertia: parseFloat($('input[name=mom-of-inertia]').val()),
        material: $('select#material-input').find('option:selected').val()
      }
    }),
    dataType: "json",
    contentType: "application/json; charset=utf-8"
  })
    .done(function(data) {
      console.log(data)
      var x = data.x
      var y = data.y
      for (i=0; i<x.length; i++) {
        deflectedShape(p, x[i], y[i]);
      }
    });
  });
}

$(beamCalcButtons)
