define([
  'FileAPI',
  'vent',
  'injector',
  'underscore',
  'json!#config/config.json',
  'json!#config/api.json',
],

function (FileAPI, vent, injector, _,config, apiConfig) {
  'use strict';

  var upload = function (options) {
    console.log('___> Launch upload on : '+JSON.stringify(options));
    return FileAPI.upload(options);
  }

  var acceptPattern = /(.+)\//;

  var filename = function (name, idx) {
    console.log(name, idx);
    return name;
  };

  var mimeType = function (input) {
    var match = input.accept.match(acceptPattern)
    return match ? match[1] : null;
  };

  var uploadUrl = function (type) {
   var  baseUrl = injector.get(injector.cfg.baseServerUrl);

   return  /*apiConfig.api.baseUrl*/baseUrl+'/file';

  };

 

  var UploadHelper = function (fileinput, options,bind) {
    this.options = options;

    //
    this.fileinput = fileinput;
    this.type = mimeType(fileinput);

    // bind
    if (bind)
      FileAPI.event.on(fileinput, 'change', this.upload.bind(this));
  };

  UploadHelper.getDropFiles=function(dropEvent,callback) {
      FileAPI.getDropFiles(dropEvent,function(files) {
        callback.call(null,files);
      });
  };

  UploadHelper.prototype = {

    setDebugId:function(_idDebug) {
      this.debugId = _idDebug;
    },

    upload: function (event) {
      console.log('---> Launcing UPLOAD : '+this.debugId);
      var files = FileAPI.getFiles(event);
      this.lastUploadedFile = files[0];
      upload({
        headers : {"X-CSRFToken" : injector.get(injector.cfg.csrfToken)},
        url: uploadUrl(this.type),
        files: {
          file: files[0]
        },
        upload: _.bind(this.onUpload, this),
        filecomplete: _.bind(this.onComplete, this)
      });
    },

    //for drag & drop
    uploadFile:function(file) {
      this.lastUploadedFile = file;
      upload({
        headers : {"X-CSRFToken" : injector.get(injector.cfg.csrfToken)},
        url: uploadUrl(this.type),
        files: {
          file: file
        },
        upload: _.bind(this.onUpload, this),
        filecomplete: _.bind(this.onComplete, this)
      });
    },

    onUpload: function (xhr, options) {
      this.xhr = xhr;
      this.trigger('start',this.fileinput,this.lastUploadedFile);
    },

    onComplete: function (err, xhr, file) {
      console.log('---> onComplete UPLOAD : '+this.debugId);
      if (err) {
        this.trigger('error', err);
      }
      else {
        console.log('---> onComplete UPLOAD SUCCESS : '+this.debugId);
        this.trigger('success', JSON.parse(xhr.responseText), this.fileinput);
        console.log('TRIGGERED !! ---> onComplete UPLOAD SUCCESS : '+this.debugId);
      }
    }
  };

  _.extend(UploadHelper.prototype, vent);

  return UploadHelper;
});
