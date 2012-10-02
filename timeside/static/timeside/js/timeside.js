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
 * Root javascript file for TimesideUI, to be manually included in your web page (see online doc)
 */

/**
 *global variable housing all Timeside variables/mathods/classes:
 */
var Timeside = {
    Class:undefined,
    classes:{},
    player:undefined,
    config: {
        /**
         *set to true to see debug messages on the console (only error or warning messages shown)
         */
        debug: false,
        /*
         * timeside scripts to be loaded when Timeside.load is called. URL paths are relative to the timeside folder, which
         * will be determined according to the src attribute of the timeside.js script path (to be included in the <head> of the page)
         */
        timesideScripts: ['rulermarker.js','markermap.js', 'player.js', 'ruler.js'],
        //vml config variables. Used only if svg is NOT supported
        vml : {
            /*
            * raphael script to be loaded when Timeside.load is called and svg is not supported. It will be prepended to the
            * timesideScripts array defined above in config. URL paths are relative to the timeside folder, which
            * will be determined according to the src attribute of the timeside.js script path (to be included in the <head> of the page)
            */
            raphaelScript : 'libs/raphael-min.js',
            /*
             * available attributes which can be converted from css-svg to Raphael attributes (see Raphael.js):
             */
            raphaelAttributes : ["clip-rect", "cursor",'fill', "fill-opacity",'opacity', 'stroke', "stroke-dasharray", "stroke-linecap", "stroke-linejoin","stroke-miterlimit","stroke-opacity","stroke-width", "text-anchor"]
        }
    },
    utils:{
        /**
         * Returns an uniqid by creating the current local time in millisecond + a random number.
         * Used for markers in markermap. The method is kind of public in order to be more accessible for other functions
         * by calling Timeside.utils.uniqid(), in case it is needed
         */
        uniqid : function() {
            var d = new Date();
            return new String(d.getTime() + '' + Math.floor(Math.random() * 1000000)).substr(0, 18);
        },
        /**
         * vml object which will be populated by vml functions to interface timeside and raphael. See timeside.load.
         * We could implement functions here for code readability, however,
         * we delegate Timeside.load so that if svg is supported memory is free from unused vml methods.
         * IN ANY CASE, svg support can be detected anywhere by calling, eg:
         *  var svg = !Timeside.utils.vml;
         */
        vml: undefined,

        /**
         * property that will be set to false if soundManager fails to initialize flash
         */
        flashFailed : false
    }
};


/* Simple JavaScript Inheritance
 * By John Resig http://ejohn.org/
 * MIT Licensed.
 * (Inspired by base2 and Prototype)
 */

/*
 * In few words: the lightest and most-comprehensive way to implement inhertance and OOP in javascript. Usages can be found below.
 * Basically,
 * 1) a new Class is instantiated with Class.extend(). This function takes a dictionary
 * of properties/methods which will be put IN THE PROTOTYPE of the class, so that each instance will share the same properties/methods
 * and the latter don't have to be created for each instance separately.
 * 2) If var A = Class.extend({...}) and var B = A.extend({..}), then methods which are found in B will override the same methods in A.
 * In this case, the variable this._super inside the overridden methods will refers to the super-method and can thus be called safely.
 * Consequently, if a _super property/method is implemented in the extend dictionary, it WILL NOT be accessible
 * to the overriding methods of B. Basically, don't use _super as a key of the argument of extend.
 * 3) AFTER the prototype has been populated, the init function, if exists, is called. The latter can be seen as a class constructor in java,
 * with a substantial difference: when executing the init() method the class prototype has already been populated with all inherited methods.
 * Private variable can be declared in the init function, as well as
 * relative getters and setters, if needed. Downside is that the privileged getters and setters can’t be put in the prototype,
 * i.e. they are created for each instance separately, and the _super keyword does not apply to them. Another issue is the overhead of closures in general (basically, write as less as possible
 * in the init function, in particular if the class has to be declared several times)
 * Of course, the this._super keyword of methods implemented in the init constructor does not work
 *
 * EXAMPLE:
 * var MyClass = Class.extend({
 *   init: function(optionalArray){ //constructor
 *       this._super();             //!!!ERROR: Class is the base class and does not have a super construcor
 *       var me = [];               //private variable
 *       this.count = 6;            //set the value of the public property defined below
 *       this.getMe = function(){   //public method
 *           this._super();         //!!!ERROR: methods defined in the init function don't have acces to _super
 *       }
 *       this.alert = function(){   //another public method, !!!WARNING: this will be put in the MyClass scope (NOT in the prototype)
 *           alert('ok');
 *       }
 *   },
 *   count:0,                       //public property
 *   alert: function(){             //public method. !!!WARNING: this method will be put in the prototype BEFORE the init is called,
 *      alert('no');                //  so the alert defined above will be actually called
 *   }
 * });
 * var MyClass2 = MyClass.extend({
 *  init: function(){
 *      this._super();                  //call the super constructor
 *  }
 *  alert: function(){                  //override a method
 *      this._super();                  //call the super method, ie alerts 'no'. WARNING: However, as long as there is an alert written
 *                                      //in the init method of the superclass (see above), THAT method will be called
 *  }
 * });
 *
 */


(function(parent){

    var initializing = false, fnTest = /xyz/.test(function(){
        xyz;
    }) ? /\b_super\b/ : /.*/;

    /*The xyz test above determines whether the browser can inspect the textual body of a function.
     *If it can, you can perform an optimization by only wrapping an overridden method if it
     *actually calls this._super() somewhere in its body.
     *Since it requires an additional closure and function call overhead to support _super,
     *it’s nice to skip that step if it isn’t needed.
     */

    //ADDED BY ME:
    // before was: this.Class = function(){}, where this here is the DomWindow
    // In order to chose where to attach the Class object, we added the argument parent (see above):
    //if parent is undefined, attach Class to the DomWindow (same as before):
    if(!parent){
        parent= window;
    }
    parent.Class = function(){};

    //from here on, the code is untouched:
    //
    //We have the base Class implementation (does nothing)
    //and we write here below the method extend which returns the Class with inhertance implemented:
    // Create a new Class that inherits from this class
    parent.Class.extend = function(prop) {
        var _super = this.prototype;

        // Instantiate a base class (but only create the instance,
        // don't run the init constructor)
        initializing = true;
        var prototype = new this();
        initializing = false;

        // Copy the properties over onto the new prototype
        for (var name in prop) {
            // Check if we're overwriting an existing function
            prototype[name] = typeof prop[name] == "function" &&
            typeof _super[name] == "function" && fnTest.test(prop[name]) ?
            (function(name, fn){
                return function() {
                    var tmp = this._super;

                    // Add a new ._super() method that is the same method
                    // but on the super-class
                    this._super = _super[name];

                    // The method only need to be bound temporarily, so we
                    // remove it when we're done executing
                    var ret = fn.apply(this, arguments);
                    this._super = tmp;

                    return ret;
                };
            })(name, prop[name]) :
            prop[name];
        }

        // The dummy class constructor
        function Class() {
            // All construction is actually done in the init method
            if ( !initializing && this.init ){
                this.init.apply(this, arguments);
            }
        }

        // Populate our constructed prototype object
        Class.prototype = prototype;

        // Enforce the constructor to be what we expect
        Class.constructor = Class;

        // And make this class extendable
        Class.extend = arguments.callee;

        return Class;
    };
})(Timeside);



//Defining the base TimeClass class. Timeside.classes.[Player, Ruler, MarkerMap...] are typical implementations (see js files)
//Basically we store here static methods which must be accessible in several timside sub-classes
Timeside.classes.TimesideClass = Timeside.Class.extend({
    //init constructor. Define the 'bind' and 'fire' (TODO: rename as 'trigger'?) methods
    //we do it in the init function so that we can set a private variable storing all
    //listeners. This means we have to re-write all methods
    init: function(){
        //the map for listeners. Must be declared in the init as it's private and NOT shared by all instances
        //(ie, every instance has its own copy)
        this.listenersMap={};
    },

    cssPrefix : 'ts-', //actually almost uneuseful, still here for backward compatibility with old code (TODO: remove?)
    $J : jQuery, //reference to jQuery for faster lookup inside methods
    $TU : Timeside.utils, //reference to Timeside variable for faster lookup inside methods
    debugging : false,
    debug : Timeside.config.debug ? function(message) {
        var C = console;
        if (C && C.log) {
            C.log(message);
        }
    } : function(message){},

    /**
     * 3 methods defining listeners, events fire and bind (aloing the lines of jQuery.bind, unbind and trigger.
     * the only difference is that 'trigger' is 'fire' here). namespaces are allowed as in jQuery
     */
    bind : function(eventType, callback, optionalThisArgInCallback){
        if(!callback || typeof callback !== 'function'){
            this.debug('TimesideClass.bind: cannot bind '+eventType+' to callback: the latter is null or not a function');
            return;
        }
        if(!eventType){
            this.debug('TimesideClass.bind: eventType is empty in bind');
            return;
        }
        var listenersMap = this.listenersMap;
        if(optionalThisArgInCallback){
            var cb = callback;
            callback = function(data){
                cb.apply(optionalThisArgInCallback,[data]);
            };
        }

        if(listenersMap.hasOwnProperty(eventType)){
            listenersMap[eventType].push(callback);
        }else{
            listenersMap[eventType] = [callback];
        }

        var idx = eventType.indexOf('.');
        if(idx <= 0 || idx >= eventType.length-1){
            return;
        }

        eventType = eventType.substring(0,idx);


        if(listenersMap.hasOwnProperty(eventType)){
            listenersMap[eventType].push(callback);
        }else{
            listenersMap[eventType] = [callback];
        }

    },
    unbind : function(){
        var listenersMap = this.listenersMap;
        var key,keyPlusDot;
        if(arguments.length>0){
            key = arguments[0];
            if(listenersMap.hasOwnProperty(key)){
                var callbacks = listenersMap[key];
                var idx = key.indexOf('.');
                if(idx>0 && idx < key.length-1){
                    //key is "eventtype.namespace", delete also functions stored in "eventType", if any
                    var baseKey = key.substring(0,idx);
                    var baseCallbacks = listenersMap[baseKey];
                    if(baseCallbacks){
                        for( var i = baseCallbacks.length; i>-1; i--){
                            var bc = baseCallbacks[i];
                            for( var j = callbacks.length; j>-1; j--){
                                if(bc === callbacks[j]){
                                    baseCallbacks.splice(i,1);
                                }
                            }
                        }
                    }
                }else if(idx<0){
                    //key is "eventtype", delete also all functions stored in "eventType.namespace", if any
                    keyPlusDot = key+'.';
                    for(var k in listenersMap){
                        if(listenersMap.hasOwnProperty(k) && k.indexOf(keyPlusDot)==0 && k.length > keyPlusDot.length){
                            delete listenersMap[k];
                        }
                    }
                }
                delete listenersMap[key];
            }
        }else{
            for(key in listenersMap){
                if(listenersMap.hasOwnProperty(key)){
                    delete listenersMap[key];
                }
            }
        }
    },
    fire : function(key, dataArgument){
        var listenersMap = this.listenersMap;
        if(!(listenersMap.hasOwnProperty(key))){
            return;
        }
        if(arguments.length < 2 || !dataArgument){
            dataArgument = {};
        }
        var callbacks = listenersMap[key];
        var len = callbacks && callbacks.length ? callbacks.length : 0;
        for(var i=0; i<len; i++){
            callbacks[i](dataArgument);
        }
    },

    /*
     *formats (ie returns a string representation of) a time which is in the form seconds,milliseconds (eg 07.6750067)
     * formatArray is an array of strings which can be:
     * 'h' hours. Use 'hh' for a zero-padding to 10 (so that 6 hours is rendered as '06')
     * 'm' hours. Use 'mm' for a zero-padding to 10 (so that 6 minutes is rendered as '06')
     * 's' hours. Use 'ss' foar a zero-padding to 10 (so that 6 seconds is rendered as '06')
     * 'D' deciseconds
     * 'C' centiseconds (it will be padded to 10, so that 5 centiseconds will be rendered as '05')
     * 'S' milliseconds (it will be padded to 100, so that 5 milliseconds will be rendered as '005')
     * If formatArray is null or undefined or zero-length, it defaults to ['mm','ss']
     * 'h','m' and 's' will be prepended the separator ':'. For the others, the prepended separator is '.'
     * Examples:
     * makeTimeLabel(607,087)               returns '10:07' (formatArray defaults to ['mm','ss'])
     * makeTimeLabel(607,087,['m':'s'])     returns '10:7'
     * makeTimeLabel(607,087,['m':'s','C']) returns '10:7.09'
     */
    makeTimeLabel: function(time, formatArray){
        if(!(formatArray)){
            formatArray = ['mm','ss'];
        }

        //marker offset is in float format second.decimalPart
        var pInt = parseInt;
        var round = Math.round;
        var factor = 3600;
        var hours = pInt(time/factor);
        time-=hours*factor;
        factor = 60;
        var minutes = pInt(time/factor);
        time-=minutes*factor;
        var seconds = pInt(time);
        time-=seconds;

        //here below the function to format a number
        //ceilAsPowerOfTen is the ceil specifiedas integer indicating the relative power of ten
        //(0: return the number as it is, 1: format as "0#" and so on)
        //Examples: format(6) = "6", format(6,1)= "06", format(23,1)= "23"

        //first of all, instantiate the power function once (and not inside the function or function's loop):
        //note that minimumNumberOfDigits lower to 2 returns integer as it is
        var mpow = Math.pow; //instantiate mpow once
        var format = function(integer,minimumNumberOfDigits){
            var n = ""+integer;
            var zero = "0"; //instantiating once increases performances???
            for(var i=1; i< minimumNumberOfDigits; i++){
                if(integer<mpow(10,i)){
                    n = zero+n;
                }
            }
            return n;
        };
        var ret = [];
        for(var i =0; i<formatArray.length; i++){
            var f = formatArray[i];
            var separator = ":";
            if(f=='h'){
                ret[i]=hours;
            }else if(f=='hh'){
                ret[i]=format(hours,2);
            }else if(f=='m'){
                ret[i]=minutes;
            }else if(f=='mm'){
                ret[i]=format(minutes,2);
            }else if(f=='s'){
                ret[i]=seconds;
            }else if(f=='ss'){
                ret[i]=format(seconds,2);
            }else if(f=='S'){
                separator = ".";
                ret[i]=format(round(time*1000),3);
            }else if(f=='C'){
                separator = ".";
                ret[i]=format(round(time*100),2);
            }else if(f=='D'){
                separator = ".";
                ret[i]= round(time*10);
            }
            if(i>0){
                ret[i] = separator+ret[i];
            }
        }
        return ret.join("");
    }
});

/**
 * An Array-like implementation that suits the need of Marker mnanagement
 * Ruler, MarkerMap and MarkerMapDiv implement this class
 */
Timeside.classes.TimesideArray = Timeside.classes.TimesideClass.extend({
    init: function(optionalArray){
        this._super();
        //here methods that CANNOT be overridden
        var me= optionalArray ? optionalArray : [];
        //note that this method written here OVERRIDES the same method written outside init in the children!!!!
        this.toArray = function(returnACopy){
            if(returnACopy){
                var ret = [];
                for(var i=0; i<me.length; i++){
                    ret.push(me[i]);
                }
                return ret;
            }
            return me;
        };
        this.length = me.length; //in order to match the javascript array property
    },
    //adds at the end of the array. If index is missing the object is appended at the end
    add : function(object, index){
        var array = this.toArray();
        if(arguments.length<2){
            index = array.length;
        }
        array.splice(index,0,object);
        this.length = array.length; //note that length is a property and must be updated!!!
        return object;
    },
    //removes item at index, returns the removed element
    remove : function(index){
        var array = this.toArray();
        var ret =  array.splice(index,1)[0];
        this.length = array.length; //note that length is a property and must be updated!!!
        return ret;
    },
    //Iterate over the array, with the same syntax of jQuery.each, ie, executes a function(index,element)
    //for each element from startIndexInclusive to
    //endIndexExclusive.
    //The only required argument is callback:
    //1) each(callback) iterates over all elements executing callback
    //2) each(m, callback) iterates over the elements from m executing callback
    //3) each(m,n,callback) iterates over the elements from m (inclusive) to n-1 (inclusive) executing callback

    //NOTE: writing   each : function(startInclusive, endExclusive, callback) throws an error in chrome, as the last
    //argument (even if it is a function) is a number. Why?????
    //Anyway, we write the function arguments as empty
    each : function(){
        var startInclusive, endExclusive, callback;

        var arg = arguments;
        var len = arg.length;
        var l = this.length;
        switch(len){
            case 0:
                this.debug('TimesideClass.each: each called without arguments!!!');
                return;
            case 1:
                startInclusive = 0;
                endExclusive = l;
                break;
            case 2:
                if(arg[0] >= l){
                    return;
                }
                startInclusive = arg[0]=== undefined ? 0 : arg[0];
                endExclusive = l;
                break;
            default:
                startInclusive = arg[0]=== undefined ? 0 : arg[0];
                endExclusive = arg[1]=== undefined ? l : arg[1];
        }
        callback = arg[len-1];
        if(!(callback instanceof Function)){
            this.debug('TimesideClass.each: callback NOT a function!!!');
            return;
        }
        var me =this.toArray();
        for(var i = startInclusive; i<endExclusive; i++){
            callback(i,me[i]);
        }

    },

    //clears the array and the events associated to it, ie removes all its elements and calls unbind(). Returns the array of the removed elements
    clear: function(){
        this.unbind();
        var me = this.toArray();
        var l = me.length;
        this.length = 0;
        if(l==0){
            return [];
        }
        return me.splice(0,l);
    },
    //moves the element at position from into position to
    //the element that was at from will be at position to
    //returns:
    //-1 if from or to not integers, or from or to not within the array bounds (lower than zero or greater or equal to this.length)
    //from if from === to (no move)
    //to otherwise (move succesful)
    move : function(from, to){

        var pInt = parseInt;
        if(pInt(from)!==from || pInt(to)!==to){ //just a check
            return -1;
        }
        if(from === to){
            return from;
        }
        var me =this.toArray();
        var len = me.length;
        if((from<0 || from>=len)||(to<0 || to>=len)){
            return -1;
        }
        var elm = me.splice(from,1)[0];
        me.splice(to,0,elm);

        return to;
    }
});



/**
 *Main Timeside method to load player (see Timeside online doc)
 */

Timeside.load =function(config){

    var $J = jQuery;
    var win = window;
    var doc = document;
    //function to be called onready or onerror:
    var loadAll = function() {


        //get the current script path (this file name is timeside.js?... or simplt timeside.js)
        var scripts = $J('script');
        var thisScriptPath = '';
        scripts.each(function(i,s){
            var src = $J(s).attr('src');
            if(src){
                var srcName = src.split(/\//);
                if(srcName.length){
                    srcName = srcName[srcName.length-1];
                    //is this script ? consider the case here we are loading timeside.js?....
                    if(srcName.replace(/\.js(?:\?[^\?]*)*$/,'.js') == 'timeside.js'){
                        src[src.length-1] = '';
                        thisScriptPath = src.replace(/\/[^\/]+$/, '');
                    }
                }
            }
        });

        var ts = Timeside;
        var ts_scripts = ts.config.timesideScripts;
        //detect SVG support and load Raphael in case. Copied from Raphael code v 1.5.2:
        var svg = (win.SVGAngle || doc.implementation.hasFeature("http://www.w3.org/TR/SVG11/feature#BasicStructure", "1.1"));
        if(!svg){
            //add the raphael path. Raphael will be loaded in Timeside.load (see below)
            ts_scripts.splice(0,0,ts.config.vml.raphaelScript);
            //populate the vml object with methods to be used in ruler and rulermarker:

            //global private variable:
            //map to store each class name to the relative dictionary for raphael attr function (VML only)
            var classToRaphaelAttr = {};
            //get the raphael attributes for which a conversion css -> raphael_attribute is possible:
            var availableAttrs = ts.config.vml.raphaelAttributes;
            //here below we store  Raphael paper objects. var paper = Raphael(htmlElement) is the raphel method to build
            //a new paper object. Internally, the method builds a div embedding vmls inside htmlElement, retriavable via the
            //paper.node property.
            //However, calling again var paper = Raphael(htmlElement) does not use the already created paper,
            //but creates a new paper with a new paper.node (div). Too bad. The possibility to wrap existing paper node
            //into a Raphael paper would be a nice and almost necessary feature, which however is not even
            //planned to be implemented according to raphael developers (see raphael forums).
            //In case of markers lines, we want to draw a new marker
            //on the same raphael paper. Therefore, we store here raphael papers in a map htmlElement -> paper
            var raphael_papers = {};
            ts.utils.vml = {
                getVmlAttr: function(className){

                    if(classToRaphaelAttr.hasOwnProperty(className)){
                        //if(className in classToRaphaelAttr){
                        return classToRaphaelAttr[className];
                    }
                    var d = document;
                    var dottedclassName = className.replace(/^\.*/,'.'); //add a dot if not present
                    var ssheets = d.styleSheets;
                    var len = ssheets.length-1;

                    var attr = {};
                    for(var i=0; i<len; i++){
                        var rules = ssheets[i].rules;
                        var l = rules.length;
                        for(var j=0; j <l; j++){
                            var rule = rules[j];

                            if(rule.selectorText === dottedclassName){

                                var style = rule.style;
                                for(var k =0; k<availableAttrs.length; k++){
                                    var val = style[availableAttrs[k]];
                                    if(val){
                                        attr[availableAttrs[k]] = val;
                                    }
                                }
                            }
                        }
                    }
                    classToRaphaelAttr[className] = attr;
                    return attr;
                },

                Raphael: function(element,w,h){
                    //pass jQueryElm.get(0) as first argument, in case)
                    if(raphael_papers[element]){
                        return raphael_papers[element];
                    }
                    var paper = Raphael(element,w,h);
                    raphael_papers[element] = paper;
                    //paper canvas is a div with weird dimensions. You can check it by printing paper.canvas.outerHTML in IE.
                    //We set them to 100% so we dont have clipping regions when resizing (maximizing)
                    paper.canvas.style.width='100%';
                    paper.canvas.style.height='100%';
                    paper.canvas.width='100%';
                    paper.canvas.height='100%';
                    //apparently, there is also a clip style declaration made by raphael. The following code trhows an error in IE7:
                    //paper.canvas.style.clip = 'auto';
                    //however, even leaving the clip style declaration as it is, it seems to work (the div spans the whole width)
                    return paper;
                }

            };
        }

        ts.player = undefined;
        if(config.onReady && typeof config.onReady === 'function'){
            var oR = config.onReady;
            config.onReady = function(player){
                ts.player = player;
                oR(player);
            };
        }else{
            config.onReady = function(player){
                ts.player = player;
            };
        }

        //finally,define the error function
        ts.utils.loadScripts(thisScriptPath,ts_scripts, function() {
            new ts.classes.Player(config); //do not assign it to any variable, we do it only onready
        },config.onError);
    };




    $J(win).ready(function(){
        var s = soundManager;
        //grab the case of soundManager init errors:
        s.onerror = function() {
            Timeside.utils.flashFailed = true;
            //end('SoundManager error. If your browser does not support HTML5, Flash player (version '+soundManager.flashVersion+'+) must be installed.\nIf flash is installed, try to:\n - Reload the page\n - Empty the cache (see browser preferences/options/tools) and reload the page\n - Restart the browser');

            //and load all anyway:
            loadAll();
        };

        //if soundmanager is ready, the callback is executed immetiately
        //onready is executed BEFORE onload, it basically queues several onload events.
        //It it is executed immetiately if soundmanager has already been loaded
        s.onready(function(){loadAll();});
    });
};

/**
* Loads scripts asynchronously
* can take up to four arguments:
* scriptsOptionalRoot (optional): a string specifying the root (such as '/usr/local/'). IF IT IS A NONEMPTY STRING AND
*                                 DOES NOT END WITH A SLASH, A SLASH WILL B APPENDED
* scriptArray: a string array of js script filenames, such as ['script1.js','script2.js']
* optionalOnOkCallback (optional): callback to be executed when ALL scripts are succesfully loaded
* optionalOnErrorCallback (optional) a callback receiving a string as argument to be called if some script is not found
* optionalSynchroLoad (optional): if true scripts are loaded in synchronously, ie each script is loaded only once the
*                                 previous has been loaded. Otherise (including missing argument) an asynchronous load is performed
*                                 and the optional onOkCallback is executed once ALL scripts are loaded
*/
Timeside.utils.loadScripts = function(scriptsOptionalRoot,scriptArray, optionalOnOkCallback, optionalOnErrorCallback, optionalSynchroLoad){
    //var optionalRoot='', callback=undefined, loadInSeries=false;
    if(!optionalOnOkCallback || typeof optionalOnOkCallback !== 'function'){
        optionalOnOkCallback = function(){};
    }
    if(!optionalOnErrorCallback || typeof optionalOnErrorCallback !== 'function'){
        optionalOnErrorCallback = function(msg){};
    }

    if(!scriptArray || !scriptArray.length){
        optionalOnOkCallback();
        return;
    }
    var len = scriptArray.length;
    var i=0;
    if(scriptsOptionalRoot){
        scriptsOptionalRoot = scriptsOptionalRoot.replace(/\/*$/,"/"); //add slash at end if not present
        for(i =0; i<len; i++){
            scriptArray[i] = scriptsOptionalRoot+scriptArray[i];
        }
    }

    var $J = jQuery;
    //there is a handy getScript function in jQuery, which however does NOT manage the onError case (script load error)
    //looking at jQuery doc, getScript is the same as the followig ajax request,
    //to which we added the error property to manage errors:
    var loadScript = function(url,onSuccess,onError){
        $J.ajax({
            url: url,
            dataType: 'script',
            success: onSuccess,
            error: function(a,b,errorThrown){
                onError('file "'+url+'" error: '+errorThrown);
            }
        });
    };
    if(optionalSynchroLoad){
        var load = function(index){
            if(index<len){
                loadScript(scriptArray[index],function(){
                    load(index+1);
                }, function(msg){
                    optionalOnErrorCallback(msg);
                });
            }else if(index==len){
                optionalOnOkCallback();
            }
        };
        load(0);
    }else{
        var count=0;
        var s;
        for(i=0; i <len; i++){
            s = scriptArray[i];
            //this means that onError all scripts will be loaded.
            //However, if everything works fine, asynchornous load (here) should be faster
            loadScript(s, function(){
                count++;
                if(count===len){
                    optionalOnOkCallback();
                }
            },function(msg){
                count = len+1; //avoid calling optionalOkOnCallback
                optionalOnErrorCallback(msg);
            });
        }
    }
};
