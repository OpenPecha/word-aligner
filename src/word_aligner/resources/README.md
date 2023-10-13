# About resource folder

Some of the folder you might not see because the size was too big and was put in gitignore,
but you understand better with all information available.

## all_BO_EN_list.txt

Contains list of all tibetan text corpus (starting iwth BO..) and corresponding english
text corpus (starting with EN...)
The content is copied from the link:

https://github.com/OpenPecha-Data/C1A81F448/blob/main/C1A81F448.opc/meta.yml

and the file is used to get all the list of TM files (this is done by getting the IDs from bo files). such that from file name BO0133, we get ID 0133 and we know there a corresponding TM
file name TM0133.

## all_TM_list.txt

Contains all the TM file names extracted from all_BO_EN_list.txt.


## སྨོན་2020-headwords.csv

Contains all the headwords from the dictionary སྨོན་2020. The file is used to get the list of headwords

link: https://github.com/OpenPecha/dictionaries
folder: bo-bo


## mahavyutpatti.csv

Contains tibetan words and its corresponding sanskrit translation from the dictionary mahavyutpatti.
The file is used to get the list of tibetan words.

link: https://github.com/OpenPecha/dictionaries
folder: bo-san

## Illuminator.xlsx

Contains tibetan words, thier description / defination and english words if possible in double quotes.
link: https://github.com/OpenPecha/dictionaries
folder: bo-en

## tibetan_english_dictionary.json
Contains tibetan words and their corresponding english words parse from Illuminator.xlsx file.
