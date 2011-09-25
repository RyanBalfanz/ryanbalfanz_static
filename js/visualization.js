var chartProperties = {
	numDataPoints: 150,
	height: 100,
	width: 940,
	redrawInterval: 1000*30
};

var randomData = function(n){
	n = typeof(n) != 'undefined' ? n : 1;
	
	var newData = [];
	for (i=0; i<n; i++){
		newData.push(Math.random());
	}
	
	return newData;
};

var data = randomData(chartProperties.numDataPoints);

var chart = d3.select("div.chartContainer")
	.append("svg:svg")
		.attr("class", "chart")
		.attr("width", chartProperties.width)
		.attr("height", chartProperties.height);
		
var x = d3.scale.ordinal()
	.domain(data)
	.rangeBands([0, chartProperties.width]);
	
var y = d3.scale.linear()
	.domain([0, d3.max(data)])
	.range([0, chartProperties.height]);
	
chart.selectAll("rect")
	 .data(data)
	.enter().append("svg:rect")
		.attr("x", x)
		.attr("y", 0)
		.attr("height", y)
		.attr("width", 940 / data.length);
		
function redraw() {
	console.log("redrawing");
	data = randomData(chartProperties.numDataPoints);
	chart.selectAll("rect")
		 .data(data)
		.transition()
			.duration(chartProperties.redrawInterval*0.1)
			// .attr("x", x)
			// .attr("y", 0)
			.attr("height", y)
			.attr("width", 940 / data.length);
}

function step() {
	randomData(chartProperties.numDataPoints);
	// console.log(data);
	redraw();
}

setInterval(function(){
	randomData(chartProperties.numDataPoints);
	// console.log(data);
	redraw();
}, chartProperties.redrawInterval);
