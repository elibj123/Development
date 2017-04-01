/**
 * Created by elibj on 27-Mar-17.
 */


app = angular.module('AltTVWebGui');

app.controller(
    'KeyMapsCtrl',
    function($scope, $http, $interval) {
            $scope.base_api_url = 'http://127.0.0.1:8080/api/keymaps/';
            $scope.keymaps  = [];
            $scope.currentFileDescription = '';
            $scope.rebootAfterActivation = true;
            $scope.timeToReboot = 10;
            $scope.currentId = 0;

            $scope.Selected = function(index) {
                $scope.currentFileDescription = $scope.keymaps[index].description;
            };

            function setMapIds() {
                for (var i = 0; i < $scope.keymaps.length; i++)
                    $scope.keymaps[i].id = i
            };

            $scope.ActiveKeyMap = function() {
             //  var time = parseInt($scope.timeToReboot);
            };
            $scope.refreshData = function() {
                $http.get($scope.base_api_url + 'keymaps.json').then(function (response) {
                    if (response.data.success && response.data.maps.length > 0) {
                        $scope.keymaps = response.data.maps;
                        setMapIds()
                    }
                    else {
                        $scope.keymaps = []
                    }
                });
            };
            $scope.refreshData();
            $interval($scope.refreshData, 2000);
    }
);