
define([
  'marionette'
],

function (Marionette) {
  'use strict';

  var Router = Marionette.AppRouter.extend({
    appRoutes: {
      '': 'home',
      'temp_hom' : 'temp_home',


      'item/:idItem' : 'item_view',
      'item/:idItem/' : 'item_view',

      /*----------------- Auth---------------------------*/
      'auth/forgetpassword' : 'auth_forgetpassword',
      'reset/:token' : 'auth_newpassword',
      'logout' : 'logout',


      /*----------------- Users---------------------------*/
      /*'users/list' : 'list_users',
      'users/edit/:id' : 'edit_user',
      'users/editmine' : 'edit_myprofile',
      'users/new' : 'new_user',*/

      
    }
  });

  return Router;
});
