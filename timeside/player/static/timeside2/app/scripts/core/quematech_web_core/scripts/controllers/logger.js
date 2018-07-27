define([
  'json!#config/config.json',
  'injector'
],

function (config, injector) {
  'use strict';

  // update baseurl
  var Logger = function() {
    this.showAlerts = config.env==="DEV";

    this.checkShowLogs = config.env!=="PROD";

    this.mappingLogs = {
      "audio" : true,
      "taxi" : true,
      "country" : false,
      "map-loader" : false
    }
  };

  Logger.prototype = {
    alertLog:function(id,log) {
      if (this.showAlerts)
        alert(id+" : "+log);
    },

    showLog:function(id) {
      if (! this.checkShowLogs)
        return false;
      if (this.mappingLogs && this.mappingLogs[id]!==undefined)
        return this.mappingLogs[id];
      return true;
    },

    log:function(id,log) {
      if (this.showLog(id))
        console.log(id+" : "+log);
    }
  }

  return new Logger();
});
