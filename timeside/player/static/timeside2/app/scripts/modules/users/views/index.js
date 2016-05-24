define([
  
  './edituser',
  './config_listusers',
  './edit_myprofile'
],

function (EditUser,ConfigListUsers,EditMyProfile) {

  return {
  	views : {
	    'editUser' : EditUser,
	    'editMyProfile' : EditMyProfile
	    
	},
	popups : {
		
	},
	configList : ConfigListUsers
  };

});
