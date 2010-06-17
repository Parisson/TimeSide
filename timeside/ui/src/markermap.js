/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N, $J) {

$N.Class.create("MarkerMap", $N.Core, {
    markers: null,

    initialize: function($super, markers) {
        $super();
        if (!markers)
            markers = [];
        this.markers = markers;
    },

    toArray: function() {
        return [].concat(this.markers);
    },

    byIndex: function(index) {
        return this.markers[index];
    },

    byId: function(id) {
        var marker = null;
        for (var i in this.markers) {
            if (this.markers[i].id == id) {
                marker = this.markers[i];
                break;
            }
        }
        return marker;
    },

    indexOf: function(marker) {
        var index = null;
        for (var i in this.markers) {
            if (this.markers[i].id == marker.id) {
                index = parseInt(i);
                break;
            }
        }
        return index;
    },

    _reorder: function() {
        this.markers.sort(this.compare);
        for (var i in this.markers) {
            this.fire('indexchange', {marker: this.markers[i], index: parseInt(i)});
        }
    },

    add: function(offset, desc) {
        var id = this.uniqid();
        var marker = {id: id, offset: offset, desc: desc};
        var i = this.markers.push(marker) - 1;
        this.fire('add', {marker: marker, index: i});
        this._reorder();
        return marker;
    },

    remove: function(marker) {
        if (marker) {
            var i = this.indexOf(marker);
            this.markers.splice(i, 1);
            this.fire('remove', {marker: marker});
            this._reorder();
        }
        return marker;
    },

    compare: function(marker1, marker2) {
        if (marker1.offset > marker2.offset)
            return 1;
        if (marker1.offset < marker2.offset)
            return -1;
        return 0;
    },

    move: function(marker, offset) {
        oldMarkers = [].concat(this.markers);
        marker.offset = offset;
        this._reorder();
    },

    getPrevious: function(offset, skip) {
        var marker = null;
        if (!skip) skip = 0;
        markers = [].concat(this.markers).reverse();
        $J(markers).each(function(i, m) {
            if (offset > m.offset && !(skip--)) {
                marker = m;
                return false;
            }
        });
        return marker;
    },

    getNext: function(offset, skip) {
        var marker = null;
        if (!skip) skip = 0;
        $J(this.markers).each(function(i, m) {
            if (offset < m.offset && !(skip--)) {
                marker = m;
                return false;
            }
        });
        return marker;
    },

    each: function(callback) {
        $J(this.markers).each(callback);
    }
});

$N.notifyScriptLoad();

});
