angular.module('Sportomatics').controller 'ClubFanController', ($scope, MapService) ->

    $scope.loaded = true
    console.log $scope.loaded
    $scope.fans =[{
        name: 'Олег'
        lastname:'Иванов'
        citizenship:
            title: 'Россия'
        location: 'Москва'
    }, {
        name: 'Петр'
        lastname:'Сидоров'
        citizenship:
            title: 'Россия'
        location: 'Санкт-Петербург'
    },{
        name: 'Вячеслав'
        lastname:'Рябинин'
        citizenship:
            title: 'Россия'
        location: 'Санкт-Петербург'
    },

        {
            name: 'Олег',
            lastname: 'Иванов',
            citizenship: {
                title: 'Россия'
            },
            location: 'Москва'
        }, {
            name: 'Петр',
            lastname: 'Сидоров',
            citizenship: {
                title: 'Россия'
            },
            location: 'Санкт-Петербург'
        }, {
            name: 'Вячеслав',
            lastname: 'Рябинин',
            citizenship: {
                title: 'Россия'
            },
            location: 'Санкт-Петербург'
        },
        {
            name: 'Олег',
            lastname: 'Иванов',
            citizenship: {
                title: 'Россия'
            },
            location: 'Москва'
        }, {
            name: 'Петр',
            lastname: 'Сидоров',
            citizenship: {
                title: 'Россия'
            },
            location: 'Санкт-Петербург'
        }, {
            name: 'Вячеслав',
            lastname: 'Рябинин',
            citizenship: {
                title: 'Россия'
            },
            location: 'Санкт-Петербург'
        },
        {
            name: 'Олег',
            lastname: 'Иванов',
            citizenship: {
                title: 'Россия'
            },
            location: 'Москва'
        }, {
            name: 'Петр',
            lastname: 'Сидоров',
            citizenship: {
                title: 'Россия'
            },
            location: 'Санкт-Петербург'
        }, {
            name: 'Вячеслав',
            lastname: 'Рябинин',
            citizenship: {
                title: 'Россия'
            },
            location: 'Санкт-Петербург'
        }
    ]

    $scope.compare = (actual) ->
        if not $scope.selectedPlace? then return true
        return actual.location.toUpperCase() is $scope.selectedPlace

    $scope.$watch 'selectedPlace', 'change', ->
        return

    MapService.setContext($scope);
    MapService.remove() if MapService.isRendered()
    MapService.createClubsMap($scope.fans, 'fans')

    return