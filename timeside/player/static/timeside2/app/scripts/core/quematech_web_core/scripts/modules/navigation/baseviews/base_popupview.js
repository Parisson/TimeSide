define([
  'marionette',
  'templates',
  'vent',
  'injector',
  'jquery',
  '#behaviors/index'
],

function (Marionette, templates, vent,injector, $,behaviors) {
  'use strict';

  return Marionette.ItemView.extend({
   
    behaviors: function () {
      return {
        Popup: {
          behaviorClass: behaviors.popup
        },
        Validate: {
          behaviorClass: behaviors.validate
        },
        Form: {
          behaviorClass: behaviors.formNew
        },
        ViewUploadImage: {
          behaviorClass: behaviors.viewUploadImage
        }
      }
    },


    
   
  });
});
