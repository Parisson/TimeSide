define([
  
  './test1',
  './test2'
],

function (Test1View,Test2View) {

  return {
  	views : {
    		test1 : Test1View,
        test2 : Test2View
  	},
  	popups : {
  		
  	},
  	configList : {
    }

  }
});
