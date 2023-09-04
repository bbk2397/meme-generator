# Overview
With this ***meme generator*** one can generate and visualize meme in various ways: through a **command line interface** or through a **web interface**. You can use your own images and quotes or you can use images and quotes provided with this project in the */src/_data* directory (of course, you can add more quotes if you respect the already used format and also new photos). This project includes a **requirements.txt** file that can be used to install the dependencies of this project in your virtual environment.

# Instructions
## Assumptions
Please not that this documentation is done assuming a Linux system.

## Creating a virtual environment and installing the dependencies
If you don't have a virtual environment, you can add one to the root directory of this project, e.g. by running:

> python -m venv meme_generator

Then, assuming that you have opened a Terminal and that your path is in the root directory of the project, you can activate the virtual environment you just created, e.g. by running:

> source meme_generator/bin/activate

followed by the installation of the dependencies: use the **requirements.txt** file, e.g. by running:

> pip install -r requirements.txt.

Of course, you check the dependency list in that **requirements.txt** file. For example, you can see that tools such as the Flask framework, requests, python-docx, Jinja2, Pandas, Numpy, and Pillow were used.

What you also need to install is **Xpdf** so that the pdftotext (not the one that comes through PIP) can be used by the PDF ingestor:

> sudo apt-get install -y xpdf

You'll also need `arial.ttf`, because this is the font used for the quote text that will be added to the image used to generate the meme.

## Using the command line interface
Assuming that you have opened a Terminal and that you are in the /src directory.

This command line interface gives you various ways of generating memes by using the /src/**meme.py** file, but you may want to know that first of all you can:

+ ask for help by using one of the next two commands:

+ > python3 meme.py -h

+ > python3 meme.py --help

+ and also generate a meme with a random image and random quote by just running:

+ > python3 meme.py

The generated meme can be seen in the **/src/tmp** directory. If you don't have such a directory it will be created; also if you have it and also have files in it, the program will attempt to avoid overwriting any files you have there. The path to this file can also be seen in the Terminal after you run the command (this path is relative to the /src directory).

But, as you have seen in the help, there are also optional parameters, so you can optionally give the path to an image you want to have a quote to or you can give only the body and the author (if you give only the body without the author, there will be an error) or you can enter both the image and the quote (again, with both body and author). Therefore, the next commands are valid:

> python3 meme.py --path='/home/username/src/_data/photos/dog/xander_1.jpg'

> python3 meme.py --path='/home/username/src/_data/photos/dog/xander_1.jpg' --body='Body' --author='Author'

> python3 meme.py --body='Body' --author='Author'

But commands such as the next ones are not:

> python3 meme.py --path='/home/username/src/_data/photos/dog/xander_1.jpg' --body='Body'

> python3 meme.py --body='Body'

If you give only the author, a quote will chosen randomly.

> python3 meme.py --path='/home/username/src/_data/photos/dog/xander_1.jpg' --author='Author'

> python3 meme.py --author='Author'

## Using the web interface
Assuming that you have opened a Terminal and that you are in the /src directory.

Now you'll deal with the /src/**app.py** file. First of all, you'll have to start the server. If you are in the /src directory, run:

> export FLASK_APP=app.py

> flask run --host 0.0.0.0 --port 3000 --reload

If the /src/**/static directory exists, it will be created. Otherwise, it will just be used, but it will be attempted to avoid overwriting any file in it.

Now you can navigate to:

> http://127.0.0.1:3000/

On this page, you'll see a meme and you'll be able to generate another random meme by pressing on the **Random button**. If you press on the **Creator button** you will be redirected to:

> http://127.0.0.1:3000/create

On this page there is a form that you can complete in order to generate a meme. In the first field you are supposed to enter the URL of the image you want to be used for the meme. You can introduce a quote (the body should be introduced in the second field, and the author of the quote in the third field). When you are ready, you can press on the **Create Meme! button**. You should have your own meme displayed!.

What you should note here is the fact you have to fill up all fields in order to create a meme. Currently, there is less flexibility than for the command line tool where you can partially customize the meme.

# Roles and responsibilities of various sub-modules

## The Meme Engine
The Meme Engine has its code in the /src/**MemeEngine** directory. Within this directory there is only an **__init__.py** file for the imports and the **MemeEngine.py** where the functionality is implemented. The MemeEngine class generates the **/tmp** directory if it does not exist, so it depends on the **os** module from the standard library. This class is also responsible for handling various exceptional cases, e.g. it throws an exception if the image file to have a quote on it does not exist (because of this check has a dependency to the **pathlib** module from the standard library), it throws an exception if the image file does not have an allowed extension. But what is the most import is that this class also has to handle the image processing part done with the **Pillow** library: it reads the file
to put a quote on, it appropriately changes its width, and it draws the text (and also styles it so that it looks nice). Of course, this class also saves the file, but it does it in such a way no existing file from the tmp directory is overwritten, so no already processed file is lost by overwriting.

## The Quote Engine
The Quote Engine has its code in the /src/**QuoteEngine** directory. Inside this directory there is a **__init__.py** file for the imports and many many ingestor files (an ingestor interface, an ingestor for csv, one for docx, one for pdf, one for text, and one ingestor that uses all of the other ingestors), a model for quotes, i.e. QuoteModel, an exception in case no quote is found (e.g. if a line is empty, it does not have a quote), and two clases where code was refactored in order to avoid duplicate code, i.e. the StrQuoteParser and the TextFileQuoteParser classes (each of these two are used by at least two other classes: StrQuoteParser refactors in the DocxIngestor and TextFileQuoteParser classes, while TextFileQuoteParser refactors code in the PDFIngestor and TextIngestor classes). Each of the ingestors depend on the **typing** module from the standard library for handling explicitly the List type hint, and they are depending also on the QuoteModel in order to handle quotes.

The role of the ingestor interface is to implement a common functionality, i.e. the *can_ingest* class method, but also to have an abstract method (the *parse* class method) that has to be implemented by subclasses. This ingestor interface, being modeled as an abstract class, uses the **abc** module from the standard library. The allowed_extensions will be different based on the subclass.

Each of the specific ingestors (the csv ingestor, the docx ingestor, the pdf ingestor, the text ingestor, and the general ingestor) has its own implementation of the *parse* class method (of course, the ingestor interface is the super class), its own array of allowed extensions, and may have its own set of dependencies: the csv ingestor depends also on **pandas** library for ingesting csv files, the docx ingestor depends also on the **docx** library for ingesting docx files, and the pdf ingestor also depends  on **subprocess** library from the standard library (in order to use **pdftotext** from **Xpdf**, *not the one that comes through PIP*). The pdf ingestor also handles the deletion of the file created by the **pdftotext** utility, so the pdf ingestor also depends on the **os** module from the standard library. If the given file cannot be ingested by one of these specific ingestors, an exception is raised. The general ingestor has a list of all of the other ingestors and uses them depending on the file given for ingestion.

## meme.py and the /tmp directory
In the **meme.py** file is implemented the command line interface. The generate_meme function handles various cases for generating a meme, e.g. randomly selecting a quote or an image in case one of these is not provided (there is a dependency to the **random** module from the standard library), searching for all images and quote files (there is a dependency to the **os** module from the standard library). This is using the sub-modules QuoteEngine and MemeEngine to collect quotes, and generate memes, respectively. Also, meme.py depends on the **argparse** module from the standard library for creating the command line interface by defining the names of the optional parameters, their type, and hints for each of them. The generated memes are saved to the **/tmp** (if this is not already created, it will be created).

## app.py, the /templates and /static directories
In the **app.py** file is implemented the web interface using Flask. In this interface it is possible to create a random meme, so the **random** module from the standard library is used. Of course, the already created sub-modules are also used, i.e. the Quote and Meme Engines. The customized generated memes are saved to the **/static** (if this is not already created, it will be created during the initialization. During the initialization also the images and quotes are retrieved). 

Of course, the Flask application is initialized using the **Flask** class from the **flask module**.

There are 3 endpoints:

> **GET /** - used to create generate a random meme. This endpoint uses the meme.html template from the /templates directory.

> **GET /create** - used to get the form. This endpoint uses the meme_form.html template from the /templates directory.

> **POST /create** - used to create a meme by using the image from the given URL and the given quote body and quote author. In order to retrieve the image from the given URL, the **requests** module from the standard library is used, and in order to delete the temporary file the **os** module from the standard library is used. This endpoint uses the meme.html template from the /templates directory and it retrieves data from the form defined in the meme_form.html template (also from the /templates directory). The data is retrieved from the form using the **request** module from the **flask module**, and a template is rendered using the **render_template** function also from the **flask module**.


# Other observations
I have used `pycodestyle` and `pydocstyle` to check the style of my code, and doc strings, respectively. Some useful commands for checking your these styles could be:
  
> `pydocstyle . | head -n 5`

> `pycodestyle . | head -n 5`

> `clear`
