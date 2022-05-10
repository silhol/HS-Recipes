## This python script extracts from HS the recipes and stores them in a text file for printing
# Each recipe is stored in a different txt file
# Some recipes are behind a paywall, for those one needs to login first before calling this program

# Recipes for testing:
# Burger: https://www.hs.fi/ruoka/art-2000008022831.html
# BBQ: https://www.hs.fi/ruoka/art-2000008022816.html
# Salattia: https://www.hs.fi/ruoka/art-2000008008508.html
# Gazpacho: https://www.hs.fi/ruoka/art-2000008022959.html  (BEHIND PAYWALL)
# without paywall: https://www.hs.fi/ruoka/reseptit/art-2000008160097.html 
# without paywall: https://www.hs.fi/ruoka/art-2000008229534.html
# without paywall: https://www.hs.fi/ruoka/art-2000008205463.html
# Peruna: https://www.hs.fi/ruoka/art-2000008205467.html

# Implementation Plan:
# Step 1: Ask user for URL
# Step 2: Load page & Catch Authentication - > user input / new load of URL after user-input
# Step 3: Discover & extract title recipes
# Step 4: Ask user which recipes
# Step 5: Extract full recipes and store each selected recipe in a file with the recipe name as name
# Step 6: Print
# Step 7: error catching test with list of websites above
# Step 8: Clean-up of code

# !/usr/bin/env python
# coding: utf-8

import pip
import bs4
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib import request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import sys
from tkinter import *
import lxml
import os
import chromedriver_autoinstaller
import selenium


def web_page_loader(url):
    # Works, when browser open and logged in

    # Next few lines are for checking if the webdriver is there and what version.
    # This is needed for web_page_loader and for login_and_get_page functions
    chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
    # and if it doesn't exist, download it automatically, then add chromedriver to path
    driver= webdriver.Chrome()
    # driver = webdriver.Chrome(ChromeDriverManager().install()) # always installs

    if "hs." not in url: # if this url is not from Hessari
        print("Are you sure you gave the right link for HS ruoka page? Try again.")
        exit()

    try: # if this is not a URL
        html = request.urlopen(url).read().decode('utf8')
    except:
        print("The URL give could not be opened")
        exit()

    soup = BeautifulSoup(html, 'html.parser') # contains links to recipes
    soup_lxml = bs4.BeautifulSoup(html, 'lxml') # (does not give links to recipes)
    sleep(3)  # if you want to wait 3 seconds for the page to load
    return soup, soup_lxml


def findall(p, s):
    # Yields all the positions of the pattern p in the string s.
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)

def select_recipe(soup, url):
    # find in content the recipe titles and start of the recipes, put titles in a list
    urls = []
    page_source_as_text = str(soup)

    # search_for="https://pakki-delivery.datadesk.hs.fi/?appI"
    search_for= "pakki-deli"  # search term for the page

    # https://pakki-delivery.datadesk.hs.fi?appId=f585bb25-0808-4322-9f9d-78e8409e0928 (example URL)
    # we find the "spot" where pakki-deli is, but we extract the rest of the URL
    # they are then found all and put into a list called urls
    urls = [page_source_as_text[i-8:i+72] for i in findall(search_for, page_source_as_text)]
    # this list contains the pakki-urls with the recipes, some double elements in there
    driver = webdriver.Chrome()

    # make urls list only to have unique elements
    unique_urls = []
    recipies_dict = {}  # dictionary with recipe title and URL
    if urls:
        # traverse through all found pakki-URLs in the list
        for x in urls:
            # check if exists in unique_list or not
            if x not in unique_urls: # check if already in list, if not append
                unique_urls.append(x)
        titles = []
        for u in unique_urls:
            # Working code for retrieving the recipe from pakki-delivery page and printing it in clear text
            driver.get(u)
            sleep(3)  # if you want to wait 3 seconds for the page to load
            page_source = driver.page_source
            web_page_html = bs4.BeautifulSoup(page_source, 'lxml')
            otsikko = web_page_html.find("p") # find headline of the recipe
            titles.append(otsikko.get_text())
            otsikko_short = otsikko.get_text()[:12]  # This is for the file names to store the recipe
            text = ""
            with open(otsikko_short + '.txt', 'w', encoding='utf-8') as the_file:
                for para in web_page_html.find_all("p"):
                    text += para.get_text() + '\n'
                # print(text)
                text += '\n' + "Resepti: Helsingin Sanomat" + '\n'
                text += url
                text = text.encode('utf-8').decode('utf-8', 'ignore')
                # Some good tutorial on different codes and characters
                # https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/
                the_file.write(text)
            recipies_dict[otsikko.get_text()] = otsikko_short + '.txt'
        # driver.quit()
    else: # e.g. for recipes of the form: https://www.hs.fi/ruoka/reseptit/art-2000008444582.html
        page_title = str(soup.title)  # this gives the title of the page, which does not need to be the titel of the recipe
        page_title = page_title.strip('<title>')
        page_title = page_title.strip('- Reseptit | HS.fi</')
        # print("page title: ", page_title)
        text = ""
        text += page_title + '\n' + '\n'
        for para in soup.find_all("p"):
            text += para.get_text() + '\n'
        text += '\n' + "Resepti: Helsingin Sanomat" + '\n'
        text += url
        text = text.encode('utf-8').decode('utf-8', 'ignore')
        otsikko_short = page_title[:12]
        with open(otsikko_short + '.txt', 'w', encoding='utf-8') as the_file:
            the_file.write(text)
        recipies_dict[otsikko_short + '.txt'] = text

    return recipies_dict, unique_urls

def selection_UI(a_recipies): # a_recipes contains the dictionary of recipies
    # https://www.tutorialsteacher.com/python/create-gui-using-tkinter-python (good tutorial on tkinker for UI)
    data= list(a_recipies.keys())
    window = Tk()
    # btn = Button(window, text="This is the UI for recipe selection", fg='blue')
    # btn.place(x=80, y=100)
    # lbl.place(x=80, y=80)
    lbl = Label(window, text="Please click the recipies you like to print", fg='red', font=("Helvetica", 16)).grid(row=0, sticky=W)
    l = len(data)

    # Creating a list of the recipes to click
    i=0
    v=[]
    C=[]

    for receipe_t in data:
        v.append(IntVar()) # extend list for i'th element
        # Create entry for each receipe
        C.append(Checkbutton(window, text=receipe_t, variable=v[i]))
        C[i].grid(row=i+2, sticky=W)
        i = i + 1

    def var_states():
        global selected_recipes_list
        selected_recipes_list =[]
        not_selected_recipes_list =[]
        print("\n")
        for i in range(l): # Loop for printing which recipes have been selected
            # next line shows if a recipe has been clicked or not
            # print(data[i] + ": %d " % (v[i].get())) # the v[1].get() fetches the state of the checkbox, 1 if clicked, zero if not
            # Storing the names of the selected recipes
            if v[i].get() != 0: # if selected
                name_short = data[i][:12]  # shorten the name
                selected_recipes_list.append(name_short + ".txt") #store file name for selected
            else:
                name_short = data[i][:12]
                not_selected_recipes_list.append(name_short + ".txt") # file names of the not selected for deletion

        # remove not needed recipes
        k = 0
        if not not_selected_recipes_list:  #checks if list is not empty
            for i in not_selected_recipes_list:
                os.remove(not_selected_recipes_list[k])
        window.destroy()
        return

    # https://www.python-course.eu/tkinter_checkboxes.php - checkboxes and clicking them tutorial
    Button(window, text='Done', command=var_states, font="ariel 15 bold", bg="black", fg="white").grid(row=l+3, sticky=W, pady=l+3)
    # This button, if clicked calls the var_states function, which checks what checkbuttons were clicked

    # Window format stuff
    window.title('UI Recipe Selection')
    window.geometry("500x400+10+10")
    window.wm_attributes("-topmost", 1)  # puts window on top
    window.mainloop()

    return selected_recipes_list

def print_selected_recipes(file_names):
    # print recipe from pakki-delivery url
    for file in file_names:
        f = open(file, 'r', encoding='utf-8')
        file_contents = f.read()
        # print to printer: https://stackoverflow.com/questions/12723818/print-to-standard-printer-from-python
        os.startfile(file, "print")  # this line automatically prints out the selected recipes
        f.close()
    return

def main():

    print("Example URL: https://www.hs.fi/ruoka/art-2000008205467.html")

    url_to_analyze = input("What HS webpage do you want to extract the recipes from: ")
    page_content, page_content_lxml = web_page_loader(url_to_analyze)

    all_recipes, returned_urls = select_recipe(page_content, url_to_analyze) #returns receipe dictionary
    if returned_urls: # if some recipes were found
        recipes_to_print = selection_UI(all_recipes)
    else:
        recipes_to_print = list(all_recipes.keys())

    want_to_print = input("Do you want to print to printer? y/n : ")  # small check to avoid while programming to
    # print out same recipes dozen of times
    if want_to_print == "y":
        print_selected_recipes(recipes_to_print)

if __name__ == "__main__":
    main()



