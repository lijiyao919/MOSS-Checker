# MOSS Checker

## Introduction
A [MOSS](http://theory.stanford.edu/~aiken/moss/) written in Python. The code uses API from [moss.py](https://github.com/soachishti/moss.py). It is a command line tool, you have to give it a bunch of parameters, as it is noted in the [Usage](#Usage).

You need to register with MOSS to obtain a userid.  Instructions [here](http://theory.stanford.edu/~aiken/moss/)

## Usage

It accepts  .zip file of the assignments, e.g, Canvas Exported file. And it can also work for source file like .java.

Command line requirements
-   --infile : followed by the name of the  .zip file. You can repeat this argument multiple times to include multiple .zip files. 
-   -- outfolder : followed by the name of the root folder you want to place the extracted files; it will create this folder
-   --userid : Your  MOSS  assigned userid
-   --language : Followed by the programming language, e.g, Python, Java
-  --file_ext: source file extension, e.g, py, java


If you have one .zip file, an example command line looks like…
```
python checker.py --infile submissions.zip --outfolder hw --userid 12345 --language Java
```
If you have two .zip file, an example command line looks like…
```
python checker.py --infile submissions.zip --infile submissions2.zip --outfolder hw --userid 12345 --language Java
```

If you need baseline file, add source files into base folder at the folder of checker.py, an example command line looks like (the same as previous)
```
python checker.py --infile submissions.zip --infile submissions2.zip --outfolder hw --userid 12345 --language Java
```

The program unzip all the assignments, extract each student’s source file into their own folder and then submits them all to MOSS (all file would be removed other than the source file).  When it is complete, it writes a ‘report.html’ file you can open to view the results. Refer to the [Reading the Results](http://moss.stanford.edu/general/format.html) for how to interpret the results.

## Python Compatibility
- Python - v3