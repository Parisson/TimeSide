define([
  
  './test1',
  './test2',

  './item_view',
  './item_new_view',

  './popups/popup_select_item'
],

function (Test1View,Test2View,ItemView,ItemNewView,PopupSelectItem) {

  return {
  	views : {
    		test1 : Test1View,
        test2 : Test2View,

        itemView : ItemView,
        itemNewView : ItemNewView
  	},
  	popups : {
  		selectItem : PopupSelectItem
  	},
  	configList : {
    }

  }
});
