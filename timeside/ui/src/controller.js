/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N) {

    $N.Class.create("Controller", $N.Core, {

        initialize: function($super, cfg) {
            $super();
            this.configure(cfg, {
                player: null,
                soundProvider: null,
                map: null,
                divmarkers:[]
            });
            if (this.cfg.player && !$N.isInstanceOf(this.cfg.player, 'Player')) {
                this.cfg.player = new $N.Player(this.cfg.player);
            }
            this._setupPlayer();
        //setting the divmarkers
        //this.cfg.map.observe('add')
            
        },

        _setupPlayer: function() {
            
            this.cfg.player
            .setSoundProvider(this.cfg.soundProvider)
            .setMarkerMap(this.cfg.map)
            .observe('play', $N.attachFunction(this.cfg.soundProvider, this.cfg.soundProvider.play))
            .observe('pause', $N.attachFunction(this.cfg.soundProvider, this.cfg.soundProvider.pause))
            .observe('move', this.attach(this._onMove))
            .observe('markeradd', this.attach(this._onMarkerAdd))
            //player markermove listens for changes of ruler markermove which listens
            //foir changes in each marker move
            .observe('markermove', this.attach(this._onMarkerMove))
            
            .draw();
            this.loadHTTP();

            this.cfg.map.observe('add',this.attach(this._onMarkerMapAdd));
            this.cfg.map.observe('remove',this.attach(this._onMarkerMapRemove));
            this.cfg.map.observe('moved',this.attach(this._onMarkerMapMoved));
            
        },


        _onMove: function(e, data) {
            this.cfg.soundProvider.seek(data.offset);
        },

        //called whenever a marker is moved in the ruler BUT NOT in the map
        _onMarkerMove: function(e, data) {
            if (this.cfg.map) {
                $N.Util.selectMarkerTab(); //defined in utils.js
                this.cfg.map.move(data.index, data.offset);
            //this will fire the method below
            }
        },

        _onMarkerMapMoved:function(e, data){
            var from = data.fromIndex;
            var to = data.toIndex;
            if(from===to){
                //just update the div in order to show the new time offset
                //and start edit
                this.cfg.divmarkers[from].setIndex(to);
                return;
            }
            this.cfg.player.ruler.move(from,to);
            var m = this.cfg.divmarkers.splice(from,1)[0]; //remove
            this.cfg.divmarkers.splice(to,0,m); //add
            this.updateIndices(from,to);
        },

        //called whenever a marker is added to the ruler BUT NOT in the map
        _onMarkerAdd: function(e, data) {
            if (this.cfg.map) {
                $N.Util.selectMarkerTab(); //defined in mediaitem|_detail.html
                var idx = this.cfg.map.add(data.offset); //this will call the method below _onMarkerMapAdd,
                //which btw adds a new div to divmarkers
                //now update the indices for the div (which also sets the event bindings as clicks etc...
                this.updateIndices(idx);
            }
        },
        //fired from markermap, attached as listener above in
        //this.cfg.map.observe('add',this.attach(this._onMarkerMapAdd));
        //this method basically adds the html elements, but updateIndices must be called elsewhere after this function
        //(see _onMarkerAdd and loadHTTP)
        _onMarkerMapAdd: function(e, data) {
            if (this.cfg.map) {
                //$N.Util.selectMarkerTab(); //defined in mediaitem|_detail.html
                //this.refreshMarkersText(this.cfg.map);
                //var idx = this.cfg.map.add(data.offset);
                //alert('df');
                var idx = data.index;
                var divMarker = new $N.DivMarker(this.cfg.map);
                this.cfg.divmarkers.splice(idx,0, divMarker);
                this.cfg.player.ruler.add(data.marker, idx);
            }
        },

        //fired from markermap, attached as listener above in
        //this.cfg.map.observe('add',this.attach(this._onMarkerMapAdd));
        _onMarkerMapRemove: function(e, data) {
            if (this.cfg.map) {
                //$N.Util.selectMarkerTab(); //defined in mediaitem|_detail.html
                //this.refreshMarkersText(this.cfg.map);
                //var idx = this.cfg.map.add(data.offset);
                //alert('df');
                var idx = data.index;
                var divRemoved = this.cfg.divmarkers.splice(idx,1)[0]; //there is only one element removed
                divRemoved.remove();
                this.cfg.player.ruler.remove(idx);
                this.updateIndices(idx);
            }
        },

        updateIndices: function(from, to){
            if(from===undefined || from==null){
                from = 0;
            }
            var len = this.cfg.divmarkers.length-1;
            if(from>len){
                //it might happen when we remove the last element
                //suppose [0,1,2], we remove [2] then we call
                //updateIndices[2] but array till 1 (there is nothing to update)
                return;
            }
            if(to==undefined || to ==null){
                to = len;
            }
            if(to<from){
                var tmp = to;
                to=from;
                from=tmp;
            }
            for(var i = from; i <= to; i++){
                this.cfg.divmarkers[i].setIndex(i);
            }
            this.cfg.player.ruler.updateMarkerIndices(from,to);
        },


        loadHTTP: function(){

            //itemid is the item (spund file) name
            var sPath = window.location.pathname;
            //remove last "/" or last "/#", if any...
            sPath = sPath.replace(/\/#*$/,"");
            var itemid = sPath.substring(sPath.lastIndexOf('/') + 1);

            //WARNING: use single quotes for the whole string!!
            //see http://stackoverflow.com/questions/4809157/i-need-to-pass-a-json-object-to-a-javascript-ajax-method-for-a-wcf-call-how-can
            var data2send = '{"id":"jsonrpc","params":["'+itemid+'"], "method":"telemeta.get_markers","jsonrpc":"1.0"}';
            var map = this.cfg.map;
            var update = this.updateIndices;
            var me = this;
            $.ajax({
                type: "POST",
                url: '/json/',
                contentType: "application/json",
                data: data2send,
                dataType: "json",
                success: function(data) {
                    if(data){
                        if(data.result && data.result.length>0){
                            var result = data.result;
                            
                            for(var i =0; i< result.length; i++){
                                map.add(result[i]);
                            }
                            //we call now updateindices
                            update.apply(me);
                            
                        }
                        
                    }
                    //We call mediaitem_detail.setUpTabs from controller once all markers have been loaded
                    //this because setLabelDescription, which sets the label text according to the div width,
                    //needs to have all elements visible.
                    $N.Util.setUpTabs();
                //setUpTabs(); //which hides the marker div. Call with argument 1 to set up marker div
                //as visible as startup
                }
            });
        //var g = 9;
        }

    

    });

    $N.notifyScriptLoad();

});
