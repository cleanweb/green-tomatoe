
// tomatoe's dataset -> google's data table
function datasetToDataTable(dataset){
	var data = new google.visualization.DataTable();
    data.addColumn('string', 'State');
    var numColumns = dataset.columns.length; 
    
    $.each(dataset.columns, function(index, value){
    	if(index != 0){
    		data.addColumn('number', value.title);	
    	}
    });
    
    data.addRows(dataset.data.length);
    
    $.each(dataset.data, function(index, value){
    	for(var i=0; i<numColumns; i++)
    		if(i != 0) data.setValue(index, i, parseInt(value[i]));	
    		else data.setValue(index, i, value[i]);
    });
    
    return data;
}

// tomatoe's dataset -> google's data table
function datasetToDataTableWithOneColumn(dataset, columnIndex){
	var data = new google.visualization.DataTable();
    data.addColumn('string', 'State');
    var numColumns = dataset.columns.length; 
    
    data.addColumn('number', dataset.columns[columnIndex].title);	
    
    data.addRows(dataset.data.length);
    
    $.each(dataset.data, function(index, value){	
    	data.setValue(index, 1, parseInt(value[columnIndex]));	
    	data.setValue(index, 0, value[0]);
    });
    
    return data;
}

function barChart(dataset, containerId){
	var data = datasetToDataTable(dataset);
    
    var chart = new google.visualization.ColumnChart(document.getElementById(containerId));
        // copy pase all over the place
        var p = $(document).scrollTop();
        google.visualization.events.addListener(chart, 'ready', function() {
            setTimeout(function(){
                $(document).scrollTop(p);
            }, 1);
        });
        // ------------------------------    
    chart.draw(data, {width: 700, height: 300, 
                      xAxis: {title: 'State', titleTextStyle: {color: 'red'}},
                      isStacked : true, legend : 'bottom'
                     });
                     
    _.defer(function(){window.scroll(0, 0);});     	
}

function lineChart(dataset, containerId){
	var data = datasetToDataTable(dataset);

        var chart = new google.visualization.LineChart(document.getElementById(containerId));
        // copy pase all over the place
        var p = $(document).scrollTop();
        google.visualization.events.addListener(chart, 'ready', function() {
            setTimeout(function(){
                $(document).scrollTop(p);
            }, 1);
        });
        // ------------------------------    
    chart.draw(data, {width: 700, height: 300, legend : 'bottom'});
    	
	_.defer(function(){window.scroll(0, 0);});
}

function handleColumnSelectionChange(selector, dataset, containerId, renderer){
	selector.bind("change",function(){
		var index = -1;
		var selectedValue = $(this).attr("value"); 
		
		$.each(dataset.columns, function(i,col){ 
			if(col.title == selectedValue) index = i; 
		});
		
		if(index != -1){
			$("#" + containerId).html("");
			renderer(dataset,containerId,index);
		}
	});
}

function nonStateColumns(dataset){
	var cols = new Object;
	cols.columns = [];
	
	$.each(dataset.columns,function(index,col){
		if(index != 0) cols.columns.push(col);
	});
	return cols;
}

function buildColumnSelector(dataset,cols,index,containerId){
	var columnSelector = jQuery(_.template($("#template-column-selector").html())(cols));
	columnSelector.val(dataset.columns[index].title); 
	$("#"+containerId).prepend(columnSelector);
	return columnSelector;	
}

function areaChart(dataset, containerId, columnIndex) {
	var cols = nonStateColumns(dataset);
	
	if(columnIndex == undefined) columnIndex = 1;
	
	var data = datasetToDataTableWithOneColumn(dataset,columnIndex);
	
	var chart = new google.visualization.AreaChart(document.getElementById(containerId));
        // copy pase all over the place
        var p = $(document).scrollTop();
        google.visualization.events.addListener(chart, 'ready', function() {
            setTimeout(function(){
                $(document).scrollTop(p);
            }, 1);
        });
        // ------------------------------    
    chart.draw(data, {width: 700, height: 300, legend : 'bottom', title: dataset.columns[columnIndex].title});

	var columnSelector = buildColumnSelector(dataset,cols,columnIndex,containerId);
	/*
	var columnSelector = jQuery(_.template($("#template-column-selector").html())(cols));
	columnSelector.val(dataset.columns[columnIndex].title); 
	$("#"+containerId).prepend(columnSelector);
	*/
	
	handleColumnSelectionChange(columnSelector, dataset, containerId, areaChart);
}

function pieChart(dataset, containerId, columnIndex){
	var cols = nonStateColumns(dataset);
	if(columnIndex == undefined) columnIndex = 1;
	var data = datasetToDataTableWithOneColumn(dataset,columnIndex);        
	var chart = new google.visualization.PieChart(document.getElementById(containerId));
        // copy pase all over the place
        var p = $(document).scrollTop();
        google.visualization.events.addListener(chart, 'ready', function() {
            setTimeout(function(){
                $(document).scrollTop(p);
            }, 1);
        });
        // ------------------------------
	 chart.draw(data, {width: 700, height: 300, legend : 'bottom', title: dataset.columns[columnIndex].title});         
	
	 var columnSelector = buildColumnSelector(dataset,cols,columnIndex,containerId);
	 handleColumnSelectionChange(columnSelector, dataset, containerId, pieChart);	
        
         
}

function mapChart(dataset, containerId, columnIndex){
	
	var cols = nonStateColumns(dataset);
	if(columnIndex == undefined) columnIndex = 1;
	var data = datasetToDataTableWithOneColumn(dataset,columnIndex);
	
	var options = {region: 'us_metro', 'dataMode' : 'markers' };

    var container = document.getElementById(containerId);
    var geochart = new google.visualization.GeoMap(container);
    geochart.draw(data, options);
    
    var columnSelector = buildColumnSelector(dataset,cols,columnIndex,containerId);
	handleColumnSelectionChange(columnSelector, dataset, containerId, mapChart);	
    
}
