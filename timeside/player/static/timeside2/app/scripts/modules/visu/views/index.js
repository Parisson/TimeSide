define([
  
  './test1',
  './test2',

  './item_view'
],

function (Test1View,Test2View,ItemView) {

  return {
  	views : {
    		test1 : Test1View,
        test2 : Test2View,

        itemView : ItemView
  	},
  	popups : {
  		
  	},
  	configList : {
    }

  }
});
