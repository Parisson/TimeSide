define([
  'jquery',
  'marionette',
  'underscore',
  'vent',
  '#behaviors/index',
  '#upload/helpers/upload',
],
function ($,Marionette, _, vent,behaviors,UploadHelper) {
  'use strict';

  /****
  Upload behavior
    Attend de la view qu'elle porte un attribut de type 
    uploadImageTargets : [
      {container : '$selector', fileInput : '$selector'}
    ]
    Container recevra le rendu de canevas, fileInput est le sélecteur
      ATTENTION : pas testé si les sélecteurs trouvent plus d'un élément!!!! (et complexe alors...)

    this.elements contient des objets de type
      $container : $container, $fileInput : $fileInput, uploadHelper : upload helper, hasFile=0 si rien ou 1 s'il y a
        un fichier...


  ****/
  return Marionette.Behavior.extend({

   
   
    initialize: function () {
      this.elementsLoaded=false;
      this.elements = [];
      
    },

    onRender:function() {
      if (this.elementsLoaded)
        return;

      this.onChangeFileInputMethod = _.bind(this.onFileInputChangeEvent,this);
      this.onContainerClickMethod = _.bind(this.onClickContainer,this);
      this.onUploadSuccessMethod = _.bind(this.onUploadSuccess,this);
      var instance=this;
      if (this.view.uploadImageTargets) {
        _.each(this.view.uploadImageTargets,function(obj) {
          if (obj.container && obj.fileInput) {
            var $container = instance.$el.find(obj.container);
            var $fileInput = instance.$el.find(obj.fileInput);
            var idElement = obj.idElement;
            if ($container.length>0 && $fileInput.length>0) {

              var _uploadHelper = new UploadHelper($fileInput[0]);
              _uploadHelper.on('success', instance.onUploadSuccessMethod, this);
              _uploadHelper.setDebugId(idElement);

              instance.elements.push({$container : $container, $fileInput : $fileInput, 
                uploadHelper : _uploadHelper, hasFile : 0, idElement : idElement});
              $fileInput.on('change',instance.onChangeFileInputMethod);
              $container.on('click',instance.onContainerClickMethod);


            }
          }
        });
      }
      this.elementsLoaded=true;
    },



    //destroy hook
    onBeforeDestroy:function() {
      var self=this;
      _.each(this.elements,function(elt) {
        elt.$fileInput.off('change',self.onChangeFileInputMethod);
        elt.$container.off('click',self.onContainerClickMethod);
        elt.uploadHelper.off('success',self.onUploadSuccessMethod, this);
      });
    },

    //////////////////////////////////////////////////////////////////
   
    //////////////////////////////////////////////////////////////////
    // File input change event & logic for preview

    onClickContainer:function(ev) {
      ev.preventDefault();
      ev.stopImmediatePropagation();

      var inputTarget;
      _.each(this.elements,function(elt) {
        if (elt.$container[0]===ev.currentTarget)
          inputTarget=elt.$fileInput;
      });
      if (inputTarget)
        inputTarget.click();
    },

    onFileInputChangeEvent:function(ev) {
      console.log('hey on fileInputEventChange');
      var containerTarget;
      _.each(this.elements,function(elt) {
        if (elt.$fileInput[0]===ev.currentTarget) {
          containerTarget=elt.$container;
          elt.hasFile=1;
        }

      });
      if (! (containerTarget) ) {
        alert('error : missing containerTarget && uploadHelper upload behavior');
        return;
      }

      containerTarget.find("img, .sprite").remove();
          
      for (var i = 0; i < ev.target.files.length; i++) {
        var file = ev.target.files[i];
        canvasResize(file, {
            width: 600,
            height: 0,
            crop: false,
            quality: 70,
            //rotate: 90,
            callback: function (data, width, height) {
              var _loadedOnce = false;
              $('<img>').load(function () {
                  if (_loadedOnce)
                    return;
                  _loadedOnce=true;
                  if (width > height) {
                      var myWidth = containerTarget.width();
                      var myHeight = (myWidth / width) * height;
                      var myLabelHeight = containerTarget.height();
                      if (myHeight > myLabelHeight) {
                          myHeight = myLabelHeight;
                          myWidth = (width * myHeight) / Math.max(height, 1);
                      } else {
                          var myMargin = (myLabelHeight - myHeight) / 2;
                          $(this).css({
                              marginTop: myMargin,
                              marginBottom: myMargin
                          });
                      }
                  } else {
                      var myHeight = containerTarget.height();
                      var myWidth = (myHeight / height) * width;
                  }
                  $(this).css({
                      width: myWidth,
                      height: myHeight,
                      opacity: 0
                  });


                  var myWidth = containerTarget.width();
                  var myHeight = (myWidth / width) * height;
                  //containerTarget.css({ minHeight: 0 });
                  var txt = containerTarget.find(".label-text");
                  if(txt.length>0 && txt.attr("data-ok-text"))
                    txt.text(txt.attr("data-ok-text"));
                  $(this).prependTo(containerTarget).animate({ opacity: 1 }, 200);
              }).attr('src', data);
            }
        });
      }
    },


    //////////////////////////////////////////////////////////////////
    // Upload management

    onStartUploadImages:function(callBack) {
      this.successCallback = callBack;
      this.indexElements = 0;
      this.serverFiles = [];

      this.uploadNextImage();
    },

    uploadNextImage:function() {
      if (this.indexElements===this.elements.length) {
        this.endUpload();
        return;
      }

      //go to next index with file
      var newElt;
      while (this.indexElements < this.elements.length) {
        var _elt = this.elements[this.indexElements];
        if (_elt.hasFile===1 && _elt.$fileInput[0].files && _elt.$fileInput[0].files.length>0) {
          newElt = _elt;
          break;
        }
        this.indexElements++;      
      }


      if (newElt===undefined) {
        this.endUpload();
        return;
      }

      var _file = newElt.$fileInput[0].files[0];
      newElt.uploadHelper.uploadFile(_file);

    },

    onUploadSuccess:function(file, input) {
      console.log('___> Upload success on : '+JSON.stringify( this.elements[this.indexElements]));

      //fix ? well... cette méthode peut être appelée à nouveau quand le 2° upload démarre....
      var alreadyIn = _.find(this.serverFiles,function(_serverFile) {
        return _serverFile.idFile===file.id;
      });
      if (alreadyIn) {
        console.log('   Already In. Return;');
        return;
      }

      this.serverFiles.push({idFile : file.id, idElement : this.elements[this.indexElements].idElement});
      this.indexElements++;

      return this.uploadNextImage();
      //this.uploadNextImage();

    },

    endUpload:function() {
      this.successCallback(this.serverFiles);
    },




    
  });
});

