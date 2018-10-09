#!/bin/bash

#==========================================================================
curl --version
if ! [[ $? -eq 0 ]]
then
    echo "Ошибка: пакет curl неустановлен"
    exit 1
fi
echo


# проверка числа параметров
argc=3
if (($# != $argc))
then
    echo "Ошибка: параметров должно быть $argc"
    exit 1
fi


# попытка создания дирректории 
results_dir=$1
mkdir -p $results_dir
# при отсутствии прав доступа скрипт завершит работу
if ! [[ $? -eq 0 ]]
then
    echo "Ошибка: директория '$results_dir' недоступна"
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
    # вообще говоря, существует еще много других протоколов кроме http и https
    # то же верно и про сервисы, которые могли бы быть на месте www
    # но для простоты команды учтем только их
    purified_domain=$(echo $domain | sed -e '
        s!^http://!!
        s!^https://!!
        s!^www\.!!
        s!^ftp\.!!')
    echo "Запрос к $purified_domain"
    f_out=$(echo $purified_domain | sed "s!\.!_!g")".html"
    #wget --no-verbose -O $wget_fout "$whois_service""$purified_domain"
    curl -o $f_out -L -s "$whois_service""$purified_domain"
    echo
done

echo "Завершено"
