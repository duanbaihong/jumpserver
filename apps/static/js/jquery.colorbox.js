/*
 Colorbox 1.5.14
 license: MIT
 http://www.jacklmoore.com/colorbox
*/
(function(c,p,A){function g(a,f,F){a=p.createElement(a);f&&(a.id="cbox"+f);F&&(a.style.cssText=F);return c(a)}function S(){return A.innerHeight?A.innerHeight:c(A).height()}function N(a,f){f!==Object(f)&&(f={});this.cache={};this.el=a;this.value=function(a){if(void 0===this.cache[a]){var b=c(this.el).attr("data-cbox-"+a);void 0!==b?this.cache[a]=b:void 0!==f[a]?this.cache[a]=f[a]:void 0!==T[a]&&(this.cache[a]=T[a])}return this.cache[a]};this.get=function(a){a=this.value(a);return c.isFunction(a)?a.call(this.el,
this):a}}function O(a){var b=l.length;a=(n+a)%b;return 0>a?b+a:a}function h(a,f){return Math.round((/%/.test(a)?("x"===f?v.width():S())/100:1)*parseInt(a,10))}function ea(a,f){return a.get("photo")||a.get("photoRegex").test(f)}function fa(a,f){return a.get("retinaUrl")&&1<A.devicePixelRatio?f.replace(a.get("photoRegex"),a.get("retinaSuffix")):f}function ha(a){"contains"in e[0]&&!e[0].contains(a.target)&&a.target!==w[0]&&(a.stopPropagation(),e.focus())}function G(a){G.str!==a&&(e.add(w).removeClass(G.str).addClass(a),
G.str=a)}function ma(b){n=0;b&&!1!==b&&"nofollow"!==b?(l=c(".cboxElement").filter(function(){var a=c.data(this,"colorbox");return(new N(this,a)).get("rel")===b}),n=l.index(a.el),-1===n&&(l=l.add(a.el),n=l.length-1)):l=c(a.el)}function C(a){c(p).trigger(a);q.triggerHandler(a)}function P(b){if(!H){var f=c(b).data("colorbox");a=new N(b,f);ma(a.get("rel"));if(!x){x=I=!0;G(a.get("className"));e.css({visibility:"hidden",display:"block",opacity:""});k=g("div","LoadedContent","width:0; height:0; overflow:hidden; visibility:hidden");
r.css({width:"",height:""}).append(k);t=U.height()+V.height()+r.outerHeight(!0)-r.height();u=W.width()+X.width()+r.outerWidth(!0)-r.width();y=k.outerHeight(!0);z=k.outerWidth(!0);b=h(a.get("initialWidth"),"x");f=h(a.get("initialHeight"),"y");var F=a.get("maxWidth"),d=a.get("maxHeight");a.w=(!1!==F?Math.min(b,h(F,"x")):b)-z-u;a.h=(!1!==d?Math.min(f,h(d,"y")):f)-y-t;k.css({width:"",height:a.h});m.position();C("cbox_open");a.get("onOpen");Y.add(Z).hide();e.focus();a.get("trapFocus")&&p.addEventListener&&
(p.addEventListener("focus",ha,!0),q.one("cbox_closed",function(){p.removeEventListener("focus",ha,!0)}));if(a.get("returnFocus"))q.one("cbox_closed",function(){c(a.el).focus()})}b=parseFloat(a.get("opacity"));w.css({opacity:b===b?b:"",cursor:a.get("overlayClose")?"pointer":"",visibility:"visible"}).show();a.get("closeButton")?Q.html(a.get("close")).appendTo(r):Q.appendTo("<div/>");na()}}function ia(){e||(aa=!1,v=c(A),e=g("div").attr({id:"colorbox","class":!1===c.support.opacity?"cboxIE":"",role:"dialog",
tabindex:"-1"}).hide(),w=g("div","Overlay").hide(),R=c([g("div","LoadingOverlay")[0],g("div","LoadingGraphic")[0]]),D=g("div","Wrapper"),r=g("div","Content").append(Z=g("div","Title"),ba=g("div","Current"),J=c('<button type="button"/>').attr({id:"cboxPrevious"}),K=c('<button type="button"/>').attr({id:"cboxNext"}),E=g("button","Slideshow"),R),Q=c('<button type="button"/>').attr({id:"cboxClose"}),D.append(g("div").append(g("div","TopLeft"),U=g("div","TopCenter"),g("div","TopRight")),g("div",!1,"clear:left").append(W=
g("div","MiddleLeft"),r,X=g("div","MiddleRight")),g("div",!1,"clear:left").append(g("div","BottomLeft"),V=g("div","BottomCenter"),g("div","BottomRight"))).find("div div").css({"float":"left"}),L=g("div",!1,"position:absolute; width:9999px; visibility:hidden; display:none; max-width:none;"),Y=K.add(J).add(ba).add(E));p.body&&!e.parent().length&&c(p.body).append(w,e.append(D,L))}function oa(){function b(a){1<a.which||a.shiftKey||a.altKey||a.metaKey||a.ctrlKey||(a.preventDefault(),P(this))}if(e){if(!aa)if(aa=
!0,K.click(function(){m.next()}),J.click(function(){m.prev()}),Q.click(function(){m.close()}),w.click(function(){a.get("overlayClose")&&m.close()}),c(p).bind("keydown.cbox",function(b){var c=b.keyCode;x&&a.get("escKey")&&27===c&&(b.preventDefault(),m.close());x&&a.get("arrowKey")&&l[1]&&!b.altKey&&(37===c?(b.preventDefault(),J.click()):39===c&&(b.preventDefault(),K.click()))}),c.isFunction(c.fn.on))c(p).on("click.cbox",".cboxElement",b);else c(".cboxElement").live("click.cbox",b);return!0}return!1}
function na(){var b,f=m.prep,e=++ca;I=!0;d=!1;C("cbox_purge");C("cbox_load");a.get("onLoad");a.h=a.get("height")?h(a.get("height"),"y")-y-t:a.get("innerHeight")&&h(a.get("innerHeight"),"y");a.w=a.get("width")?h(a.get("width"),"x")-z-u:a.get("innerWidth")&&h(a.get("innerWidth"),"x");a.mw=a.w;a.mh=a.h;a.get("maxWidth")&&(a.mw=h(a.get("maxWidth"),"x")-z-u,a.mw=a.w&&a.w<a.mw?a.w:a.mw);a.get("maxHeight")&&(a.mh=h(a.get("maxHeight"),"y")-y-t,a.mh=a.h&&a.h<a.mh?a.h:a.mh);var B=a.get("href");ja=setTimeout(function(){R.show()},
100);if(a.get("inline")){var da=c(B);var k=c("<div>").hide().insertBefore(da);q.one("cbox_purge",function(){k.replaceWith(da)});f(da)}else a.get("iframe")?f(" "):a.get("html")?f(a.get("html")):ea(a,B)?(B=fa(a,B),d=new Image,c(d).addClass("cboxPhoto").bind("error",function(){f(g("div","Error").html(a.get("imgError")))}).one("load",function(){e===ca&&setTimeout(function(){c.each(["alt","longdesc","aria-describedby"],function(b,f){var e=c(a.el).attr(f)||c(a.el).attr("data-"+f);e&&d.setAttribute(f,e)});
a.get("retinaImage")&&1<A.devicePixelRatio&&(d.height/=A.devicePixelRatio,d.width/=A.devicePixelRatio);if(a.get("scalePhotos")){b=function(){d.height-=d.height*e;d.width-=d.width*e};if(a.mw&&d.width>a.mw){var e=(d.width-a.mw)/d.width;b()}a.mh&&d.height>a.mh&&(e=(d.height-a.mh)/d.height,b())}a.h&&(d.style.marginTop=Math.max(a.mh-d.height,0)/2+"px");l[1]&&(a.get("loop")||l[n+1])&&(d.style.cursor="pointer",d.onclick=function(){m.next()});d.style.width=d.width+"px";d.style.height=d.height+"px";f(d)},
1)}),d.src=B):B&&L.load(B,a.get("data"),function(b,d){e===ca&&f("error"===d?g("div","Error").html(a.get("xhrError")):c(this).contents())})}var T={html:!1,photo:!1,iframe:!1,inline:!1,transition:"elastic",speed:300,fadeOut:300,width:!1,initialWidth:"600",innerWidth:!1,maxWidth:!1,height:!1,initialHeight:"450",innerHeight:!1,maxHeight:!1,scalePhotos:!0,scrolling:!0,opacity:.3,preloading:!0,className:!1,overlayClose:!0,escKey:!0,arrowKey:!0,top:!1,bottom:!1,left:!1,right:!1,fixed:!1,data:void 0,closeButton:!0,
fastIframe:!0,open:!1,reposition:!0,loop:!0,slideshow:!1,slideshowAuto:!0,slideshowSpeed:2500,slideshowStart:"start slideshow",slideshowStop:"stop slideshow",photoRegex:/\.(gif|png|jp(e|g|eg)|bmp|ico|webp|jxr|svg)((#|\?).*)?$/i,retinaImage:!1,retinaUrl:!1,retinaSuffix:"@2x.$1",current:"image {current} of {total}",previous:"previous",next:"next",close:"close",xhrError:"This content failed to load.",imgError:"This image failed to load.",returnFocus:!0,trapFocus:!0,onOpen:!1,onLoad:!1,onComplete:!1,
onCleanup:!1,onClosed:!1,rel:function(){return this.rel},href:function(){return c(this).attr("href")},title:function(){return this.title}},w,e,D,r,U,W,X,V,l,v,k,L,R,Z,ba,E,K,J,Q,Y,q=c("<a/>"),a,t,u,y,z,n,d,x,I,H,ja,ca=0,la={},aa,pa=function(){function b(){clearTimeout(ka)}function c(){if(a.get("loop")||l[n+1])b(),ka=setTimeout(m.next,a.get("slideshowSpeed"))}function d(){E.html(a.get("slideshowStop")).unbind("click.cbox").one("click.cbox",g);q.bind("cbox_complete",c).bind("cbox_load",b);e.removeClass("cboxSlideshow_off").addClass("cboxSlideshow_on")}
function g(){b();q.unbind("cbox_complete",c).unbind("cbox_load",b);E.html(a.get("slideshowStart")).unbind("click.cbox").one("click.cbox",function(){m.next();d()});e.removeClass("cboxSlideshow_on").addClass("cboxSlideshow_off")}function k(){h=!1;E.hide();b();q.unbind("cbox_complete",c).unbind("cbox_load",b);e.removeClass("cboxSlideshow_off cboxSlideshow_on")}var h,ka;return function(){h?a.get("slideshow")||(q.unbind("cbox_cleanup",k),k()):a.get("slideshow")&&l[1]&&(h=!0,q.one("cbox_cleanup",k),a.get("slideshowAuto")?
d():g(),E.show())}}();if(!c.colorbox){c(ia);var m=c.fn.colorbox=c.colorbox=function(a,f){var b=this;a=a||{};if(c.isFunction(b))b=c("<a/>"),a.open=!0;else if(!b[0])return b;if(!b[0])return b;ia();if(oa()){f&&(a.onComplete=f);b.each(function(){var b=c.data(this,"colorbox")||{};c.data(this,"colorbox",c.extend(b,a))}).addClass("cboxElement");var e=new N(b[0],a);e.get("open")&&P(b[0])}return b};m.position=function(b,f){function d(){U[0].style.width=V[0].style.width=r[0].style.width=parseInt(e[0].style.width,
10)-u+"px";r[0].style.height=W[0].style.height=X[0].style.height=parseInt(e[0].style.height,10)-t+"px"}var g=0,k=0,l=e.offset();v.unbind("resize.cbox");e.css({top:-9E4,left:-9E4});var n=v.scrollTop();var p=v.scrollLeft();a.get("fixed")?(l.top-=n,l.left-=p,e.css({position:"fixed"})):(g=n,k=p,e.css({position:"absolute"}));k=!1!==a.get("right")?k+Math.max(v.width()-a.w-z-u-h(a.get("right"),"x"),0):!1!==a.get("left")?k+h(a.get("left"),"x"):k+Math.round(Math.max(v.width()-a.w-z-u,0)/2);g=!1!==a.get("bottom")?
g+Math.max(S()-a.h-y-t-h(a.get("bottom"),"y"),0):!1!==a.get("top")?g+h(a.get("top"),"y"):g+Math.round(Math.max(S()-a.h-y-t,0)/2);e.css({top:l.top,left:l.left,visibility:"visible"});D[0].style.width=D[0].style.height="9999px";var M={width:a.w+z+u,height:a.h+y+t,top:g,left:k};if(b){var q=0;c.each(M,function(a){M[a]!==la[a]&&(q=b)});b=q}la=M;b||e.css(M);e.dequeue().animate(M,{duration:b||0,complete:function(){d();I=!1;D[0].style.width=a.w+z+u+"px";D[0].style.height=a.h+y+t+"px";a.get("reposition")&&
setTimeout(function(){v.bind("resize.cbox",m.position)},1);c.isFunction(f)&&f()},step:d})};m.resize=function(b){if(x){b=b||{};b.width&&(a.w=h(b.width,"x")-z-u);b.innerWidth&&(a.w=h(b.innerWidth,"x"));k.css({width:a.w});b.height&&(a.h=h(b.height,"y")-y-t);b.innerHeight&&(a.h=h(b.innerHeight,"y"));if(!b.innerHeight&&!b.height){var c=k.scrollTop();k.css({height:"auto"});a.h=k.height()}k.css({height:a.h});c&&k.scrollTop(c);m.position("none"===a.get("transition")?0:a.get("speed"))}};m.prep=function(b){if(x){var f=
"none"===a.get("transition")?0:a.get("speed");k.remove();k=g("div","LoadedContent").append(b);k.hide().appendTo(L.show()).css({width:function(){a.w=a.w||k.width();a.w=a.mw&&a.mw<a.w?a.mw:a.w;return a.w}(),overflow:a.get("scrolling")?"auto":"hidden"}).css({height:function(){a.h=a.h||k.height();a.h=a.mh&&a.mh<a.h?a.mh:a.h;return a.h}()}).prependTo(r);L.hide();c(d).css({"float":"none"});G(a.get("className"));var h=function(){function b(){!1===c.support.opacity&&e[0].style.removeAttribute("filter")}var d=
l.length;if(x){var g=function(){clearTimeout(ja);R.hide();C("cbox_complete");a.get("onComplete")};Z.html(a.get("title")).show();k.show();1<d?("string"===typeof a.get("current")&&ba.html(a.get("current").replace("{current}",n+1).replace("{total}",d)).show(),K[a.get("loop")||n<d-1?"show":"hide"]().html(a.get("next")),J[a.get("loop")||n?"show":"hide"]().html(a.get("previous")),pa(),a.get("preloading")&&c.each([O(-1),O(1)],function(){var a=l[this];var b=new N(a,c.data(a,"colorbox"));(a=b.get("href"))&&
ea(b,a)&&(a=fa(b,a),b=p.createElement("img"),b.src=a)})):Y.hide();if(a.get("iframe")){var h=p.createElement("iframe");"frameBorder"in h&&(h.frameBorder=0);"allowTransparency"in h&&(h.allowTransparency="true");a.get("scrolling")||(h.scrolling="no");c(h).attr({src:a.get("href"),name:(new Date).getTime(),"class":"cboxIframe",allowFullScreen:!0}).one("load",g).appendTo(k);q.one("cbox_purge",function(){h.src="//about:blank"});a.get("fastIframe")&&c(h).trigger("load")}else g();"fade"===a.get("transition")?
e.fadeTo(f,1,b):b()}};"fade"===a.get("transition")?e.fadeTo(f,0,function(){m.position(0,h)}):m.position(f,h)}};m.next=function(){!I&&l[1]&&(a.get("loop")||l[n+1])&&(n=O(1),P(l[n]))};m.prev=function(){!I&&l[1]&&(a.get("loop")||n)&&(n=O(-1),P(l[n]))};m.close=function(){x&&!H&&(H=!0,x=!1,C("cbox_cleanup"),a.get("onCleanup"),v.unbind(".cbox"),w.fadeTo(a.get("fadeOut")||0,0),e.stop().fadeTo(a.get("fadeOut")||0,0,function(){e.hide();w.hide();C("cbox_purge");k.remove();setTimeout(function(){H=!1;C("cbox_closed");
a.get("onClosed")},1)}))};m.remove=function(){e&&(e.stop(),c.colorbox.close(),e.stop(!1,!0).remove(),w.remove(),H=!1,e=null,c(".cboxElement").removeData("colorbox").removeClass("cboxElement"),c(p).unbind("click.cbox").unbind("keydown.cbox"))};m.element=function(){return c(a.el)};m.settings=T}})(jQuery,document,window);