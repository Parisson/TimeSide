define([
  './base_qeopaview',
  '#qt_core/controllers/all',
  './subs/sub_array_genericlist'
],


/**
  This is a generic item for confirming XLSX Import
    {
      title,
     lists : ARRAY OF : 
        {
          title,
          dataAttrib,

          //// ORDER MATTERS!
          headers : [] can be string (function?)
          getters : [] getter to use to show parameter value in tab. MUST be string : we look at the parameter of the JSON object
        }
    }
**/
function (BaseQeopaView,A,ArrayView) {
  'use strict';

  return BaseQeopaView.extend({


    ////////////////////////////////////////////////////////////////////////////////////
    //View definition

    template: templates['navigation/base_generic_confirmimport'],
    className: 'generic_confirmimport',

    initialize: function (options) { 
        if (! options.confirmParameters)
          throw new Error('calling generic import without parameters');
       
       this.confirmParameters = options.confirmParameters;
       this.confirmData = A.injector.get(A.injector.cfg.resultImport);
    },


    onRender:function() {
      if (! this.arraysCreated) {
        if (! (this.confirmParameters.lists && _.isArray(this.confirmParameters.lists))) {
          return console.error('No lists in confirm parameters');
          
        }
        this.arrayViews = [];
        _.each(this.confirmParameters.lists,function(_listConfig) {
          var dataReady = this.prepareDataForArray(_listConfig);

          //main title
          this.ui.containerArray.append('<h3>Data : '+_listConfig.title+'</h3>');  
          if (dataReady.added && dataReady.added.length>0) {
            this.ui.containerArray.append('<h4>'+dataReady.added.length+' new data detected</h4>');
            var arrayViewAdded = new ArrayView();
            arrayViewAdded.setData(_listConfig.headers,dataReady.added);
            this.ui.containerArray.append(arrayViewAdded.render().$el);  
          }

          if (dataReady.merged && dataReady.merged.length>0) {
            this.ui.containerArray.append('<h4>'+dataReady.merged.length+' merged data detected</h4>');
            var arrayViewMerged = new ArrayView();
            arrayViewMerged.setData(_listConfig.headers,dataReady.merged);
            this.ui.containerArray.append(arrayViewMerged.render().$el);
          }

        },this);

        this.arraysCreated = true;
      }

    },


    onClose: function () {
    },

    ui : {
      containerArray : '.generic_array_container',
      btnValidateImport : '.btn-confirm-import'
    },

    events : {
      'click @ui.btnValidateImport' : 'onValidateImport'
    },


    ////////////////////////////////////////////////////////////////////////////////////
    //Validate import
    onValidateImport:function() {

      A.vent.trigger(A.Cfg.events.ui.notification.show, 
          {type : 'warning', title : 'Import',text : 'Are your sure you want to import this file?',
          actions : [
            {label : 'Import', type : 'danger', callback : _.bind(this.onValidateOk,this)},
            {label : 'Cancel', type : 'info', callback :  _.bind(this.onValidateCancel,this)}
          ]});

      
    },

    onValidateOk:function() {
      var fileId = A.injector.get(A.injector.cfg.fileIDImport);
      
      A.vent.trigger(this.confirmParameters.eventValidate,{file : fileId, save : true, 
        urlAfter : this.confirmParameters.urlAfterValidate});

      A.vent.trigger(A.Cfg.events.ui.notification.hide);
    },

    onValidateCancel:function() {
      A.vent.trigger(A.Cfg.events.ui.notification.hide);
    },

    
    ////////////////////////////////////////////////////////////////////////////////////
    //Preping data for array
    //returns {merged : array, }
    prepareDataForArray :function(parameters) {
      var _dataOk = {merged : [], added : []};
      var dataAttrib = parameters.dataAttrib;

      var _dataIn = this.confirmData[dataAttrib];
      if (! (_dataIn)){//} && _dataIn.merged && _dataIn.added)) {
        console.error("prepareDataForArray in BASE generic Confirm import, but no attrib on "+dataAttrib);
        return _dataOk;
      }


      if (_.isFunction(parameters.beforeShowDataFunc))
        _dataIn = parameters.beforeShowDataFunc(_dataIn); //scope?



      //generating data for array. Keeping (praying) for getters order.
      _.each(_dataIn.merged,function(_data) {
        _data.computed_values = [];
        _.each(parameters.getters,function(_getter) {
          //must be String or Function. @TODO checking type. 
          var _value = _.isString(_getter) ? _data[_getter] : _getter(_data);

          _data.computed_values.push(_value);
        },this); 
      },this);

      _.each(_dataIn.added,function(_data) {
        _data.computed_values = [];
        _.each(parameters.getters,function(_getter) {
          //must be String or Function. @TODO checking type. 
          var _value = _.isString(_getter) ? _data[_getter] : _getter(_data);

          _data.computed_values.push(_value);
        },this); 
      },this);

      return _dataIn;
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Managing data
    serializeData: function () {
      var nbErrors = this.confirmData.errors ? this.confirmData.errors.length : 0;
      var hasError = nbErrors>0;
      var errorMessage = hasError ? "Warning : "+nbErrors+" errors have been found importing your file" : "No error was found importing your file";

      
      return {
        mainTitle : this.confirmParameters.title,
        hasError : hasError,
        errorMessage : errorMessage,
        errors : this.confirmData.errors
      }
    },

    
   
  });
});
