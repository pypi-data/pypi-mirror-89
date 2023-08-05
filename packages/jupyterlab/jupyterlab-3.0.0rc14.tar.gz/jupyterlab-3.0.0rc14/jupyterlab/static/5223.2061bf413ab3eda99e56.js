(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[5223],{13328:(r,n,e)=>{"use strict";e.d(n,{Z:()=>i});var o=e(94015);var a=e.n(o);var t=e(23645);var c=e.n(t);var s=c()(a());s.push([r.id,"/**\n * Pastel On Dark theme ported from ACE editor\n * @license MIT\n * @copyright AtomicPages LLC 2014\n * @author Dennis Thompson, AtomicPages LLC\n * @version 1.1\n * @source https://github.com/atomicpages/codemirror-pastel-on-dark-theme\n */\n\n.cm-s-pastel-on-dark.CodeMirror {\n\tbackground: #2c2827;\n\tcolor: #8F938F;\n\tline-height: 1.5;\n}\n.cm-s-pastel-on-dark div.CodeMirror-selected { background: rgba(221,240,255,0.2); }\n.cm-s-pastel-on-dark .CodeMirror-line::selection, .cm-s-pastel-on-dark .CodeMirror-line > span::selection, .cm-s-pastel-on-dark .CodeMirror-line > span > span::selection { background: rgba(221,240,255,0.2); }\n.cm-s-pastel-on-dark .CodeMirror-line::-moz-selection, .cm-s-pastel-on-dark .CodeMirror-line > span::-moz-selection, .cm-s-pastel-on-dark .CodeMirror-line > span > span::-moz-selection { background: rgba(221,240,255,0.2); }\n\n.cm-s-pastel-on-dark .CodeMirror-gutters {\n\tbackground: #34302f;\n\tborder-right: 0px;\n\tpadding: 0 3px;\n}\n.cm-s-pastel-on-dark .CodeMirror-guttermarker { color: white; }\n.cm-s-pastel-on-dark .CodeMirror-guttermarker-subtle { color: #8F938F; }\n.cm-s-pastel-on-dark .CodeMirror-linenumber { color: #8F938F; }\n.cm-s-pastel-on-dark .CodeMirror-cursor { border-left: 1px solid #A7A7A7; }\n.cm-s-pastel-on-dark span.cm-comment { color: #A6C6FF; }\n.cm-s-pastel-on-dark span.cm-atom { color: #DE8E30; }\n.cm-s-pastel-on-dark span.cm-number { color: #CCCCCC; }\n.cm-s-pastel-on-dark span.cm-property { color: #8F938F; }\n.cm-s-pastel-on-dark span.cm-attribute { color: #a6e22e; }\n.cm-s-pastel-on-dark span.cm-keyword { color: #AEB2F8; }\n.cm-s-pastel-on-dark span.cm-string { color: #66A968; }\n.cm-s-pastel-on-dark span.cm-variable { color: #AEB2F8; }\n.cm-s-pastel-on-dark span.cm-variable-2 { color: #BEBF55; }\n.cm-s-pastel-on-dark span.cm-variable-3, .cm-s-pastel-on-dark span.cm-type { color: #DE8E30; }\n.cm-s-pastel-on-dark span.cm-def { color: #757aD8; }\n.cm-s-pastel-on-dark span.cm-bracket { color: #f8f8f2; }\n.cm-s-pastel-on-dark span.cm-tag { color: #C1C144; }\n.cm-s-pastel-on-dark span.cm-link { color: #ae81ff; }\n.cm-s-pastel-on-dark span.cm-qualifier,.cm-s-pastel-on-dark span.cm-builtin { color: #C1C144; }\n.cm-s-pastel-on-dark span.cm-error {\n\tbackground: #757aD8;\n\tcolor: #f8f8f0;\n}\n.cm-s-pastel-on-dark .CodeMirror-activeline-background { background: rgba(255, 255, 255, 0.031); }\n.cm-s-pastel-on-dark .CodeMirror-matchingbracket {\n\tborder: 1px solid rgba(255,255,255,0.25);\n\tcolor: #8F938F !important;\n\tmargin: -1px -1px 0 -1px;\n}\n","",{version:3,sources:["webpack://./node_modules/codemirror/theme/pastel-on-dark.css"],names:[],mappings:"AAAA;;;;;;;EAOE;;AAEF;CACC,mBAAmB;CACnB,cAAc;CACd,gBAAgB;AACjB;AACA,+CAA+C,iCAAiC,EAAE;AAClF,4KAA4K,iCAAiC,EAAE;AAC/M,2LAA2L,iCAAiC,EAAE;;AAE9N;CACC,mBAAmB;CACnB,iBAAiB;CACjB,cAAc;AACf;AACA,gDAAgD,YAAY,EAAE;AAC9D,uDAAuD,cAAc,EAAE;AACvE,8CAA8C,cAAc,EAAE;AAC9D,0CAA0C,8BAA8B,EAAE;AAC1E,uCAAuC,cAAc,EAAE;AACvD,oCAAoC,cAAc,EAAE;AACpD,sCAAsC,cAAc,EAAE;AACtD,wCAAwC,cAAc,EAAE;AACxD,yCAAyC,cAAc,EAAE;AACzD,uCAAuC,cAAc,EAAE;AACvD,sCAAsC,cAAc,EAAE;AACtD,wCAAwC,cAAc,EAAE;AACxD,0CAA0C,cAAc,EAAE;AAC1D,6EAA6E,cAAc,EAAE;AAC7F,mCAAmC,cAAc,EAAE;AACnD,uCAAuC,cAAc,EAAE;AACvD,mCAAmC,cAAc,EAAE;AACnD,oCAAoC,cAAc,EAAE;AACpD,8EAA8E,cAAc,EAAE;AAC9F;CACC,mBAAmB;CACnB,cAAc;AACf;AACA,yDAAyD,sCAAsC,EAAE;AACjG;CACC,wCAAwC;CACxC,yBAAyB;CACzB,wBAAwB;AACzB",sourcesContent:["/**\n * Pastel On Dark theme ported from ACE editor\n * @license MIT\n * @copyright AtomicPages LLC 2014\n * @author Dennis Thompson, AtomicPages LLC\n * @version 1.1\n * @source https://github.com/atomicpages/codemirror-pastel-on-dark-theme\n */\n\n.cm-s-pastel-on-dark.CodeMirror {\n\tbackground: #2c2827;\n\tcolor: #8F938F;\n\tline-height: 1.5;\n}\n.cm-s-pastel-on-dark div.CodeMirror-selected { background: rgba(221,240,255,0.2); }\n.cm-s-pastel-on-dark .CodeMirror-line::selection, .cm-s-pastel-on-dark .CodeMirror-line > span::selection, .cm-s-pastel-on-dark .CodeMirror-line > span > span::selection { background: rgba(221,240,255,0.2); }\n.cm-s-pastel-on-dark .CodeMirror-line::-moz-selection, .cm-s-pastel-on-dark .CodeMirror-line > span::-moz-selection, .cm-s-pastel-on-dark .CodeMirror-line > span > span::-moz-selection { background: rgba(221,240,255,0.2); }\n\n.cm-s-pastel-on-dark .CodeMirror-gutters {\n\tbackground: #34302f;\n\tborder-right: 0px;\n\tpadding: 0 3px;\n}\n.cm-s-pastel-on-dark .CodeMirror-guttermarker { color: white; }\n.cm-s-pastel-on-dark .CodeMirror-guttermarker-subtle { color: #8F938F; }\n.cm-s-pastel-on-dark .CodeMirror-linenumber { color: #8F938F; }\n.cm-s-pastel-on-dark .CodeMirror-cursor { border-left: 1px solid #A7A7A7; }\n.cm-s-pastel-on-dark span.cm-comment { color: #A6C6FF; }\n.cm-s-pastel-on-dark span.cm-atom { color: #DE8E30; }\n.cm-s-pastel-on-dark span.cm-number { color: #CCCCCC; }\n.cm-s-pastel-on-dark span.cm-property { color: #8F938F; }\n.cm-s-pastel-on-dark span.cm-attribute { color: #a6e22e; }\n.cm-s-pastel-on-dark span.cm-keyword { color: #AEB2F8; }\n.cm-s-pastel-on-dark span.cm-string { color: #66A968; }\n.cm-s-pastel-on-dark span.cm-variable { color: #AEB2F8; }\n.cm-s-pastel-on-dark span.cm-variable-2 { color: #BEBF55; }\n.cm-s-pastel-on-dark span.cm-variable-3, .cm-s-pastel-on-dark span.cm-type { color: #DE8E30; }\n.cm-s-pastel-on-dark span.cm-def { color: #757aD8; }\n.cm-s-pastel-on-dark span.cm-bracket { color: #f8f8f2; }\n.cm-s-pastel-on-dark span.cm-tag { color: #C1C144; }\n.cm-s-pastel-on-dark span.cm-link { color: #ae81ff; }\n.cm-s-pastel-on-dark span.cm-qualifier,.cm-s-pastel-on-dark span.cm-builtin { color: #C1C144; }\n.cm-s-pastel-on-dark span.cm-error {\n\tbackground: #757aD8;\n\tcolor: #f8f8f0;\n}\n.cm-s-pastel-on-dark .CodeMirror-activeline-background { background: rgba(255, 255, 255, 0.031); }\n.cm-s-pastel-on-dark .CodeMirror-matchingbracket {\n\tborder: 1px solid rgba(255,255,255,0.25);\n\tcolor: #8F938F !important;\n\tmargin: -1px -1px 0 -1px;\n}\n"],sourceRoot:""}]);const i=s},23645:r=>{"use strict";r.exports=function(r){var n=[];n.toString=function n(){return this.map((function(n){var e=r(n);if(n[2]){return"@media ".concat(n[2]," {").concat(e,"}")}return e})).join("")};n.i=function(r,e,o){if(typeof r==="string"){r=[[null,r,""]]}var a={};if(o){for(var t=0;t<this.length;t++){var c=this[t][0];if(c!=null){a[c]=true}}}for(var s=0;s<r.length;s++){var i=[].concat(r[s]);if(o&&a[i[0]]){continue}if(e){if(!i[2]){i[2]=e}else{i[2]="".concat(e," and ").concat(i[2])}}n.push(i)}};return n}},94015:r=>{"use strict";function n(r,n){return c(r)||t(r,n)||o(r,n)||e()}function e(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}function o(r,n){if(!r)return;if(typeof r==="string")return a(r,n);var e=Object.prototype.toString.call(r).slice(8,-1);if(e==="Object"&&r.constructor)e=r.constructor.name;if(e==="Map"||e==="Set")return Array.from(r);if(e==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(e))return a(r,n)}function a(r,n){if(n==null||n>r.length)n=r.length;for(var e=0,o=new Array(n);e<n;e++){o[e]=r[e]}return o}function t(r,n){if(typeof Symbol==="undefined"||!(Symbol.iterator in Object(r)))return;var e=[];var o=true;var a=false;var t=undefined;try{for(var c=r[Symbol.iterator](),s;!(o=(s=c.next()).done);o=true){e.push(s.value);if(n&&e.length===n)break}}catch(i){a=true;t=i}finally{try{if(!o&&c["return"]!=null)c["return"]()}finally{if(a)throw t}}return e}function c(r){if(Array.isArray(r))return r}r.exports=function r(e){var o=n(e,4),a=o[1],t=o[3];if(typeof btoa==="function"){var c=btoa(unescape(encodeURIComponent(JSON.stringify(t))));var s="sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(c);var i="/*# ".concat(s," */");var l=t.sources.map((function(r){return"/*# sourceURL=".concat(t.sourceRoot||"").concat(r," */")}));return[a].concat(l).concat([i]).join("\n")}return[a].join("\n")}},65223:(r,n,e)=>{"use strict";e.r(n);e.d(n,{default:()=>i});var o=e(93379);var a=e.n(o);var t=e(13328);var c={};c.insert="head";c.singleton=false;var s=a()(t.Z,c);const i=t.Z.locals||{}},93379:(r,n,e)=>{"use strict";var o=function r(){var n;return function r(){if(typeof n==="undefined"){n=Boolean(window&&document&&document.all&&!window.atob)}return n}}();var a=function r(){var n={};return function r(e){if(typeof n[e]==="undefined"){var o=document.querySelector(e);if(window.HTMLIFrameElement&&o instanceof window.HTMLIFrameElement){try{o=o.contentDocument.head}catch(a){o=null}}n[e]=o}return n[e]}}();var t=[];function c(r){var n=-1;for(var e=0;e<t.length;e++){if(t[e].identifier===r){n=e;break}}return n}function s(r,n){var e={};var o=[];for(var a=0;a<r.length;a++){var s=r[a];var i=n.base?s[0]+n.base:s[0];var l=e[i]||0;var A="".concat(i," ").concat(l);e[i]=l+1;var d=c(A);var p={css:s[1],media:s[2],sourceMap:s[3]};if(d!==-1){t[d].references++;t[d].updater(p)}else{t.push({identifier:A,updater:C(p,n),references:1})}o.push(A)}return o}function i(r){var n=document.createElement("style");var o=r.attributes||{};if(typeof o.nonce==="undefined"){var t=true?e.nc:0;if(t){o.nonce=t}}Object.keys(o).forEach((function(r){n.setAttribute(r,o[r])}));if(typeof r.insert==="function"){r.insert(n)}else{var c=a(r.insert||"head");if(!c){throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.")}c.appendChild(n)}return n}function l(r){if(r.parentNode===null){return false}r.parentNode.removeChild(r)}var A=function r(){var n=[];return function r(e,o){n[e]=o;return n.filter(Boolean).join("\n")}}();function d(r,n,e,o){var a=e?"":o.media?"@media ".concat(o.media," {").concat(o.css,"}"):o.css;if(r.styleSheet){r.styleSheet.cssText=A(n,a)}else{var t=document.createTextNode(a);var c=r.childNodes;if(c[n]){r.removeChild(c[n])}if(c.length){r.insertBefore(t,c[n])}else{r.appendChild(t)}}}function p(r,n,e){var o=e.css;var a=e.media;var t=e.sourceMap;if(a){r.setAttribute("media",a)}else{r.removeAttribute("media")}if(t&&typeof btoa!=="undefined"){o+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(t))))," */")}if(r.styleSheet){r.styleSheet.cssText=o}else{while(r.firstChild){r.removeChild(r.firstChild)}r.appendChild(document.createTextNode(o))}}var m=null;var u=0;function C(r,n){var e;var o;var a;if(n.singleton){var t=u++;e=m||(m=i(n));o=d.bind(null,e,t,false);a=d.bind(null,e,t,true)}else{e=i(n);o=p.bind(null,e,n);a=function r(){l(e)}}o(r);return function n(e){if(e){if(e.css===r.css&&e.media===r.media&&e.sourceMap===r.sourceMap){return}o(r=e)}else{a()}}}r.exports=function(r,n){n=n||{};if(!n.singleton&&typeof n.singleton!=="boolean"){n.singleton=o()}r=r||[];var e=s(r,n);return function r(o){o=o||[];if(Object.prototype.toString.call(o)!=="[object Array]"){return}for(var a=0;a<e.length;a++){var i=e[a];var l=c(i);t[l].references--}var A=s(o,n);for(var d=0;d<e.length;d++){var p=e[d];var m=c(p);if(t[m].references===0){t[m].updater();t.splice(m,1)}}e=A}}}}]);