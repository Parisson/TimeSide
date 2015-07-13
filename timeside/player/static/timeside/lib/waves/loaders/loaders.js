var PRS$0 = (function(o,t){o["__proto__"]={"a":t};return o["a"]===t})({},{});var DP$0 = Object.defineProperty;var GOPD$0 = Object.getOwnPropertyDescriptor;var MIXIN$0 = function(t,s){for(var p in s){if(s.hasOwnProperty(p)){DP$0(t,p,GOPD$0(s,p));}}return t};var SP$0 = Object.setPrototypeOf||function(o,p){if(PRS$0){o["__proto__"]=p;}else {DP$0(o,"__proto__",{"value":p,"configurable":true,"enumerable":false,"writable":true});}return o};var OC$0 = Object.create;/* written in ECMAscript 6 */
/**
 * @file Loaders: AudioBuffer loader and utilities
 * @author Samuel Goldszmidt
 * @version 0.1.1
 */

var _ = require('lodash'),
  events = require('events'),
  path = require('path'),
  audioContext = require("audio-context");

require("native-promise-only");

/**
 * Gets called if a parameter is missing and the expression
 * specifying the default value is evaluated.
 * @function
 */
function throwIfMissing() {
  throw new Error('Missing parameter');
}


/**
 * Loader
 * @class
 * @classdesc Promise based implementation of XMLHttpRequest Level 2 for GET method.
 */

var Loader = (function(super$0){"use strict";if(!PRS$0)MIXIN$0(Loader, super$0);var proto$0={};

  /**
   * @constructs
   * @param {string} [responseType=""] - responseType's value, "text" (equal to ""), "arraybuffer", "blob", "document" or "json"
   */
  function Loader() {var responseType = arguments[0];if(responseType === void 0)responseType = "";
    super$0.call(this);
    this.responseType = responseType;
    this.progressCb = undefined;
  }if(super$0!==null)SP$0(Loader,super$0);Loader.prototype = OC$0(super$0!==null?super$0.prototype:null,{"constructor":{"value":Loader,"configurable":true,"writable":true}, progressCallback: {"get": $progressCallback_get$0, "set": $progressCallback_set$0, "configurable":true,"enumerable":true}});DP$0(Loader,"prototype",{"configurable":false,"enumerable":false,"writable":false});

  /**
   * @function - Method for a promise based file loading.
   * Internally switch between loadOne and loadAll.
   * @public
   * @param {(string|string[])} fileURLs - The URL(s) of the files to load. Accepts a URL pointing to the file location or an array of URLs.
   * @returns {Promise}
   */
  proto$0.load = function() {var fileURLs = arguments[0];if(fileURLs === void 0)fileURLs = throwIfMissing();
    if (fileURLs === undefined) throw (new Error("load needs at least a url to load"));
    if (Array.isArray(fileURLs)) {
      return this.loadAll(fileURLs);
    } else {
      return this.loadOne(fileURLs);
    }
  };

  /**
   * @function - Load a single file
   * @private
   * @param {string} fileURL - The URL of the file to load.
   * @returns {Promise}
   */
  proto$0.loadOne = function(fileURL) {
    return this.fileLoadingRequest(fileURL);
  };

  /**
   * @function - Load all files at once in a single array and return a Promise
   * @private
   * @param {string[]} fileURLs - The URLs array of the files to load.
   * @returns {Promise}
   */
  proto$0.loadAll = function(fileURLs) {
    var urlsCount = fileURLs.length,
      promises = [];

    for (var i = 0; i < urlsCount; ++i) {
      promises.push(this.fileLoadingRequest(fileURLs[i], i));
    }

    return Promise.all(promises);
  };

  /**
   * @function - Load a file asynchronously, return a Promise.
   * @private
   * @param {string} url - The URL of the file to load
   * @param {string} [index] - The index of the file in the array of files to load
   * @returns {Promise}
   */
  proto$0.fileLoadingRequest = function(url, index) {var this$0 = this;
    var promise = new Promise(
      function(resolve, reject)  {
        var request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.index = index;
        this$0.emit('xmlhttprequest', request);
        request.responseType = this$0.responseType;
        request.addEventListener('load', function() {
          // Test request.status value, as 404 will also get there
          if (request.status === 200 || request.status === 304) {
            // Hack for iOS 7, to remove as soon as possible
            if (this.responseType === 'json' && typeof(request.response) === 'string') {
              request.response = JSON.parse(request.response);
            }
            resolve(request.response);
          } else {
            reject(new Error(request.statusText));
          }
        });
        request.addEventListener('progress', function(evt)  {
          if (this$0.progressCallback) {
            if (index !== undefined) {
              this$0.progressCallback({
                index: index,
                value: evt.loaded / evt.total,
                loaded: evt.loaded,
                total: evt.total
              });
            } else {
              this$0.progressCallback({
                value: evt.loaded / evt.total,
                loaded: evt.loaded,
                total: evt.total
              });
            }
          }
        });
        // Manage network errors
        request.addEventListener('error', function() {
          reject(new Error("Network Error"));
        });

        request.send();
      });
    return promise;
  };

  /**
   * @function - Get the callback function to get the progress of file loading process.
   * This is only for the file loading progress as decodeAudioData doesn't
   * expose a decode progress value.
   * @returns {Loader~progressCallback}
   */
  function $progressCallback_get$0() {
    return this.progressCb;
  }

  /**
   * @function - Set the callback function to get the progress of file loading process.
   * This is only for the file loading progress as decodeAudioData doesn't
   * expose a decode progress value.
   * @param {Loader~progressCallback} callback - The callback that handles the response.
   */
  function $progressCallback_set$0(callback) {
    this.progressCb = callback;
  }

MIXIN$0(Loader.prototype,proto$0);proto$0=void 0;return Loader;})(events.EventEmitter);


/**
 * AudioBufferLoader
 * @class
 * @classdesc Promise based implementation of XMLHttpRequest Level 2 for GET method and decode audio data for arraybuffer.
 * Inherit from Loader class
 */
var AudioBufferLoader = (function(super$0){"use strict";if(!PRS$0)MIXIN$0(AudioBufferLoader, super$0);var proto$0={};

  /**
   * @constructs
   * Set the responseType to 'arraybuffer' and initialize options.
   */
  function AudioBufferLoader() {
    this.options = {
      "wrapAroundExtension": 0
    };
    this.responseType = 'arraybuffer';
    super$0.call(this, this.responseType);
  }if(super$0!==null)SP$0(AudioBufferLoader,super$0);AudioBufferLoader.prototype = OC$0(super$0!==null?super$0.prototype:null,{"constructor":{"value":AudioBufferLoader,"configurable":true,"writable":true}});DP$0(AudioBufferLoader,"prototype",{"configurable":false,"enumerable":false,"writable":false});

  /**
   * @function - Method for promise audio file loading and decoding.
   * @param {(string|string[])} fileURLs - The URL(s) of the audio files to load. Accepts a URL pointing to the file location or an array of URLs.
   * @param {{wrapAroundExtension: number}} [options] - Object with a wrapAroundExtension key which set the length, in seconds to be copied from the begining
   * at the end of the returned AudioBuffer
   * @returns {Promise}
   */
  proto$0.load = function() {var fileURLs = arguments[0];if(fileURLs === void 0)fileURLs = throwIfMissing();var options = arguments[1];if(options === void 0)options = {};
    this.options = options;
    this.options.wrapAroundExtension = this.options.wrapAroundExtension || 0;
    return super$0.prototype.load.call(this, fileURLs);
  };

  /**
   * @function - Load a single audio file, decode it in an AudioBuffer, return a Promise
   * @private
   * @param {string} fileURL - The URL of the audio file location to load.
   * @returns {Promise}
   */
  proto$0.loadOne = function(fileURL) {
    return super$0.prototype.loadOne.call(this, fileURL)
      .then(
        this.decodeAudioData.bind(this),
        function(error) {
          throw error;
        });
  };

  /**
   * @function - Load all audio files at once in a single array, decode them in an array of AudioBuffers, and return a Promise.
   * @private
   * @param {string[]} fileURLs - The URLs array of the audio files to load.
   * @returns {Promise}
   */
  proto$0.loadAll = function(fileURLs) {var this$0 = this;
    return super$0.prototype.loadAll.call(this, fileURLs)
      .then(
        function(arraybuffers)  {
          return Promise.all(arraybuffers.map(function(arraybuffer)  {
            return this$0.decodeAudioData.bind(this$0)(arraybuffer);
          }));
        }, function(error)  {
          throw error; // TODO: better error handler
        });
  };

  /**
   * @function - Decode Audio Data, return a Promise
   * @private
   * @param {arraybuffer} - The arraybuffer of the loaded audio file to be decoded.
   * @returns {Promise}
   */
  proto$0.decodeAudioData = function(arraybuffer) {var this$0 = this;
    return new Promise(function(resolve, reject)  {
      audioContext.decodeAudioData(
        arraybuffer, // returned audio data array
        function(buffer)  {
          if (this$0.options.wrapAroundExtension === 0) resolve(buffer);
          else resolve(this$0.__wrapAround(buffer));
        }, function(error)  {
          reject(new Error("DecodeAudioData error"));
        }
      );
    });
  };

  /**
   * @function - WrapAround, copy the begining input buffer to the end of an output buffer
   * @private
   * @param {arraybuffer} inBuffer {arraybuffer} - The input buffer
   * @returns {arraybuffer} - The processed buffer (with frame copied from the begining to the end)
   */
  proto$0.__wrapAround = function(inBuffer) {
    var length = inBuffer.length + this.options.wrapAroundExtension * inBuffer.sampleRate,
      outBuffer = audioContext.createBuffer(inBuffer.numberOfChannels, length, inBuffer.sampleRate),
      arrayChData, arrayOutChData;
    for (var channel = 0; channel < inBuffer.numberOfChannels; channel++) {
      arrayChData = inBuffer.getChannelData(channel);
      arrayOutChData = outBuffer.getChannelData(channel);
      _.forEach(arrayOutChData, function(sample, index) {
        if (index < inBuffer.length) arrayOutChData[index] = arrayChData[index];
        else arrayOutChData[index] = arrayChData[index - inBuffer.length];
      });
    }
    return outBuffer;
  };

MIXIN$0(AudioBufferLoader.prototype,proto$0);proto$0=void 0;return AudioBufferLoader;})(Loader);


/**
 * SuperLoader
 * @class
 * @classdesc Helper to load multiple type of files, and get them in their useful type, json for json files, AudioBuffer for audio files.
 */
var SuperLoader = (function(){"use strict";var proto$0={};

  /**
   * @constructs
   * Use composition to setup appropriate file loaders
   */
  function SuperLoader() {
    this.bufferLoader = new AudioBufferLoader();
    this.loader = new Loader("json");
  }DP$0(SuperLoader,"prototype",{"configurable":false,"enumerable":false,"writable":false});


  /**
   * @function - Method for promise audio and json file loading (and decoding for audio).
   * @param {(string|string[])} fileURLs - The URL(s) of the files to load. Accepts a URL pointing to the file location or an array of URLs.
   * @param {{wrapAroundExtension: number}} [options] - Object with a wrapAroundExtension key which set the length, in seconds to be copied from the begining
   * at the end of the returned AudioBuffer
   * @returns {Promise}
   */
  proto$0.load = function() {var fileURLs = arguments[0];if(fileURLs === void 0)fileURLs = throwIfMissing();var options = arguments[1];if(options === void 0)options = {};
    this.options = options;
    this.options.wrapAroundExtension = this.options.wrapAroundExtension || 0;
    if (Array.isArray(fileURLs)) {
      var i = -1;
      var pos = [
        [],
        []
      ]; // pos is used to track the positions of each fileURL
      var otherURLs = _.filter(fileURLs, function(url, index) {
        var extname = path.extname(url);
        i += 1;
        if (extname == '.json') {
          pos[0].push(i);
          return true;
        } else {
          pos[1].push(i);
          return false;
        }
      });
      var audioURLs = _.difference(fileURLs, otherURLs);
      var promises = [];
      if (otherURLs.length > 0) promises.push(this.loader.load(otherURLs));
      if (audioURLs.length > 0) promises.push(this.bufferLoader.load(audioURLs, this.options));

      return new Promise(function(resolve, reject)  {
        Promise.all(promises).then(
          function(datas)  {
            // Need to reorder and flatten all of these fulfilled promises
            // @todo this is ugly
            if (datas.length === 1) {
              resolve(datas[0]);
            } else {
              var outData = [];
              for (var j = 0; j < pos.length; j++) {
                for (var k = 0; k < pos[j].length; k++) {
                  outData[pos[j][k]] = datas[j][k];
                }
              }
              resolve(outData);
            }
          }, function(error)  {
            throw error;
          });
      });
    }
  };

MIXIN$0(SuperLoader.prototype,proto$0);proto$0=void 0;return SuperLoader;})();

// CommonJS function export
module.exports = {
  Loader: Loader,
  AudioBufferLoader: AudioBufferLoader,
  SuperLoader: SuperLoader
};
