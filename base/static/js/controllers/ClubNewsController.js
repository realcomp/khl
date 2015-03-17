angular.module('Sportomatics')
    .controller('ClubNewsController', function($scope, $http, ChartFactory, LocaleFactory, $timeout){
        $scope.club = $("#team-name-hidden").length ? $("#team-name-hidden").val() : 'Club';
        $scope.data = [
            {
                date: '2001',
                values: 17
            },
            {
                date: '2002',
                values: 14
            },
            {
                date: '2003',
                values: 12
            },
            {
                date: '2004',
                values: 10
            },
            {
                date: '2005',
                values: 12
            },
            {
                date: '2006',
                values: 8
            },
            {
                date: '2007',
                values: 12
            },
            {
                date: '2008',
                values: 6
            },
            {
                date: '2009',
                values: 4
            }
        ];
        $scope.matchData = [
            {
                date: '21.09.2014',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 1,
                resultOpponent: 4
            },
            {
                date: '14.01.2013',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 4,
                resultOpponent: 1
            },
            {
                date: '04.07.2012',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 4,
                resultOpponent: 1
            },
            {
                date: '30.11.2000',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 1,
                resultOpponent: 4
            },
            {
                date: '21.09.2014',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 1,
                resultOpponent: 2,
                resultNote: 'Б'
            },
            {
                date: '14.01.2013',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 6,
                resultOpponent: 1
            },
            {
                date: '04.07.2012',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 4,
                resultOpponent: 1
            },
            {
                date: '30.11.2000',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 5,
                resultOpponent: 4
            },
            {
                date: '21.09.2014',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 3,
                resultOpponent: 3
            },
            {
                date: '14.01.2013',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 5,
                resultOpponent: 2
            },
            {
                date: '04.07.2012',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 4,
                resultOpponent: 1
            },
            {
                date: '30.11.2000',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 1,
                resultOpponent: 4
            }
        ];

        $scope.setCurrentSeasonString = function(date, value){
            $timeout(function(){

                $scope.currentSeason = date;
                $scope.currentPlace = value;
                $scope.currentSeasonString = parseInt($scope.currentSeason)-1 + '/' + $scope.currentSeason;
            }, 100)
        };
        $scope.setCurrentSeasonString(2001, 17);

        $scope.makeGraph = function(id, title, color, field, valueAxis, localeObject){
            console.log(id, title, color, field);
            var graph = new AmCharts.AmGraph();
            graph.id = "gl"+id;
            graph.valueAxis = valueAxis; // we have to indicate which value axis should be used
            graph.title = title + ' ' + field;
            graph.valueField = "values"+id;
            graph.bullet = "none";
            graph.hideBulletsCount = 30;
            graph.bulletBorderThickness = 1;
            graph.lineColor = color;
            graph.fillColor = "#FFFFFF";
            graph.fillAlphas = 0;
            graph.lineThickness = 1;
            graph.type = 'line';
            return graph;
        };


        $scope.graph = $scope.makeGraph('', 'positions', "#408e3a", null, null, LocaleFactory.locale_ru);
        $scope.graphs = [$scope.graph];
        ChartFactory.generateSerialLineChart('position', $scope.data, LocaleFactory.locale_ru, $scope.graphs).then(function(chart){
            chart.addListener("rendered", addListeners);

            function addListeners(){
                var categoryAxis = chart.categoryAxis;
                categoryAxis.addListener("clickItem", handleClick);
                categoryAxis.addListener("rollOverItem", handleOver);
                categoryAxis.addListener("rollOutItem", handleOut);
            }

            function handleClick(event){
                var value = _.where($scope.data, {date: event.value.toString()})[0].values;
                console.log(event.value, value);
                $scope.setCurrentSeasonString(event.value, value);
            }

            function handleOut(event){
                event.target.setAttr("cursor", "default");
                event.target.setAttr("fill", "#000000");
            }


            function handleOver(event){
                event.target.setAttr("cursor", "pointer");
                event.target.setAttr("fill", "#CC0000");
            }

            chart.write("chartdiv");

        })
    })