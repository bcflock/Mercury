# Mercury

Mercury is a code generation via templating tool designed to quickly create functions for accessing Data within SQL Databases on the cloud. 
Many times, you have many similar functions on the cloud, responsible for slightly different things; you could improve upon this system by reducing the number of functions, but that can increase code coupling. 
Mercury allows you to keep the same number of very similar functions using only two inputs:

- a template directory, that can contain both static and template files,
- and `config.mercury.yml`, which contains specifications for each of these functions.

The configuration within `config.mercury.yml` is applied to the template directory, **for each function in the config**. 
A new directory is then made for each function, with the static files copied over as-is, and the template files transformed with the appropriate configuration applied to them

## Supported languages:
Currently only Python is supported as an output language. 

## Templating

Let's say you have a file called `app.py`, and you want to make it into a template file. The first thing to do is to rename the file to `app.mercury.py`

There are a few important commands for creating a template. Each of these are inserted into the document on a separate line; when that line is encountered, Mercury converts that line into a generated codeblock

- **{mercury::parameters::declare}**: This command will insert parameter initializations and assignments.
- **{mercury::parameters::validate}** This command applies constraints to the parameters. Make sure to put this line below **{mercury::parameters::declare}**
- **{mercury::imports}** This should be placed at the top of the file, and will import any code necessary for the generated code to run. These are based on assumptions contained within the generated code. 
- **{mercury::query::declare}** This command will create a variable called Query. This variable will store the query to execute, though execution is done separately and is not handled by Mercury at this time.

These four commands are likely the extent of what you need to get started with mercury templating. There are other templating commands, but at present they are only used in query generation. These will be laid out in the **Configuration** section of README
The `/template` directory in this repository contains examples of static files and template files

## Configuration
...

## Running
...
