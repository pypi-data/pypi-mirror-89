import{g as j,c as g,a as c}from"../common/_commonjsHelpers-4f955397.js";import{r as y}from"../common/index-378ae6ec.js";import"../common/inheritsLoose-c0355cfb.js";import{h as p,c as x}from"../common/index-253eeb75.js";import"../common/memoize.browser.esm-b0306449.js";var O=g(function(k,u){var v=c&&c.__extends||function(){var r=function(s,e){return r=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(n,t){n.__proto__=t}||function(n,t){for(var a in t)t.hasOwnProperty(a)&&(n[a]=t[a])},r(s,e)};return function(s,e){r(s,e);function n(){this.constructor=s}s.prototype=e===null?Object.create(e):(n.prototype=e.prototype,new n)}}(),l=c&&c.__makeTemplateObject||function(r,s){return Object.defineProperty?Object.defineProperty(r,"raw",{value:s}):r.raw=s,r},_=c&&c.__importStar||function(r){if(r&&r.__esModule)return r;var s={};if(r!=null)for(var e in r)Object.hasOwnProperty.call(r,e)&&(s[e]=r[e]);return s.default=r,s};Object.defineProperty(u,"__esModule",{value:!0});var b=_(y),w=function(r){v(s,r);function s(){var e=r!==null&&r.apply(this,arguments)||this;return e.thickness=function(){var n=e.props.size,t=p.parseLengthAndUnit(n).value;return t/5},e.lat=function(){var n=e.props.size,t=p.parseLengthAndUnit(n).value;return(t-e.thickness())/2},e.offset=function(){return e.lat()-e.thickness()},e.color=function(){var n=e.props.color;return p.calculateRgba(n,.75)},e.before=function(){var n=e.props.size,t=e.color(),a=e.lat(),i=e.thickness(),o=e.offset();return x.keyframes(f||(f=l([`
      0% {width: `,"px;box-shadow: ","px ","px ",", ","px ","px ",`}
      35% {width: `,";box-shadow: 0 ","px ",", 0 ","px ",`}
      70% {width: `,"px;box-shadow: ","px ","px ",", ","px ","px ",`}
      100% {box-shadow: `,"px ","px ",", ","px ","px ",`}
    `],[`
      0% {width: `,"px;box-shadow: ","px ","px ",", ","px ","px ",`}
      35% {width: `,";box-shadow: 0 ","px ",", 0 ","px ",`}
      70% {width: `,"px;box-shadow: ","px ","px ",", ","px ","px ",`}
      100% {box-shadow: `,"px ","px ",", ","px ","px ",`}
    `])),i,a,-o,t,-a,o,t,p.cssValue(n),-o,t,o,t,i,-a,-o,t,a,o,t,a,-o,t,-a,o,t)},e.after=function(){var n=e.props.size,t=e.color(),a=e.lat(),i=e.thickness(),o=e.offset();return x.keyframes(h||(h=l([`
      0% {height: `,"px;box-shadow: ","px ","px ",", ","px ","px ",`}
      35% {height: `,";box-shadow: ","px 0 ",", ","px 0 ",`}
      70% {height: `,"px;box-shadow: ","px ","px ",", ","px ","px ",`}
      100% {box-shadow: `,"px ","px ",", ","px ","px ",`}
    `],[`
      0% {height: `,"px;box-shadow: ","px ","px ",", ","px ","px ",`}
      35% {height: `,";box-shadow: ","px 0 ",", ","px 0 ",`}
      70% {height: `,"px;box-shadow: ","px ","px ",", ","px ","px ",`}
      100% {box-shadow: `,"px ","px ",", ","px ","px ",`}
    `])),i,o,a,t,-o,-a,t,p.cssValue(n),o,t,-o,t,i,o,-a,t,-o,a,t,o,a,t,-o,-a,t)},e.style=function(n){var t=e.props.size,a=p.parseLengthAndUnit(t),i=a.value,o=a.unit;return x.css(d||(d=l([`
      position: absolute;
      content: "";
      top: 50%;
      left: 50%;
      display: block;
      width: `,`;
      height: `,`;
      border-radius: `,`;
      transform: translate(-50%, -50%);
      animation-fill-mode: none;
      animation: `,` 2s infinite;
    `],[`
      position: absolute;
      content: "";
      top: 50%;
      left: 50%;
      display: block;
      width: `,`;
      height: `,`;
      border-radius: `,`;
      transform: translate(-50%, -50%);
      animation-fill-mode: none;
      animation: `,` 2s infinite;
    `])),""+i/5+o,""+i/5+o,""+i/10+o,n===1?e.before():e.after())},e.wrapper=function(){var n=e.props.size;return x.css(m||(m=l([`
      position: relative;
      width: `,`;
      height: `,`;
      transform: rotate(165deg);
    `],[`
      position: relative;
      width: `,`;
      height: `,`;
      transform: rotate(165deg);
    `])),p.cssValue(n),p.cssValue(n))},e}return s.prototype.render=function(){var e=this.props,n=e.loading,t=e.css;return n?x.jsx("div",{css:[this.wrapper(),t]},x.jsx("div",{css:this.style(1)}),x.jsx("div",{css:this.style(2)})):null},s.defaultProps=p.sizeDefaults(50),s}(b.PureComponent);u.default=w;var f,h,d,m}),z=j(O);export default z;
