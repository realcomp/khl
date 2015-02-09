angular.module('Sportomatics')
    .factory('LocaleFactory', function($rootScope){
        return {
            getFieldName: function(field, locale){
                var fieldNames = {
                    count: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    goals: {
                        shortName: 'Ш',
                        fullName: 'Заброшенные шайбы'
                    },
                    assists: {
                        shortName: 'А',
                        fullName: 'Передачи'
                    },
                    points: {
                        shortName: 'О',
                        fullName: 'Очки'
                    },
                    plus_minus: {
                        shortName: '+/-',
                        fullName: 'Плюс/Минус'
                    },
                    penalty_time: {
                        shortName: 'Штр',
                        fullName: 'Штрафное время'
                    },
                    es_goals: {
                        shortName: 'ШР',
                        fullName: 'Шайбы в равенстве'
                    },
                    pp_goals: {
                        shortName: 'ШБ',
                        fullName: 'Шайбы в большинстве'
                    },
                    ev_goals: {
                        shortName: 'ШМ',
                        fullName: 'Шайбы в меньшинстве'
                    },
                    overtime_goals: {
                        shortName: 'ШО',
                        fullName: 'Шайбы в овертайме'
                    },
                    win_goals: {
                        shortName: 'ШП',
                        fullName: 'Победные шайбы'
                    },
                    bullet_goals: {
                        shortName: 'РБ',
                        fullName: 'Решающие буллиты'
                    },
                    shots: {
                        shortName: 'БВ',
                        fullName: 'Броски по воротам'
                    },
                    pis__avg: {
                        shortName: '%БВ',
                        fullName: 'Процент реализованных бросков'
                    },
                    shots__avg: {
                        shortName: 'БВ/И',
                        fullName: 'Среднее количество бросков по воротам за игру'
                    },
                    faceoff: {
                        shortName: 'Вбр',
                        fullName: 'Вбрасывания'
                    },
                    winfaceoff: {
                        shortName: 'ВВбр',
                        fullName: 'Выигранные вбрасывания'
                    },
                    winfaceoff_p__avg: {
                        shortName: '%Вбр',
                        fullName: 'Процент выигранных вбрасываний'
                    },
                    gamingtime__avg: {
                        shortName: 'ВП/И',
                        fullName: 'Среднее время на площадке за игру'
                    },
                    change_time__avg: {
                        shortName: 'См/И',
                        fullName: 'Среднее количество смен за игру'
                    }
                };
                var fieldNamesEn = {
                    count: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    goals: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    assists: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    points: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    plus_minus: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    penalty_time: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    es_goals: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    pp_goals: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    ev_goals: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    overtime_goals: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    win_goals: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    bullet_goals: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    shots: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    pis__avg: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    shots__avg: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    faceoff: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    winfaceoff: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    winfaceoff_p__avg: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    gamingtime__avg: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    change_time__avg: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    }
                };
                return (locale === 'en') ? fieldNamesEn[field]['fullName'] : fieldNames[field]['fullName'];
            }
        }

    })