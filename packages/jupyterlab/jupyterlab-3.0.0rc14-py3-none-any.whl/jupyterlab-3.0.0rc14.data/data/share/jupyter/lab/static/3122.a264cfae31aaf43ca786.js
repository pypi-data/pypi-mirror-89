(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[3122],{49627:(r,e,n)=>{"use strict";n.d(e,{Z:()=>i});var a=n(94015);var o=n.n(a);var c=n(23645);var t=n.n(c);var s=t()(o());s.push([r.id,".cm-s-erlang-dark.CodeMirror { background: #002240; color: white; }\n.cm-s-erlang-dark div.CodeMirror-selected { background: #b36539; }\n.cm-s-erlang-dark .CodeMirror-line::selection, .cm-s-erlang-dark .CodeMirror-line > span::selection, .cm-s-erlang-dark .CodeMirror-line > span > span::selection { background: rgba(179, 101, 57, .99); }\n.cm-s-erlang-dark .CodeMirror-line::-moz-selection, .cm-s-erlang-dark .CodeMirror-line > span::-moz-selection, .cm-s-erlang-dark .CodeMirror-line > span > span::-moz-selection { background: rgba(179, 101, 57, .99); }\n.cm-s-erlang-dark .CodeMirror-gutters { background: #002240; border-right: 1px solid #aaa; }\n.cm-s-erlang-dark .CodeMirror-guttermarker { color: white; }\n.cm-s-erlang-dark .CodeMirror-guttermarker-subtle { color: #d0d0d0; }\n.cm-s-erlang-dark .CodeMirror-linenumber { color: #d0d0d0; }\n.cm-s-erlang-dark .CodeMirror-cursor { border-left: 1px solid white; }\n\n.cm-s-erlang-dark span.cm-quote      { color: #ccc; }\n.cm-s-erlang-dark span.cm-atom       { color: #f133f1; }\n.cm-s-erlang-dark span.cm-attribute  { color: #ff80e1; }\n.cm-s-erlang-dark span.cm-bracket    { color: #ff9d00; }\n.cm-s-erlang-dark span.cm-builtin    { color: #eaa; }\n.cm-s-erlang-dark span.cm-comment    { color: #77f; }\n.cm-s-erlang-dark span.cm-def        { color: #e7a; }\n.cm-s-erlang-dark span.cm-keyword    { color: #ffee80; }\n.cm-s-erlang-dark span.cm-meta       { color: #50fefe; }\n.cm-s-erlang-dark span.cm-number     { color: #ffd0d0; }\n.cm-s-erlang-dark span.cm-operator   { color: #d55; }\n.cm-s-erlang-dark span.cm-property   { color: #ccc; }\n.cm-s-erlang-dark span.cm-qualifier  { color: #ccc; }\n.cm-s-erlang-dark span.cm-special    { color: #ffbbbb; }\n.cm-s-erlang-dark span.cm-string     { color: #3ad900; }\n.cm-s-erlang-dark span.cm-string-2   { color: #ccc; }\n.cm-s-erlang-dark span.cm-tag        { color: #9effff; }\n.cm-s-erlang-dark span.cm-variable   { color: #50fe50; }\n.cm-s-erlang-dark span.cm-variable-2 { color: #e0e; }\n.cm-s-erlang-dark span.cm-variable-3, .cm-s-erlang-dark span.cm-type { color: #ccc; }\n.cm-s-erlang-dark span.cm-error      { color: #9d1e15; }\n\n.cm-s-erlang-dark .CodeMirror-activeline-background { background: #013461; }\n.cm-s-erlang-dark .CodeMirror-matchingbracket { outline:1px solid grey; color:white !important; }\n","",{version:3,sources:["webpack://./node_modules/codemirror/theme/erlang-dark.css"],names:[],mappings:"AAAA,+BAA+B,mBAAmB,EAAE,YAAY,EAAE;AAClE,4CAA4C,mBAAmB,EAAE;AACjE,mKAAmK,mCAAmC,EAAE;AACxM,kLAAkL,mCAAmC,EAAE;AACvN,wCAAwC,mBAAmB,EAAE,4BAA4B,EAAE;AAC3F,6CAA6C,YAAY,EAAE;AAC3D,oDAAoD,cAAc,EAAE;AACpE,2CAA2C,cAAc,EAAE;AAC3D,uCAAuC,4BAA4B,EAAE;;AAErE,uCAAuC,WAAW,EAAE;AACpD,uCAAuC,cAAc,EAAE;AACvD,uCAAuC,cAAc,EAAE;AACvD,uCAAuC,cAAc,EAAE;AACvD,uCAAuC,WAAW,EAAE;AACpD,uCAAuC,WAAW,EAAE;AACpD,uCAAuC,WAAW,EAAE;AACpD,uCAAuC,cAAc,EAAE;AACvD,uCAAuC,cAAc,EAAE;AACvD,uCAAuC,cAAc,EAAE;AACvD,uCAAuC,WAAW,EAAE;AACpD,uCAAuC,WAAW,EAAE;AACpD,uCAAuC,WAAW,EAAE;AACpD,uCAAuC,cAAc,EAAE;AACvD,uCAAuC,cAAc,EAAE;AACvD,uCAAuC,WAAW,EAAE;AACpD,uCAAuC,cAAc,EAAE;AACvD,uCAAuC,cAAc,EAAE;AACvD,uCAAuC,WAAW,EAAE;AACpD,uEAAuE,WAAW,EAAE;AACpF,uCAAuC,cAAc,EAAE;;AAEvD,sDAAsD,mBAAmB,EAAE;AAC3E,gDAAgD,sBAAsB,EAAE,sBAAsB,EAAE",sourcesContent:[".cm-s-erlang-dark.CodeMirror { background: #002240; color: white; }\n.cm-s-erlang-dark div.CodeMirror-selected { background: #b36539; }\n.cm-s-erlang-dark .CodeMirror-line::selection, .cm-s-erlang-dark .CodeMirror-line > span::selection, .cm-s-erlang-dark .CodeMirror-line > span > span::selection { background: rgba(179, 101, 57, .99); }\n.cm-s-erlang-dark .CodeMirror-line::-moz-selection, .cm-s-erlang-dark .CodeMirror-line > span::-moz-selection, .cm-s-erlang-dark .CodeMirror-line > span > span::-moz-selection { background: rgba(179, 101, 57, .99); }\n.cm-s-erlang-dark .CodeMirror-gutters { background: #002240; border-right: 1px solid #aaa; }\n.cm-s-erlang-dark .CodeMirror-guttermarker { color: white; }\n.cm-s-erlang-dark .CodeMirror-guttermarker-subtle { color: #d0d0d0; }\n.cm-s-erlang-dark .CodeMirror-linenumber { color: #d0d0d0; }\n.cm-s-erlang-dark .CodeMirror-cursor { border-left: 1px solid white; }\n\n.cm-s-erlang-dark span.cm-quote      { color: #ccc; }\n.cm-s-erlang-dark span.cm-atom       { color: #f133f1; }\n.cm-s-erlang-dark span.cm-attribute  { color: #ff80e1; }\n.cm-s-erlang-dark span.cm-bracket    { color: #ff9d00; }\n.cm-s-erlang-dark span.cm-builtin    { color: #eaa; }\n.cm-s-erlang-dark span.cm-comment    { color: #77f; }\n.cm-s-erlang-dark span.cm-def        { color: #e7a; }\n.cm-s-erlang-dark span.cm-keyword    { color: #ffee80; }\n.cm-s-erlang-dark span.cm-meta       { color: #50fefe; }\n.cm-s-erlang-dark span.cm-number     { color: #ffd0d0; }\n.cm-s-erlang-dark span.cm-operator   { color: #d55; }\n.cm-s-erlang-dark span.cm-property   { color: #ccc; }\n.cm-s-erlang-dark span.cm-qualifier  { color: #ccc; }\n.cm-s-erlang-dark span.cm-special    { color: #ffbbbb; }\n.cm-s-erlang-dark span.cm-string     { color: #3ad900; }\n.cm-s-erlang-dark span.cm-string-2   { color: #ccc; }\n.cm-s-erlang-dark span.cm-tag        { color: #9effff; }\n.cm-s-erlang-dark span.cm-variable   { color: #50fe50; }\n.cm-s-erlang-dark span.cm-variable-2 { color: #e0e; }\n.cm-s-erlang-dark span.cm-variable-3, .cm-s-erlang-dark span.cm-type { color: #ccc; }\n.cm-s-erlang-dark span.cm-error      { color: #9d1e15; }\n\n.cm-s-erlang-dark .CodeMirror-activeline-background { background: #013461; }\n.cm-s-erlang-dark .CodeMirror-matchingbracket { outline:1px solid grey; color:white !important; }\n"],sourceRoot:""}]);const i=s},23645:r=>{"use strict";r.exports=function(r){var e=[];e.toString=function e(){return this.map((function(e){var n=r(e);if(e[2]){return"@media ".concat(e[2]," {").concat(n,"}")}return n})).join("")};e.i=function(r,n,a){if(typeof r==="string"){r=[[null,r,""]]}var o={};if(a){for(var c=0;c<this.length;c++){var t=this[c][0];if(t!=null){o[t]=true}}}for(var s=0;s<r.length;s++){var i=[].concat(r[s]);if(a&&o[i[0]]){continue}if(n){if(!i[2]){i[2]=n}else{i[2]="".concat(n," and ").concat(i[2])}}e.push(i)}};return e}},94015:r=>{"use strict";function e(r,e){return t(r)||c(r,e)||a(r,e)||n()}function n(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}function a(r,e){if(!r)return;if(typeof r==="string")return o(r,e);var n=Object.prototype.toString.call(r).slice(8,-1);if(n==="Object"&&r.constructor)n=r.constructor.name;if(n==="Map"||n==="Set")return Array.from(r);if(n==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return o(r,e)}function o(r,e){if(e==null||e>r.length)e=r.length;for(var n=0,a=new Array(e);n<e;n++){a[n]=r[n]}return a}function c(r,e){if(typeof Symbol==="undefined"||!(Symbol.iterator in Object(r)))return;var n=[];var a=true;var o=false;var c=undefined;try{for(var t=r[Symbol.iterator](),s;!(a=(s=t.next()).done);a=true){n.push(s.value);if(e&&n.length===e)break}}catch(i){o=true;c=i}finally{try{if(!a&&t["return"]!=null)t["return"]()}finally{if(o)throw c}}return n}function t(r){if(Array.isArray(r))return r}r.exports=function r(n){var a=e(n,4),o=a[1],c=a[3];if(typeof btoa==="function"){var t=btoa(unescape(encodeURIComponent(JSON.stringify(c))));var s="sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(t);var i="/*# ".concat(s," */");var l=c.sources.map((function(r){return"/*# sourceURL=".concat(c.sourceRoot||"").concat(r," */")}));return[o].concat(l).concat([i]).join("\n")}return[o].join("\n")}},43122:(r,e,n)=>{"use strict";n.r(e);n.d(e,{default:()=>i});var a=n(93379);var o=n.n(a);var c=n(49627);var t={};t.insert="head";t.singleton=false;var s=o()(c.Z,t);const i=c.Z.locals||{}},93379:(r,e,n)=>{"use strict";var a=function r(){var e;return function r(){if(typeof e==="undefined"){e=Boolean(window&&document&&document.all&&!window.atob)}return e}}();var o=function r(){var e={};return function r(n){if(typeof e[n]==="undefined"){var a=document.querySelector(n);if(window.HTMLIFrameElement&&a instanceof window.HTMLIFrameElement){try{a=a.contentDocument.head}catch(o){a=null}}e[n]=a}return e[n]}}();var c=[];function t(r){var e=-1;for(var n=0;n<c.length;n++){if(c[n].identifier===r){e=n;break}}return e}function s(r,e){var n={};var a=[];for(var o=0;o<r.length;o++){var s=r[o];var i=e.base?s[0]+e.base:s[0];var l=n[i]||0;var A="".concat(i," ").concat(l);n[i]=l+1;var d=t(A);var u={css:s[1],media:s[2],sourceMap:s[3]};if(d!==-1){c[d].references++;c[d].updater(u)}else{c.push({identifier:A,updater:p(u,e),references:1})}a.push(A)}return a}function i(r){var e=document.createElement("style");var a=r.attributes||{};if(typeof a.nonce==="undefined"){var c=true?n.nc:0;if(c){a.nonce=c}}Object.keys(a).forEach((function(r){e.setAttribute(r,a[r])}));if(typeof r.insert==="function"){r.insert(e)}else{var t=o(r.insert||"head");if(!t){throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.")}t.appendChild(e)}return e}function l(r){if(r.parentNode===null){return false}r.parentNode.removeChild(r)}var A=function r(){var e=[];return function r(n,a){e[n]=a;return e.filter(Boolean).join("\n")}}();function d(r,e,n,a){var o=n?"":a.media?"@media ".concat(a.media," {").concat(a.css,"}"):a.css;if(r.styleSheet){r.styleSheet.cssText=A(e,o)}else{var c=document.createTextNode(o);var t=r.childNodes;if(t[e]){r.removeChild(t[e])}if(t.length){r.insertBefore(c,t[e])}else{r.appendChild(c)}}}function u(r,e,n){var a=n.css;var o=n.media;var c=n.sourceMap;if(o){r.setAttribute("media",o)}else{r.removeAttribute("media")}if(c&&typeof btoa!=="undefined"){a+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(c))))," */")}if(r.styleSheet){r.styleSheet.cssText=a}else{while(r.firstChild){r.removeChild(r.firstChild)}r.appendChild(document.createTextNode(a))}}var m=null;var f=0;function p(r,e){var n;var a;var o;if(e.singleton){var c=f++;n=m||(m=i(e));a=d.bind(null,n,c,false);o=d.bind(null,n,c,true)}else{n=i(e);a=u.bind(null,n,e);o=function r(){l(n)}}a(r);return function e(n){if(n){if(n.css===r.css&&n.media===r.media&&n.sourceMap===r.sourceMap){return}a(r=n)}else{o()}}}r.exports=function(r,e){e=e||{};if(!e.singleton&&typeof e.singleton!=="boolean"){e.singleton=a()}r=r||[];var n=s(r,e);return function r(a){a=a||[];if(Object.prototype.toString.call(a)!=="[object Array]"){return}for(var o=0;o<n.length;o++){var i=n[o];var l=t(i);c[l].references--}var A=s(a,e);for(var d=0;d<n.length;d++){var u=n[d];var m=t(u);if(c[m].references===0){c[m].updater();c.splice(m,1)}}n=A}}}}]);