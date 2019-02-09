# Utilities

This is a small library I've compiled for my own personal needs. Nothing really fancy and a lot could probably
be done with other Python libraries (such as numpy), but I like to write out the smaller things I need myself
rather than relying on packages.

The only reason I put this on Github in the first place is to reference it in other projects as I use it a lot.

Right now there are 7 libraries - Arrays, Excel, Files, Jsons, Lists, Math, and Strings. Each
have their own functions to do certain tasks for each class. Also, almost all the functions are static
methods so they can be accessed very easily within other modules. 

To give a quick synopsis:

Arrays includes things like swap, removing by a list of indexes, and some array index rewrites

Excel includes removing illegal characters, transforming a 2D array into an Excel file, 
parsing all the CSV and Excel files in a designated folder, etc

Files has some functions like counting the number of lines in a file, copying a file, saving and loading Python
objects, etc

Jsons includes creating dictionaries from two arrays, opening and closing json files, crossing two jsons,
and finding all keys with empty values within a dictionary

Math includes fibonacci, fibonacci sum, check prime, prime factors, sum of squares, etc

and finally Strings has functions like checking if a string is ascii compliant, biggest word in a text, and 
the last non-whitespace character of a string.

There's definitely more functions than what I just listed, but if you'd like to know more check out the code!
While some of the functions are almost certainly useless, if they're in this library, I've used them for either
a project or code competition or something like that, so they'll stay (just in case!) for future use.

I may one day write up a more thorough API with real documentation for this, but as of now this suits my needs.
Like I said, I only put it on Github to be a reference as I use it in almost all my projects.

## Install

### Dependencies

- python 3.6

#### Excel:

- xlrd
- xlwt

#### Files:

- dill

### Import

Once the dependencies are installed, you can import each library like so:

    from Files import Files as files
    
    files.get_files_in_cwd()
    .
    .
    .

Super simple!
