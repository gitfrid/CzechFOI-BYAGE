# CzechFOI-ByAge

Czech FOI data analysis

The resulting 3D diagrams are interactive HTML files that can be zoomed and rotated. 
<br>You can download them from the [Plot Results Folder](https://github.com/gitfrid/CzechFOI-ByAge/tree/main/Plot%20Results)

Example of an interactive 3D plot of the Czech FOI data - all VX and UNVX:

Example 3D plot

A solution that makes it easy to analyse, calculate and visualise FOI data in many ways.  
Requires a certain IT affinity, but is simpler, faster and more flexible than using a spreadsheet.

The original Czech FOI data, obtained through a Freedom of Information request, 
can be downloaded at [FOI Link](https://github.com/PalackyUniversity/uzis-data-analysis/blob/main/data/Vesely_106_202403141131.tar.xz)

To import view and edit the data in a SQlite database, you can use "DB Browser for SQLite" version 3.13.0, 
<br>which you can download here [DB Browser for SQLite](https://sqlitebrowser.org/dl/).

The data in the SQLite database (CZFOI.db) were imported from the file Vesely_106_202403141131.CSV. 

Dates are counted as the number of days from 1 January 2020, as an integer number is easier to handle in the Python scripts than a date.
AGE_2023 stands for the age at 1 January 2023, calculated from the year of birth.


The required views were processed using the file ‘All SQL Queries.sql’, 
and the resulting views were manually exported to CSV files to the Terra folder. 
See folder [SQLQueries](https://github.com/gitfrid/CzechFOI-ByAge/blob/main/SQLQueries/All%20SQL%20Queries.sql) and [TERRA](https://github.com/gitfrid/CzechFOI-ByAge/tree/main/TERRA) 

The Phyton scripts analyse and visualise these csv data, and saves the plot result as interactive html files.
[Phyton Scripts](https://github.com/gitfrid/CzechFOI-ByAge/tree/main/Py%20Scripts)

Phyton 3.12.5 to plot the CSV data: 
https://www.python.org/downloads/

Visual Studio Code 1.92.2 to edit and run the phyton script (optional)
https://code.visualstudio.com/download
