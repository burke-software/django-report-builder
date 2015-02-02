## bower-material

This repository contains the Bower release of [angular-material](https://github.com/angular/material).

### Installing Angular-Material

To install and use the Angular Material distribution files, change to your project's root directory.

```bash
# To get the latest stable version, use Bower from the command line.
bower install angular-material

# To get the most recent, last committed-to-master version use:
bower install angular-material#master 

# To save the bower settings for future use:
bower install angular-material --save

# Later, you can use easily update with:
bower update
```

> Please note that using Angular Material requires **Angular 1.3.x** or higher.


### Using the Bower-Material Library

Now that you have installed [locally] the Angular libraries, simply include the scripts and stylesheet in your main HTML file:

```html
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="initial-scale=1, maximum-scale=1, user-scalable=no" />
    <link rel="stylesheet" href="/bower_components/angular-material/angular-material.css">
</head>
	<body ng-app="YourApp">

	<div ng-controller="YourController">

	</div>

	<script src="/bower_components/angular/angular.js"></script>
	<script src="/bower_components/angular-aria/angular-aria.js"></script>
	<script src="/bower_components/angular-animate/angular-animate.js"></script>
	<script src="/bower_components/hammerjs/hammer.js"></script>
	<script src="/bower_components/angular-material/angular-material.js"></script>
	<script>

		// Include app dependency on ngMaterial

		angular.module( 'YourApp', [ 'ngMaterial' ] )
			.controller("YourController", YourController );

	</script>

</body>
</html>
```

#### CDN

CDN versions of Angular Material are now available at [Google Hosted Libraries](https://developers.google.com/speed/libraries/devguide#angularmaterial). 

With the Google CDN, you will not need to download local copies of the distribution files. Instead simply reference the CDN urls to easily use those remote library files. This is especially useful when using online tools such as CodePen, Plunkr, or jsFiddle.

```html
  <head>

    <!-- Angulars Material CSS now available via Google CDN; version 0.6 used here -->
    <link rel="stylesheet" href="//ajax.googleapis.com/ajax/libs/angular_material/0.6.1/angular-material.min.css">

  </head>
  <body>
  
    <!-- Angular Material Dependencies -->
    <script src="//cdn.jsdelivr.net/hammerjs/2.0.4/hammer.min.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.3.6/angular.min.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.3.6/angular-animate.min.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.3.6/angular-aria.min.js"></script>
    
    <!-- Angular Material Javascript now available via Google CDN; version 0.6 used here -->
    <script src="//ajax.googleapis.com/ajax/libs/angular_material/0.6.1/angular-material.min.js"></script>
    
  </body>
```

> Note that the above sample references the 0.6.1 CDN release. Your version will change based on the latest stable release version.

Developers seeking the latest, most-current build versions can use [RawGit.com](//rawgit.com) to
pull directly from the distribution GitHub
[Bower-Material](https://github.com/angular/bower-material) repository:

```html
  <head>

    <!-- Angulars Material CSS using RawGit to load directly from `bower-material/master` -->
    <link rel="stylesheet" href="//rawgit.com/angular/bower-material/master/angular-material.css">

  </head>
  <body>

    <!-- Angular Material Dependencies -->
    <script src="//cdn.jsdelivr.net/hammerjs/2.0.4/hammer.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.3.6/angular.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.3.6/angular-animate.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.3.6/angular-aria.js"></script>

    <!-- Angular Material Javascript using RawGit to load directly from `bower-material/master` -->
    <script src="//rawgit.com/angular/bower-material/master/angular-material.js"></script>

  </body>
```

> Please note that the above RawGit access is intended **ONLY** for development purposes or sharing
  low-traffic, temporary examples or demos with small numbers of people.
