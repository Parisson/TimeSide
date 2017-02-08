define([
  'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview',
  'd3'
],

function (Marionette,A,BaseQeopaView,d3) {
  'use strict';

  /**
    Parameter simple window
      
  **/
  return BaseQeopaView.extend({

    template: templates['visu/param_simple'],
    className: 'param-simple',

    ui: {
    },
    events: {
        'click [data-layout="delete_track"]' : 'onDeleteTrack',
        'click [data-layout="update_params"]' : 'onUpdateParams'
    },

    onUpdateParams:function() {
      alert('@Todo : get params, call https://taiga.ircam.fr/project/yomguy-diadems/task/32 && reload track');
    },

    setDaddy : function(view) {
        //view = track_waveform or track_canvas
        this.daddy = view;
    },

    //from daddy view on defineTrack
    setResultAnalysis : function(resultAnalysis) {
      this.resultAnalysis = resultAnalysis;
      this.render();

      //alert('got it : '+JSON.stringify(this.resultAnalysis));
    },

    ////////////////////////////////////////////////////////////////////////////////////
    onDeleteTrack:function(ev) {
        A._v.trigCfg('ui_project.deleteTrack','',this.daddy);
    },      

    ////////////////////////////////////////////////////////////////////////////////////
    initialize: function () {

    },

    onRender:function() {
       
    },

    onDestroy: function () {     
    },


    serializeData: function () {
      
      //WARN : REMOVE JSON stringify!!!!!!!!!!!!!!!!!!!!!!
      if (!this.resultAnalysis)
        return {};
      var result = {
        parametrizable : this.resultAnalysis.get('parametrizable'),
        parameters_schema : this.resultAnalysis.get('parameters_schema'),
        parameters_default : this.resultAnalysis.get('parameters_default')
      };

      var listNameProperties = _.keys(result.parameters_schema.properties);
      var listPropertiesOk = _.map(listNameProperties,function(nameProperty) {
        return _.extend(result.parameters_schema.properties[nameProperty],{
          name : nameProperty
        });
      });
      result.propertiesOk = listPropertiesOk;


      return result;
    },


    
    
   
  });
});
