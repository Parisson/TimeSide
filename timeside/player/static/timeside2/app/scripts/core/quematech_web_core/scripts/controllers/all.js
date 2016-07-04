define([
  'injector',
  'vent',
  'jquery',
  'underscore',
  'logger',
  '#qt_core/controllers/config',

  '#qt_core/controllers/helpers/datacommand_helper',
  '#qt_core/controllers/helpers/apievents_helper',
  'views/helpers/admin_helper',

  'core/models/index',
  'moment'

  

],

function (injector,vent,$,underscore,log,Cfg,DataCommandHelper,ApiEventsHelper,AdminViewHelper,Models,Moment
  ) {

  

  var all = {
  	'injector' : injector,
    'vent' : vent,
    '$' : $,
    '_' : underscore,
    'log' : log,
    'Cfg' : Cfg,
    'DataCommandHelper' : DataCommandHelper,
    'ApiEventsHelper' : ApiEventsHelper,
    'AdminViewHelper' : AdminViewHelper,

    'models' : Models


  };

  //////////////////////////////////////////////////////////////////////
  // Sys tools

  all.systools = {
    byString :function(o, s) {
      s = s.replace(/\[(\w+)\]/g, '.$1'); 
      s = s.replace(/^\./, '');          
      var a = s.split('.');
      for (var i = 0, n = a.length; i < n; ++i) {
          var k = a[i];
          if (k in o) {
              o = o[k];
          } else {
              return;
          }
      }
      return o;
    },

    //won't work with dates & regexp & cyclic stuff!!!
    deepClone:function(obj) {
       return JSON.parse(JSON.stringify(obj))
    }
  };

  //////////////////////////////////////////////////////////////////////
  // Specific Telemeta tools
  all.telem = {
    formatTimeMs:function(t) {
      var mom = Moment(new Date(t));

      if (t<1000*60*60)
        return mom.format('ss.SSS');
      var result = mom.format('mm:ss.SSS');
      return result;

    }
  };

  //////////////////////////////////////////////////////////////////////////////////////////////////////////
  // Injector quick

  all._i = {
    getOnCfg : function(attribInCfg) {
      var itemCfg = all.systools.byString(injector.cfg,attribInCfg);
      if (! itemCfg)
        return console.error('No injector config on '+attribInCfg);
      return injector.get(itemCfg);
    },
    setOnCfg : function(attribInCfg,value) {
      var itemCfg = all.systools.byString(injector.cfg,attribInCfg);
      if (! itemCfg)
        return console.error('No injector config on '+attribInCfg);
      return injector.set(itemCfg,value);
    }

  };






  //////////////////////////////////////////////////////////////////////////////////////////////////////////
  // Vent quick

  //tools
  getChangeEventFunc = function(modificator) {
    var _hop = {"api" : Cfg.eventApi,"ok" : Cfg.eventOk, "error" : Cfg.eventError, 
      "apiok" : Cfg.eventApiOk, "apierror" : Cfg.eventApiError};
    return _hop[modificator];
  };

  getEventOk = function(attribInCfg,modificator) {
    var itemCfg = all.systools.byString(Cfg.events,attribInCfg);
    if (! itemCfg)
      return console.error('No event found : '+attribInCfg);

    if (modificator && modificator.length>0) {
      var func = getChangeEventFunc(modificator);
      if (! func)
        return console.error('No modificator found for '+modificator);
      itemCfg = func(itemCfg);
    }
    return itemCfg;

  };

  all._v = {

    


    onCfg : function(attribInCfg,modificator,func,scope) {
      var itemCfg = getEventOk(attribInCfg,modificator);
      vent.on(itemCfg,func,scope);
    },
    offCfg : function(attribInCfg,modificator,func,scope) {
      var itemCfg = getEventOk(attribInCfg,modificator);
      vent.off(itemCfg,func,scope);
    },
    trigCfg:function(attribInCfg,modificator,val1,val2,val3,val4,val5,val6) {
      var itemCfg = getEventOk(attribInCfg,modificator);
      vent.trigger(itemCfg,val1,val2,val3,val4,val5,val6);
    }

  };



  DataCommandHelper.init(all);

  //tmp
  window.quemall = all;

  return all;

});
