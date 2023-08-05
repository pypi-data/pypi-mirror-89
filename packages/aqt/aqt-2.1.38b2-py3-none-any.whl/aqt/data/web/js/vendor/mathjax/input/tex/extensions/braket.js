!function(e){var t={};function r(a){if(t[a])return t[a].exports;var o=t[a]={i:a,l:!1,exports:{}};return e[a].call(o.exports,o,o.exports,r),o.l=!0,o.exports}r.m=e,r.c=t,r.d=function(e,t,a){r.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:a})},r.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},r.t=function(e,t){if(1&t&&(e=r(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var a=Object.create(null);if(r.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)r.d(a,o,function(t){return e[t]}.bind(null,o));return a},r.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return r.d(t,"a",t),t},r.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},r.p="",r(r.s=12)}([function(e,t,r){"use strict";var a,o=this&&this.__extends||(a=function(e,t){return(a=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(e,t){e.__proto__=t}||function(e,t){for(var r in t)t.hasOwnProperty(r)&&(e[r]=t[r])})(e,t)},function(e,t){function r(){this.constructor=e}a(e,t),e.prototype=null===t?Object.create(t):(r.prototype=t.prototype,new r)});Object.defineProperty(t,"__esModule",{value:!0}),t.BraketItem=void 0;var n=r(6),i=r(2),c=r(7),u=function(e){function t(){return null!==e&&e.apply(this,arguments)||this}return o(t,e),Object.defineProperty(t.prototype,"kind",{get:function(){return"braket"},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"isOpen",{get:function(){return!0},enumerable:!1,configurable:!0}),t.prototype.checkItem=function(t){return t.isKind("close")?[[this.factory.create("mml",this.toMml())],!0]:t.isKind("mml")?(this.Push(t.toMml()),this.getProperty("single")?[[this.toMml()],!0]:n.BaseItem.fail):e.prototype.checkItem.call(this,t)},t.prototype.toMml=function(){var t=e.prototype.toMml.call(this),r=this.getProperty("open"),a=this.getProperty("close");if(this.getProperty("stretchy"))return c.default.fenced(this.factory.configuration,r,t,a);var o={fence:!0,stretchy:!1,symmetric:!0,texClass:i.TEXCLASS.OPEN},n=this.create("token","mo",o,r);o.texClass=i.TEXCLASS.CLOSE;var u=this.create("token","mo",o,a);return this.create("node","mrow",[n,t,u],{open:r,close:a,texClass:i.TEXCLASS.INNER})},t}(n.BaseItem);t.BraketItem=u},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a=r(10),o=r(2),n=r(11),i={};i.Macro=a.default.Macro,i.Braket=function(e,t,r,a,o,i){var c=e.GetNext();if(""===c)throw new n.default("MissingArgFor","Missing argument for %1",e.currentCS);var u=!0;"{"===c&&(e.i++,u=!1),e.Push(e.itemFactory.create("braket").setProperties({barmax:i,barcount:0,open:r,close:a,stretchy:o,single:u}))},i.Bar=function(e,t){var r="|"===t?"|":"\u2225",a=e.stack.Top();if("braket"!==a.kind||a.getProperty("barcount")>=a.getProperty("barmax")){var n=e.create("token","mo",{texClass:o.TEXCLASS.ORD,stretchy:!1},r);e.Push(n)}else{if("|"===r&&"|"===e.GetNext()&&(e.i++,r="\u2225"),a.getProperty("stretchy")){var i=e.create("node","TeXAtom",[],{texClass:o.TEXCLASS.CLOSE});e.Push(i),a.setProperty("barcount",a.getProperty("barcount")+1),i=e.create("token","mo",{stretchy:!0,braketbar:!0},r),e.Push(i),i=e.create("node","TeXAtom",[],{texClass:o.TEXCLASS.OPEN}),e.Push(i)}else{var c=e.create("token","mo",{stretchy:!1,braketbar:!0},r);e.Push(c)}}},t.default=i},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.TEXCLASS=MathJax._.core.MmlTree.MmlNode.TEXCLASS,t.TEXCLASSNAMES=MathJax._.core.MmlTree.MmlNode.TEXCLASSNAMES,t.indentAttributes=MathJax._.core.MmlTree.MmlNode.indentAttributes,t.AbstractMmlNode=MathJax._.core.MmlTree.MmlNode.AbstractMmlNode,t.AbstractMmlTokenNode=MathJax._.core.MmlTree.MmlNode.AbstractMmlTokenNode,t.AbstractMmlLayoutNode=MathJax._.core.MmlTree.MmlNode.AbstractMmlLayoutNode,t.AbstractMmlBaseNode=MathJax._.core.MmlTree.MmlNode.AbstractMmlBaseNode,t.AbstractMmlEmptyNode=MathJax._.core.MmlTree.MmlNode.AbstractMmlEmptyNode,t.TextNode=MathJax._.core.MmlTree.MmlNode.TextNode,t.XMLNode=MathJax._.core.MmlTree.MmlNode.XMLNode},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.isObject=MathJax._.components.global.isObject,t.combineConfig=MathJax._.components.global.combineConfig,t.combineDefaults=MathJax._.components.global.combineDefaults,t.combineWithMathJax=MathJax._.components.global.combineWithMathJax,t.MathJax=MathJax._.components.global.MathJax},function(e,t,r){"use strict";var a;Object.defineProperty(t,"__esModule",{value:!0}),t.BraketConfiguration=void 0;var o=r(5),n=r(0);r(8),t.BraketConfiguration=o.Configuration.create("braket",{handler:{character:["Braket-characters"],macro:["Braket-macros"]},items:(a={},a[n.BraketItem.prototype.kind]=n.BraketItem,a)})},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.Configuration=MathJax._.input.tex.Configuration.Configuration,t.ConfigurationHandler=MathJax._.input.tex.Configuration.ConfigurationHandler,t.ParserConfiguration=MathJax._.input.tex.Configuration.ParserConfiguration},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.MmlStack=MathJax._.input.tex.StackItem.MmlStack,t.BaseItem=MathJax._.input.tex.StackItem.BaseItem},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default=MathJax._.input.tex.ParseUtil.default},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a=r(9),o=r(1);new a.CommandMap("Braket-macros",{bra:["Macro","{\\langle {#1} \\vert}",1],ket:["Macro","{\\vert {#1} \\rangle}",1],braket:["Braket","\u27e8","\u27e9",!1,1/0],set:["Braket","{","}",!1,1],Bra:["Macro","{\\left\\langle {#1} \\right\\vert}",1],Ket:["Macro","{\\left\\vert {#1} \\right\\rangle}",1],Braket:["Braket","\u27e8","\u27e9",!0,1/0],Set:["Braket","{","}",!0,1],ketbra:["Macro","{\\vert {#1} \\rangle\\langle {#2} \\vert}",2],Ketbra:["Macro","{\\left\\vert {#1} \\right\\rangle\\left\\langle {#2} \\right\\vert}",2],"|":"Bar"},o.default),new a.MacroMap("Braket-characters",{"|":"Bar"},o.default)},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.AbstractSymbolMap=MathJax._.input.tex.SymbolMap.AbstractSymbolMap,t.RegExpMap=MathJax._.input.tex.SymbolMap.RegExpMap,t.AbstractParseMap=MathJax._.input.tex.SymbolMap.AbstractParseMap,t.CharacterMap=MathJax._.input.tex.SymbolMap.CharacterMap,t.DelimiterMap=MathJax._.input.tex.SymbolMap.DelimiterMap,t.MacroMap=MathJax._.input.tex.SymbolMap.MacroMap,t.CommandMap=MathJax._.input.tex.SymbolMap.CommandMap,t.EnvironmentMap=MathJax._.input.tex.SymbolMap.EnvironmentMap},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default=MathJax._.input.tex.base.BaseMethods.default},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default=MathJax._.input.tex.TexError.default},function(e,t,r){"use strict";r.r(t);var a=r(3),o=r(4),n=r(0),i=r(1);Object(a.combineWithMathJax)({_:{input:{tex:{braket:{BraketConfiguration:o,BraketItems:n,BraketMethods:i}}}}})}]);