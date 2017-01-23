define([
  'marionette',
  'templates',
  'injector',
  'jquery',
  'vent',
  'json!#config/config.json',
  'json!#config/views.json',
  'json!#config/ariannes.json',
  '#qt_core/controllers/all'
],

function (Marionette, templates, injector,$,vent,Config,CfgViews,CfgAriannes,A) {
  'use strict';

  return Marionette.ItemView.extend({
    template: templates.header,
    className: 'header',

    ui : {
      btnBack : 'button#btnBack',
      btnNavigate : 'button.btn_navigate_category',

      lblConnectedUser : '#connected_user_lbl',

      btnsHighlightCategory : '[data-category]',
      linkEditMyProfile : 'a.link_edit_myprofile',

      arianneContainer : '.breadcrumb'
    },

    events: {
       'click @ui.btnBack' : 'onClickBack',
       'click @ui.btnNavigate' : 'onClickNavigate'
    },
    

    initialize:function() {
      
    },

    onRender: function () {

    },

    //new : update arianne
    updateArianne:function(view) {
      var arianneDefinition = CfgAriannes[view.viewid];
      var html="";
      if (arianneDefinition && _.isArray(arianneDefinition) &&  arianneDefinition.length>0)
        _.each(arianneDefinition,function(_arianneElt) {
          html+= _arianneElt.url && _arianneElt.url.length>0 ? 
            '<li><a href="'+_arianneElt.url+'">'+_arianneElt.name+'</a></li>' : 
            '<li class="active">'+_arianneElt.name+'</li>';
        });
      this.ui.arianneContainer.empty().append(html);

      //console.dir(arianneDefinition);
    },

    //used to update if selected restaurant exists
    onPageUpdate:function() {
      var _currentUser = A.injector.get(A.injector.cfg.currentUser);
      if (_currentUser) {
        this.ui.lblConnectedUser.empty().append('User : '+_currentUser.get('username'));
        
      }
    },

    updateFromLayout:function(headerMode) {
      
      this.render();
    },

    serializeData: function () {
      
      return {
         
      };
    },

   

    
    

  });
});
