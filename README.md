# France Mean Hourly Salaries

The goal of this project is to serve data on average salaries in France and can be used for example for target marketing.
The data we use is available as open data in  [csv](https://www.data.gouv.fr/en/datasets/salaire-net-horaire-moyen-selon-la-categorie-socioprofessionnelle-le-sexe-et-lage-en-2014/)  
We build an API in flask with frontends serving endpoints in javascript.
Documentation for the API is available [here](https://documenter.getpostman.com/view/6947361/SWLb8ouT?version=latest) 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
pip install -r requirements.txt
```

### Installing

We start by creating and activating a virtual environment

```
python3 -m venv env
```

And activate

```
source env/bin/activate
```

Then install dependencies

```
pip3 install -r requirements.txt
```

## Built With

* [Flask](http://flask.palletsprojects.com/en/1.1.x/) - The web framework used
* [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) - Javascript front end
* [Folium](https://python-visualization.github.io/folium/) - Python package for map visualisation




