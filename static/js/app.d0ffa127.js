(function(e){function t(t){for(var n,o,i=t[0],s=t[1],c=t[2],d=0,f=[];d<i.length;d++)o=i[d],Object.prototype.hasOwnProperty.call(r,o)&&r[o]&&f.push(r[o][0]),r[o]=0;for(n in s)Object.prototype.hasOwnProperty.call(s,n)&&(e[n]=s[n]);u&&u(t);while(f.length)f.shift()();return l.push.apply(l,c||[]),a()}function a(){for(var e,t=0;t<l.length;t++){for(var a=l[t],n=!0,i=1;i<a.length;i++){var s=a[i];0!==r[s]&&(n=!1)}n&&(l.splice(t--,1),e=o(o.s=a[0]))}return e}var n={},r={app:0},l=[];function o(t){if(n[t])return n[t].exports;var a=n[t]={i:t,l:!1,exports:{}};return e[t].call(a.exports,a,a.exports,o),a.l=!0,a.exports}o.m=e,o.c=n,o.d=function(e,t,a){o.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:a})},o.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},o.t=function(e,t){if(1&t&&(e=o(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var a=Object.create(null);if(o.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var n in e)o.d(a,n,function(t){return e[t]}.bind(null,n));return a},o.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return o.d(t,"a",t),t},o.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},o.p="/";var i=window["webpackJsonp"]=window["webpackJsonp"]||[],s=i.push.bind(i);i.push=t,i=i.slice();for(var c=0;c<i.length;c++)t(i[c]);var u=s;l.push([0,"chunk-vendors"]),a()})({0:function(e,t,a){e.exports=a("56d7")},"56d7":function(e,t,a){"use strict";a.r(t);a("e260"),a("e6cf"),a("cca6"),a("a79d");var n,r,l=a("2b0e"),o=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("v-app",[a("v-img",{staticClass:"align-end",attrs:{src:"http://ashewa.com/static/img/bg-mobile-fallback.jpg",gradient:"to bottom left, #8bff8b59, rgb(31 48 27 / 72%)","aspect-ratio":6}},[a("div",{staticClass:"mx-5"},[a("v-col",{staticClass:"white--text dopeStyle"},[a("h1",{staticStyle:{"font-size":"42px"}},[e._v("Ashewa")]),a("h2",{staticStyle:{"font-size":"17px"}},[a("span",{staticClass:"px-1",staticStyle:{"font-size":"20px"}},[e._v("Coming Soon!")]),e._v(" We are coming with a brand new ashewa platforms, Stay Tight. ")]),a("v-btn",{attrs:{dark:"",color:"green darken-3 dopeStyle font-weight-bold",depressed:""},on:{click:e.popUp}},[a("v-icon",[e._v("mdi-download")]),e._v(" Download Ashewa Document")],1)],1),a("v-col",{staticClass:"white--text my-5",attrs:{cols:"12",lg:"4"}},[a("h2",{staticClass:"dopeStyle",staticStyle:{"font-size":"30px"}},[e._v("CONTACT US")]),a("v-form",{ref:"form",attrs:{"lazy-validation":""},model:{value:e.valid,callback:function(t){e.valid=t},expression:"valid"}},[a("v-text-field",{staticClass:"mt-3",attrs:{dark:"",filled:"",rules:e.nameRules,outlined:"",placeholder:"Full Name"},model:{value:e.fullName,callback:function(t){e.fullName=t},expression:"fullName"}}),a("v-text-field",{attrs:{dark:"",rules:e.emailRules,filled:"",outlined:"",placeholder:"Email Address"},model:{value:e.email,callback:function(t){e.email=t},expression:"email"}}),a("v-textarea",{attrs:{filled:"",dark:"",rules:e.messageRules,outlined:"",placeholder:"Message"},model:{value:e.message,callback:function(t){e.message=t},expression:"message"}})],1),a("v-btn",{attrs:{large:"",dark:"",loading:e.loading,color:"green darken-3",width:"250"},on:{click:e.submitMessage}},[e._v("Submit")])],1),a("v-spacer",{staticClass:"mb-15"})],1)])],1)},i=[],s=(a("9911"),a("8785")),c=a("9530"),u=a.n(c),d=u()(n||(n=Object(s["a"])(["\n  mutation userMessage($email: String!, $fullName: String!, $message: String!) {\n    userMessage(email: $email, fullName: $fullName, message: $message) {\n      payload\n    }\n  }\n"]))),f=u()(r||(r=Object(s["a"])(["\n  query {\n    getCoreDocs {\n      doc\n    }\n  }\n"]))),p={data:function(){return{loading:!1,valid:!1,fullName:"",email:"",message:"",nameRules:[function(e){return!!e||"Name is required"},function(e){return e&&e.length<=50||"Name must be less than 50 characters"}],messageRules:[function(e){return!!e||"Message is required"}],emailRules:[function(e){return!!e||"E-mail is required"},function(e){return/.+@.+\..+/.test(e)||"E-mail must be valid"}],link:""}},mounted:function(){var e=this;this.$apollo.query({query:f}).then((function(t){var a=t.data;e.link="http://ashewa.com/media/".concat(a.getCoreDocs[0].doc,"")})).catch((function(e){console.error(e)}))},methods:{popUp:function(){window.open(this.link,!0)},submitMessage:function(){var e=this;this.$refs.form.validate()&&(this.loading=!0,this.$apollo.mutate({mutation:d,variables:{fullName:this.fullName,email:this.email,message:this.message}}).then((function(t){var a=t.data;e.loading=!1,a.userMessage.payload&&(alert("Thanks for your reponse"),e.$refs.form.reset())})).catch((function(t){e.loading=!1,console.error("some thing happened"),console.error(t)})))}}},m=p,h=(a("5c0b"),a("2877")),g=a("6544"),v=a.n(g),b=a("7496"),y=a("8336"),w=a("62ad"),x=a("4bd4"),k=a("132d"),S=a("adda"),O=a("2fa4"),C=a("8654"),_=a("a844"),j=Object(h["a"])(m,o,i,!1,null,null,null),N=j.exports;v()(j,{VApp:b["a"],VBtn:y["a"],VCol:w["a"],VForm:x["a"],VIcon:k["a"],VImg:S["a"],VSpacer:O["a"],VTextField:C["a"],VTextarea:_["a"]});var P=a("f309");l["a"].use(P["a"]);var $=new P["a"]({}),M=a("74ca"),q=a("2bf2"),T=a("0014"),V=a.n(T),R=a("d634"),z=a("522d");l["a"].config.productionTip=!1;var A={watchQuery:{fetchPolicy:"no-cache",errorPolicy:"ignore"},query:{fetchPolicy:"no-cache",errorPolicy:"all"}},D=new M["a"]({defaultOptions:A,cache:new q["a"],link:R["a"].from([V()({uri:"http://ashewa.com/graphql/"})]),uri:"http://ashewa.com/graphql/"}),E=new z["a"]({defaultClient:D});l["a"].use(z["a"]),new l["a"]({vuetify:$,apolloProvider:E,render:function(e){return e(N)}}).$mount("#app")},"5c0b":function(e,t,a){"use strict";a("9c0c")},"9c0c":function(e,t,a){}});
//# sourceMappingURL=app.d0ffa127.js.map
