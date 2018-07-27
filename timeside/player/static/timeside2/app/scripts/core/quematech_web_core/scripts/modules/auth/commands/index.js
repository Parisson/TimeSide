define([
  './me',
  './login',
  './login_forheader',
  './logout',
  './register',
  './askresetpassword',
  './changepassword',
  './confirm',
  './edit'
], function (me, login, loginForHeader,logout, register, askResetPassword,changePassword, confirm,edit) {
  return {
    me: me,
    login: login,
    loginForHeader: loginForHeader,
    
    logout: logout,
    register: register,
    askResetPassword:askResetPassword,
    changePassword: changePassword,
    confirm: confirm,
    edit:edit
  };
});
