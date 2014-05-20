/*
 * Copyright (C) 2007-2011 Parisson
 * Copyright (c) 2011 Riccardo Zaccarelli <riccardo.zaccarelli@gmail.com>
 * Copyright (c) 2010 Olivier Guilyardi <olivier@samalyse.com>
 *
 * This file is part of TimeSide.
 *
 * TimeSide is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * TimeSide is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Authors: Riccardo Zaccarelli <riccardo.zaccarelli@gmail.com>
 *          Olivier Guilyardi <olivier@samalyse.com>
 */

/**
 * Class representing a RulerMarker in TimesideUI
 * Requires jQuery Raphael and all associated player classes. rulerDiv position MUST be relative
 * (if this class is called from within player, it is)
 */

Timeside.classes.RulerMarker = Timeside.classes.TimesideClass.extend({

    
    init: function(ruler, waveImgDiv, className) {
        this._super();
        var rulerDiv = ruler.getRulerContainer();
        var $J = this.$J;

        var tooltip = '';

        var cssPref = this.cssPrefix;

        var label = $J('<a/>')
        .addClass(cssPref + className)
        .css({
            display: 'block',
            textAlign: 'center',
            position: 'absolute',
            zIndex: 1000
        }).append($J('<span/>')).attr('href', '#');
        
        if (tooltip){
            label.attr('title', tooltip);
        }
        rulerDiv.append(label);

        //rulerDiv MUST HAVE POSITON relative or absolute (it is relative, see player.resize)
        if(className != "pointer"){
            label.css('bottom','0');
        }else{
            label.css('top','0');
        }
        
        //set the index,
        var index = -1;
        this.setIndex = function(idx, optionalUpdateLabelWidth){
            index = idx;
            this.setText(idx+1, optionalUpdateLabelWidth ? true : false);
        };
        this.getIndex = function(){
            return index;
        };

        //end=======================================================
        //creating public methods:
        this.getLabel = function(){
            return label;
        };


        this.getRulerWidth = function(){
            return rulerDiv.width();
        };
        this.getWaveHeight = function(){
            return waveImgDiv.height();
        };

        this.positionInPixels = 0;
        this.positionAsViewerRatio = 0;

        var arrowBaselineWidth = 9;

        var canvas = undefined;
        var canvasClass = cssPref + 'svg-'+className+'-line';
        var vml = this.$TU.vml; //if vml, this class is populated with methods and NOT undefined
        var round = Math.round;
        if(!vml){
            canvas = this.createCanvasSvg(waveImgDiv, arrowBaselineWidth);
            var path = canvas.childNodes[0]; //note that $J(canvas).find('path') does not work in FF at least 3.5
            path.setAttributeNS(null,'class',canvasClass);
            this.moveCanvas = function(pixelOffset){
                pixelOffset = round(pixelOffset);
                canvas.setAttributeNS( null, "transform", "translate("+pixelOffset+",0)");
            };
            this.jQueryCanvas = $J(canvas);
        }else{
            canvas = this.createCanvasVml(waveImgDiv, arrowBaselineWidth);
            this.jQueryCanvas = $J(canvas.node);
            var attributes = vml.getVmlAttr(canvasClass);
            canvas.attr(attributes); //Raphael method
            this.moveCanvas = function(pixelOffset){
                pixelOffset = round(pixelOffset);
                //for some reason, coordinates inside the VML object are stored by raphael with a zoom of 10:
                this.jQueryCanvas.css('left',(10*pixelOffset)+'px');
            };
            //apparently, when resizing the markers loose their attributes. Therefore:
            var r = this.refreshPosition; //reference to current refreshPosition
            this.refreshPosition = function(){
                r.apply(this);
                canvas.attr(attributes);
            }
        }
    },
    
    //sets the text of the marker, if the text changes the marker width and optionalUpdateLabelPosition=true,
    //re-arranges the marker position to be center-aligned with its vertical line (the one lying on the wav image)
    setText: function(text, optionalUpdateLabelPosition) {
        var label = this.getLabel();
        if (label) {
            var oldWidth = label.width();
            label.find('span').html(text);
            var labelWidth = label.width();
            if(oldWidth != labelWidth && optionalUpdateLabelPosition){
                this.refreshLabelPosition();
            }
        }
        return this;
    },
    
    //these methods are executed only if marker is movable (see Ruler.js)
    move : function(pixelOffset) {
        var width =  this.getRulerWidth();
        if (this.positionInPixels != pixelOffset) {
            if (pixelOffset < 0) {
                pixelOffset = 0;
            } else if (pixelOffset >= width) {
                pixelOffset = width - 1;
            }
           //defined in the init method (it depends on wehter the current browser supports SVG or not)
            this.moveCanvas(pixelOffset);
           
            this.positionInPixels = pixelOffset;
            this.refreshLabelPosition(width);
            //store relative position (see refreshPosition below)
            this.positionAsViewerRatio = pixelOffset == width-1 ? 1 : pixelOffset/width;
        }
        return this;
    },

    refreshLabelPosition : function(optionalContainerWidth){
        if(!(optionalContainerWidth)){
            optionalContainerWidth = this.getRulerWidth();
        }
        var label = this.getLabel();
        var width = optionalContainerWidth;
        var pixelOffset = this.positionInPixels;
        var labelWidth = label.outerWidth(); //consider margins and padding
        var labelPixelOffset = pixelOffset - labelWidth / 2;
        if (labelPixelOffset < 0){
            labelPixelOffset = 0;
        }else if (labelPixelOffset + labelWidth > width){
            labelPixelOffset = width - labelWidth;
        }
        label.css({
            left: this.mRound(labelPixelOffset) + 'px'
        });

    },

    //function called on ruler.resize. Instead of recreating all markers, simply redraw them
    refreshPosition : function(){
        var width =  this.getRulerWidth();
        //store relativePosition:
        var rp = this.positionAsViewerRatio;
        this.move(this.mRound(this.positionAsViewerRatio*width));
        //reset relative position, which does not have to change
        //but in move might have been rounded:
        this.positionAsViewerRatio = rp;
    },

    
    remove : function() {
        var label = this.getLabel();
        label.remove();
        this.jQueryCanvas.remove(); //defined in the constructor
        return this;
    },


    createCanvasSvg: function(container, arrowBaseWidth){
        //create svg. Note that elements must be created within a namespace (createElementNS)
        //and attributes must be set via .setAttributeNS(null,name,value)
        //in other words, jQuery does not work (maybe in future releases)
        var $J = this.$J;
        var svgNS = "http://www.w3.org/2000/svg";
        var d = document;
        var svg = undefined;
        if(container.children().length>0){
            svg = container.children().get(0);
        }else{
            svg = d.createElementNS(svgNS, "svg:svg");
            container.append($J(svg));
        }
            var group = d.createElementNS(svgNS, "svg:g");
            group.setAttributeNS( null, "transform", "translate(0,0)");

            var path = d.createElementNS(svgNS, "svg:path");
            path.setAttributeNS( null, "d", this.createCanvasPath(0,arrowBaseWidth));
            
            group.appendChild(path);
            svg.appendChild(group);
       
        return group; //return the group, not the path, as it is the group that will be translated when moving
    },

    createCanvasVml: function(container, arrowBaseWidth){
        var vml = this.$TU.vml;
        var paper = vml.Raphael(container.get(0),container.width(),container.height());
        var shape = paper.path(this.createCanvasPath(0, arrowBaseWidth));
        return shape;
    },

    //w must be odd. Cause the central line must be centered. Example:
    //
    //      xxxxx
    //       xxx
    //        x
    //        x
    //        x
    //
    createCanvasPath: function(x,w){
        var halfW = w >>> 1;
        //in order to calculate the line height, we could simply set the wave height. However, due to potential
        //resizing afterwards, the line could not stretch till the bottom (if it overflows it's fine, as the wave div container has 
        //overflow = hidden). As we do not want to rebuild the canvas on resize,
        //we assess an height which will 99% overflow the wave height in any case.
        //We use the wave height and the window height, and take 2 times
        //the maximum of those heights:
        var wdwH = this.$J(window).height();
        var waveH = this.getWaveHeight();
        var h = 2* (wdwH > waveH ? wdwH : waveH);
        return 'M '+(x-halfW)+' 0 L '+(x)+' '+(halfW)+' L '+x+' '+h+
        ' L '+ (x+1)+' '+h+' L '+(x+1)+ ' '+(halfW)+' L '+(x+halfW+1)+' 0 z';
    },

    //used for faster lookup
    mRound: Math.round

});
