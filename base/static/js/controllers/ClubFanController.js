angular.module('Sportomatics').controller('ClubFanController', function($scope, MapService) {
  $scope.loaded = true;
  console.log($scope.loaded);
  $scope.fans = [
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
    }, {
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
    }, {
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
    }, {
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
  ];
  $scope.compare = function(actual) {
    if ($scope.selectedPlace == null) {
      return true;
    }
    return actual.location.toUpperCase() === $scope.selectedPlace;
  };
  $scope.$watch('selectedPlace', 'change', function() {});
  MapService.setContext($scope);
  if (MapService.isRendered()) {
    MapService.remove();
  }
  MapService.createClubsMap($scope.fans, 'fans');
});
