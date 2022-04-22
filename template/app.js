'use strict'

var app = angular.module('app',[])

app.controller("myController", function($scope, Service){
    $scope.user = {}
    $scope.init = function() {
        Service.getSentences().then(function(res){
            $scope.sentences = res.data.data
        })
    }

    $scope.disable = function() {
        if (!$scope.user.profile || !$scope.user.experience) {
            return true
        }
        for(var i =0; i < $scope.sentences.length ; i++) {
            if(!$scope.sentences[i].response && (!$scope.sentences[i].sensivel || !$scope.sentences[i].confuso)) {
                return true;
            }
        }
        return false
    }

    $scope.send = function() {
        var tosend = {
            "user":$scope.user,
            "sentences": $scope.sentences
        }
        Service.saveResponse(tosend).then(function(res){
            console.log(res.data)
        })
    }
})

app.factory('Service', function($http) {
    return  {
        getSentences: function() {
            return $http.get("/get-sentences");
        },
        saveResponse: function(data) {
            return $http.post("/save-response",data)
        }
    }
})