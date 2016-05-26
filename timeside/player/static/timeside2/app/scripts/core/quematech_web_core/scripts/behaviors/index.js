define([
  './views/waiting',
  './views/upload_image',
  './views/navigate_viewid',


  './validate_new/validate',
  './validate_new/form',
  './popup/popup',
],

function (ViewWaiting,ViewUploadImage,ViewNavigateOnViewId,   ValidateNew,FormNew,Popup) {
  'use strict';

  return {
    viewWaiting : ViewWaiting,
    viewUploadImage : ViewUploadImage,
    viewNavigateOnViewId : ViewNavigateOnViewId,
    validate:ValidateNew,
    formNew:FormNew,
    popup:Popup
  };
});
