var app = angular.module('NoteApp', [/*'ui.router','restangular']*/]);

app.config(function($stateProvider, $urlRouterProvider, RectangularProvider) {
	$urlRouterProvider.otherwise('');
	$stateProvider.state('index', {
			url: '/',
			templateUrl: "/media/tpl/notes/notes_list.html",
			controller: "NotesList"
		})
})