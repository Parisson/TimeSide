define([
  './views/waiting',
  './views/upload_image',
  './views/navigate_viewid',
  './views/parameters_track',


  './validate_new/validate',
  './validate_new/form',
  './popup/popup',
],

function (ViewWaiting,ViewUploadImage,ViewNavigateOnViewId, ParameterTrack,  ValidateNew,FormNew,Popup) {
  'use strict';

  return {
    viewWaiting : ViewWaiting,
    viewUploadImage : ViewUploadImage,
    viewNavigateOnViewId : ViewNavigateOnViewId,
    viewParameterTrack : ParameterTrack,
    validate:ValidateNew,
    formNew:FormNew,
    popup:Popup
  };
});
