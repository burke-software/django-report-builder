/*!
 * Angular Material Design
 * https://github.com/angular/material
 * @license MIT
 * v0.11.0-rc2-master-587cd22
 */
function getDirective(e){function i(e){function i(i,r,o){var a=e(o[t]);r.on(n,function(e){i.$apply(function(){a(i,{$event:e})})})}return{restrict:"A",link:i}}var t="md"+e,n="$md."+e.toLowerCase();return i.$inject=["$parse"],i}goog.provide("ng.material.components.swipe"),goog.require("ng.material.core"),angular.module("material.components.swipe",["material.core"]).directive("mdSwipeLeft",getDirective("SwipeLeft")).directive("mdSwipeRight",getDirective("SwipeRight")),ng.material.components.swipe=angular.module("material.components.swipe");