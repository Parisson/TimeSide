define([
  'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview'
],

function (Marionette,A,BaseQeopaView,d3,TrackNavigatorView,TrackWaveformView) {
  'use strict';

  return BaseQeopaView.extend({

    template: templates['visu/test2'],
    className: 'visu-test2',

    ui: {
      'btnLaunchTest' : 'button[data-layout="test"]',
    },
    events: {
      'click @ui.btnLaunchTest' : 'onLaunchTest'
    },


    ////////////////////////////////////////////////////////////////////////////////////
    //Func
    onLaunchTest:function() {

      var canvas = this.$el.find('canvas.canvas-test')[0];
      var ctx = canvas.getContext("2d");
      var img = new Image();
      var self=this;
      img.onload = function() {
        console.log('loaded img : '+img.width+" ? "+img.height);

         /// step 1 - resize to 50%
        var oc = document.createElement('canvas'),
            octx = oc.getContext('2d');

        oc.width = img.width * 0.5;
        oc.height = img.height * 0.5;
        octx.drawImage(img, 0, 0, oc.width, oc.height);

        /// step 2 - resize 50% of step 1
        octx.drawImage(oc, 0, 0, oc.width * 0.5, oc.height * 0.5);

        //step 3 - resize to final size
        //add ed scalar
        var okScalar = 1/self.scalar;//(so if scalar =2, we zoom by 2...)

        ctx.drawImage(oc, 0, 0, oc.width * 0.5*okScalar, oc.height * 0.5,
        0, 0, canvas.width, canvas.height);

      }

      img.src="/data/picture.jpg";


    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Life cycle

    initialize: function () {
        window.test = this;
        this.scalar = 1;
    },

    onRender:function() {
    },
       

    onDestroy: function () {      
    },

    onDomRefresh:function() {
    },

    serializeData: function () {
      

      return {
       
      }
    },


    
    
   
  });
});
