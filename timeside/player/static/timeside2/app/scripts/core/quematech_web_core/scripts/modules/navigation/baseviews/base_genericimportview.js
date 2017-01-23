define([
  './base_qeopaview',
  '#qt_core/controllers/all',
  '#upload/helpers/upload'
],


/**
  This is a generic importation item. paramaters are : 
    {
      'eventUpload' : 'event for uploading data, waiting on back for showing data'
      'title' : title,
      viewIdConfirm : viewid for confirmation

    }
**/
function (BaseQeopaView,A,UploadHelper) {
  'use strict';

  return BaseQeopaView.extend({

    ////////////////////////////////////////////////////////////////////////////////////
    //View definition

    template: templates['navigation/base_genericimportview'],
    className: 'generic_import',

    initialize: function (options) { 
        if (! options.importParameters)
          throw new Error('calling generic import without parameters');
        this.importParameters = options.importParameters;

        this.hasFile=false;
        
    },

    ui : {
      inputFile : '.upload_data_file',
      btnStartUpload : '.btn-upload-file',
      btnDownloadSample : '.btn-download-sample'
    },

    events : {
      'click @ui.btnStartUpload' : 'onStartUpload',
      'change @ui.inputFile' : 'onChangeFileInputMethod',
      'click @ui.btnDownloadSample' : 'onDownloadSample'
    },

    onRender:function() {
      if (! this.uploadSet) {
        var $fileInput = this.ui.inputFile;
        this.uploadHelper = new UploadHelper($fileInput[0]);
        this.uploadHelper.on('success', this.onUploadSuccessMethod, this);
        //$fileInput.on('change',this.onChangeFileInputMethod,this);
        this.uploadSet=true;
      }
    },


    onDestroy: function () {
      if (this.uploadSet) {
        this.uploadHelper.off('success', this.onUploadSuccessMethod, this);
        //$fileInput.off('change',this.onChangeFileInputMethod,this);
      }
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Sample download
    onDownloadSample:function() {
      if (this.importParameters && this.importParameters.urlSample)
        window.open(this.importParameters.urlSample);
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Start upload
    onStartUpload:function() {
      if (! this.hasFile)
        return;

      var _file = this.ui.inputFile[0].files[0];
      if (! _file)
        return;
      this.uploadHelper.uploadFile(_file);
      this.waitingForUpload=true;
    },


    ////////////////////////////////////////////////////////////////////////////////////
    //File input management
    onUploadSuccessMethod:function(arg) {
      if (! this.waitingForUpload)
        return;      
      this.waitingForUpload=false;
      //go to controller
      A.vent.trigger(this.importParameters.eventUpload,{file : arg.id, save : false, viewIdConfirm : this.importParameters.viewIdconfirm});
    },

    onChangeFileInputMethod:function(ev) {
      this.hasFile = ev.target.files && ev.target.files.length>0;
      if (this.hasFile)
        this.ui.btnStartUpload.removeClass('disabled');
      else
        this.ui.btnStartUpload.addClass('disabled');
    },


    ////////////////////////////////////////////////////////////////////////////////////
    //Managing data
    serializeData: function () {
      
      return {
        mainTitle : this.importParameters.title
      }
    },

    
   
  });
});
