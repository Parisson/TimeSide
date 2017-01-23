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
      
    },
    initializeResponsive : function() {
        
    },
    initialize: function () { 
        
    },

    onRender:function() {
      
    },


    onClose: function () {
      
    },


    ////////////////////////////////////////////////
    //generation des données de pagination  pour la vue

    addValuePagination:function(results,value,baseUrl,current) {

      //console.log('Trying to add : '+value);

      if (_.isNumber(value) && (value>this.paginationLimits.max || value < this.paginationLimits.min))
        return;

      var alreadyThere =_.find(results,function(_result) {
        return _result.trueValue===value;
      });
      if (alreadyThere && value!=='...')
        return;
      

      results.push({
        trueValue : value,
        value : _.isNumber(value) ? value+1 : value,
        selected : value===current,
        url : _.isNumber(value) ? baseUrl+'/'+value : '',
        active : baseUrl!=='' && _.isNumber(value)
      });

      //console.log('   Added : '+value);
    },

    /**
      On aura toujours 1,2,...x-1,x,x+1,...max-1,max
    **/
    generatePaginationData:function(baseUrl,min,max,current) {
      var results  = [];

      this.paginationLimits = {min : min, max : max};

      //adding min value
      this.addValuePagination(results,min,baseUrl,current);
      
      //adding min+1
      this.addValuePagination(results,min+1,baseUrl,current);

      //if space between min & current
      if (current>(min+1))
        this.addValuePagination(results,'...','');

      if (current>1)
      this.addValuePagination(results,current-1,baseUrl,current);

      this.addValuePagination(results,current,baseUrl,current);

      if (current+1 <=max)
        this.addValuePagination(results,current+1,baseUrl,current);

      if (current+1 < max)
        this.addValuePagination(results,'...','');

      if (max>1)
      this.addValuePagination(results,max-1,baseUrl,current);
      this.addValuePagination(results,max,baseUrl,current);

      return results;


    }

    
   
  });
});
