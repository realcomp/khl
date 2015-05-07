angular.module('Sportomatics').controller('ClubCoachesController', function($scope, $timeout) {
  $scope.seasonsData = [];
  $scope.seasonsDataInitial = [
    {
      title: 'Сезон 2014-2015',
      coaches: [
        {
          fio: 'Иванов Вячеслав',
          role: 'главный тренер'
        }, {
          fio: 'Иванов Вячеслав',
          role: 'главный тренер'
        }, {
          fio: 'Иванов Вячеслав',
          role: 'главный тренер'
        }, {
          fio: 'Иванов Вячеслав',
          role: 'главный тренер'
        }
      ]
    }, {
      title: 'Сезон 2013-2014',
      coaches: [
        {
          fio: 'Иванов Вячеслав',
          role: 'помощник тренера'
        }, {
          fio: 'Иванов Вячеслав',
          role: 'главный тренер'
        }, {
          fio: 'Иванов Вячеслав',
          role: 'главный тренер'
        }, {
          fio: 'Иванов Вячеслав',
          role: 'главный тренер'
        }
      ]
    }
  ];
  $scope.loadSeason = function() {
    var loader;
    $scope.loader = true;
    loader = $('.loader');
    loader.addClass('active');
    return $timeout(function() {
      $scope.seasonsData.push($scope.seasonsDataInitial[0]);
      return loader.removeClass('active');
    }, 1000);
  };
  $('.b-tabs-content').visibility({
    once: false,
    observeChanges: true,
    onBottomVisible: function() {
      console.log('bottom');
      return $scope.loadSeason();
    }
  });
});
