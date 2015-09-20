/*!
 * Angular Material Design
 * https://github.com/angular/material
 * @license MIT
 * v0.11.0-rc2-master-587cd22
 */
goog.provide("ng.material.components.backdrop"),goog.require("ng.material.core"),angular.module("material.components.backdrop",["material.core"]).directive("mdBackdrop",["$mdTheming","$animate","$rootElement","$window","$log","$$rAF","$document",function(o,t,e,r,a,n,i){function p(p,m,d){var l=r.getComputedStyle(i[0].body);if("fixed"==l.position){var s=parseInt(l.height,10)+Math.abs(parseInt(l.top,10));m.css({height:s+"px"})}t.pin&&t.pin(m,e),n(function(){var t=m.parent()[0];if(t){var e=r.getComputedStyle(t);"static"==e.position&&a.warn(c)}o.inherit(m,m.parent())})}var c="<md-backdrop> may not work properly in a scrolled, static-positioned parent container.";return{restrict:"E",link:p}}]),ng.material.components.backdrop=angular.module("material.components.backdrop");