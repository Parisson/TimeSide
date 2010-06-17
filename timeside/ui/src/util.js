/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N, $J) {

$N.Util = {
    _loadChild: function(container, tag, className, index, contents) {
        var p = $N.cssPrefix;
        var element = container.find('.' + p + className);
        if (!element.length) {
            element = $J(document.createElement(tag)).addClass(p + className);
            if (contents[className]) {
                element.text(contents[className]);
            }
            var children = container.children();
            if (index < children.length) {
                children.eq(index).before(element);
            } else {
                container.append(element);
            }
        }
        return element;
    },

    _loadUI: function(container, skeleton, contents) {
        var i = 0;
        var elements = {};
        with ($N.Util) {
            if (skeleton[0]) {
                $J(skeleton).each((function(i, selector) {
                    var s = selector.split('.');
                    elements[$N.Util.camelize(s[1])] = _loadChild(container, s[0], s[1], i++, contents);
                }));
            } else {
                for (key in skeleton) {
                    var s = key.split('.');
                    var e = _loadChild(container, s[0], s[1], i++, contents);
                    elements[$N.Util.camelize(s[1])] = e;
                    $N.extend(elements, _loadUI(e, skeleton[key], contents));
                    
                }
            }
        }
        return elements;
    },

    loadUI: function(container, skeleton, contents) {
        return $N.Util._loadUI($J(container), skeleton, contents);
    },

    makeTimeLabel: function(offset) {
        var minutes = Math.floor(offset / 60);
        if (minutes < 10)
            minutes = '0' + minutes;
        var seconds = Math.floor(offset % 60);
        if (seconds < 10)
            seconds = '0' + seconds;
        return minutes + ':' + seconds;
    },

    camelize: function(str) {
        var parts = str.split('-'), len = parts.length;
        if (len == 1) return parts[0];

        var camelized = str.charAt(0) == '-'
          ? parts[0].charAt(0).toUpperCase() + parts[0].substring(1)
          : parts[0];

        for (var i = 1; i < len; i++)
          camelized += parts[i].charAt(0).toUpperCase() + parts[i].substring(1);

        return camelized;
    }

}

$N.notifyScriptLoad();

});
