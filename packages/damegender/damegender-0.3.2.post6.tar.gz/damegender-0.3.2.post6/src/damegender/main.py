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





from app.dame_gender import Gender
from app.dame_sexmachine import DameSexmachine
from app.dame_utils import DameUtils
import sys
import os
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("name", help="display the gender")
parser.add_argument('--ml', choices=['nltk', 'svc', 'sgd', 'gaussianNB', 'multinomialNB', 'bernoulliNB', 'forest', 'tree', 'mlp'])
parser.add_argument('--total', default="us", choices=['at', 'au', 'be', 'ca', 'de', 'es', 'fi', 'ie', 'ine', 'is', 'nz', 'mx', 'pt', 'si', 'uy', 'uk', 'us', 'luciahelena', 'genderguesser', 'all'])
parser.add_argument('--version', action='version', version='0.3')
parser.add_argument('--verbose', default=False, action="store_true")
args = parser.parse_args()

results = []

s = DameSexmachine()
du = DameUtils()

if (args.total == "genderguesser"):
        name = args.name.capitalize()
        cmd = 'grep -i "' + name + '" files/names/nam_dict.txt > files/logs/grep.tmp'
#        print(cmd)
        os.system(cmd)
        for i in open('files/logs/grep.tmp', 'r').readlines():
                results.append(i)
        male = 0
        female = 0
        for i in results:
                regex = "(M|F|=|\?|1)( |M|F)?( )(" + name + ")"
                r = re.match(regex, i)
                if (r is not None):
                        prob = r.group(1) + r.group(2)
                else:
                        prob = ""
                if (('F' == prob) or ('F ' == prob) or (prob == '?F') or (prob == '1F')):
                        female = female + 1
                elif (('M' == prob) or ('M ' == prob) or ('?M' == prob) or ('1M' == prob)):
                        male = male + 1
        if ( female > male ):
                print("gender: female")
        if ( male > female ):
                print("gender: male")
        elif ( male == female ):
                print("gender: unknown")
                print("you can try predict with --ml")
                
elif (args.total == "luciahelena"):
        g = Gender()
        males = g.csv2names(path="files/names/allnoundefined.males.csv")
        females = g.csv2names(path="files/names/allnoundefined.females.csv")
        print("%s was classified as: " % args.name)
        if (args.name in males):
                print("male")
        elif (args.name in females):
                print("female")
        else:
                print("this name was not classified as male or female")
elif ((args.verbose) or (args.total == "all")):

        num_males = s.name_frec(args.name, dataset="at")['males']
        num_females = s.name_frec(args.name, dataset="at")['females']
        print("%s males for %s from Austria statistics" % (num_males, args.name))
        print("%s females for %s from Austria statistics" % (num_females, args.name))        
        num_males = s.name_frec(args.name, dataset="ine")['males']
        num_females = s.name_frec(args.name, dataset="ine")['females']
        print("%s males for %s from Spain statistics (INE.es)" % (num_males, args.name))
        print("%s females for %s from Spain statistics (INE.es)" % (num_females, args.name))
        num_males = s.name_frec(args.name, dataset="ie")['males']
        num_females = s.name_frec(args.name, dataset="ie")['females']
        print("%s males for %s from Ireland statistics" % (num_males, args.name))
        print("%s females for %s from Ireland statistics" % (num_females, args.name))
        num_males = s.name_frec(args.name, dataset="de")['males']
        num_females = s.name_frec(args.name, dataset="de")['females']
        print("%s males for %s from Deutchsland statistics" % (num_males, args.name))
        print("%s females for %s from Deutchsland statistics" % (num_females, args.name))
        num_males = s.name_frec(args.name, dataset="is")['males']
        num_females = s.name_frec(args.name, dataset="is")['females']
        print("%s males for %s from Iceland statistics" % (num_males, args.name))
        print("%s females for %s from Iceland statistics" % (num_females, args.name))
        num_males = s.name_frec(args.name, dataset="fi")['males']
        num_females = s.name_frec(args.name, dataset="fi")['females']
        print("%s males for %s from Finland statistics" % (num_males, args.name))
        print("%s females for %s from Finland statistics" % (num_females, args.name))        
        num_males = s.name_frec(args.name, dataset="uy")['males']
        num_females = s.name_frec(args.name, dataset="uy")['females']
        print("%s males for %s from Uruguay statistics" % (num_males, args.name))
        print("%s females for %s from Uruguay statistics" % (num_females, args.name))
        num_males = s.name_frec(args.name, dataset="uk")['males']
        num_females = s.name_frec(args.name, dataset="uk")['females']
        print("%s males for %s from United Kingdom statistics" % (num_males, args.name))
        print("%s females for %s from United Kingdom statistics" % (num_females, args.name))
        num_males = s.name_frec(args.name, dataset="nz")['males']
        num_females = s.name_frec(args.name, dataset="nz")['females']
        print("%s males for %s from New Zealand statistics" % (num_males, args.name))
        print("%s females for %s from New Zealand statistics" % (num_females, args.name))
        num_males = s.name_frec(args.name, dataset="ca")['males']
        num_females = s.name_frec(args.name, dataset="ca")['females']
        print("%s males for %s from Canada statistics" % (num_males, args.name))
        print("%s females for %s from Canada statistics" % (num_females, args.name))
        num_males = s.name_frec(args.name, dataset="pt")['males']
        num_females = s.name_frec(args.name, dataset="pt")['females']
        print("%s males for %s from Portugal statistics" % (num_males, args.name))
        print("%s females for %s from Portugal statistics" % (num_females, args.name))        
        num_males = s.name_frec(args.name, dataset="us")['males']
        num_females = s.name_frec(args.name, dataset="us")['females']
        print("%s males for %s from United States of America statistics" % (num_males, args.name))
        print("%s females for %s from United States of America statistics" % (num_females, args.name))
        num_males = s.name_frec(args.name, dataset="au")['males']
        num_females = s.name_frec(args.name, dataset="au")['females']
        print("%s males for %s from Australia statistics" % (num_males, args.name))
        print("%s females for %s from Australia statistics" % (num_females, args.name))
        num_males = s.name_frec(args.name, dataset="mx")['males']
        num_females = s.name_frec(args.name, dataset="mx")['females']
        print("%s males for %s from Mexico statistics" % (num_males, args.name))
        print("%s females for %s from Mexico statistics" % (num_females, args.name))
        num_males = s.name_frec(args.name, dataset="be")['males']
        num_females = s.name_frec(args.name, dataset="be")['females']
        print("%s males for %s from Belgium statistics" % (num_males, args.name))
        print("%s females for %s from Belgium statistics" % (num_females, args.name))
        num_males = s.name_frec(args.name, dataset="si")['males']
        num_females = s.name_frec(args.name, dataset="si")['females']
        print("%s males for %s from Slovenia statistics" % (num_males, args.name))
        print("%s females for %s from Slovenia statistics" % (num_females, args.name))        
        
        guess = s.guess(args.name, binary=True, ml="nltk")
        print("%s gender predicted with nltk is %s" % (str(args.name), du.int2gender(guess)))
        # guess = s.guess(args.name, binary=True, ml="sgd")
        # print("%s gender predicted with sgd is %s" % (str(args.name), du.int2gender(guess)))
        # guess = s.guess(args.name, binary=True, ml="svc")
        # print("%s gender predicted with svc is %s" % (str(args.name), du.int2gender(guess)))
        # guess = s.guess(args.name, binary=True, ml="gaussianNB")
        # print("%s gender predicted with gaussianNB is %s" % (str(args.name), du.int2gender(guess)))
        # guess = s.guess(args.name, binary=True, ml="multinomialNB")
        # print("%s gender predicted with multinomialNB is %s" % (str(args.name), du.int2gender(guess)))
        # guess = s.guess(args.name, binary=True, ml="bernoulliNB")
        # print("%s gender predicted with bernoulliNB is %s" % (str(args.name), du.int2gender(guess)))
        # guess = s.guess(args.name, binary=True, ml="forest")
        # print("%s gender predicted with forest is %s" % (str(args.name), du.int2gender(guess)))
        # guess = s.guess(args.name, binary=True, ml="tree")
        # print("%s gender predicted with tree is %s" % (str(args.name), du.int2gender(guess)))
        # guess = s.guess(args.name, binary=True, ml="mlp")
        # print("%s gender predicted with mlp is %s" % (str(args.name), du.int2gender(guess)))

else:
    s = DameSexmachine()
    num_males = s.name_frec(args.name, dataset=args.total)['males']
    num_females = s.name_frec(args.name, dataset=args.total)['females']
    if (int(num_males) > int(num_females)):
        print("%s's gender is male" % (str(args.name)))
        prob = int(num_males) / (int(num_males) + int(num_females))
        print("probability: %s" % str(prob))
    elif (int(num_males) < int(num_females)):
        print("%s's gender is female" % (str(args.name)))
        prob = int(num_females) / (int(num_females) + int(num_males))
        print("probability: %s" % str(prob))
    elif ((int(num_males) == 0) and (int(num_females) == 0)):
        args.ml = 'nltk'

    if (args.ml):
        if (args.ml == "nltk"):
            guess = s.guess(args.name, binary=True, ml="nltk")
        if (args.ml == "sgd"):
            guess = s.guess(args.name, binary=True, ml="sgd")
        elif (args.ml == "svc"):
            guess = s.guess(args.name, binary=True, ml="svc")
        elif (args.ml == "gaussianNB"):
            guess = s.guess(args.name, binary=True, ml="gaussianNB")
        elif (args.ml == "multinomialNB"):
            guess = s.guess(args.name, binary=True, ml="multinomialNB")
        elif (args.ml == "bernoulliNB"):
            guess = s.guess(args.name, binary=True, ml="bernoulliNB")
        elif (args.ml == "forest"):
            guess = s.guess(args.name, binary=True, ml="forest")
        elif (args.ml == "xgboost"):
            guess = s.guess(args.name, binary=True, ml="xgboost")
        elif (args.ml == "tree"):
            guess = s.guess(args.name, binary=True, ml="tree")
        elif (args.ml == "mlp"):
            guess = s.guess(args.name, binary=True, ml="mlp")
        if (guess == 1):
            sex = "male"
        elif (guess == 0):
            sex = "female"
        elif (guess == 2):
            sex = "unknown"
        print("%s gender predicted is %s" % (str(args.name), sex))

    if (args.total == "at"):
        print("%s males for %s from Austria statistics" % (num_males, args.name))
        print("%s females for %s from Austria statistics" % (num_females, args.name))
    elif (args.total == "au"):
        print("%s males for %s from Australia statistics" % (num_males, args.name))
        print("%s females for %s from Australia statistics" % (num_females, args.name))
    elif (args.total == "be"):
        print("%s males for %s from Belgium statistics" % (num_males, args.name))
        print("%s females for %s from Belgium statistics" % (num_females, args.name))
    elif (args.total == "de"):
        print("%s males for %s from Deutchsland statistics" % (num_males, args.name))
        print("%s females for %s from Deutchsland statistics" % (num_females, args.name))
    elif (args.total == "ie"):
        print("%s males for %s from Ireland statistics" % (num_males, args.name))
        print("%s females for %s from Ireland statistics" % (num_females, args.name))
    elif (args.total == "is"):
        print("%s males for %s from Iceland statistics" % (num_males, args.name))
        print("%s females for %s from Iceland statistics" % (num_females, args.name))
    elif ((args.total == "ine") or (args.total == "es")):
        print("%s males for %s from Spain statistics (INE.es)" % (num_males, args.name))
        print("%s females for %s from Spain statistics (INE.es)" % (num_females, args.name))
    elif (args.total == "fi"):
        print("%s males for %s from Finland statistics" % (num_males, args.name))
        print("%s females for %s from Finland statistics" % (num_females, args.name))
    elif (args.total == "mx"):
        print("%s males for %s from Mexico statistics" % (num_males, args.name))
        print("%s females for %s from Mexico statistics" % (num_females, args.name))
    elif (args.total == "si"):
        print("%s males for %s from Slovenia statistics" % (num_males, args.name))
        print("%s females for %s from Slovenia statistics" % (num_females, args.name))        
    elif (args.total == "uy"):
        print("%s males for %s from Uruguay statistics" % (num_males, args.name))
        print("%s females for %s from Uruguay statistics" % (num_females, args.name))
    elif (args.total == "uk"):
        print("%s males for %s from United Kingdom statistics" % (num_males, args.name))
        print("%s females for %s from United Kingdom statistics" % (num_females, args.name))
    elif (args.total == "us"):
        print("%s males for %s from United States of America statistics" % (num_males, args.name))
        print("%s females for %s from United States of America statistics" % (num_females, args.name))
    elif (args.total == "nz"):
        print("%s males for %s from New Zealand statistics" % (num_males, args.name))
        print("%s females for %s from New Zealand statistics" % (num_females, args.name))
    elif (args.total == "ca"):
        print("%s males for %s from Canada statistics" % (num_males, args.name))
        print("%s females for %s from Canada statistics" % (num_females, args.name))
    elif (args.total == "pt"):
        print("%s males for %s from Portugal statistics" % (num_males, args.name))
        print("%s females for %s from Portugal statistics" % (num_females, args.name))        
