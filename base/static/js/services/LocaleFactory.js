angular.module('Sportomatics')
    .factory('LocaleFactory', function($rootScope){
        var chosen = 'ru';
        var self = this;
        var factory = {
            setLocale: function(contentLanguage){
                factory.selectedLocale = factory['locale_'+contentLanguage]
            },
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
                        fullName: 'Штрафное время, мин'
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
                    change_count__avg: {
                        shortName: 'См/И',
                        fullName: 'Среднее количество смен за игру'
                    },
                    shots_received: {
                        shortName: 'Бр',
                        fullName: 'Броски'
                    },
                    loose_goals: {
                        shortName: 'ПШ',
                        fullName: 'Пропущенные шайбы'
                    },
                    saves: {
                        shortName: 'ОШ',
                        fullName: 'Отраженные броски'
                    },
                    saves_p__avg: {
                        shortName: '%ОШ',
                        fullName: 'Процент отраженных бросков'
                    },
                    sf__avg: {
                        shortName: 'КН',
                        fullName: 'Коэффициент надежности'
                    },
                    matches_win: {
                        shortName: 'В',
                        fullName: 'Выигрыши'
                    },
                    matches_lose: {
                        shortName: 'П',
                        fullName: 'Проигрыши'
                    },
                    zero_goals_matches: {
                        shortName: 'И"0"',
                        fullName: '"Сухие игры"'
                    },
                    bullet_matches: {
                        shortName: 'ИБ',
                        fullName: 'Игры с буллитными сериями'
                    }
                };
                var fieldNamesEn = {
                    count: {
                        shortName: 'GP',
                        fullName: 'Games played'
                    },
                    goals: {
                        shortName: 'G',
                        fullName: 'Goals'
                    },
                    assists: {
                        shortName: 'A',
                        fullName: 'Assists'
                    },
                    points: {
                        shortName: 'PTS',
                        fullName: 'Points'
                    },
                    plus_minus: {
                        shortName: '+/-',
                        fullName: 'Plus/Minus'
                    },
                    penalty_time: {
                        shortName: 'PIM',
                        fullName: 'Penalty in minutes'
                    },
                    es_goals: {
                        shortName: 'ESG',
                        fullName: 'Even Strength Goals'
                    },
                    pp_goals: {
                        shortName: 'PPG',
                        fullName: 'Power play goals'
                    },
                    ev_goals: {
                        shortName: 'SHG',
                        fullName: 'Shorthanded goals'
                    },
                    overtime_goals: {
                        shortName: 'OTG',
                        fullName: 'Overtime goals'
                    },
                    win_goals: {
                        shortName: 'GWG',
                        fullName: 'Game winning goals'
                    },
                    bullet_goals: {
                        shortName: 'SDS',
                        fullName: 'Shootouts deciding shots'
                    },
                    shots: {
                        shortName: 'SOG',
                        fullName: 'Shots on goal'
                    },
                    pis__avg: {
                        shortName: '%SOG',
                        fullName: 'Shots on goal percentage'
                    },
                    shots__avg: {
                        shortName: 'S/G',
                        fullName: 'Average Shots/Game'
                    },
                    faceoff: {
                        shortName: 'FO',
                        fullName: 'Faceoffs'
                    },
                    winfaceoff: {
                        shortName: 'FOW',
                        fullName: 'Faceoffs won'
                    },
                    winfaceoff_p__avg: {
                        shortName: '%FO',
                        fullName: 'Faceoffs won percentage'
                    },
                    gamingtime__avg: {
                        shortName: 'TOI/G',
                        fullName: 'Average time on ice/Game'
                    },
                    change_count__avg: {
                        shortName: 'SFT/G',
                        fullName: 'Average Shifts/Game'
                    }
                };
                return (locale === 'en') ? fieldNamesEn[field]['fullName'] : fieldNames[field]['fullName'];
            },
            locale_ru: {
                fieldNames: {
                    count: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр',
                        field: 'count'
                    },
                    goals: {
                        shortName: 'Ш',
                        fullName: 'Заброшенные шайбы',
                        field: 'goals'
                    },
                    assists: {
                        shortName: 'А',
                        fullName: 'Передачи',
                        field: 'assists'
                    },
                    points: {
                        shortName: 'О',
                        fullName: 'Очки',
                        field: 'points'
                    },
                    plus_minus: {
                        shortName: '+/-',
                        fullName: 'Коэффициент полезности',
                        field: 'plus_minus'
                    },
                    penalty_time: {
                        shortName: 'Штр',
                        fullName: 'Штрафное время, мин',
                        field: 'penalty_time'
                    },
                    es_goals: {
                        shortName: 'ШР',
                        fullName: 'Шайбы в равенстве',
                        field: 'es_goals'
                    },
                    pp_goals: {
                        shortName: 'ШБ',
                        fullName: 'Шайбы в большинстве',
                        field: 'pp_goals'
                    },
                    ev_goals: {
                        shortName: 'ШМ',
                        fullName: 'Шайбы в меньшинстве',
                        field: 'ev_goals'
                    },
                    overtime_goals: {
                        shortName: 'ШО',
                        fullName: 'Шайбы в овертайме',
                        field: 'overtime_goals'
                    },
                    win_goals: {
                        shortName: 'ШП',
                        fullName: 'Победные шайбы',
                        field: 'win_goals'
                    },
                    bullet_goals: {
                        shortName: 'РБ',
                        fullName: 'Решающие буллиты',
                        field: 'bullet_goals'
                    },
                    shots: {
                        shortName: 'БВ',
                        fullName: 'Броски по воротам',
                        field: 'shots'
                    },
                    pis__avg: {
                        shortName: '%БВ',
                        fullName: 'Процент реализованных бросков',
                        field: 'pis__avg'
                    },
                    shots__avg: {
                        shortName: 'БВ/И',
                        fullName: 'Среднее количество бросков по воротам за игру',
                        field: 'shots__avg'
                    },
                    faceoff: {
                        shortName: 'Вбр',
                        fullName: 'Вбрасывания',
                        field: 'faceoff'
                    },
                    winfaceoff: {
                        shortName: 'ВВбр',
                        fullName: 'Выигранные вбрасывания',
                        field: 'winfaceoff'
                    },
                    winfaceoff_p__avg: {
                        shortName: '%Вбр',
                        fullName: 'Процент выигранных вбрасываний',
                        field: 'winfaceoff_p_avg'
                    },
                    gamingtime__avg: {
                        shortName: 'ВП/И',
                        fullName: 'Среднее время на площадке за игру, мин',
                        field: 'gamingtime__avg'
                    },
                    change_count__avg: {
                        shortName: 'См/И',
                        fullName: 'Среднее количество смен за игру',
                        field: 'change_count__avg'
                    },
                    shots_received: {
                        shortName: 'Бр',
                        fullName: 'Броски',
                        field: 'shots_received'
                    },
                    loose_goals: {
                        shortName: 'ПШ',
                        fullName: 'Пропущенные шайбы',
                        field: 'loose_goals'
                    },
                    saves: {
                        shortName: 'ОШ',
                        fullName: 'Отраженные броски',
                        field: 'saves'
                    },
                    saves_p__avg: {
                        shortName: '%ОШ',
                        fullName: 'Процент отраженных бросков',
                        field: 'saves_p__avg'
                    },
                    sf__avg: {
                        shortName: 'КН',
                        fullName: 'Коэффициент надежности',
                        field: 'sf__avg'
                    },
                    matches_win: {
                        shortName: 'В',
                        fullName: 'Выигрыши',
                        field: 'matches_win'
                    },
                    matches_lose: {
                        shortName: 'П',
                        fullName: 'Проигрыши',
                        field: 'matches_lose'
                    },
                    zero_goals_matches: {
                        shortName: 'И"0"',
                        fullName: '"Сухие игры"',
                        field: 'zero_goals_matches'
                    },
                    bullet_matches: {
                        shortName: 'ИБ',
                        fullName: 'Игры с буллитными сериями',
                        field: 'bullet_matches'
                    },
                    position: {
                        shortName: '',
                        fullName: 'Место',
                        field: 'position'
                    }
                },
                buttonNames: {
                    month: 'По месяцам',
                    season: 'По сезонам',
                    allSeasons: 'Все сезоны'
                },
                monthNames: ["Янв", "Фев", "Мар", "Апр", "Май", "Июн",
                    "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
                monthNamesFull: ["Январь", "Феввраль", "Март", "Апрель", "Май", "Июнь",
                    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
                words: {
                    season: 'Сезон',
                    moths: 'Месяц'
                }
            },
            locale_en: {
                fieldNames: {
                    count: {
                        shortName: 'GP',
                        fullName: 'Games played',
                        field: 'count'
                    },
                    goals: {
                        shortName: 'G',
                        fullName: 'Goals',
                        field: 'goals'
                    },
                    assists: {
                        shortName: 'A',
                        fullName: 'Assists',
                        field: 'assists'
                    },
                    points: {
                        shortName: 'PTS',
                        fullName: 'Points',
                        field: 'points'
                    },
                    plus_minus: {
                        shortName: '+/-',
                        fullName: 'Plus/Minus',
                        field: 'plus_minus'
                    },
                    penalty_time: {
                        shortName: 'PIM',
                        fullName: 'Penalty in minutes',
                        field: 'penalty_time'
                    },
                    es_goals: {
                        shortName: 'ESG',
                        fullName: 'Even Strength Goals',
                        field: 'es_goals'
                    },
                    pp_goals: {
                        shortName: 'PPG',
                        fullName: 'Power play goals',
                        field: 'pp_goals'
                    },
                    ev_goals: {
                        shortName: 'SHG',
                        fullName: 'Shorthanded goals',
                        field: 'ev_goals'
                    },
                    overtime_goals: {
                        shortName: 'OTG',
                        fullName: 'Overtime goals',
                        field: 'overtime_goals'
                    },
                    win_goals: {
                        shortName: 'GWG',
                        fullName: 'Game winning goals',
                        field: 'win_goals'
                    },
                    bullet_goals: {
                        shortName: 'SDS',
                        fullName: 'Shootouts deciding shots',
                        field: 'bullet_goals'
                    },
                    shots: {
                        shortName: 'SOG',
                        fullName: 'Shots on goal',
                        field: 'shots'
                    },
                    pis__avg: {
                        shortName: '%SOG',
                        fullName: 'Shots on goal percentage',
                        field: 'pis__avg'
                    },
                    shots__avg: {
                        shortName: 'S/G',
                        fullName: 'Average Shots/Game',
                        field: 'shots__avg'
                    },
                    faceoff: {
                        shortName: 'FO',
                        fullName: 'Faceoffs',
                        field: 'faceoff'
                    },
                    winfaceoff: {
                        shortName: 'FOW',
                        fullName: 'Faceoffs won',
                        field: 'winfaceoff'
                    },
                    winfaceoff_p__avg: {
                        shortName: '%FO',
                        fullName: 'Faceoffs won percentage',
                        field: 'winfaceoff_p__avg'
                    },
                    gamingtime__avg: {
                        shortName: 'TOI/G',
                        fullName: 'Average time on ice/Game',
                        field: 'gamingtime__avg'
                    },
                    change_count__avg: {
                        shortName: 'SFT/G',
                        fullName: 'Average Shifts/Game',
                        field: 'change_count__avg'
                    }
                },
                buttonNames: {
                    month: 'By month',
                    season: 'By season'
                },
                monthNames : ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                words: {
                    season: 'Season',
                    moths: 'Month'
                }
            }
        }
        factory.selectedLocale = factory.locale_ru;

        return factory;

    })
