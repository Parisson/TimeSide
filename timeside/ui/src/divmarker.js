/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Riccardo Zaccarelli
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N, $J) {

    $N.Class.create("DivMarker", $N.Core, {
        //static constant variables to retireve the Marker Html Elements (MHE)
        //to be used with the function below getHtmElm, eg:
        //getHtmElm(marker, this.MHE_OFFSET_LABEL)
        e_indexLabel:null,
        e_descriptionText:null,
        e_offsetLabel:null,
        e_deleteButton:null,
        e_okButton:null,
        e_header:null,
        e_editButton:null,
        e_titleText:null,
        me:null,
        markerMap:null,
        markerIndex:-1,
        //static constant variables for edit mode:
        EDIT_MODE_SAVED:0,
        EDIT_MODE_EDIT_TEXT:1,
        EDIT_MODE_MARKER_MOVED:2,

        initialize: function($super, markermap) {
            $super();
            //sets the fields required???? see ruler.js createPointer
            this.configure({
                //why instantiating a variable to null?
                parent: [null, 'required']
            });
            this.cfg.parent = $J("#markers_div_id");
            this.markerMap = markermap;
            this.me = this.createDiv();
        //set the index insert the div and set events on elements
        //this.setIndex(insertionIndex);
        },


        //creates a new div. By default, text is hidden and edit button is visible
        createDiv: function(){
            
            var div = this.cfg.parent;
            var markerDiv;
            if(div){
                

                //var indexLabel, descriptionText, offsetLabel, deleteButton, okButton, header, editButton, descriptionLabel;
                var margin = '1ex';

                //index label
                this.e_indexLabel = $J('<span/>')
                .addClass('markersdivIndexLabel')
                .addClass('markersdivTopElement');

                //offset label
                this.e_offsetLabel = $J('<span/>')
                .addClass('markersdivTopElement')
                .addClass('markersdivOffset')
                

                //title text
                this.e_titleText = $J('<input/>')
                .attr('type','text')
                .addClass('markersdivTitle')
                .addClass('markersdivTopElement')
                

                //close button
                this.e_deleteButton = $J('<a/>')
                .addClass('markersdivDelete')
                .addClass('markersdivTopElement')
                .attr('title','delete marker')
                .attr("href","#")
               
                //edit button
                this.e_editButton = $J('<a/>')
                .addClass('roundBorder4')
                .addClass('markersdivEdit')
                .addClass('markersdivTopElement')
                .attr('title','edit marker description')
                .attr("href","#")
                .html('<span>EDIT</span>')
                                

                //add all elements to header:
                this.e_header = $J('<div/>')
                .append(this.e_indexLabel)
                .append(this.e_offsetLabel)
                .append(this.e_titleText)
                .append(this.e_deleteButton)
                .append(this.e_editButton);
                
                //description text
                this.e_descriptionText = $J('<textarea/>')
                .addClass('markersdivDescription')

                //ok button
                this.e_okButton = $J('<a/>')
                .attr('title','save marker description and offset')
                .addClass('roundBorder6')
                .addClass('markersdivSave')
                .attr("href","#")
                .html("OK");
                //                .append($J('<img/>').attr("src","/images/marker_ok_green.png").css({
                //                    width:'3em'
                //                }))

                //create marker div and append all elements
                markerDiv = $J('<div/>')
                .append(this.e_header)
                .append(this.e_descriptionText)
                .append(this.e_okButton)
                .addClass('roundBorder8')
                .addClass('markerdiv');

            }
            return markerDiv;
        },

        setIndex: function(index){
            var map = this.markerMap;
            var marker = map.get(index);
            this.e_indexLabel.attr('title',marker.toString());
            this.e_indexLabel.html(index+1);
            this.e_offsetLabel.html(this.formatMarkerOffset(marker.offset));
            if(index!=this.markerIndex){ 
                //add it to the parent div or move the div
                if(this.markerIndex!=-1){
                    //here is the case when the div is already added, so we have to remove it from the parent
                    //The .detach() method is the same as .remove(), except that .detach() keeps
                    //all jQuery data associated with the removed elements.
                    //This method is useful when removed elements are to be reinserted into the DOM at a later time.
                    this.me.detach();
                    //note that we might have index!=this.markerIndex without the need to detach the div
                    //we leave this code to be sure, especially on loading 
                }else{
                    //div is not added: set description and title
                    this.e_descriptionText.val(marker.desc ? marker.desc : "");
                    this.e_titleText.val(marker.title ? marker.title : "");
                }
                //the div is still to be added
                var divLen = this.cfg.parent.children().length;
                //this.cfg.parent.append(this.me);
                if(index==divLen){
                    this.cfg.parent.append(this.me);
                }else{
                    $( this.cfg.parent.children()[index] ).before(this.me);
                }
            }
            
            if(!marker.isEditable || marker.isSaved){
                this.e_okButton.hide();
                this.e_descriptionText.attr('readonly','readonly').addClass('markersdivUneditable');
                this.e_titleText.attr('readonly','readonly').addClass('markersdivUneditable');
                if(!marker.isEditable){
                    this.e_deleteButton.hide();
                    this.e_editButton.hide();
                    return;
                }
            }
            if(index!=this.markerIndex){
                //update events associated to anchors
                this.markerIndex = index;
                var remove = map.remove;
                this.e_deleteButton.unbind('click').click( function(){
                    remove.apply(map,[index]);
                    return false; //avoid scrolling of the page on anchor click
                }).show();

                var dText = this.e_descriptionText;
                var tText  = this.e_titleText;
                var okB = this.e_okButton;
                this.e_editButton.unbind('click').click( function(){
                    dText.removeAttr('readonly').removeClass('markersdivUneditable').show();
                    tText.removeAttr('readonly').removeClass('markersdivUneditable').show();
                    okB.show();
                    $(this).hide();
                    tText.select();
                    return false; //avoid scrolling of the page on anchor click
                });
                var eB = this.e_editButton;
                //action for ok button
                this.e_okButton.unbind('click').click( function(){
                    //if(marker.desc !== descriptionText.val()){ //strict equality needed. See note below
                    marker.desc = dText.val();
                    marker.title = tText.val();
                    map.sendHTTP(marker,
                    
                    function(){
                    dText.attr('readonly','readonly').addClass('markersdivUneditable');
                    tText.attr('readonly','readonly').addClass('markersdivUneditable');
                    eB.show();
                    okB.hide();
                    },
                    true
                    );
                    //}
                    //                func_fem.apply(klass,[marker,editModeSaved,editButton, descriptionText,
                    //                    descriptionLabel, okButton]);
                    return false; //avoid scrolling of the page on anchor click
                });
                //set the title text width. This method
                var w = tText.parent().width();
                w-=tText.outerWidth(true)-tText.width(); //so we consider also tText margin border and padding
                var space = w-this.e_indexLabel.outerWidth(true) - this.e_offsetLabel.outerWidth(true) -
                this.e_editButton.outerWidth(true) - this.e_deleteButton.outerWidth(true);
                tText.css('width',space+'px');
            }
            if(!marker.isSaved){
                this.e_editButton.trigger('click');
            }
            
        },

        remove: function(){
            this.me.remove();
            this.e_indexLabel = null;
            this.e_descriptionText=null;
            this.e_offsetLabel=null;
            this.e_deleteButton=null;
            this.e_okButton=null;
            this.e_header=null;
            this.e_editButton=null;
            this.e_titleText=null;
            this.me=null;
        },

        formatMarkerOffset: function(markerOffset){
            //marker offset is in float format second.decimalPart
            var hours = parseInt(markerOffset/(60*24));
            markerOffset-=hours*(60*24);
            var minutes = parseInt(markerOffset/(60));
            markerOffset-=minutes*(60);
            var seconds = parseInt(markerOffset);
            markerOffset-=seconds;
            var msec = Math.round(markerOffset*100); //show only centiseconds
            //(use 1000* to show milliseconds)
            var format = (hours<10 ? "0"+hours : hours )+":"+
            (minutes<10 ? "0"+minutes : minutes )+":"+
            (seconds<10 ? "0"+seconds : seconds )+"."+
            (msec<10 ? "0"+msec : msec );
            return format;
        }
   


    });

    $N.notifyScriptLoad();

});


Object.prototype.toString = function(){
    var s="";
    for(var k in this){
        s+=k+": "+this[k]+"\n";
    }
    return s;
}