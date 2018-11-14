define([
  'jquery',
  'marionette',
  'underscore',
  'vent',
  '#behaviors/index'
],
function ($,Marionette, _, vent,behaviors) {
  'use strict';

  /****
  Tool parameters Track behavior
    We expect the view to declare in its template : 

      data-layout="show_parameters" button to show/hide
      and a data-layout="parameters_container" container to include

     And to declare a parametersConfig with {
        getParameterView() : returns a specific parameters view for this track
     } 

  ****/
  return Marionette.Behavior.extend({

    events : {
      'click [data-layout="show_parameters"]' : 'onClickShowParameters'
    },

    ui : {
      parametersContainer : '[data-layout="parameters_container"]'
    },
   
    initialize: function () {
      this.parametersConfig = this.view.parametersConfig;
    },

    onClickShowParameters:function() {
      this.$el.toggleClass('parameters-visible');
    },

    //////////////////////////////////////////////////////////////////
    onRender:function() {
      if (! ( this.parametersConfig && this.parametersConfig.getParameterView) )
        return;

      if (!this.paramView) {
        var paramView = this.parametersConfig.getParameterView();
        this.ui.parametersContainer.append(paramView.render().$el);
        this.paramView = paramView;
        this.paramView.setDaddy(this.view);
        this.view.parametersView = this.paramView;
      }
    },

    
    //destroy hook
    onDestroy:function() {
      if (this.paramView)
        this.paramView.destroy();
    }



    
  });
});
