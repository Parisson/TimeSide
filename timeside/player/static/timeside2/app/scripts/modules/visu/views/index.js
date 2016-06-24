define([
  
  './test1',
  './test2',

  './item_view',
  './item_new_view'
],

function (Test1View,Test2View,ItemView,ItemNewView) {

  return {
  	views : {
    		test1 : Test1View,
        test2 : Test2View,

        itemView : ItemView,
        itemNewView : ItemNewView
  	},
  	popups : {
  		
  	},
  	configList : {
    }

  }
});
