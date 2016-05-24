define([
  './login',
  './popups/forget_password',
  './popups/new_password'
],

function (LoginView,
	PopupForgetPassword,PopupNewPassword) {

  return {
  	views : {
	    'login' : LoginView,
	    
	},
	popups : {
		'forgetPassword' : PopupForgetPassword,
		'newPassword' : PopupNewPassword
	}
  };

});
