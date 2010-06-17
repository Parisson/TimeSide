/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N) {

$N.Class.create("SoundProvider", $N.Core, {
    sound: null,
    timer: null,
    buggyPosition: null,
    isDurationForced: false,
    state: {
        position: null,
        duration: null,
        playing: false,
        buffering: false
    },
    lastState: null,

    initialize: function($super, cfg) {
        $super();
        this.configure(cfg, {
            source: null,
            duration: null
        });
        this.sound = this.cfg.source;
        if (this.cfg.duration) {
            this.forceDuration(this.cfg.duration);
        }
        this.state.position = 0;
        this.update = this.attach(this._update);
        this.timer = setInterval(this.update, 43);
    },

    free: function($super) {
        this.sound = null;
        $super();
    },

    play: function() {
        if (this.sound) {
            if (!this.sound.playState) {
                this.sound.play();
            } else if (this.sound.paused) {
                this.sound.resume();
            }
        }
        return this;
    },

    pause: function() {
        if (this.sound)
            this.sound.pause();
        return this;
    },

    seek: function(offset) {
        if (this.sound) {
            this.sound.setPosition(offset * 1000);
            if (!this.state.playing) {
                this.buggyPosition = this.sound.position / 1000;
                this.state.position = offset;
            }
        }
        return this;
    },

    isPlaying: function() {
        return this.state.playing;
    },

    getPosition: function() {
        if (this.state.position == null)
            this._retrieveState();
        return this.state.position;
    },

    getDuration: function() {
        if (this.state.duration == null)
            this._retrieveState();
        return this.state.duration;
    },

    forceDuration: function(duration) {
        this.state.duration = duration;
        this.isDurationForced = true;
    },

    isBuffering: function() {
        return this.state.buffering;
    },

    _retrieveState: function() {
        if (this.sound) {
            this.state.playing = (this.sound.playState && !this.sound.paused);
            if (this.state.playing) {
                var position = this.sound.position / 1000;
                if (position != this.buggyPosition) {
                    this.state.position = position;
                    this.buggyPosition = null;
                }
            }
            if (!this.isDurationForced) {
                if (this.sound.readyState == 1) {
                    this.state.duration = this.sound.durationEstimate / 1000;
                } else {
                    this.state.duration = this.sound.duration / 1000;
                }
            }
            this.state.buffering = (this.sound.readyState == 1 && this.state.position > this.sound.duration / 1000);
        }
    },

    _update: function() {
        this._retrieveState();
        var updated = false;
        if (this.lastState) {
            for (k in this.state) {
                if (this.state[k] != this.lastState[k]) {
                    updated = true;
                    break;
                }
            }
        } else {
            this.lastState = {};
            updated = true;
        }
        if (updated) {
            for (k in this.state) {
                this.lastState[k] = this.state[k];
            }
            this.fire('update');
        }
    },

    setSource: function(source) {
        this.debug("setting source");
        this.sound = source;
        return this;
    }

});

$N.notifyScriptLoad();

});
