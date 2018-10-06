#!/bin/bash

#==========================================================================
# проверка числа параметров
argc=3
if (($# != $argc))
then
    echo "Ошибка: параметров должно быть $argc"
    exit 1
fi


# проверка существовании директории для сохранения файлов с результатами
results_dir=$1
if ! [[ -d $results_dir ]]
then
    echo "Ошибка: директория '$results_dir' не найдена"
    exit 1
# проверка возможности записи в эту дирректорию
elif ! [[ -w $results_dir ]]
then
    echo "Ошибка: нет прав для создания файлов в директории '$results_dir'"
    exit 1
fi


# проверка правильности второго аргумента
input_type=$2
if ! [[ $input_type = "file" || $input_type = "domain" ]]
then
    echo "Ошибка: неверное значение второго аргумента '$input_type', возможные значения - 'file' или 'domain'"
    exit 1
fi


# проверка существования файла с доменами и наличия прав на чтение
input=$3
if [[ $input_type = "file" && -f $input && -r $input ]]
then
    domains_list=$(cat $input)
elif [[ $input_type = "domain" ]]
then
    domains_list=$input
else
    echo "Ошибка: файл '$input' или не существует или недоступен для чтения"
    exit 1
fi


#==========================================================================
#
whois_service="https://www.whois.com/whois/"
for domain in $domains_list
do
    echo "Запрос к $domain"
    wget_fout=$(echo $domain | sed "s![/:\.]!_!g")".html"
    wget --no-verbose -O $wget_fout "$whois_service""$domain"
    echo
done

echo "Завершено"
