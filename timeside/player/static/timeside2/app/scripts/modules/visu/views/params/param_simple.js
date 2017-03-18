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
      


      //1 - set this parameter as waiting for change
      this.$el.css('opacity','0.5');

      //2 - lets find the set-parameters
      var params = _.map(this.$el.find('[data-layout="edit_param"]'),function(input) {
        switch (input.dataset.element) {
          case 'input' : 
            return {name : input.dataset.name, value : $(input).val()}
          default : 
            break;
        }
      });

      var paramsOk = {};
      _.each(params,function(param) {
        paramsOk[param.name] = param.value;
      })

      

      A._i.getOnCfg('analysisController').updateParametersOnAnalysisTrack(paramsOk,this.resultAnalysis.get('uuid'),function(ok) {
        alert('in final callback piahz');
      });
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
