define([
'underscore',
  'wreqr.injector',
  'json!#config/injector.json',
  'json!#config_core/injector.json',
],

function (_,Injector,ConfigInjector,ConfigCoreInjector) {
  'use strict';
  var injector = new Injector();

  var configOk = _.extend(ConfigInjector,ConfigCoreInjector);

  injector.config = configOk;//ConfigInjector;
  injector.cfg= configOk;//ConfigInjector;


  //Overriding injector get & set and check what happens

  //Override get & set & check if exists in config
  (function() {
    var _get = _.bind(injector.get,injector);                   // <-- Reference
    injector.get = function(attrib) {
    	if (! injector.cfg[attrib])
    		console.error('Injector get called on unknown : '+attrib);
		return _get(attrib);
    };

    var _set = _.bind(injector.set,injector);                   // <-- Reference
    injector.set = function(attrib,value) {
    	if (! injector.cfg[attrib])
    		console.error('Injector set called on unknown : '+attrib);
		return _set(attrib,value);
    };


   })();

  return injector;
});
