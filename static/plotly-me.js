function setUp() {
  t = document.getElementById("tester");
}

window.onload = setUp;

// ----------------------- Keeping track of traces -----------------------------
var traceIndex = []
// =============================================================================


// ----------------------- Initializing a new plot -----------------------------
function initPlot(div) {
  var data = [{
    x: 0,
    y: 2,
    name: "init"
  }];
  var layout = {
    yaxis: {
      showticklabels: false,
      showgrid: false,
      showline: false,
      linewidth: 0,
      range: [0, 3]
    },
    xaxis: {
      showgrid: false,
      zeroline: false
    }
  };
  Plotly.newPlot(div, data, layout);
}
// =============================================================================


// --------------------------- Adding a node -----------------------------------
var nodeCounter = 1;
function plotNode (div, loc) {
  var data = [{
    x: [loc, loc],
    y: [2, 2],
    marker: {
      color: "blue",
      size: 5
    },
    mode: "markers",
    showlegend: false,
    name: "Node " + nodeCounter,
    text: loc + " ft",
    hoverinfo: "name+text"
  }];
  Plotly.addTraces(div, data);
  nodeCounter += 1;
}
// =============================================================================


// ------------------------- Adding an element ---------------------------------
var elementCounter = 1;
function plotElement (div, n1, n2) {
  var data = [{
    x: [n1, n2],
    y: [2, 2],
    marker: {
      color: "blue"
    },
    name: "element",
    mode: "lines",
    showlegend: false,
    hoverinfo: "none"
  }];
  Plotly.addTraces(div, data);
  elementCounter += 1;
}
// =============================================================================


// --------------------------- Adding a support --------------------------------
var boundCounter = 1;
function plotSupport (div, loc, boundType) {
  if (boundType == 'simple') {
    data = [{
      x: [loc, loc],
      y: [1.9, 1.9],
      marker: {
        color: "green",
        symbol: "triangle-up",
        size: 10
      },
      mode: "markers",
      showlegend: false,
      name: "Boundary " + boundCounter,
      text: "Type: simple",
      hoverinfo: "name+text"
    }];
  } else if (boundType == 'fixed') {
    data = [{
      x: [loc, loc],
      y: [1.9, 1.9],
      marker: {
        color: "green",
        symbol: "square",
        size: 10
      },
      mode: "markers",
      showlegend: false,
      name: "Boundary " + boundCounter,
      text: "Type: fixed",
      hoverinfo: "name+text"
    }];
  }

  Plotly.addTraces(div, data);
  boundCounter += 1;
}
// =============================================================================


// ------------------------- Adding a point load -------------------------------
var loadCounter = 1;
function plotPointLoad (div, loc, load) {
  var data = [{
    x: [loc, loc],
    y: [2.05, 2.05],
    marker: {
      color: "red",
      symbol: "triangle-down",
      size: 8,
    },
    name: "point load",
    mode: "markers",
    showlegend: false,
    hoverinfo: "none"
  }, {
    x: [loc, loc],
    y: [2.05, 3],
    marker: {
      color: "red"
    },
    mode: "lines",
    showlegend: false,
    text: load + " k",
    name: "Point load " + loadCounter,
    hoverinfo: "name+text"
  }];
  Plotly.addTraces(div, data);
  loadCounter += 1;
}
// =============================================================================


// ------------------------ Adding a distributed load --------------------------
var distLoadCounter = 1
function getPlotRange (div) {
  var rightSide = div.layout.xaxis.range[1];
  var leftSide = div.layout.xaxis.range[0];
  return rightSide - leftSide;
}

function generateDistLoadLine (loc) {
  var line = {
    x: [loc, loc],
    y: [2.05, 2.5],
    marker: {
      color: "red"
    },
    mode: "lines",
    name: "dist load line",
    showlegend: false,
    hoverinfo: "none"
  };
  return line;
}

function plotDistLoad (div, loc1, loc2, load) {
  var loadLength = loc2 - loc1;
  var maxDistBtwnLines = getPlotRange(div)/10.0;
  var numSpaces = Math.max(1, Math.floor(loadLength/maxDistBtwnLines));
  var numLines = numSpaces + 1;
  var distBtwnLines = loadLength/numSpaces;
  var lineXs = [];
  var lineYs = [];
  for (var i = 0; i < numLines; i++) {
    lineXs.push(loc1 + distBtwnLines*i);
    lineYs.push(2.05);
  }
  var data = [{
    x: lineXs,
    y: lineYs,
    marker: {
      color: "red",
      symbol: "triangle-down",
      size: 8,
    },
    name: "dist load arrows",
    mode: "markers",
    showlegend: false,
    hoverinfo: "none"
  }, {
    x: [loc1, loc2],
    y: [2.5, 2.5],
    marker: {
      color: "red"
    },
    mode: "lines",
    name: "Distributed Load " + distLoadCounter,
    text: load + " k/ft",
    showlegend: false,
    hoverinfo: "name+text"
  }];
  for (var i = 0; i < lineXs.length; i++) {
    data.push(generateDistLoadLine(lineXs[i]));
  }
  Plotly.addTraces(div, data);
}
// =============================================================================


// --------------------------- Updating an element -----------------------------
function updateElement (div, index, newX) {
  var origX = div.data[index].x[0];
  var update = {
    x: [[origX, newX]]
  };
  Plotly.restyle(div, update, index);
}
// =============================================================================


// --------------------------- Updating a support ------------------------------
function updateSupport (div, loc, boundType) {
  for (var i = 0; i < div.data.length; i++) {
    if (div.data[i].x[0] == loc & div.data[i].name.includes("Boundary")) {
      index = i;
      break;
    }
  }
  if (boundType == 'simple') {
    update = {
      marker: {
        color: "green",
        symbol: "triangle-up",
        size: 10
      }
    };
  } else if (boundType == 'fixed') {
    update = {
      marker: {
        color: "green",
        symbol: "square",
        size: 10
      }
    };
  }
  Plotly.restyle(div, update, index);
}
// =============================================================================


// ------------------------ Deleting a support ---------------------------------
function deleteSupport (div, loc) {
  for (var i = 0; i < div.data.length; i++) {
    if (div.data[i].x[0] == loc & div.data[i].name.includes("Boundary")) {
      index = i;
      break;
    }
  }
  Plotly.deleteTraces(div, index);
}
// =============================================================================


// --------------------- Drawing a deflected shape -----------------------------
function deflectedShape (div, nodes, defls) {
  for (var i = 0; i < defls.length; i++) {
    defls[i] = defls[i] + 2
  }
  var data = [{
    x: nodes,
    y: defls,
    mode: "lines",
    line: {
      color: "purple",
      shape: "spline",
      dash: "dash"
    },
    name: "deflected shape",
    showlegend: false
  }]
  Plotly.addTraces(div, data)
}
// =============================================================================
