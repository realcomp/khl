angular.module('Sportomatics')
    .factory('LocaleFactory', function($rootScope){
        var chosen = 'ru';
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
                    change_time__avg: {
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
                        fullName: 'Коэффициент полезности'
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
                },
                buttonNames: {
                    month: 'По месяцам',
                    season: 'По сезонам'
                },
                monthNames: ["Янв", "Фев", "Мар", "Апр", "Май", "Июн",
                    "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
                words: {
                    season: 'Сезон',
                    moths: 'Месяц'
                }
            },
            locale_en: {
                fieldNames: {
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
                    change_time__avg: {
                        shortName: 'SFT/G',
                        fullName: 'Average Shifts/Game'
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

    })