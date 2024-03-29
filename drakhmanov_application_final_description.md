**[ ЗАГОЛОВОК ЗАЯВКИ ]**

БЫЛО:

Рахманов Данила - “Приложение для анализа наиболее выгодного местоположения открытия торговых точек”

СТАЛО:

Рахманов Данила - "Montesume"


**[ НАЗВАНИЕ ПРОЕКТА ]**

БЫЛО:

“Приложение для анализа наиболее выгодного местоположения торговых точек”

СТАЛО:

"Montesume"


**[ ПРОБЛЕМНОЕ ПОЛЕ ]**

БЫЛО:

Предполагается использовать для малого и среднего бизнеса, ориентированного на открытие торговых точек. Удачный и правильный выбор местоположения объекта торговли - залог успеха в бизнесе, способ повысить доходы относительно других конкурентов. Важными критериями для выбора места открытия новой торговой точки являются:

* Удалённость от конкурентов.
* Трафик/проходимость людей в непосредственной близости от торговой точки.
* Плотность населения в области расположения торговой точки.

Заявляемый программный продукт является вспомогательным инструментом, нацеленным на выявление наиболее эффективного местоположения торговых точек относительно ранее упомянутых критериев.

СТАЛО:

Предполагается использовать для малого и среднего бизнеса, ориентированного на открытие новых перспективных торговых точек. Удачный и правильный выбор местоположения объекта торговли - залог успеха в бизнесе, способ повысить доходы и выручку относительно других конкурентов. Важными критериями для выбора места открытия новой торговой точки являются:

* Удалённость от конкурентов.
* Трафик/проходимость людей в непосредственной близости от торговой точки.
* Плотность населения в области расположения торговой точки.

Заявляемый программный продукт является вспомогательным инструментом, нацеленным на поиск наиболее выгодного местоположения торговых точек с соблюдением ранее упомянутых критериев.

**[ ЗАКАЗЧИК / ПОТЕНЦИАЛЬНАЯ АУДИТОРИЯ ]**

БЫЛО:

Юридические и физические лица, нацеленные на открытие или расширение собственного бизнеса различных направлений путём поиска наиболее выгодного местоположения открытия торговых точек и иные объекты, которые могут требовать критерии, упомянутые выше. 

СТАЛО:

Юридические и физические лица, нацеленные на открытие или расширение собственного бизнеса различных направлений путём поиска наиболее выгодного местоположения для новых торговых точек или иных объектов.

**[ АППАРАТНЫЕ ТРЕБОВАНИЯ ]**

БЫЛО:

Chrome v. 85+, FireFox v. 80+, Safari v. 13.1+, Opera v. 70+

СТАЛО:

Chrome v. 26+, FireFox v. 21+, Safari v. 6.1+, Opera v. 15+

**[ ФУНКЦИОНАЛЬНЫЕ ТРЕБОВАНИЯ ]**

БЫЛО:

Программный продукт будет предоставлять следующие возможности:
* Указывать интересующий тип объектов
* Составлять семантическую базу, ориентированную на поиск нужных объектов
* Отображение наиболее выгодных областей для расположения объекта
* Отображение конкурентов по заданным критериям на карте
* Получение наиболее выгодного местоположения для открытия объекта

СТАЛО:

Программный продукт будет предоставлять следующие возможности:
* Выполнение поиска расположения будущей торговой точки пользователя различными способами.
* Отображение торговых точек, привлекающих трафик типа бизнеса пользователя по заданным критериям, на карте.
* Отображение указанных пользователем конкурентов на карте.
* Отображение наиболее выгодных областей для расположения торговой точки пользователя.
* Сохранение координат и адресов понравившихся пользователю точек расположения будущего бизнеса.


**[ ПОХОЖИЕ / АНАЛОГИЧНЫЕ ПРОДУКТЫ ]**, Добавление пункта

Mestomer.com: пользователь не может выбирать типы бизнесов, привлекающих трафик для его будущей торговой точки


**[ ИНСТРУМЕНТЫ РАЗРАБОТКИ ]**

БЫЛО:

HTML / CSS / JS / Python – для разработки веб-версии.

СТАЛО:

HTML / CSS / JavaScript / Python


**[ ЭТАПЫ РАЗРАБОТКИ ]**

БЫЛО:

* Разработка технического заключения.
* Проектирование интерфейса/составление гайд дизайна.
* Построение структуры анализа.
* Формирование API запросов к Яндекс.Картам с целью получения информации для анализа.
* Написание серверной части для анализа.
* Проектирование базы данных, необходимых для проведения более качественного анализа, а также сбора информации.
* Вёрстка страниц.
* Написание API запросов к серверу для вывода информации на страницу.
* Тестирование, отладка.
* Подготовка проекта к защите.

СТАЛО:

* Разработка технического заключения.
* Проектирование интерфейса/составление гайд дизайна.
* Построение структуры анализа.
* Формирование API запросов к Яндекс.Картам с целью получения информации для анализа.
* Написание серверной части для анализа.
* Проектирование баз данных, необходимых для проведения более качественного анализа и сбора информации.
* Вёрстка страниц.
* Написание API запросов к серверу для вывода информации на страницу.
* Тестирование, отладка.
* Подготовка к защите проекта.


**[ Исправление файла с алгоритмом выявления благоприятной торговой точки ]**

БЫЛО:

Алгоритм для выявления наиболее выгодного расположения торговых точек:
* Составить семантическую базу для выявления всех схожих конкурентных объектов для заданного типа искомого объекта.
* Выявить местоположение всех найденных конкретных объектов.
* Выявить равноудалённую благоприятную область, где будет располагаться искомый объект.
* Определить в найденных областях плотность населения.
* Определить трафик населения путём выявления объектов, увеличивающих его (классифицировать эти объекты по количеству притягиваемого трафика).
* Выявить местоположение всех объектов, увеличивающих трафик.
* Выявить наиболее благоприятное местоположение, относительно плотности населения, в полученной области, а также относительно объектов, увеличивающих трафик  .

Алгоритм предназначен для выявления наиболее выгодного расположения торговых точек, однако неточности, которые могут быть в нём получены, могут быть связаны с следующим рядом факторов:

* Недостоверная общественная информация плотности населения.
* Отсутствие некоторых конкурентных объектов на искомых картах.
* Недостоверная общественная информация для классификации объектов по количеству притягиваемого трафика.
* В силу вышеперечисленных факторов, информация, предлагаемая программным продуктом, может не соответствовать действительности, все источники используемой информации будут указаны в программном продукте или его документации.

СТАЛО:

Алгоритм для выявления наиболее выгодного расположения торговых точек:

* Составить семантическую базу для выявления всех схожих конкурентных объектов для заданного типа искомого объекта.
* Выявить местоположение всех найденных конкретных объектов.
* Выявить равноудалённую благоприятную область, где будет располагаться искомый объект.
* Определить в найденных областях плотность населения.
* Определить трафик населения путём выявления объектов, увеличивающих его (классифицировать эти объекты по количеству притягиваемого трафика).
* Выявить местоположение всех объектов, увеличивающих трафик.
* Выявить наиболее благоприятное местоположение, относительно плотности населения в полученной области, а также относительно объектов, увеличивающих трафик.

Алгоритм предназначен для выявления наиболее выгодного расположения торговых точек. Однако, неточности, которые могут быть в нём получены, возможно, будут связаны со следующими факторами:

* Недостоверная общественная информация плотности населения.
* Отсутствие некоторых конкурентных объектов на искомых картах.
* Недостоверная общественная информация для классификации объектов по количеству притягиваемого трафика.
* В силу вышеперечисленных факторов, информация, предлагаемая программным продуктом, может не соответствовать действительности. Все источники используемой информации будут указаны в программном продукте или прилагаемой к нему документации.
