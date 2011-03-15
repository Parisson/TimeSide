/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N, $J) {

    $N.Class.create("Marker", $N.Core, {
        id: null,
        painter: null,
        visible: false,
        position: 0,
        label: null,
        blinking: false,
        nodes: null,
        mouseDown: false,
        blinkAnimation: null,

        initialize: function($super, cfg) {
            $super();
            //sets the fields required???? see ruler.js createPointer
            this.configure(cfg, {
                rulerLayout: [null, 'required'],
                viewer: [null, 'required'],
                fontSize: 10,
                zIndex: null,
                className: [null, 'required'],
                index: null,
                tooltip: null,
                canMove: false
            });
            this.cfg.rulerLayout = $J(this.cfg.rulerLayout);
            this.cfg.viewer = $J(this.cfg.viewer);

            this.width = this.cfg.viewer.width();
            this.painter = new jsGraphics(this.cfg.viewer.get(0));
            this._create();
            if(this.cfg.canMove){
                this._observeMouseEvents();
            }
            //if it is the pointer, cfg.index is undefined
            if(cfg.index !== undefined && cfg.className!='pointer'){
                this.setIndex(cfg.index);
            }
        },

        setIndex: function(index){
            this.index = index;
            this.setText(index+1);
        },

        free: function($super) {
            this.cfg.rulerLayout = null;
            this.cfg.viewer = null;
            $super();
        },

        clear: function() {
            this.painter.clear();
            $J(this.painter.cnv).remove();
            this.label.remove();
            return this;
        },

        _create: function() {
            this.debug('create marker');
            var y = this.cfg.rulerLayout.find('.' + $N.cssPrefix + 'label').outerHeight();
            this.label = $J('<a/>')
            .css({
                display: 'block',
                width: '10px', 
                textAlign: 'center', 
                position: 'absolute', 
                fontSize: this.cfg.fontSize + 'px', 
                fontFamily: 'monospace', 
                top: y + 'px'
            })
            .attr('href', '#')
            .addClass($N.cssPrefix + this.cfg.className)
            .append('<span />')
            .hide();

            if (this.cfg.tooltip){
                this.label.attr('title', this.cfg.tooltip);
            }
            this.cfg.rulerLayout.append(this.label);

            var height = this.cfg.viewer.height();
            var x = 0;
            this.painter.drawLine(x, 0, x, height);
            x     = [-4, 4, 0];
            var y = [0, 0, 4];
            this.painter.fillPolygon(x, y);
            this.painter.paint();
            this.nodes = $J(this.painter.cnv).children();

            var style = {};
            if (this.cfg.zIndex) {
                style.zIndex = this.cfg.zIndex;
                this.label.css(style);
            }
            style.backgroundColor = '';

            this.nodes.hide().css(style).addClass($N.cssPrefix + this.cfg.className)
            .each(function(i, node) {
                node.originalPosition = parseInt($J(node).css('left'));
            });
        },

        setText: function(text) {
            if (this.label) {
                text += '';
                var labelWidth = this._textWidth(text, this.cfg.fontSize) + 10;
                labelWidth += 'px';
                if (this.label.css('width') != labelWidth) {
                    this.label.css({
                        width: labelWidth
                    });
                }
                this.label.find('span').html(text);
            }
            return this;
        },

        move: function(pixelOffset) {
            if (this.position != pixelOffset) {
                if (pixelOffset < 0) {
                    pixelOffset = 0;
                } else if (pixelOffset >= this.width) {
                    pixelOffset = this.width - 1;
                }
                this.nodes.each(function(i, node) {
                    $J(node).css('left', Math.round(node.originalPosition + pixelOffset) + 'px');
                });
                var labelWidth = this.label.width();
                var labelPixelOffset = pixelOffset - labelWidth / 2;
                if (labelPixelOffset < 0)
                    labelPixelOffset = 0;
                else if (labelPixelOffset + labelWidth > this.width)
                    labelPixelOffset = this.width - labelWidth;
                this.label.css({
                    left: Math.round(labelPixelOffset) + 'px'
                });
                this.position = pixelOffset;
            }
            return this;
        },

        show: function(offset) {
            if (!this.visible) {
                this.nodes.show();
                this.label.show();
                this.visible = true;
            }
            return this;
        },

        hide: function() {
            this.nodes.hide();
            this.label.hide();
            this.visible = false;
            return this;
        },

        isVisible: function() {
            return this.visible;
        },

        blink: function(state) {
            var speed = 200;
            if (this.label && this.blinking != state) {
                var span = this.label.find('span');

                span.stop();

                function fade(on) {
                    if (on) {
                        span.animate({
                            opacity: 1
                        }, speed, null,
                        function() {
                            fade(false)
                        });
                    } else {
                        span.animate({
                            opacity: 0.4
                        }, speed, null,
                        function() {
                            fade(true)
                        })
                    }
                }

                if (state) {
                    fade();
                } else {
                    span.animate({
                        opacity: 1
                    }, speed);
                }

                this.blinking = state;
            }
            return this;
        },

        _onMouseDown: function(evt) {
            this.mouseDown = true;
            this._onMouseMove(evt);
            return false;
        },

        _onMouseMove: function(evt) {
            if (this.mouseDown) {
                var offset = (evt.pageX - this.cfg.rulerLayout.offset().left);
                this.move(offset);
                this.fire('move', { //calls move (see above)
                    offset: this.position,
                    finish: false
                });
                return false;
            }
        },

        _onMouseUp: function(evt) {
            if (this.mouseDown) {
                this.mouseDown = false;
                this.fire('move', {
                    index: this.index,
                    offset: this.position,
                    finish: true
                });
                return false;
            }
        },

        _observeMouseEvents: function() {
            this.label.mousedown(this.attachWithEvent(this._onMouseDown))
            .bind('click dragstart', function() {
                return false;
            });
            this.cfg.rulerLayout.mousemove(this.attachWithEvent(this._onMouseMove));
            this.cfg.rulerLayout.mouseup(this.attachWithEvent(this._onMouseUp));
            $J(document).mouseup(this.attachWithEvent(this._onMouseUp));
        }

    //    _toString: function() {
    //        return "<marker id="+id+" position="+position+" description=\""+
    //            +description+"\"/>";
    //    }


    });

    $N.notifyScriptLoad();

});
