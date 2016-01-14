var studentApp = angular.module('studentApp', ['ui.router']);

studentApp.config(function($stateProvider, $urlRouterProvider){

	$urlRouterProvider.otherwise("/student_projects");

	$stateProvider.state('student_projects', {
		url:"/student_projects",
		templateUrl: "partials/student_projects.html"
	});

	});
