define([
  'marionette',
  'templates',
  'injector',
  'jquery',
  'vent',
  'hammer',
  './helpers/header',
  '#qt_core/controllers/config',
  "swiper"
],

function (Marionette, templates, injector,$,vent,Hammer,
    HeaderView,Cfg,Swiper) {
  'use strict';
  //console.log(templates);
  return Marionette.LayoutView.extend({
    template: templates.layout,
    className: 'layout',

    regions: {
      main: '.main',
      header: 'header',
      popupContainer : '.popup-container'
    },

    ui : {
      'notification'        : '.notification',
      'notificationContent' : '.notification .modal-body .alert',
      'notificationFooter'  : '.modal-footer',
      'btnClosePopup'       : '.btn-close-popup',
      'mainContainer'       : '.main-container'
    },

    

    ////////////////////////////////////////////////////////////////////////
    // Lifecycle
    initialize:function() {
      vent.on(Cfg.events.ui.notification.show,this.showNotification,this);
      vent.on(Cfg.events.ui.notification.hide,this.hideNotification,this);
      vent.on(Cfg.events.ui.popup.forceclose,this.forceClosePopup,this); //called by navigation when show view
     

      this.currentPopup=undefined;
      this.popup=undefined;
      this.timeoutNotification = undefined;
      this.checkRegions=false;
      
    },

    onShow: function () {
      this.headerView = new HeaderView();
      this.header.show(this.headerView);


      this.setLayout('none');

    },
   
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // LAYOUT & VIEW

    /**
      Force region to create elements if not
    **/
    assertRegionElementsExist:function() {
      if (! this.checkRegions) {
        this.header._ensureElement();
        this.popupContainer._ensureElement();
        this.checkRegions=true;
      }
    },

    /*Called from module navigation, onShow method
      Vise à mettre à jour le layout.
      view element 
      All : la page prend tout as LoginView*/
    setLayout:function(view)  {
      var layoutid = view.layoutid;
      var headerMode = view.headerMode;

      var showHeader = layoutid && layoutid!=="full" && headerMode!=="none";
      
      var _displayHeader = 'hidden';//showHeader ? 'visible' : 'hidden';
      
      this.assertRegionElementsExist();

      this.header.$el.attr('class',_displayHeader);

      this.headerView.updateFromLayout(headerMode);
      this.headerView.updateArianne(view);
    },


    /*Called from module navigation, onShow method*/
    showView:function(view) {

      this.headerView.onPageUpdate();
      this.main.show(view);
    },


    ////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // POPUP

    _getPopup:function() {
      if (this.popup)
        return this.popup;
      this.popup = $('.popup');
      return this.popup;
    },

    showPopup:function(popup) {
      this.currentPopup = popup;
      this.assertRegionElementsExist();
      this.$el.addClass("popup-visible");
      this.popupContainer.show(popup);
      this.popupContainer.$el.modal({show : true});
    },

    closePopup:function(e) {
      console.log(this, e);
      this.assertRegionElementsExist();
      if (this.currentPopup && this.currentPopup.historyBackOnClose && this.currentPopup.historyBackOnClose())
        window.history.back();
      this.popupContainer.$el.modal({show : false});
    },

    forceClosePopup:function(data) {
      this.assertRegionElementsExist();
      if (this.currentPopup && this.currentPopup.historyBackOnClose && this.currentPopup.historyBackOnClose())
        window.history.back();
      this.popupContainer.$el.modal('hide');
    },


    ////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // NOTIFICATIONS

    /**
      msg can be string (the only show)
      or can be obj {type : success|warning|info|danger, text : string,title : string, actions : [{label,callback,type}]}
    **/
    showNotification:function(msg) {

      //no notification planned in this project, for now, deactivate
      return alert(JSON.stringify(msg));

      var _hasActions = msg.actions && msg.actions.length>0;
      this.ui.notificationFooter.find('button.btn').off('click');

      var _title = msg.title ? msg.title : '...';
      this.ui.notification.find('h4')[0].innerText=_title;

      if (_.isString(msg)) {
        this.ui.notificationContent[0].innerText = msg;
      }
      else if (msg.type && msg.text){
        var _newClassName="alert-"+msg.type; //bootstrap specific
        if (this.oldClassName) {
          this.ui.notificationContent.removeClass(this.oldClassName);
        }
        this.oldClassName=_newClassName;
        this.ui.notificationContent.addClass(_newClassName);
        this.ui.notificationContent[0].innerText = msg.text;
      }

      if (_hasActions) {
        //let's create stuff
        var _innerHTML="";
        var _modalActions = [], i=0;

        _.each(msg.actions,function(_action) {
          _modalActions[i]=_action.callback;
          _innerHTML=_innerHTML+'<button class="btn btn-'+_action.type+'" data-action="'+i+'"  >'
            +'<i class="fa fa-spinner fa-spin" style="display:none;"></i>'
            +_action.label+"</button>";
          i++;
        });

        this.modalActions=_modalActions;
        this.ui.notificationFooter[0].innerHTML=_innerHTML;
        this.ui.notificationFooter.find('button.btn').on('click',_.bind(this.onClickNotificationAction,this));
        this.ui.notificationFooter.css('display','block');
      }
      else {
        this.ui.notificationFooter.css('display','none');
      }

      this.ui.notification.modal();
     
    },

    onClickNotificationAction:function(evt) {
      var _target = evt.currentTarget;
      if (_target.dataset && _target.dataset.action) {


        var _actionId = parseInt(_target.dataset.action);
        var _callback = this.modalActions[_actionId];

        this.modalActions = []; //hop
        if (_callback) {
          var _waitingElt = $(evt.currentTarget).find('i.fa-spinner');
          _waitingElt.css('display','inline-block');

          this.ui.notificationFooter.find('button.btn').off('click');

          _callback();
        }

      }
    },
   

    
    hideNotification:function() {
       this.ui.notification.modal('hide');
    }

  });
});
