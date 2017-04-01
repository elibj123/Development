/**
 * Created by elibj on 26-Mar-17.
 */
app = angular.module('AltTVWebGui');

app.controller(
        'MonitorCtrl',
        function($scope, $http, $interval) {
            $scope.base_api_url = 'http://127.0.0.1:8080/api/';
            $scope.monitors  = [];
                        $scope.editButtonLabel = 'Save';
            $scope.errorString = '';

            $scope.ClearForm = function() {
                $scope.editing = -1;
                $scope.monitor_name = '';
                $scope.process_name = '';
                $scope.init_path = '';
                $scope.recovery_path = '';
                $scope.interval = '';
                $scope.tolerance = '';
                $scope.editButtonLabel = 'Create';
            };

            function LoadForm() {
                $http({
                    method: 'GET',
                    url: $scope.base_api_url + 'monitor/' + $scope.monitors[$scope.editing].monitorName + '/params.json'
                })
                    .then(function(response) {
                        $scope.monitor_name = response.data.params.monitor_name;
                        $scope.process_name = response.data.params.process_name;
                        $scope.init_path = response.data.params.init_path;
                        $scope.recovery_path = response.data.params.recovery_path;
                        $scope.interval = response.data.params.interval;
                        $scope.tolerance = response.data.params.tolerance;
                        $scope.editButtonLabel = 'Save';
                    });
            }

            EditMonitor = function(index) {
                if ($scope.editing == index)
                    return;

                $scope.editing = index;
                LoadForm();
            };

            DeleteMonitor = function(index) {
                if ($scope.editing == index)
                    return;

                $http({
                    method: 'DELETE',
                    url: $scope.base_api_url + 'monitor/' + $scope.monitors[index].monitorName
                })
                    .then(function(response) {
                        $scope.refreshData();
                    });
            };

            StopMonitor = function(index) {
                $http({
                    method: 'POST',
                    url: $scope.base_api_url + 'monitor/' + $scope.monitors[index].monitorName + '/stop'
                })
                    .then(function(response) {
                       $scope.refreshData();
                    });
            };

            StartMonitor = function(index) {
                $http({
                    method: 'POST',
                    url: $scope.base_api_url + 'monitor/' + $scope.monitors[index].monitorName + '/start'
                })
                    .then(function(response) {
                        $scope.refreshData();
                    });
            };

            EnableMonitor = function(index) {
                $http({
                    method: 'POST',
                    url: $scope.base_api_url + 'monitor/' + $scope.monitors[index].monitorName + '/enable'
                })
                    .then(function(response) {
                        $scope.refreshData();
                    });
            };

            DisableMonitor = function(index) {
                $http({
                    method: 'POST',
                    url: $scope.base_api_url + 'monitor/' + $scope.monitors[index].monitorName + '/disable'
                })
                    .then(function(response) {
                        $scope.refreshData();
                    });
            };

            setMonitorsActions = function() {
                for (i = 0; i < $scope.monitors.length; i++){
                    $scope.monitors[i].actions = [];
                    if ($scope.monitors[i].monitorRunning)
                        $scope.monitors[i].actions.push({'text': 'Stop', 'target': StopMonitor});
                    else
                        $scope.monitors[i].actions.push({'text': 'Start', 'target': StartMonitor});

                    if ($scope.monitors[i].monitorEnabled)
                        $scope.monitors[i].actions.push({'text': 'Disable', 'target': DisableMonitor});
                    else
                        $scope.monitors[i].actions.push({'text': 'Enable', 'target': EnableMonitor});

                    $scope.monitors[i].actions.push(
                        {'text': 'Edit', 'target': EditMonitor});
                    $scope.monitors[i].actions.push(
                        {'text': 'Delete', 'target': DeleteMonitor});
               }
            };

            function setMonitorsIds() {
                for (i = 0; i < $scope.monitors.length; i++){
                    $scope.monitors[i].id = i;
                }
            };

            function setMonitorsColors() {
                for (i = 0; i < $scope.monitors.length; i++) {
                    monitorStatus = $scope.monitors[i].status;
                    if (monitorStatus == 'Not Responding') {
                        color = 'orange';
                    }
                    else if (monitorStatus == 'Running') {
                        color = 'greenyellow';
                    }
                    else if (monitorStatus == 'Unknown') {
                        color = 'yellow';
                    }
                    else if (monitorStatus == 'Down') {
                        color = 'red';
                    }
                    else {
                        color = 'white'
                    }
                    $scope.monitors[i].colorStyle = {'background-color': color};
                }
            };

            $scope.refreshData = function() {
                $http.get($scope.base_api_url + 'monitors/status.json').then(function (response) {
                    if (response.data.success && response.data.status.length > 0) {
                        $scope.monitors = response.data.status;
                        setMonitorsIds();
                        setMonitorsActions();
                        setMonitorsColors();
                        $scope.errorString = '';
                    }
                    else {
                        $scope.monitors = []
                        $scope.errorString = 'Errors: ';

                        errors = response.data.errors;
                        for (var i = 0; i < errors.length; i++)
                            $scope.errorString += errors[i] + '; ';
                    }
                });
            };

            $scope.SubmitMonitor = function() {
                if ($scope.editing == -1)
                    CreateMonitor();
                else
                    SaveMonitor();
            };

            SaveMonitor = function() {
                formdata = '';
                if ($scope.interval != '')
                    formdata += "&interval=" + $scope.interval;

                if ($scope.tolerance != '')
                    formdata += "&tolerance=" + $scope.tolerance;

                $http({
                    method: 'PATCH',
                    url: $scope.base_api_url + 'monitor/' + $scope.monitor_name,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    data: formdata
                })
                    .then(function(response) {
                        if (response.data.success) {
                            $scope.ClearForm();
                            $scope.refreshData();
                        }
                        else {
                            alert(response.data.errors);
                        }
                    });
            }

            CreateMonitor = function() {
                formdata = '';
                if ($scope.monitor_name == '') {
                    return;
                }

                if ($scope.process_name == '') {
                    return;
                }
                formdata += '&process_name=' + $scope.process_name;

                if ($scope.init_path == '') {
                    return;
                }
                formdata += '&init_path=' + $scope.init_path;

                if ($scope.recovery_path != '')
                    formdata += '&recovery_path=' + $scope.recovery_path;

                if ($scope.interval != '')
                    formdata += "&interval=" + $scope.interval;

                if ($scope.tolerance != '')
                    formdata += "&tolerance=" + $scope.tolerance;

                $http({
                    method: 'PUT',
                    url: $scope.base_api_url + 'monitor/' + $scope.monitor_name,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    data: formdata
                })
                    .then(function(response) {
                        if (response.data.success) {
                            $scope.ClearForm();
                            $scope.refreshData();
                        }
                        else {
                            alert(response.data.errors);
                        }
                    });
            }

            $scope.ClearForm();
            $scope.refreshData();
            $interval($scope.refreshData, 2000);
        }
);


