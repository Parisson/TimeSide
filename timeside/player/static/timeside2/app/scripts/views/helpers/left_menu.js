define([
  'marionette',
  'templates',
  'injector',
  'jquery',
  'vent',
  'json!#config/config.json',
  'json!#config/views.json',
  '#qt_core/controllers/all'
],

function (Marionette, templates, injector,$,vent,Config,CfgViews,A) {
  'use strict';

  return Marionette.ItemView.extend({
    template: templates.leftmenu,
    className: 'left_menu',

    ui : {
      itemFilteredByRole : '[data-role]',
      itemFilteredByRoleArray : '[data-rolearray]',

      itemFilteredByCategory : '[data-category]'
    },

    events: {
      
    },

    ////////////////////////////
    onLogin:function() {
      var user = A.injector.get(A.injector.cfg.currentUser);
      if (! user)
        return;

      var role = user.get('role');
      console.log('LEFT-MENU : detected role is : '+role);
      this.ui.itemFilteredByRole.each(function() {
        $(this).addClass('hidden');
        if (this.dataset.role && (this.dataset.role===role || this.dataset.role==="ALL"))
          $(this).removeClass('hidden');
      });
      this.ui.itemFilteredByRoleArray.each(function() {
        $(this).addClass('hidden');
        if (this.dataset.rolearray) {
          var rolearray = this.dataset.rolearray.split(',');
          var hasRole = _.find(rolearray,function(testRole) {
            return testRole===role;
          })
          if (hasRole)
            $(this).removeClass('hidden');
        }
      });

    },
    

    ////////////////////////////
    initialize:function() {
      //listen for login
      A.vent.on(A.Cfg.eventApiOk(A.Cfg.events.auth.login),this.onLogin,this);
      A.vent.on(A.Cfg.eventApiOk(A.Cfg.events.users.me),this.onLogin,this);
    },

    onDestroy:function() {
      A.vent.off(A.Cfg.eventApi(A.Cfg.events.auth.login),this.onLogin,this);
    },

    onRender: function () {
      this.ui.itemFilteredByRole.addClass('hidden');
      this.ui.itemFilteredByRoleArray.addClass('hidden');

      this.onLogin(); //aucazou
    },

    

    //used to update if selected restaurant exists
    onPageUpdate:function() {
      


    },

    updateFromLayout:function(category) {
      //1 unselect every data-category and close all collapse
      //this.ui.itemFilteredByCategory.removeClass('active');

      //opening good collapse if exists, hiding the others
      try {
        this.ui.itemFilteredByCategory.each(function() {
          var zis=$(this);
          var collapse = zis.find('.panel-collapse');
          if (this.dataset.category===category) {
            zis.addClass('active');
            collapse.collapse('show');
          }
          else {
            zis.removeClass('active');
            collapse.collapse('hide');
          }
        });
      }
      catch(e) {console.error('Error in updateFromLayout : '+e.toString())}


    },

    serializeData: function () {
      
      return {
         
      };
    },

   

    
    

  });
});
