define([
  'marionette',
  'templates',
  '#qt_core/controllers/all',
  './edituser'
],

/**

  Edition / création d'un référentiel data
**/

function (Marionette, templates, A,EditUserView) {
  'use strict';

 
  return EditUserView.extend({
   
    

    ////////////////////////////////////////////////////////////////////////////////////
    //form behavior (just to override one thing)
     ////////////////////////////////////////////////////////////////////////////////////
    //Form behavior
    formConfig : _.extend(_.clone(EditUserView.prototype.formConfig),
      {
        launchEvent : /*A.Cfg.eventApi(*/A.Cfg.events.users.edit_mine/*)*/ //no more api directly, go by controller
      }
    ),

    
   
    ////////////////////////////////////////////////////////////////////////////////////
    //Life cycle

    initialize: function () {
      

    },

    onRender:function() {
      var ta = this.$el.find('textarea');

      //cf http://ckeditor.com/comment/123266#comment-123266
      /*ta.ckeditor({
        removeButtons : 'Link,Unlink,Anchor,Image,Table,HorizontalRule,SpecialChar,Styles,Format,About,NumberedList,BulletedList,Outdent,Indent,Blockquote'
      });*/
       _.each(ta,function(_ta) {
        window.CKEDITOR.replace(_ta,{
          removeButtons : 'Link,Unlink,Anchor,Image,Table,HorizontalRule,SpecialChar,Styles,Format,About,NumberedList,BulletedList,Outdent,Indent,Blockquote'
        });
      });

      this.updateViewOnRoleSelected();

      var selectRole = this.$el.find('select.select-role');
      selectRole[0].disabled=true;

      
    },


    onClose: function () {
      
    },

    



    
   
  });
});
;