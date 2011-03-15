/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N, $J) {

    $N.extend = function(destination, source) {
        for (var property in source){
            destination[property] = source[property];
        }
        return destination;
    };

    $N.objectKeys = function(object) {
        var keys = [];
        for (var property in object){
            keys.push(property);
        }
        return keys;
    };

    $N.argumentNames = function(method) {
        var names = method.toString().match(/^[\s\(]*function[^(]*\(([^\)]*)\)/)[1]
        .replace(/\s+/g, '').split(',');
        return names.length == 1 && !names[0] ? [] : names;
    };

    $N.argsToArray = function(args) {
        var length = args.length || 0, result = new Array(length);
        while (length--){
            result[length] = args[length];
        }
        return result;
    };

    $N.wrapFunction = function(wrapper, method) {
        return function() {
            var args = $N.argsToArray(arguments);
            return wrapper.apply(this, [$N.attachFunction(this, method)].concat(args));
        }
    };
 
    $N.attachFunction = function() {
        if (arguments.length < 3 && (typeof arguments[1] == 'undefined')){
            return arguments[0];
        }
        var args = $N.argsToArray(arguments);
        var object = args.shift();
        var method = args.shift();
        return function() {
            var _args = $N.argsToArray(arguments);
            return method.apply(object, args.concat(_args));
        }
    };

    $N.attachAsEventListener = function() {
        var args = $N.argsToArray(arguments), object = args.shift();
        var method = args.shift();
        return function(event) {
            return method.apply(object, [event || window.event].concat(args));
        }
    };

    $N.isInstanceOf = function(obj, className) {
        if (typeof obj == 'object' && obj.__class__) {
            var c = obj.__class__;
            if (c.__name__ == className) {
                return true;
            }
            while (c = c.__super__) {
                if (c.__name__ == className) {
                    return true;
                }
            }
        }
        return false;
    }

    $N.Class = {
        create: function() {
            var parent = null, className = null;
            var properties = $N.argsToArray(arguments)
            if (typeof properties[0] == "string"){
                className = properties.shift();
            }
            if (typeof properties[0] == "function"){
                parent = properties.shift();
            }
    
            function klass() {
                this.initialize.apply(this, arguments);
            }
            //Merge the contents of $N.Class.Methods into klass:
            $N.extend(klass, $N.Class.Methods);
            klass.__name__ = className;
            klass.__super__ = parent;
            klass.__subclasses__ = [];
    
            if (parent) {
                var subclass = function() { };
                subclass.prototype = parent.prototype;
                klass.prototype = new subclass;
                parent.__subclasses__.push(klass);
            }
    
            klass.prototype.__class__ = klass;
            for (var i = 0; i < properties.length; i++){
                klass.addMethods(properties[i]);
            }
      
            if (!klass.prototype.initialize){
                klass.prototype.initialize = function () {};

            }
    
            klass.prototype.constructor = klass;
   
            if (className) {
                $N[className] = klass;
            }
            return klass;
        }
    };
 
    $N.Class.Methods = {
        addMethods: function(source) {
            var ancestor   = this.__super__ && this.__super__.prototype;
            var properties = $N.objectKeys(source);
    
            if (!$N.objectKeys({
                toString: true
            }).length){
                properties.push("toString", "valueOf");
            }
            for (var i = 0, length = properties.length; i < length; i++) {
                var property = properties[i], value = source[property];
                if (ancestor && (typeof value == 'function') &&
                    $N.argumentNames(value)[0] == "$super") {
                    var method = value;
                    value = $N.wrapFunction(method, (function(m) {
                        return function() {
                            return ancestor[m].apply(this, arguments)
                        };
                    })(property));
 
                    value.valueOf = $N.attachFunction(method, method.valueOf);
                    value.toString = $N.attachFunction(method, method.toString);
                }
                this.prototype[property] = value;
            }
    
            return this;
        }
    };
 
    $N.Core = $N.Class.create("Core", {
        eventContainer: null,
        eventPrefix: '',
        cfg: {},

        initialize: function() {
            this.debug("new instance");
            $N.registerInstance(this);
            this.eventContainer = $J('<div/>');
            this.forwardEvent = this.attach(this._forwardEvent);
        },

        free: function() {
            this.eventContainer = null;
        },

        configure: function(config, defaults) {
            if (!config){
                config = {};

            }
            for (k in defaults) {
                var value = null, flags = [];

                if (defaults[k] && typeof defaults[k][0] !== 'undefined') {
                    value = defaults[k][0];
                    if (defaults[k][1]) {
                        flags = defaults[k][1].split(",");
                    }
                } else {
                    value = defaults[k];
                }

                if (typeof config[k] !== 'undefined'){
                    value = config[k];
                }

                var source = this;
                $J(flags).each(function(i, flag) {
                    switch (flag) {
                        case 'required':
                            if (value === null)
                                throw new $N.RequiredOptionError(source, k);
                            break;
                    /*
                    case 'element':
                        value = $J(value);
                        break;
                        */

                    }
                });

                this.cfg[k] = value;
            }
            return this;
        },

        observe: function(eventName, handler) {
            this.eventContainer.bind(this.eventPrefix + eventName, handler);
            return this;
        },

        fire: function(eventName, data) {
            if (!data){
                data = {};

            }
            this.eventContainer.trigger(this.eventPrefix + eventName, data);
            return this;
        },

        _forwardEvent: function(e, data) {
            if (!data){
                data = {};

            }
            this.eventContainer.trigger(e.type, data);
            return this;
        },

        _textWidth: function(text, fontSize) {
            var ratio = 3/5;
            return text.length * ratio * fontSize;
        },

        debug: function(message) {
            if ($N.debugging && typeof console != 'undefined' && console.log) {
                console.log('TimeSide.' + this.__class__.__name__ + ': ' + message);
            }
        },

        attach: function(method) {
            return $N.attachFunction(this, method);
        },

        attachWithEvent: function(method) {
            return $N.attachAsEventListener(this, method);
        },

        uniqid: function() {
            d = new Date();
            return new String(d.getTime() + '' + Math.floor(Math.random() * 1000000)).substr(0, 18);
        }
    });

    $N.Class.create("Exception", {
        _source: null,
        _message: null,

        initialize: function(source, message) {
            this._source = source;
            this._message = message;
        },
        toString: function() {
            return this.__class__.__name__ + " from TimeSide." + this._source.__class__.__name__
            + ": " + this._message;
        }
    });

    $N.Class.create("RequiredOptionError", $N.Exception, {
        initialize: function($super, source, optionName) {
            $super(source, "missing '" + optionName + "' required option");
        }
    });

    $N.Class.create("RequiredArgumentError", $N.Exception, {
        initialize: function($super, source, optionName) {
            $super(source, "missing '" + optionName + "' required argument");
        }
    });

    $N.notifyScriptLoad();

});
