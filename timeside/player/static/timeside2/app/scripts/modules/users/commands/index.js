define([
  './getusers',
  './edituser',
  './createuser'
], function (getUsers,editUser,createUser) {
  return {
    getUsers: getUsers,
    editUser : editUser,
    createUser : createUser
  };
});
