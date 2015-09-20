/*!
 * Angular Material Design
 * https://github.com/angular/material
 * @license MIT
 * v0.11.0-rc2-master-587cd22
 */
function mdCardDirective(e){return{restrict:"E",link:function(r,a,i){e(a)}}}goog.provide("ng.material.components.card"),goog.require("ng.material.core"),angular.module("material.components.card",["material.core"]).directive("mdCard",mdCardDirective),mdCardDirective.$inject=["$mdTheming"],ng.material.components.card=angular.module("material.components.card");