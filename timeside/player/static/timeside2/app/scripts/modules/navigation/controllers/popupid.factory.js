define([
  'json!#config/views.json',
  '#auth/views/index',
  '#visu/views/index'
],

function (Cfg,AuthViews,VisuViews) {
  'use strict';

  /**
    * view id names from views.json
    * factory called by navigation controller
    **/


  var factory = function () {
    
  };

  factory.prototype = {

    getPopup: function (popupId) {
      switch (popupId) {

        case Cfg.popups.selectItem.popupid : 
          return new VisuViews.popups.selectItem();
          break;

        /*case Cfg.popups.auth_forgetpassword.popupid : 
          return new AuthViews.popups.forgetPassword();
          break;
        case Cfg.popups.auth_newpassword.popupid : 
          return new AuthViews.popups.newPassword();
          break;
        case Cfg.popups.getinputtext.popupid : 
          return new PopupEnterText();
          break;
        case Cfg.popups.selectvalue.popupid : 
          return new PopupSelectValue();
          break;   
        case Cfg.popups.getPositivePrice.popupid : 
          return new PopupPositivePrice();
          break;       
        case Cfg.popups.manageProductsLivraison.popupid : 
          return new LivraisonViews.popups.arretsLivraison();
          break;      
        /*case Cfg.popups.carte_choosePlatDetail.popupid : 
          return new ViewsCommande.popups.choosePlatDetail();
          break;
        case Cfg.popups.recapcommande_choosePlatInMenu.popupid : 
          return new ViewsCommande.popups.choosePlatInMenu();
          break;  */
        
        default : 
          return undefined;  
      }
    }

  };


  return new factory();
});
