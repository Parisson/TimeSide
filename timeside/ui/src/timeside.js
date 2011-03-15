/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: GNU General Public License version 2.0
 */

//this global variable SEEMS to do a check on the variable jQuery, then
//simply executes the argument (which is a function)
var TimeSide = function() {
    //arguments is an array-like object corresponding to the arguments passed to a function
    if (arguments[0]) {
        var toolkit = null;
        if (typeof jQuery != 'undefined'){
            toolkit = jQuery;
        }
        //call arguments[0] (a function) with arguments this and jQuery
        (arguments[0])(TimeSide, toolkit)
    }
};
//this is the first function instantiated. It SEEMS to check the document status and
//load synchronously all the scripts
TimeSide(function($N, $J) {

    $N.isDomLoaded = false;
    $N.isLoaded = false;
    $N.isLoading = false;
    $N.onLoadCallbacks = [];
    $N.cssPrefix = 'ts-';
    $N.debugging = false;

    $J(document).ready(function () {
        $N.isDomLoaded = true;
    });

    $N.domReady = function(callback) {
        // simply calling jQuery.ready() *after* the DOM is loaded doesn't work reliably,
        // at least with jQuery 1.2.6
        if ($N.isDomLoaded) {
            callback();
        } else{
            $J(document).ready(callback);
        }
    }

    $N.instances = [];
    $N.registerInstance = function(obj) {
        $N.instances.push(obj);
    }

    $N.free = function() {
        $J($N.instances).each(function(i, obj) {
            obj.free();
        });
    }

    $J(window).unload($N.free);

    $N.loadScriptsNum = 0;
    $N.loadScriptsCallback = null;
    $N.loadScripts = function(root, scripts, callback) {
        if ($N.loadScriptsCallback) {
            throw "Timeside loader error: concurrent script loading";
        }

        $N.loadScriptsNum = scripts.length;
        $N.loadScriptsCallback = callback;

        var head= document.getElementsByTagName('head')[0];
        for (i = 0; i < scripts.length; i++) {

            var script = document.createElement('script');
            script.type = 'text/javascript';
            var debug = $N.debugging ? '?rand=' + Math.random() : '';
            script.src = root + scripts[i] + debug;
            head.appendChild(script);
        }
    }

    $N.notifyScriptLoad = function() {
        if (--$N.loadScriptsNum == 0 && $N.loadScriptsCallback) {
            var callback = $N.loadScriptsCallback;
            $N.loadScriptsCallback = null;
            callback();
        }
    }

    $N.debug = function(state) {
        $N.debugging = state;
    }

    $N.load = function(callback) {
        $N.domReady(function() {
            if ($N.isLoaded) {
                if (callback)
                    callback();
            } else {
                if (callback)
                    $N.onLoadCallbacks.push(callback);

                if (!$N.isLoading) {
                    $N.isLoading = true;
                    var re = /(.*)timeside.js/;
                    var root = '';
                    $J('head script').each(function(i, e) {
                        if ((match = re.exec(e.src))) {
                            root = match[1];
                        }
                    });

                    $N.loadScripts(root, ['core.js'], function() {
                        $N.loadScripts(root, ['util.js'], function() {
                            var scripts = ['controller.js', 'marker.js', 'markerlist.js',
                            'markermap.js', 'player.js', 'ruler.js','divmarker.js',
                            'soundprovider.js'];
                                                       
                            $N.loadScripts(root, scripts, function() {
                                $N.isLoaded = true;
                                $N.isLoading = false;
                                $J($N.onLoadCallbacks).each(function(i, callback) {
                                    callback();
                                });
                            });
                        });
                    });
                }
            }
        });
    }

});
