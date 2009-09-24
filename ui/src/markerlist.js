/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N) {

$N.Class.create("MarkerList", $N.Core, {
    initialize: function($super, cfg) {
        $super();
        this.cfg = this.configure(cfg, {
            container: null,
            map: null
        });
    },

    _buildItem: function(marker) {
        var dt = new Element('dt');
        var time = $N.Util.makeTimeLabel(marker.offset);


    },

    _setupInterface: function() {
    }
});

$N.notifyScriptLoad();

});
