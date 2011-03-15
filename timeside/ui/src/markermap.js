/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com> and Riccardo Zaccarelli
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N, $J) {

    $N.Class.create("MarkerMap", $N.Core, {
        markers: null,
        //the main div container:
        divContainer: $J("#markers_div_id"),
        initialize: function($super, markers) {
            $super();
            if (!markers){
                markers = [];
            }
            this.markers = markers;
        },
   
        get: function(index){
            return this.markers[index];

        },


        add: function(obj) {
            var marker = this.createMarker(obj);
            var idx = this.indexOf(marker);
            
            //adding the div
            //marker.div = this.createDiv(marker,idx);
            //setting focus and label description
            //set label description
            //this.setLabelDescription(marker);
            //finally, set the focus to the text
            //this.getHtmElm(marker,this.MHE_DESCRIPTION_TEXT).focus();


            this.markers.splice(idx,0,marker);
            //notifies controller.onMarkerMapAdd
            this.fire('add', {
                marker: marker,
                index: idx
            });
            //this.fireRefreshLabels(idx+1,this.markers.length);
            //this._reorder(marker.offset);
            //this.fireEditMode(marker);
            return idx;
        },
        //argument is either an object loaded from server or a number specifying the marker offset
        createMarker: function(argument){
            var marker = null;
            if(typeof argument == 'object'){
                var editable = CURRENT_USER_NAME === argument.author;
                marker = {
                    id: argument.public_id,
                    offset: argument.time,
                    desc: argument.description,
                    title: argument.title,
                    author: argument.author,
                    isEditable: editable,
                    isSaved: true

                };
            }else if(typeof argument == 'number'){
                marker = {
                    id: undefined, //before was: this.uniqid(),
                    //now an undefined id means: not saved on server (see sendHTTP below)
                    offset: parseFloat(argument),
                    desc: "",
                    title: "",
                    author: CURRENT_USER_NAME,
                    isEditable: true,
                    isSaved: false
                };
            }
            return marker;

        },

        remove: function(index) {
            var marker = this.get(index);
            if (marker) {
                if(marker.isSaved){
                    this.removeHTTP(marker);
                }
                this.markers.splice(index, 1);
                //notifies controller.js
                this.fire('remove', {
                    index: index
                });
            }
            return marker;
        },

        move: function(markerIndex, newOffset){
            var newIndex = this.indexOf(newOffset);
            
            //if we moved left to right, the insertion index is actually
            //newIndex-1, as we must also consider to remove the current index markerIndex, so:
            if(newIndex>markerIndex){
                newIndex--;
            }
            //this way, we are sure that if markerIndex==newIndex we do not have to move,
            //and we can safely first remove the marker then add it at the newIndex without
            //checking if we moved left to right or right to left
            var marker = this.markers[markerIndex];
            marker.offset = newOffset;
            marker.isSaved = marker.isEditable ? false : true;
            if(newIndex != markerIndex){
                this.markers.splice(markerIndex,1);
                this.markers.splice(newIndex,0,marker);
            }
            this.fire('moved', {
                fromIndex: markerIndex,
                toIndex: newIndex
            });
        },
        //
        //The core search index function: returns insertionIndex if object is found according to comparatorFunction,
        //(-insertionIndex-1) if object is not found. This assures that if the returned
        //number is >=0, the array contains the element, otherwise not and the element can be inserted at
        //-insertionIndex-1
        insertionIndex: function(object){
            var offset;
            if(typeof object == 'object'){
                offset = object.offset;
            }else if(typeof object == 'number'){
                offset = object;
            }else{ //to be sure...
                offset = parseFloat(object);
            }
            var pInt = parseInt; //reference to parseInt (to increase algorithm performances)
            var comparatorFunction = function(a,b){
                return (a<b ? -1 : (a>b ? 1 : 0));
            };
            var data = this.markers;
            var low = 0;
            var high = data.length-1;

            while (low <= high) {
                //int mid = (low + high) >>> 1;
                var mid = pInt((low + high)/2);
                var midVal = data[mid];
                var cmp = comparatorFunction(midVal.offset,offset);
                if (cmp < 0){
                    low = mid + 1;
                }else if (cmp > 0){
                    high = mid - 1;
                }else{
                    return mid; // key found
                }
            }
            return -(low + 1);  // key not found
        },
        //indexOf is the same as insertionIndex, but returns a positive number.
        //in other words, it is useful when we do not want to know if obj is already present
        //in the map, but only WHERE WOULD be inserted obj in the map. obj can be a marker
        //or an offset (time). In the latter case a dummy marker with that offset will be considered
        indexOf: function(obj){
            var idx = this.insertionIndex(obj);
            return idx<0 ? -idx-1 : idx;
        },
        each: function(callback) {
            $J(this.markers).each(callback);
        },
        //        length: function(){
        //            return this.markers ? this.markers.length : 0;
        //        },
       

        sendHTTP: function(marker, functionOnSuccess, showAlertOnError){

            //itemid is the item (spund file) name
            var sPath = window.location.pathname;
            //remove last "/" or last "/#", if any...
            sPath = sPath.replace(/\/#*$/,"");
            var itemid = sPath.substring(sPath.lastIndexOf('/') + 1);

            //WARNING: use single quotes for the whole string!!
            //see http://stackoverflow.com/questions/4809157/i-need-to-pass-a-json-object-to-a-javascript-ajax-method-for-a-wcf-call-how-can
            //            var data2send = '{"id":"jsonrpc", "params":[{"item_id":"'+ itemid+'", "public_id": "'+marker.id+'", "time": "'+
            //            marker.offset+'","description": "'+marker.desc+'"}], "method":"telemeta.add_marker","jsonrpc":"1.0"}';
           
            var isSaved = marker.id !== undefined;
            if(!isSaved){
                marker.id=this.uniqid(); //defined in core;
            }
            var method = isSaved ? "telemeta.update_marker" : "telemeta.add_marker";
            
            var s = this.jsonify;
            var data2send = '{"id":"jsonrpc", "params":[{"item_id":"'+ s(itemid)+
            '", "public_id": "'+s(marker.id)+'", "time": "'+s(marker.offset)+
            '", "author": "'+s(marker.author)+
            '", "title": "'+s(marker.title)+
            '","description": "'+s(marker.desc)+'"}], "method":"'+method+'","jsonrpc":"1.0"}';

            $.ajax({
                type: "POST",
                url: '/json/',
                contentType: "application/json",
                data: data2send,
                success: function(){
                    if(!isSaved){
                        marker.isSaved = true;
                    }
                    if(functionOnSuccess){
                        functionOnSuccess();
                    }
                },
                error: function(jqXHR, textStatus, errorThrown){
                    if(showAlertOnError){
                        var details = "\n(no further info available)";
                        if(jqXHR) {
                            details="\nThe server responded witha status of "+jqXHR.status+" ("+
                                jqXHR.statusText+")\n\nDetails (request responseText):\n"+jqXHR.responseText;
                        }
                        alert("ERROR: Failed to save marker"+details);
                    }
                }
            });

            
        },

        jsonify: function(string){
            var s = string;
            if(typeof string == "string"){
                s = string.replace(/\\/g,"\\\\")
                .replace(/\n/g,"\\n")
                .replace(/"/g,"\\\"");
            }
            return s;
        },
        removeHTTP: function(marker){

            //  //itemid is the item (spund file) name
            //  var sPath = window.location.pathname;
            //  //remove last "/" or last "/#", if any...
            //  sPath = sPath.replace(/\/#*$/,"");
            //  var itemid = sPath.substring(sPath.lastIndexOf('/') + 1);
            var public_id = marker.id;
            //WARNING: use single quotes for the whole string!!
            //see http://stackoverflow.com/questions/4809157/i-need-to-pass-a-json-object-to-a-javascript-ajax-method-for-a-wcf-call-how-can
            var data2send = '{"id":"jsonrpc","params":["'+public_id+'"], "method":"telemeta.del_marker","jsonrpc":"1.0"}';
            //            var map = this.cfg.map;
            //            var me = this;
            $.ajax({
                type: "POST",
                url: '/json/',
                contentType: "application/json",
                data: data2send,
                dataType: "json"
            
            });
            var g = 9;
        }

    });

    $N.notifyScriptLoad();

});
