# crypto_alfred

1. Приветсвие
После добавления в Чат бот посылает текст с приветсвием в личное сообщение и просит ознакомится с правилами чата,  после спрашивает какой уровень знании у него в данной сфере (4 варианта). Нет знании,начинающий, разбираюсь, спец.
Предлагает Блок обучения криптовалюте
Оставить сообщение администратору

2. Цензура
Есть база слов при использовании которых они автоматический бларятся (blur) + в чат ему посылается предуприждение, если тотже человек в течении 72 часов  еще раз использует незенцурные слова на 8 часов (mute) больше не может писать в чат. 

3. Спам
Когда человек пишет подряд 7 сообщении  бот предупреждает его что он нарушает правила чата. После предупреждения если он написал 3 сообщения подряд то он попадает в (Mute) на 2 часа. 

4. Короткая сводка новостей за сегодняшний день
Посты будут выкладываться по определенным правилам что бы это логика работала:
В конце дня бот выкладывает один пост  где собраны все статии которые выложины за день, он берет заголовок поста и слово "Читать полностью" превращает в сыслку на данный пост. 
Так же в этом посту в конце выкладывет на данный момент какой курс пример:
🔹 Курсы:
🌐 Bitcoin - $39 448 (↓5,57%)
📉 S&P 500 - 4 308 (↓1,95%)
🌕 Золото - $1 933 (↓0,73%)
⚫️ Oil Brent - $106,28 (↓2,15%)

5. Система очков (Статусов)
У статуса есть привилегии

Есть 4 вида статуса : Newbie ,Specialist,Magister,Doctor
Они оприделяются по очкам.
Их можно набирать и так же терять. 
 - 0 Mr.Anderson     (Если меньше нуля)
0 - 50   Newbie
51-150  Specialist
151-300 Magister
300 + Doctor

Каждый пользователь должен иметь доступ к информации о количестве своих очков.

Очки зарабатываются несколькими методами:
1. Активность 
Бот собирает статистику сообщении и види топ 3 самых активных пользователя
1 место - 3 очка
2 - 2
3 -1

2. Реакции на сообщения 
Всего 4 вида реации:
Палец вверх  - Получает 1 очко
Палец вниз - Теряет 1 очка
Сердце - Получает 1 очко
Огодь - Получает 1 очко

Бот высчитывает поведения учасника ( Если один учасник многим подряд ставит дизлаик то его предупреждает и напоминает о правилах чата.) Если он продолжает это делать то ему отключает возможность ставить реакции на 24 часа.

Теряет по 5 очка если попадает под санкции: Цензура, Спам


3. Реферальная система
У каждого учасника должна генерироватся своя реферальная ссылка на чат. 
Если другой человек присоеденился в часу с его ссылкой то этому учаснику начисляется 3 балла.

- Было бы прекрасно если есть возможность что бы каждый учасник смог смотреть типо свой личный кабинет.  Так инфа: сколько у него очков, сколько человек присоеденилось к часу его ссылкой, сколько раз были пременены санкции простив него и какие.

И возможно ли что бы отображались в чате их статусы рядом именами?

# Реализация
- делать ботом blur не представляется возможным, так как это будет редактирование чужого сообщения, что запрещено.
Можно попробовать удалять или помечать такие сообщения с помощью бота.
- банить на время нельзя, можно только выкинуть из группы.
- следить за реакциями бот не сможет, так как на них нет никаких приходящих ивентов.
- бот не может получать историю сообщений - только вычитывать их вживую во время отправки.
- что касается бана за частые сообщения - можно просто настроить slow mode на несколько минут.
- что касается курсов валют - есть сервисы вроде coin api которые дают бесплатную апиху, как я понял.

# ДОРАБОТКИ:
1. если человек принял условия, то потом не спрашивать его об этом повторно
2. привязать базу данных к проекту
3. сделать, чтобы было меню с кнопками "домой" и так далее - возможно это для рейтинга
4. положить по жопу Эластик, который бы искал совпадения по словам с учетом опечаток

# ЗАПУСК С ПОМОЩЬЮ КОНТЕЙНЕРА
sudo docker run -d -e TOKEN='токен' --name=node-1 luchanos/crypto_alfred:1.0.0
