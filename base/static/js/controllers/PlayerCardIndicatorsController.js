angular.module('Sportomatics')
.controller('PlayerCardIndicatorsController', ['$http', '$scope', function($http, $scope) {
    var self = this,
        url = $('#IndicatorsLink').attr('href');
    var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var monthNamesRu = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн",
        "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"];
    var localeRu = {
        'season' : 'Сезон'
    };
    var localeEn = {
        'season' : 'Season'
    };
    this.indicators_type = 'graph';
    this.field = 'goals';
    this.club = null;
    this.coach = null;
    this.groupBy = 'month';
    this.data = {};
    this.graphData = {};
    function ObjectToGenerate() {
        return {
            bindto: '#chart',
            axis: {
                x: {
                    type: 'timeseries',
                    tick: {
                        format: function (value) {
                            if (self.groupBy === 'month') return monthNames[value.getMonth()] + ' ' + value.getDate() + ', ' + value.getFullYear();
                            if (self.groupBy === 'season') return 'Сезон ' + (value.getFullYear()-1) + '-' + value.getFullYear();
                            return value;
                        }
                    }
                },
                y: {
                    min: -2,
                    label: self.field
                }
            },
            data: {
                xs: {},
                columns: [],
                colors: {

                },
                type: 'line'
            },
            point: {
                show: false
            },
            size: {
                width: 900
            },
            transition: {
            }, zoom: {
                //enabled: true,
                rescale: true
            },
            grid: {
                x: {
                    show: true
                },
                y: {
                    show: true
                }
            }

        }
    }
    this.createC3ArrayAndData = function(array, number, field, name){
        var resultArray = _.map(array, function(e){
                if(e['date'] == null){
                    console.log(new Date(e['season']['start_date'].substr(0, 4)).yyyymmdd('-'))
                    return new Date(e['season']['start_date'].substr(0,4)).yyyymmdd('-');
                }
                return new Date(e['date']).yyyymmdd('-');}
        ).sort(function(a,b){
                return new Date(a.substr(0, 4), a.substr(5, 2)-1, a.substr(8, 2)) - new Date(b.substr(0, 4),b.substr(5, 2)-1, b.substr(8, 2));
            });
        resultArray.unshift('x'+number);
        var resultArrayData = array.map(function(e){
            /*if( Object.prototype.toString.call( $scope.fieldMapping[field] ) === '[object Array]' ) {
             var sum = 0;
             _.each($scope.fieldMapping[field], function(fieldEntry){
             sum += e[fieldEntry];
             })
             return sum;
             } else*/ return e[field]; // wait for multiple players comparison
        });
        resultArrayData.unshift(name);
        return {
            array: resultArray,
            data: resultArrayData
        }
    }
    this.createFieldData = function(field, array){
        var result = [];
        var i = 0;
        //TODO: make this method accept multiple players
        var object = self.createC3ArrayAndData(array, i, field, 'Player ' + '1');
        result.push(object);
        return result;
    };

    this.setIndicatorsType = function(type) {
        this.indicators_type = type;
    };

    this.setField = function(field) {
        this.field = field;
        this.list();
    }

    this.setClub = function(club) {
        this.club = club;
        this.list();
    }

    this.setCoach = function(coach) {
        this.coach = coach;
        this.list();
    }
    this.setGraphResults = function(results) {

    }
    $scope.setGroupBy = function(groupby){
        console.log(groupby)
        self.groupBy = groupby;
        self.list();
    };
    var chart = null;
    $scope.addChart = function () {
        var params = 'group_by=season';
        if (self.club !== null) {
            params += '&club=' + self.club;
        }
        if (self.coach !== null) {
            params += '&coach=' + self.coach;
        }
        $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
                var fieldData = self.createFieldData(self.field, self.data.results);
                var objectToGenerate = new ObjectToGenerate();
                _.each(fieldData, function (c3ADObject) {
                    objectToGenerate.data.xs[c3ADObject.data[0]] = c3ADObject.array[0];
                    objectToGenerate.data.colors[c3ADObject.data[0]] = '#58cb73';
                    objectToGenerate.data.columns.push(c3ADObject.array);
                    objectToGenerate.data.columns.push(c3ADObject.data);
                    chart.flow({
                        columns: objectToGenerate.data.columns,
                        'xs.x1' : c3ADObject.array[0]
                    })
                });

            })
    };

    this.list = function(order_by) {
        var params = 'group_by=' + self.groupBy;
        if (self.club !== null) {
            params += '&club=' + self.club;
        }
        if (self.coach !== null) {
            params += '&coach=' + self.coach;
        }
        self.data = {};
        self.loader = true;
        $http.get(url + '?' + params)
            .success(function(data, status, headers) {
                self.locale = headers()['content-language'];
                self.data = data;
                self.loader = false;
                var fieldData = self.createFieldData(self.field, self.data.results);
                var objectToGenerate = new ObjectToGenerate();
                _.each(fieldData, function(c3ADObject){
                    objectToGenerate.data.xs[c3ADObject.data[0]] = c3ADObject.array[0];
                    objectToGenerate.data.colors[c3ADObject.data[0]] = '#58cb73';
                    objectToGenerate.data.columns.push(c3ADObject.array);
                    objectToGenerate.data.columns.push(c3ADObject.data);
                });
                chart = c3.generate(objectToGenerate);
            });
    };

    this.list();
}])