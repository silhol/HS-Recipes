# Helsingin Sanomat Recipe Extractor

The finnish Helsingin Sanomat (HS) has a wide range of nice recipes. When I cook, I like to print them out, so that I do not have to touch with greasy fingers my phone. But if one prints out the HS recipe pages, then one gets not only the one rececipe you like, but many other stuff that is of less interest for the cooking. The intend of this script is to keep your phone clean from grease & sauce and to print only one page of paper instead of 10 or more

The script should work with the current recipes of HS and with most older recipe pages of HS. You find two python files in this repository. One for older recipes (ie before summer 2024) and one for newer (the "updated"). HS changed their design, that is why there are two.

So my friend (Susanna Kallio) and I created this little python script. Some recipes require you to login (so please do that before you use the script for those recipes that require a login!).

For smooth working, please update your chrome browser to the newest version and restart the browser. And it also helps to update the packages used by this program (in particular anything related to browser handling). If you get an error "chrome driver incomptability", thats this issue....

## Functionalities

Start the Python script (remember in pycharm that the modules have to be in place i.e. add them via settings).

You will be requested to insert the URL with the recipe.
You will then be presented with a choice of the found recipes.
You click which ones you like to print.
The chosen one will be stored as .txt in the same directory as the python script 
You will be quickly questioned if you want to print them
Then they should go directly to the printer.

## Technical Details

We used Pycharm and Windows. A wide range of modules have been loaded (under pycharm you have to add them under settings and also update them!)

## Note of copyright

The recipes are of course property of HS and this script is only to reduce the paper waste compared to "normal print" (and since HS does not have a nice print button).

January 2023
