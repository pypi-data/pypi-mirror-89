(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[406],{75685:(e,n,r)=>{"use strict";r.d(n,{Z:()=>u});var t=r(94015);var a=r.n(t);var o=r(23645);var i=r.n(o);var c=i()(a());c.push([e.id,".cm-s-ambiance.CodeMirror {\n  -webkit-box-shadow: none;\n  -moz-box-shadow: none;\n  box-shadow: none;\n}\n","",{version:3,sources:["webpack://./node_modules/codemirror/theme/ambiance-mobile.css"],names:[],mappings:"AAAA;EACE,wBAAwB;EACxB,qBAAqB;EACrB,gBAAgB;AAClB",sourcesContent:[".cm-s-ambiance.CodeMirror {\n  -webkit-box-shadow: none;\n  -moz-box-shadow: none;\n  box-shadow: none;\n}\n"],sourceRoot:""}]);const u=c},23645:e=>{"use strict";e.exports=function(e){var n=[];n.toString=function n(){return this.map((function(n){var r=e(n);if(n[2]){return"@media ".concat(n[2]," {").concat(r,"}")}return r})).join("")};n.i=function(e,r,t){if(typeof e==="string"){e=[[null,e,""]]}var a={};if(t){for(var o=0;o<this.length;o++){var i=this[o][0];if(i!=null){a[i]=true}}}for(var c=0;c<e.length;c++){var u=[].concat(e[c]);if(t&&a[u[0]]){continue}if(r){if(!u[2]){u[2]=r}else{u[2]="".concat(r," and ").concat(u[2])}}n.push(u)}};return n}},94015:e=>{"use strict";function n(e,n){return i(e)||o(e,n)||t(e,n)||r()}function r(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}function t(e,n){if(!e)return;if(typeof e==="string")return a(e,n);var r=Object.prototype.toString.call(e).slice(8,-1);if(r==="Object"&&e.constructor)r=e.constructor.name;if(r==="Map"||r==="Set")return Array.from(e);if(r==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return a(e,n)}function a(e,n){if(n==null||n>e.length)n=e.length;for(var r=0,t=new Array(n);r<n;r++){t[r]=e[r]}return t}function o(e,n){if(typeof Symbol==="undefined"||!(Symbol.iterator in Object(e)))return;var r=[];var t=true;var a=false;var o=undefined;try{for(var i=e[Symbol.iterator](),c;!(t=(c=i.next()).done);t=true){r.push(c.value);if(n&&r.length===n)break}}catch(u){a=true;o=u}finally{try{if(!t&&i["return"]!=null)i["return"]()}finally{if(a)throw o}}return r}function i(e){if(Array.isArray(e))return e}e.exports=function e(r){var t=n(r,4),a=t[1],o=t[3];if(typeof btoa==="function"){var i=btoa(unescape(encodeURIComponent(JSON.stringify(o))));var c="sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(i);var u="/*# ".concat(c," */");var s=o.sources.map((function(e){return"/*# sourceURL=".concat(o.sourceRoot||"").concat(e," */")}));return[a].concat(s).concat([u]).join("\n")}return[a].join("\n")}},90406:(e,n,r)=>{"use strict";r.r(n);r.d(n,{default:()=>u});var t=r(93379);var a=r.n(t);var o=r(75685);var i={};i.insert="head";i.singleton=false;var c=a()(o.Z,i);const u=o.Z.locals||{}},93379:(e,n,r)=>{"use strict";var t=function e(){var n;return function e(){if(typeof n==="undefined"){n=Boolean(window&&document&&document.all&&!window.atob)}return n}}();var a=function e(){var n={};return function e(r){if(typeof n[r]==="undefined"){var t=document.querySelector(r);if(window.HTMLIFrameElement&&t instanceof window.HTMLIFrameElement){try{t=t.contentDocument.head}catch(a){t=null}}n[r]=t}return n[r]}}();var o=[];function i(e){var n=-1;for(var r=0;r<o.length;r++){if(o[r].identifier===e){n=r;break}}return n}function c(e,n){var r={};var t=[];for(var a=0;a<e.length;a++){var c=e[a];var u=n.base?c[0]+n.base:c[0];var s=r[u]||0;var f="".concat(u," ").concat(s);r[u]=s+1;var l=i(f);var d={css:c[1],media:c[2],sourceMap:c[3]};if(l!==-1){o[l].references++;o[l].updater(d)}else{o.push({identifier:f,updater:h(d,n),references:1})}t.push(f)}return t}function u(e){var n=document.createElement("style");var t=e.attributes||{};if(typeof t.nonce==="undefined"){var o=true?r.nc:0;if(o){t.nonce=o}}Object.keys(t).forEach((function(e){n.setAttribute(e,t[e])}));if(typeof e.insert==="function"){e.insert(n)}else{var i=a(e.insert||"head");if(!i){throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.")}i.appendChild(n)}return n}function s(e){if(e.parentNode===null){return false}e.parentNode.removeChild(e)}var f=function e(){var n=[];return function e(r,t){n[r]=t;return n.filter(Boolean).join("\n")}}();function l(e,n,r,t){var a=r?"":t.media?"@media ".concat(t.media," {").concat(t.css,"}"):t.css;if(e.styleSheet){e.styleSheet.cssText=f(n,a)}else{var o=document.createTextNode(a);var i=e.childNodes;if(i[n]){e.removeChild(i[n])}if(i.length){e.insertBefore(o,i[n])}else{e.appendChild(o)}}}function d(e,n,r){var t=r.css;var a=r.media;var o=r.sourceMap;if(a){e.setAttribute("media",a)}else{e.removeAttribute("media")}if(o&&typeof btoa!=="undefined"){t+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(o))))," */")}if(e.styleSheet){e.styleSheet.cssText=t}else{while(e.firstChild){e.removeChild(e.firstChild)}e.appendChild(document.createTextNode(t))}}var v=null;var p=0;function h(e,n){var r;var t;var a;if(n.singleton){var o=p++;r=v||(v=u(n));t=l.bind(null,r,o,false);a=l.bind(null,r,o,true)}else{r=u(n);t=d.bind(null,r,n);a=function e(){s(r)}}t(e);return function n(r){if(r){if(r.css===e.css&&r.media===e.media&&r.sourceMap===e.sourceMap){return}t(e=r)}else{a()}}}e.exports=function(e,n){n=n||{};if(!n.singleton&&typeof n.singleton!=="boolean"){n.singleton=t()}e=e||[];var r=c(e,n);return function e(t){t=t||[];if(Object.prototype.toString.call(t)!=="[object Array]"){return}for(var a=0;a<r.length;a++){var u=r[a];var s=i(u);o[s].references--}var f=c(t,n);for(var l=0;l<r.length;l++){var d=r[l];var v=i(d);if(o[v].references===0){o[v].updater();o.splice(v,1)}}r=f}}}}]);