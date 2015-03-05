var d3 = wavesUI.d3;
var loader = new loaders.AudioBufferLoader();

var graph_width = 1024

function waveform(div_id) {
    var id_sub = '#' + div_id + '_sub';
    // add waveform
    loader.load('download/ogg').then(function(audioBuffer) {
        try {

            var id = '#' + div_id;
            

            var data = [{
                start: audioBuffer.duration/4,
                duration: audioBuffer.duration/2
            }];

            var buffer = audioBuffer.getChannelData(0).buffer

            // 1. creat graph
            var graph = wavesUI.timeline()
                .xDomain([0, audioBuffer.duration])
                .width(graph_width)
                .height(140);

            // 2. create layers
            var waveformLayer = wavesUI.waveform()
                .data(buffer)
                .sampleRate(audioBuffer.sampleRate)
                .color('purple')
                // .opacity(0.8);

            var segmentLayer = wavesUI.segment()
                .params({
                    interactions: { editable: true },
                    opacity: 0.4,
                    handlerOpacity: 0.6
                })
                .data(data)
                .color('steelblue');

            // 3. add layers to graph
            graph.add(waveformLayer);
            graph.add(segmentLayer);

            // 4. draw graph
            d3.select(id).call(graph.draw);
	    
            var graph_sub = wavesUI.timeline()
                .xDomain([0, audioBuffer.duration])
                .width(graph_width)
                .height(140);

            var waveformLayerSub = wavesUI.waveform()
                .data(buffer)
                .sampleRate(audioBuffer.sampleRate)
                .color('purple')
                // .opacity(0.8);

            graph_sub.add(waveformLayerSub);

            d3.select(id_sub).call(graph_sub.draw);

	    // Add X-Ticks addTicks(id_sub, graph_sub);
	    // Create a svg element for the zoomer
	    var zoomerSvg = d3.select(id_sub).append('svg')
		.attr('width', graph_width)
		.attr('height', 30);

	    // Create the time axis - here a common d3 axis
	    // Graph must be drawn in order to have `graph.xScale` up to date
	    var xAxis = d3.svg.axis()
		.scale(graph_sub.xScale)
		.tickSize(1)
		.tickFormat(function(d) {
		    var form = '%S:%L';
		    var date = new Date(d * 1000);
		    var format = d3.time.format(form);
		    return format(date);
		});

	    // Add the axis to the newly created svg element
	    var axis = zoomerSvg.append('g')
		.attr('class', 'x-axis')
		.attr('transform', 'translate(0, 0)')
		.attr('fill', '#555')
		.call(xAxis);

	    var zoomLayer = wavesUI.zoomer()
            .select(id_sub)
            .on('mousemove', function(e) {
		// update graph xZoom
		graph_sub.xZoom(e);
		// update axis
		axis.call(xAxis);
		
            })
            .on('mouseup', function(e) {
                // set the final xZoom value of the graph
                graph_sub.xZoomSet();
		// update axis
		axis.call(xAxis);
            });

        } catch (err) {
            console.log(err);
        }
    }, function() {});
}



function timeline_get_data(json_url, div_id) {
    $.getJSON(json_url, function(data_list) {

    for (var i = 0; i < data_list.length; i++) {
        var data = data_list[i];
        timeline_result(data, div_id);
    }
    });
}

function timeline_result(data, div_id) {

    var time_mode = data.time_mode
    var data_mode = data.data_mode
    var id = data.id_metadata.id

    switch (time_mode) {
    case 'global':
    console.log(id, time_mode, data_mode);
    break;
    case 'event':
    switch (data_mode) {
    case 'value':
        console.log(id, time_mode, data_mode);
        break;
    case 'label':
        timeline_event_label(data, div_id);
        break;
    }
    break;
    case 'segment':
    switch (data_mode) {
    case 'value':
        timeline_segment_value(data, div_id);
        break;

    case 'label':
        console.log(id, time_mode, data_mode);
        break;
    }
    break;
    case 'framewise':
    console.log(id, time_mode, data_mode);
    break;
    }
}


function timeline_segment_value(data, div_id) {
    var duration = data.audio_metadata.duration;
    var durations = data.data_object.duration.numpyArray;
    var starts = data.data_object.time.numpyArray;
    var values = data.data_object.value.numpyArray;
    // format data
    var data = durations.map(function(dummy, index) {
        return {
            start: starts[index],
            duration: durations[index],
            height: values[index]
        };
    });


    // var minValue = Math.min.apply(null, values);
    var max_value = Math.max.apply(null, values);

    var graph = wavesUI.timeline()
        .xDomain([0, duration])
        .yDomain([0, max_value])
        .width(graph_width)
        .height(140);

    var segmentLayer = wavesUI.segment()
        .data(data)
        .color('steelblue')
        .opacity(0.8);

    // 3. add layers to graph
    graph.add(segmentLayer);

    // 4. draw graph
    d3.select('#'+div_id).call(graph.draw);

    var zoomLayer = wavesUI.zoomer()
        .select('#'+div_id)
        .on('mousemove', function(e) {
        // update graph xZoom
        graph.xZoom(e);
        })
        .on('mouseup', function(e) {
            // set the final xZoom value of the graph
            graph.xZoomSet();
        });

    // to update the data, add it to the data array and redraw the graph
    $('#add-data').on('click', function(e) {
        e.preventDefault();

        var datum = {
            start: 2,
            duration: 1,
            height: 1000
        };

        data.push(datum);
        graph.update();
    });
}

function timeline_event_label(data, div_id) {
    var duration = data.audio_metadata.duration;
    var starts = data.data_object.time.numpyArray;
    var values = data.data_object.label
    // format data
    var data = starts.map(function(dummy, index) {
        return {
            x: starts[index],
            height: values[index]
        };
    });


    // var minValue = Math.min.apply(null, values);
    var max_value = Math.max.apply(null, values);

    var graph = wavesUI.timeline()
        .xDomain([0, duration])
        .yDomain([0, max_value])
        .width(graph_width)
        .height(140);

    var markerLayer = wavesUI.marker()
        .data(data)
        .color('steelblue')
        .opacity(0.8);

    // 3. add layers to graph
    graph.add(markerLayer);

    // 4. draw graph
    d3.select('#'+div_id).call(graph.draw);

    var zoomLayer = wavesUI.zoomer()
        .select('#'+div_id)
        .on('mousemove', function(e) {
        // update graph xZoom
        graph.xZoom(e);
        })
        .on('mouseup', function(e) {
            // set the final xZoom value of the graph
            graph.xZoomSet();
        });

    // to update the data, add it to the data array and redraw the graph
    $('#add-data').on('click', function(e) {
        e.preventDefault();

        var datum = {
            start: 2,
            duration: 1,
            height: 1000
        };

        data.push(datum);
        graph.update();
    });
}
