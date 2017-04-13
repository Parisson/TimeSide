define([
  'marionette',
  '#qt_core/controllers/all',
  'localforage'
],

function (Marionette, A, localforage) {
  'use strict';

  

  try {
    localforage.ready(function () {
      localforage.setDriver('localStorageWrapper');
    });

    localforage.config({
      name        : 'qbo',
      version     : 1.0,
      size        : 4980736, // Size of database, in bytes. WebSQL-only for now.
      storeName   : 'qeopa-bo'
    });
  }
  catch (e) {
    console.log("Error on localforage init");
    console.dir(e);
  }

  return Marionette.Controller.extend({
    initialize: function () {
      A.injector.set(A.injector.config.sessionController,this);
    },

    setValue:function(attrib,value) {
      try {
        localforage.setItem(attrib,value);
      }
      catch (e) {
        console.error(e);
      }
    },

    getValue:function(attrib,callback) {
       try {
        localforage.getItem(attrib,function(err,value) {callback(value)}); 
      }
      catch (e) {
        callback(undefined);
      }
    }


  });
});
