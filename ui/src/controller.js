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
            map: null
        });
        if (this.cfg.player && !$N.isInstanceOf(this.cfg.player, 'Player')) {
            this.cfg.player = new $N.Player(this.cfg.player);
        }
        this._setupPlayer();
    },

    _setupPlayer: function() {
        this.cfg.player
            .setSoundProvider(this.cfg.soundProvider)
            .setMarkerMap(this.cfg.map)
            .observe('play', $N.attachFunction(this.cfg.soundProvider, this.cfg.soundProvider.play))
            .observe('pause', $N.attachFunction(this.cfg.soundProvider, this.cfg.soundProvider.pause))
            .observe('move', this.attach(this._onMove))
            .observe('markeradd', this.attach(this._onMarkerAdd))
            .observe('markermove', this.attach(this._onMarkerMove))
            .draw();
    },

    _onMove: function(e, data) {
        this.cfg.soundProvider.seek(data.offset);
    },

    _onMarkerMove: function(e, data) {
        if (this.cfg.map) {
            this.cfg.map.move(this.cfg.map.byId(data.id), data.offset);
        }
    },

    _onMarkerAdd: function(e, data) {
        if (this.cfg.map) {
            this.cfg.map.add(data.offset, 'marker at ' + data.offset);
        }
    }

});

$N.notifyScriptLoad();

});
