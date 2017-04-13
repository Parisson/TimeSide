define([
  'marionette',
  'templates',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/formview'/*,
  "ckeditor-jquery"*/
],

/**

  Edition / création d'un référentiel data
**/

function (Marionette, templates, A,FormView) {
  'use strict';

 
  return FormView.extend({
   
    ////////////////////////////////////////////////////////////////////////////////////
    //Validation behavior
    validatorConfig: {
      selectorInputs : '.edituser_form [data-validation]',
      dataattrib : 'validation',
      constraints : {
        email : {
          email : true,
          presence : true
        },
        username : {
          presence : true,
          length : {
            minimum : 4
          },
          format: {
            pattern: "[a-z0-9]+",
            flags: "i",
            message: "can only contain a-z and 0-9"
          }
        },
        password : {
          length : {
            minimum : 6
          }

        },
        confirm_password : {
          equality : "password"
        },
        telephone : {
          format: {
            pattern: "[+0-9]+",
            flags: "i",
            message: "can only contain 0-9 and +"
          }
        }
        
      },
      customValidation : function(objValues,view) {
        var result = {};

        if (view.isCreate) {
          if ((!objValues['password']) || objValues['password'].length===0)
            result['password'] = ["Please enter a password"];

          if ((!objValues['confirm_password']) || objValues['confirm_password'].length===0)
            result['confirm_password'] = ["Please confirm password"];
        }

        var re = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}/;
        if (objValues['password'] && objValues['password'].length>0 && (! re.test(objValues.password))) {
          result["password"] = ["must contain at least one lowercase, one uppercase and one number"];
        }




        return result;

      },

      updateComponent : 'updateComponentBootstrapValidation'
    },


    ////////////////////////////////////////////////////////////////////////////////////
    //Form behavior
    formConfig : {
      selectorInputs : '.edituser_form [data-validation]',
      dataattrib : 'validation',
      waitingSelector : 'button.has-spinner',
      setWaitingFunction : function(elt,isWaiting) {
        if (isWaiting)
          $(elt).addClass('active');
        else
          $(elt).removeClass('active');
      },
      launchEvent : function(view) {
        return view.isCreate ? A.Cfg.eventApi(A.Cfg.events.users.create) : A.Cfg.eventApi(A.Cfg.events.users.edit)
      },
      beforeSubmitFunction : function(data,view) {

        if (! view.isCreate)
          data['id'] = view.item.get('id');

        if (data['role']==="AGENT_DEPOT")
          delete data['zoneCommerciale'];
        else if (data['role']==="COMMERCIAL")
          delete data['depot'];
        else {
          delete data['zoneCommerciale'];
          delete data['depot'];
        }

        return data;
      },
      getWarnings : function(data,view) {
        return [];

      }
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Upload management
    //new on behavior
    uploadImageTargets : [
      /*{
        container : 'label#photo_upload_container',
        fileInput : 'input#photo_upload_input',
        idElement : 'visuel'
      }*/
    ],
      
    ////////////////////////////////////////////////////////////////////////////////////
    //View definition

    setDataNavigation:function(data) {
      this.isCreate = data.isCreate;

      this.item = this.isCreate ? new A.modelsClient.user() : A.injector.get(A.injector.cfg.currentEditData);
      
      this.mainLocale = A.injector.get(A.injector.cfg.currentMainLocale);
      this.subLocales = A.injector.get(A.injector.cfg.currentSubLocales);
      
    },

    template: templates['users/edit_user'],
    className: 'edit_user',

    ui: { 
      btnGo :'#btnGo',
      panelZoneCommerciale : '#panel_zonecommerciale',
      panelDepot : '#panel_depot',
      selectRole : '.select-role'
    },
    events: {
      'click @ui.btnGo' : 'onClickGo',
      'change @ui.selectRole' : 'updateViewOnRoleSelected'
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Logic

    /**
      Let's go
    **/
    onClickGo:function() {
      var self=this;
      this.triggerMethod('validateContentUI',function(success) {
        if (success)  
          self.triggerMethod('launchSubmit');
      });

      this.updateViewOnRoleSelected;
    },



    updateViewOnRoleSelected:function() {
      var roleSelected = this.ui.selectRole.val();
      this.ui.panelZoneCommerciale.addClass('hidden');
      this.ui.panelDepot.addClass('hidden');
      if (roleSelected==='AGENT_DEPOT') 
        this.ui.panelDepot.removeClass('hidden');

      if (roleSelected==='COMMERCIAL') 
        this.ui.panelZoneCommerciale.removeClass('hidden');

    },
   
    ////////////////////////////////////////////////////////////////////////////////////
    //Life cycle

    initialize: function () {
      

    },

    onRender:function() {
      var ta = this.$el.find('textarea');

      //cf http://ckeditor.com/comment/123266#comment-123266
      _.each(ta,function(_ta) {
        window.CKEDITOR.replace(_ta,{
          removeButtons : 'Link,Unlink,Anchor,Image,Table,HorizontalRule,SpecialChar,Styles,Format,About,NumberedList,BulletedList,Outdent,Indent,Blockquote'
        });
      });

      this.updateViewOnRoleSelected();

      
    },


    onClose: function () {
      
    },

    serializeData: function () {
      var itemJSON = this.item.toJSON();
      
      var allRoles = ["ADMIN_SI","DISPATCHER","COMMERCIAL","AGENT_DEPOT"];
      var selectByRole=this.isCreate;
      var rolesOk = _.map(allRoles,function(_role) {
        if (this.isCreate)
          return {id : _role, display : _role};

        var roleSelected = itemJSON.role && itemJSON.role===_role;
        if (roleSelected)
          selectByRole = roleSelected;
        return {id : _role, display : _role, selected : roleSelected};
      },this);


      var _allZonesCommerciales = A.injector.get(A.injector.cfg.allZonesCommerciales);
      var zonesCommercialesOK = A.AdminViewHelper.createListWithSelected(_allZonesCommerciales,'nom',this.mainLocale,
        this.isCreate ? null : (this.item.get('zoneCommerciale') ? this.item.get('zoneCommerciale').get('id') : null));

      var _allDepots = A.injector.get(A.injector.cfg.allDepots);
      var depotsOK = A.AdminViewHelper.createListWithSelected(_allDepots,'designation',this.mainLocale,
        this.isCreate ? null : (this.item.get('depot') ? this.item.get('depot').get('id') : null));

      return {
        title : this.isCreate ? "Création d'un utilisateur " : "Edition d'un utilisateur",
        item : itemJSON,
        mainLocale : this.mainLocale,
        subLocales : this.subLocales,
        zonesCommerciales : zonesCommercialesOK,
        depots : depotsOK,
        roles : rolesOk
      }
    },



    
   
  });
});
