#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (C) 2020  David Arroyo Menéndez (davidam@gmail.com)
# This file is part of Damegender.

# Damegender is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Damegender is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Damegender in the file GPL.txt.  If not, see
# <https://www.gnu.org/licenses/>.






# From a name give a list of countries where the people is using the name
import re
import os
import csv
import sys
from app.dame_utils import DameUtils
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("name", help="display the country")
args = parser.parse_args()

## Dictionary of countries and person names in files/names/nam_dict.txt
keyscountries = {"30": "Great Britain", "31": "Ireland", "32": "USA", "33": "Italy", "34": "Malta", "35": "Portugal", "36": "Spain", "37": "France", "38": "Belgium", "39": "Luxembourg", "40": "The Netherlands", "41": "East Frisia", "42": "Germany", "43": "Austria", "44": "Swiss", "45": "Iceland", "46": "Denmark", "47": "Norway", "48": "Sweden", "49": "Finland", "50": "Estonia", "51": "Latvia", "52": "Lithuania", "53": "Poland", "54": "Czech Republic", "55": "Slovakia", "56": "Hungary", "57": "Romania", "58": "Bulgaria", "59": "Bosnia and Herzegovina", "60": "Croatia", "61": "Kosovo", "62": "Macedonia", "63": "Montenegro", "64": "Serbia", "65": "Slovenia", "66": "Albania", "67": "Greece", "68": "Rusia", "69": "Belarus", "70": "Moldova", "71": "Ukraine", "72": "Armenia", "73": "Azerbaijan", "74": "Georgia", "75": "Kazakhstan/Uzbekistan", "76": "Turkey", "77": "Arabia/Persia", "78": "Israel", "79": "China", "80": "India/Sri Lanka", "81": "Japan", "82": "Korea", "83": "Vietnam", "84": "other countries"}

du = DameUtils()

def exists_in_country(num, arr):
    if du.is_not_blank(arr[num]):
        if ((str(arr[num]) == "A") or (str(arr[num]) == "B") or (str(arr[num]) == "C") or (str(arr[num]) == "D")):
            return True
        elif (int(arr[num])>0):
            return True
        else:
            return False
    else:
        return False

if (len(sys.argv) > 1):
    cmd = 'grep -i " ' + args.name + ' " files/names/nam_dict.txt > files/logs/grep.tmp'
    print(cmd)
    os.system(cmd)
    results = [i for i in open('files/logs/grep.tmp','r').readlines()]
    males = [ ]
    females = [ ]
    both = [ ]
    for rowres in results:
        regex = "(M|F|=|\?|1)( |M|F)?( )(\w+)( )?(\w+)?( )?(\w+)?"
        n = re.match(regex, rowres)
        if (n.group(6)):
            string = str(n.group(4)) + str(n.group(5)) + str(n.group(6))
        else:
            string = str(n.group(4)) + str(n.group(5))
        if (du.drop_white_space(args.name.capitalize()) == du.drop_white_space(string) ):
            twochars = rowres[0] + rowres[1]
            for i in range(30, 84):
                if (exists_in_country(int(i), rowres)):
                    if ((rowres[0].title() == "M") | (twochars.title() == "1M") | (twochars.title() == "?M")) :
                        males.append(keyscountries[str(i)])
                    elif ((rowres[0].title() == "F") | (twochars.title() == "1F") | (twochars.title() == "?F")):
                        females.append(keyscountries[str(i)])
                    elif (rowres[0].title() == "="):
                        both.append(keyscountries[str(i)])

    print("males: " + (str(sorted(males))))
    print("females: " + str(sorted(females)))
    print("both: " + str(sorted(both)))
