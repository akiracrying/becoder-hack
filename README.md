# **beСoder-hackaton**

## *Работа программы*

При запуске программы необходимо в файловой системе выбрать папку с локальным репозиторием. Построение графиков доступно после анализа данных при вводе порядкового номера разработчика из консоли. Текстовые файлы с отчётами обновляются после выполнения программы и содержатся в папке task.

## *Задание*

**Гипотеза 1.**

Разработчик в одних и тех же файлах ошибается чаще, чем в других.

**Гипотеза 2.**

Разработчик чаще ошибается в коде, с которым он реже работает.

**Задание 1.**

Проверить гипотезы.

**Задание 2.**

Предполагая, что первая гипотеза верна, определить:

- Коммиты, в которых весьма вероятна ошибка
- Разработчика, которому лучше доверить ревью таких коммитов

## *Решение*

### **Отчёты**

Выводом к данной задаче в нашем проекте являются **отчёты** - файлы формата **.txt**, а также **графики**, показывающие отклонение процента ошибки в файлах от среднего для каждого разработчика.

По **отчётам** можно проследить за ходом выполнения задачи.

Таким образом:

1. Первый отчёт - [stats_start](https://github.com/akiracrying/becoder-hack/blob/main/task1/stats_start.txt) приводит данные о том, сколько каждым разработчиком было сделано изменений, требующих исправлений и не требующих исправления. Вывод осуществлён в формате:

    ***Разработчик*** - {***файл***: [***количество_"неудачных"_изменений***, ***количество_"удачных"_изменений***]}.

2. Второй отчёт - [stats_probability](https://github.com/akiracrying/becoder-hack/blob/main/task1/stats_probability.txt) выводит данные о вероятности, что коммит будет требовать исправления. Данная вероятность выводится на основе процента ошибки в файлах, входящих в коммит. Вывод осуществлён в формате:

    ***Хэш_коммита*** - ***вероятность_ошибки_в_коммите (%)***

3. Третий отчёт - [stats_reviewers](https://github.com/akiracrying/becoder-hack/blob/main/task1/stats_reviewers.txt) выводит данные о том, какого разработчика, слудует назначить на ревью коммита. Для ревью выбирается тот разработчик, у которого наименьшее число ошибок в файлах данного коммита. Вывод осуществляется в формате:

    ***Хэш_коммита*** - ***ревьюер***

4. Четвёртый отчёт - [stats_deviation](https://github.com/akiracrying/becoder-hack/blob/main/task1/stats_deviation.txt) выводит данные об отклонении процента ошибки от среднего для каждого разработчика по файлам. Также выводится **Fail rate** - отношение количества отклонений выше среднего к общему количеству файлов. Вывод осуществляется в формате:

   ***Разработчик*** - [***отклонение_от_среднего***]

   ***Fail_rate***
   
 ---

### **Графики**

1. На основе четвёртого отчёта строятся графики для каждого разработчика, по ним мы можем видеть, что существуют файлы, в которых ошибки совершаются чаще, чем в остальных, что, в свою очередь, является подтверждением **первой гипотезы**.

    Пример графика:

    <div>
        <img src = "https://github.com/akiracrying/becoder-hack/blob/task1/img/graph_1.jpg"></img>
    </div>

2. На основе зависимости между количеством изменений файла и средняя вероятность ошибки за такого количество изменений. По графику видно, что, в общем случае, с большим числом изменений выше и вероятность ошибки, что является опровержением **второй гипотезы**.

    Пример графика:

    <div>
        <img src = "https://github.com/akiracrying/becoder-hack/blob/task1/img/graph_2.jpg"></img>
    </div>
