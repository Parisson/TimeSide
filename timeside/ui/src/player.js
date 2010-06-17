/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N, $J) {

$N.Class.create("Player", $N.Core, {
    skeleton: {
        'div.viewer': {
            'div.ruler': {}, 
            'div.wave': {
                'div.image-canvas': {},
                'div.image-container': ['img.image']
            }
        },
        'div.control': {
            'div.layout': {
                'div.playback': ['a.play', 'a.pause', 'a.rewind', 'a.forward', 'a.set-marker']
            }
        }/*,
        'div.marker-control': ['a.set-marker']*/
    },
    defaultContents: {
        play: 'Play',
        pause: 'Pause',
        rewind: 'Rewind',
        forward: 'Forward',
        'set-marker': 'Set marker'
    },
    elements: {},
    ruler: null,
    soundProvider: null,
    map: null,
    container: null,
    imageWidth: null,
    imageHeight: null,

    initialize: function($super, container, cfg) {
        $super();
        if (!container)
            throw new $N.RequiredArgumentError(this, 'container');
        this.container = $J(container);
        this.configure(cfg, {
            image: null
        });
    },

    free: function($super) {
        this.elements = null;
        this.container = null;
        $super();
    },

    setSoundProvider: function(soundProvider) {
        this.soundProvider = soundProvider;
        return this;
    },

    setMarkerMap: function(map) {
        this.map = map;
        return this;
    },

    setImage: function(expr) {
        this.cfg.image = expr;
        this.refreshImage();
    },

    refreshImage: function() {
        var src = null;
        if (typeof this.cfg.image == 'function') {
            src = this.cfg.image(this.imageWidth, this.imageHeight);
        } else if (typeof this.cfg.image == 'string') {
            src = this.cfg.image;
        }

        if (src) 
            this.elements.image.attr('src', src);
    },

    draw: function() {
        this.debug('drawing');
        $N.domReady(this.attach(this._setupInterface));
        return this;
    },

    _setupInterface: function() {
        this.elements = $N.Util.loadUI(this.container, this.skeleton, this.defaultContents);

        // IE apparently doesn't send the second mousedown on double click:
        var jump = $J.browser.msie ? 'mousedown dblclick' : 'mousedown';
        this.elements.rewind.attr('href', '#').bind(jump, this.attach(this._onRewind))
            .click(function() {return false; });
        this.elements.forward.attr('href', '#').bind(jump, this.attach(this._onForward))
            .click(function() {return false; });
        this.elements.pause.attr('href', '#').bind('click', this.attach(this._onPause));
        this.elements.play.attr('href', '#').bind('click', this.attach(this._onPlay));
        this.elements.control.find('a').add(this.elements.setMarker)
            .attr('href', '#')
            .each(function(i, a){
                a = $J(a);
                if (!a.attr('title'))
                    a.attr('title', a.text());
            });
            
        //this.elements.markerControl.find('a').attr('href', '#');
        if (this.map) {
            this.elements.setMarker.bind('click', this.attach(this._onSetMarker));
        } else {
            this.elements.setMarker.remove();
        }
        this.ruler = new $N.Ruler({
            viewer: this.elements.viewer,
            map: this.map,
            soundProvider: this.soundProvider
        });
        this.ruler
            .observe('markermove', this.forwardEvent)
            .observe('markeradd', this.forwardEvent)
            .observe('move', this.forwardEvent)
            .draw();
        this.refreshImage();
        this.resize();
        var resizeTimer = null;
        $J(window).resize(this.attach(function() {
            if (resizeTimer)
                clearTimeout(resizeTimer);
            resizeTimer = setTimeout(this.attach(this.resize), 100);
        }));
        //this.container.resize(this.attach(this.resize)); // Can loop ?
    },

    resize: function(overrideHeight) {
        this.debug("resizing");
        var height;
        if (overrideHeight === true) {
            this.debug("override height");
            height = this.elements.image.css('height', 'auto').height();
        } else {
            height = this.elements.wave.height();
            this.debug("wave height:" + height);
            if (!height) {
                this.elements.image.one('load', this.attach(function() {
                    this.resize(true);
                    this.debug("image loaded");
                }));
                height = this.elements.image.height();
            }
        }

        var elements = this.elements.image
            .add(this.elements.imageContainer)
            .add(this.elements.imageCanvas);

        elements.css('width', 'auto'); // for IE6

        if (!height)
            height = 200;
        var style = {
            width: this.elements.wave.width(),
            height: height
        }
        elements.css(style);
        this.imageWidth = style.width;
        this.imageHeight = style.height;
        this.refreshImage();
        this.ruler.resize();
        return this;
    },

    _onRewind: function() {
        var offset = 0;
        if (this.map) {
            var position = this.soundProvider.getPosition();
            var marker = this.map.getPrevious(position);
            if (marker && this.soundProvider.isPlaying() 
                && position - marker.offset < this.ruler.getUnitDuration())
                marker = this.map.getPrevious(marker.offset)
            if (marker) {
                offset = marker.offset;
            }
        }
        this.fire('move', {offset: offset});
        return false;
    },

    _onForward: function() {
        var offset = this.soundProvider.getDuration();
        if (this.map) {
            var marker = this.map.getNext(this.soundProvider.getPosition());
            if (marker) {
                offset = marker.offset;
            }
        }
        this.fire('move', {offset: offset});
        return false;
    },

    _onPlay: function() {
        this.fire('play');
        return false;
    },

    _onPause: function() {
        this.fire('pause');
        return false;
    },

    _onSetMarker: function() {
        if (this.map) {
            this.fire('markeradd', {offset: this.soundProvider.getPosition()});
        }
        return false;
    }
});

$N.notifyScriptLoad();

});
