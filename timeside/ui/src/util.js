/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N, $J) {

    $N.Util = {
        _loadChild: function(container, tag, className, index, contents) {
            var p = $N.cssPrefix;
            var element = container.find('.' + p + className);
            if (!element.length) {
                element = $J(document.createElement(tag)).addClass(p + className);
                if (contents[className]) {
                    element.text(contents[className]);
                }
                var children = container.children();
                if (index < children.length) {
                    children.eq(index).before(element);
                } else {
                    container.append(element);
                }
            }
            return element;
        },

        _loadUI: function(container, skeleton, contents) {
            var i = 0;
            var elements = {};
            with ($N.Util) {
                if (skeleton[0]) {
                    $J(skeleton).each((function(i, selector) {
                        var s = selector.split('.');
                        elements[$N.Util.camelize(s[1])] = _loadChild(container, s[0], s[1], i++, contents);
                    }));
                } else {
                    for (key in skeleton) {
                        var s = key.split('.');
                        var e = _loadChild(container, s[0], s[1], i++, contents);
                        elements[$N.Util.camelize(s[1])] = e;
                        $N.extend(elements, _loadUI(e, skeleton[key], contents));
                    
                    }
                }
                }
            return elements;
        },

        loadUI: function(container, skeleton, contents) {
            return $N.Util._loadUI($J(container), skeleton, contents);
        },

        makeTimeLabel: function(offset) {
            var minutes = Math.floor(offset / 60);
            if (minutes < 10)
                minutes = '0' + minutes;
            var seconds = Math.floor(offset % 60);
            if (seconds < 10)
                seconds = '0' + seconds;
            return minutes + ':' + seconds;
        },

        camelize: function(str) {
            var parts = str.split('-'), len = parts.length;
            if (len == 1) return parts[0];

            var camelized = str.charAt(0) == '-'
            ? parts[0].charAt(0).toUpperCase() + parts[0].substring(1)
            : parts[0];

            for (var i = 1; i < len; i++)
                camelized += parts[i].charAt(0).toUpperCase() + parts[i].substring(1);

            return camelized;
        },

        setUpTabs:function(selIndex) {//called from within controller.js once all markers have been loaded.
            //this is because we need all divs to be visible to calculate size. selIndex is optional, it defaults to 0
            //
            //declare variables:
            var tabContainerHeight = '5ex'; //height for the tab container
            var tabHeight = '3.5ex'; //height for the tab. Must be lower than tabContainerHeight
            var tabPaddingTop ='.8ex'; //padding top of each tab. Increasing it will increase also the tab height, so
            //compensate by decreasing tabHeight, in case. In any case, must be lower or equal to tabContainerHeight-tabHeight
            var tabWidth = '10ex'; //width of each tab. Each tab from index 1 to n will be at left=n*tabWidth
            var tabBottom ='-1px'; //bottom of each tab. Must be equal and opposite to the border of the div below the tab

            //retrieve tab container:
            var tabContainer = $("#tabs_container"); //change if tabContainer has to be retrieved diferently
            //retrieve the tabs by checking the elements whose class name starts with "tab_"
            //var tabs = $('a[class^="tab_"]'); //change if the tabs have to be determined differently.
            var tabs = tabContainer.find('a[id^="tab_"]');
            //function that retrieves the div relative to a tab (the div will be set visible.invisible according to tab click):
            var tab2div = function(tab){
                return $("#"+tab.attr("name"));
            //ie, returns the element whose id is equal to the tab name.
            //change here if div has to be determined differently
            };
            var selectedTabClassName = "tab_selected"; //change if needed
            var unselectedTabClassName = "tab_unselected"; //change if needed
            var tabClicked = function(index) {
                for(var i=0; i<tabs.length; i++){
                    var t = $(tabs[i]);
                    if(i===index){
                        t.removeClass(unselectedTabClassName).addClass(selectedTabClassName);
                        tab2div(t).fadeIn('slow');
                    }else{
                        t.removeClass(selectedTabClassName).addClass(unselectedTabClassName);
                        tab2div(t).hide();
                    }
                }
                return false; //returning false avoids scroll of the anchor to the top of the page
            //if the tab is an anchor, of course
            };
            //end of variables declaration

            //tabContainer default css:
            tabContainer.css({
                'position':'relative',
                'height':tabContainerHeight
            });
            //tabs default css:
            tabs.css({
                'position':'absolute',
                'height':tabHeight,
                'bottom':tabBottom,
                'paddingTop':tabPaddingTop,
                'width':tabWidth,
                'color': '#000000',
                'left':0, //this will be overridden for tabs from 1 to n (see below)
                'textAlign':'center'
            });
            //setting the left property for all tabs from 1 to n
            var left = parseFloat(tabWidth); //note that 40%, 33.3ex will be converted
            //succesfully to 40 and 33.3 respectively
            if(!isNaN(left)){
                //retrieve the unit
                var s = new String(left);
                var unit = '';
                if(s.length<tabWidth.length){
                    unit = tabWidth.substring(s.length,tabWidth.length);
                }
                for(var i=1; i<tabs.length; i++){
                    $(tabs[i]).css('left',(left*i)+unit);
                }
            }

            for (var i=0;i<tabs.length;i++){
                // introduce a new scope (round brackets)
                //otherwise i is retrieved from the current scope and will be always equal to tabs.length
                //due to this loop
                (function(tabIndex){
                    $(tabs[i]).click(function(){
                        return tabClicked(tabIndex);
                    });
                })(i);
            }

            this.setRoundBorder(tabs,'5px','5px',[0,1]);

            if(!(selIndex)){
                selIndex = 0;
            }
            $(tabs[selIndex]).trigger("click");
        },

        selectMarkerTab: function(){
            $('#tab_markers').trigger("click");
        },
        //set cross browser round borders.
        //elements: the html element or elements (jQuery syntax)
        //hRadius the horizontal radius, or the horizontal vertical radius if the latter is omitted (see below)
        //vRadius OPTIONAL the vertical radius. If missing, it defaults to hRadius
        //angles: OTPIONAL. An array object of the corner indices where to apply radius. Indices are
        //      considered clockwise starting from the top left corner,ie:
        //      0=topleft, 1 topright, 2 bottomright, 3 bottomleft
        //      If missing, it defaults to [0,1,2,3] (all indices)
        setRoundBorder: function(elements, hRadius, vRadius, whichAngles){
            if(!(vRadius)){
                vRadius = hRadius;
            }
            var cssVal = hRadius+' '+vRadius;
            if(!(whichAngles)){
                whichAngles = [0,1,2,3];
            }
            $(elements).each(function(){
                var element = $(this);
                for(var i=0; i<whichAngles.length; i++){
                    var keys=[];
                    if(whichAngles[i]===0){
                        keys=['-webkit-border-top-left-radius','moz-border-radius-topleft','border-top-left-radius'];
                    }else if(whichAngles[i]===1){
                        keys=['-webkit-border-top-right-radius','moz-border-radius-topright','border-top-right-radius'];
                    }else if(whichAngles[i]===2){
                        keys=['-webkit-border-bottom-right-radius','moz-border-radius-bottomright','border-bottom-right-radius'];
                    }else if(whichAngles[i]===3){
                        keys=['-webkit-border-bottom-left-radius','moz-border-radius-bottomleft','border-bottom-left-radius'];
                    }
                    if(keys){
                        for(var j=0; j<keys.length; j++){
                            element.css(keys[j],cssVal);
                        }
                    }
                //            element.css('-webkit-border-top-left-radius',hRadius+' '+vRadius);
                //            element.css('moz-border-radius-topleft',hRadius+' '+vRadius);
                //            element.css('border-top-left-radius',hRadius+' '+vRadius);
                }
            });

        },
        

    }

    $N.notifyScriptLoad();

});
