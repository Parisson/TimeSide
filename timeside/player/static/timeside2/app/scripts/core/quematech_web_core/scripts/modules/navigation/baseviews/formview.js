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

    /////



    ///

   //tagName: 'form', 
   behaviors: function () {
      return {
        Validate: {
          behaviorClass: behaviors.validate
        },
        Form: {
          behaviorClass: behaviors.formNew
        },
        /*Waiting: {
          behaviorClass: behaviors.viewWaiting
        },*/
        ViewUploadImage: {
          behaviorClass: behaviors.viewUploadImage
        },
      };
    },

    cancelSubmit:function() {
      //this.triggerMethod('stopWaitingEvent');
    },
    initializeResponsive : function() {
        //RESPONSIVE POSITIONS
        var that = this;
        that.swiperContainers = that.$el.find(".table-container");
        console.log(that.swiperContainers);
        this.responsive = {
            current : null,
            toDesktop : function() {
              that.swiperContainers.removeClass("swiper-container").children().removeClass("swiper-wrapper").children().removeClass("swiper-slide");
              that.responsive.clear();
            },
            toMobile : function() {
              that.swipers = [];
              that.swiperContainers.addClass("swiper-container").children().addClass("swiper-wrapper").children().addClass("swiper-slide");
              that.swiperContainers.each(function(){
                that.swipers.push(new Swiper($(this)[0], {
                  slidesPerView : "auto",
                  nested        : true
                }))  ;
              });
            }, 
            clear : function() {
              if(that.swipers)
                for (var i = 0;i< that.swipers.length;i++) {
                  that.swipers[i].destroy(true, true);
                }
            },
            always : function() {}
        };
    },
    initialize: function () { 
        
    },

    onRender:function() {
      
    },


    onClose: function () {
      
    },

    
   
  });
});
