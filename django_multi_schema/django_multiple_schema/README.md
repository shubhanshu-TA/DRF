# Django Multi Tenant 

##Overview
Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Django Template embeds Tiger coding guidelines and code quality standards in all app development projects. It ensures extensive support for tracing, monitoring and logging of APIs.

##Objectives
*Embed Tiger coding guidelines and code quality standards in all app development projects.

*Reuse front-end, back-end and deployment components across projects.

*Quickly configure and deploy apps in a matter of 2-4 weeks.

*Embed scalable design as a standard way of building apps.

*Best practices on deployment and monitoring.

##General Features
###Python Web-framework

*High Scalability

*Simple but powerful URL system

*Quickly configure and deploy apps in a matter of 2-4 weeks

*Best practices on deployment and monitoring

*Core Libraries
Django

Djangorestframework

drf-spectacular

django-structlog

RESTful API design and best practices

Software design guidelines and best practices

Documentation standards (templates) and guidelines for Projects

Sphinx for User documentation

Swagger for REST API documentation

Sphinx + PlantUML for architecture documentation

Standardized templates for application development

Project structure and customizable components

Tools around building docker containers, python packages and other assets (documentation, etc)

Automation around CI and CD

Invoke tasks that can be used by CI tools (GitHub Actions)

Invoke tasks that can be used by CD tools (GitHub Actions)

##Developer Stack and Tools
*IDE : Visual Studio Code

*Code Formatter : Black

*Static Code Analyser : Flake8

*Testing framework : pytest

*Automation tool : Docker

*Python Environment Management : Conda + Pip

*Python web framework : Django

*Django Plugins : DRF, django-all-auth, django-csrf , whitenoise, DRF-spectacular

*Database : PostgreSQL / MySQL, Sqlite3

*Dev/Test Environment : Windows/Linux/OSX + docker

##RESTful API Design
*URL Design - Snake_case for URLs

*Singular/plural name for resource but consistent

*Avoid deel URL hierarchies

*Avoid N+1 problem, support argument to return related objects as well (similar to prefetch in ORM)

*Return appropriate HTTP error code depending on error.

*5xx errors should be treated as bugs

##Example
`/segments
GET : return list of segments
`
`
POST : create a new segment
`
`
/segments/<id>
GET : return a particular segment info
`
`
POST : update the specific segment
`
`
DELETE :delete the specific segment
`
`
/segments/<id>?expand=channel
GET : return segment info along with the channel information
``
##HTTP Verb Usage

*GET : To read resource, params/args passed as URL params

*Idempotent, safe to cache

*Not appropriate for secrets/sensitive params

*POST : Used instead of GET for secret/sensitive or large payload

*Not cached. Not idempotent

*Update resource (generally changes the app state)

*PUT : To create new resource

*Idempotent (error if object is already created)

*DELETE : To delete resource

*Idempotent (error if object is already deleted)

*PATCH : Used for partial update of the resource

*Apply partial update to a resource.

*Can be efficient for large payloads

##Software Design Consideration
*Avoid tight coupling between application and data storage model (DB tables)

*Define a API for the required interface and define explicit converters for DB to Object mapping (instead of ORMs). This allows the application to be more flexible regarding Data storage layer

*Avoid tight coupling to DB storage layout

*Define domain models for application and build services and views around domain models. Create explicit adapters to convert to/from DB ORM models

*In existing code bases, a simple way forward would be to define domain classes inspired by the current app DB layer and define simple adapters. In future, for diff DB layout, we will only need to update adapter

*Serializers of ORM objects should handle nested objects and deep hierarchies and avoid repeated queries to DB

*Avoid N+1 problem in DB layer and API Layer

*For ORM, use raw SQL queries or ‘select_related` /prefetch_related method on ORM object

*For SQL, support parameters to return related data (GraphQL is prob. an overkill)

##ORM vs Queries

*ORM is useful for CRUD operations. Integrates well with framework and utilities

*For complex queries, prefer hand-written SQL with named parameters. Use a library like aiosql to manage the queries

##Django Framework
*Current version 4.0. Last stable release 3.2.*.
*Stable and mature. Releases every 9 months or so
*Actively maintained. Huge community (DjangoCon)
*Used by high traffic sites in production

##Django RESTful framework (DRF)
*Preferred approach to create RESTful APIs using Django

*Supports both FBV or CBV

*FBV : customize/extend through Mixins and inheritance

*CBV : customize/extend through decorators

*Provides Viewset or APIView base class (If using CBV)

*APIView : simpler but more code

*Viewsets : specifying Queryset, Serializer, etc. is sufficient for supporting standard CRUD operations. URLS are automatically constructed using Routers

*Provides serialization framework that works with/without Django ORM

*Provides Schema definition mechanism for validation and generating swagger documentation

*Extensible framework through Mixins

*Provides Django packages to leverage mixins for pluggable features.

*Django-ninja : Inspired by FASTAPI but works with Django DRF by integrating it with pydantic support

# Usage

To use this template to start your own project:

### Existing virtualenv

If your project is already in an existing python3 virtualenv first install django by running

    $ pip install -r requirements.txt
    
And then run the `manage.py` command to start the new project:

    $ python manage.py runserver
      
### No virtualenv

This assumes that `python3` is linked to valid installation of python 3 and that `pip` is installed and `pip3`is valid
for installing python 3 packages.

Installing inside virtualenv is recommended, however you can start your project without virtualenv too.
First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com/USERNAME/django_multiple_schema.git
    $ cd django_multiple_schema
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py makemigrations
    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver