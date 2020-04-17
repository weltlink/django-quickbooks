# Django Quickbooks

This is an ongoing project to integrate any Django project with Quickbooks Desktop and Quickbooks Online. Quickbooks 
integration support for <b>Python 3.6+</b> and <b>Django 2.0+</b>

<div align="center">
  Join our active, engaged community: <br>
  <span> | </span>
  <a href="https://spectrum.chat/django-quickbooks">Spectrum</a>
  <span> | </span>
</div>


| Version:  | 0.6.4.2                                                                                                                |
|-----------|--------------------------------------------------------------------------------------------------------------------|
| Download: | https://pypi.org/project/django-quickbooks/                                                                        |
| Source:   | https://github.com/weltlink/django-quickbooks/                                                                     |
| Keywords: | quickbooks,quickbooks-django,django,quickbooks-desktop,quickbooks-online,qb,qbwc,qwc,integration,django-quickbooks |

## Features

### Quickbooks Desktop
- Soap session handling for 8 basic quickbooks web connector operations:
    1. authenticate()
    2. clientVersion()
    3. closeConnection()
    4. connectionError()
    5. getLastError()
    6. getServerVersion()
    7. receiveResponseXML()
    8. sendRequestXML()
    9. interactiveDone() - not really implemented
    10. interactiveRejected() - not really implemented
    11. interactiveUrl() - not really implemented
- Several Realm management model (for handling multiple web connector integration)
- Realm Session management model (for handling concurrent web connector connections)
- QuickBooks Task management model (for handling object synchronization updates)
- Abstract Processor implementation for easier QBXML response handling
- Abstract Object implementation for easier QBXML bidirectional data conversion
- Abstract Service implementation for easier QBXML object manipulation


### Quickbooks Online
...


## Roadmap
 - [x] Quickbooks Desktop Integration (most of the job is done, but can be improved)
 - [ ] Add all other remaining quickbooks objects (or most important ones) 
 - [ ] Add all other remaining services (or most important ones)
 - [ ] Add all other remaining processors (or most important ones)
 - [ ] Quickbooks Online Integration (or most important ones)

 
## Requirements
 * Python 3.6+
 * Django 2.0+
 * RabbitMQ (or reimplementation of QueueManager)
 * Redis (or reimplementation of QueueManager)
 * Celery (for handling asynchronous tasks)


## Notice
Soap server for Quickbooks Web Connector is built on top of Spyne and Lxml.


## Setup & Documentation
### Installation
Installation from pypi: 
```shell script
pip install django-quickbooks
```  
OR
  
Installation from source (github): 
```shell script
pip install -e git+https://github.com/weltlink/django-quickbooks.git@master#egg=django-quickbooks
````   
You can run `pip install django-quickbooks pika spyne celery redis` to install all of the dependencies.

Run migrations: `manage.py makemigrations` , `manage.py migrate`

### Create a new record in django_quickbooks_realm
You should create a new realm for each of your users.  
We will do that from the django shell.  
Execute the command `manage.py shell` and follow these instructions:

```python
from django_quickbooks.models import Realm
realm = Realm(name='TEST NAME', is_active=True, schema_name='default')
realm.set_password('RAW PASSWORD')
# django-quickbooks hashes the raw password and only store the hash similar to what django user do.
# this password is what the user will be using in QBWC
realm.save()
```
>You should automate the previous steps in your code to create a new realm for each user of yours

>If you want to communicate with QBPOS instead of QB Desktop you should edit the settings.py file in django-quickbooks itself,
Go to setting.py and change `QB_TYPE = 'QBPOS'` instead of `'QBFS'` in `DEFAULTS` dict.
>this will be changed to a better approach later.

### QBWC and .qwc file
Download QBWC from [http://marketplace.intuit.com/webconnector].  
>Make sure to use the compatible QBWC versions with your QB Desktop or QB POS version, Note that latest != compatible, 
you may need an older version to work with your QB solution.

Now we need to create a qwc file
`manage.py create_qwc` choose a realm and walk through the steps, copy the output to a `.txt` file and change the extension to `.qwc`
open your QB or QB POS company file
double click the `.qwc` file, give permission to QBWC to access your company file
enter the realm password for this user


### RabbitMQ
You need to install RabbitMQ (if you want to use default QueueManager) which is a widely known message broker. 
However, RabbitMQ implementation of QueueManager is being deprecated as it could not be implemented in the right way to 
keep robust connection, instead it is recommended to use Redis. You can find instructions on how to install RabbitMQ 
[here](https://www.rabbitmq.com/download.html).

### Redis
You can also install Redis (as an alternative to RabbitMQ implementation of QueueManager) which is a widely 
known as in-memory data structure. You can find instructions on how to install Redis 
[here](https://redis.io/topics/quickstart).

### Implementation
Add `django_quickbooks` to your installed apps in `settings.py`.  
Add the following line to `urlspatterns` list inside `urls.py`:  

`path(r'^qwc/', include("django_quickbooks.urls"))`

Inherit the `QBDModelMixin` to the model that you want to sync with QB or QBPOS.
Make sure to add and implement these 2 methods: `to_qbd_obj()` and `from_qbd_obj()` inside your model, so that django_quickbooks can communicate with your project model

```python
from django_quickbooks.models import QBDModelMixin

# This is just an example, you should have your own fields
class Customer(models.Model, QBDModelMixin):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=10)
    street = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
	
    def to_qbd_obj(self, **fields):
        from django_quickbooks.objects import Customer as QBCustomer
        # map your fields to the qbd_obj fields
        return QBCustomer(Name=self.__str__(),
                          IsActive=True,
                          Phone=self.phone,
                          )

    @classmethod			  
    def from_qbd_obj(cls, qbd_obj):
        # map qbd_obj fields to your model fields
        return cls(
            first_name=qbd_obj.Name,
	    phone=qbd_obj.Phone,
            qbd_object_id=qbd_obj.ListID,
            qbd_object_version=qbd_obj.EditSequence
        )
```


### Signal Handler
We are almost finished, add a signal handler for the desired events i.e. `post_save`, `post_delete`, etc  

```python
from django.db.models.signals import pre_delete, post_save
@receiver(post_save, sender=Customer)
def send_customer_to_qbtask(sender, instance, **kwargs):
	QBDTask.objects.create(qb_operation=QUICKBOOKS_ENUMS.OPP_ADD,
                       qb_resource=QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER,
                       object_id=instance.id,
                       content_type=ContentType.objects.get_for_model(instance),
                       realm_id="YOUR REALM ID"
                       )
```
You can use any method you would like to create a record in QBDTask, make sure to populate all these fields correctly.



## Contributing

Check out our [smaller-roadmap](/README.md#Roadmap) or [larger-roadmap](https://github.com/weltlink/django-quickbooks/projects/1) 
to see on what you can help us to improve. Or if you have any problem just drop us a line 
or open an [issue](https://github.com/weltlink/django-quickbooks/issues/new) and we’ll work out how to handle it.

## Links
* [Django Web Framework](https://www.djangoproject.com/)
* [Spyne Official Repository](https://github.com/arskom/spyne)
* [lxml Official Repository](https://github.com/lxml/lxml)


## References
This library could not be possible without contributions from other open-source projects.
Thanks for [quickbooks-php](https://github.com/consolibyte/quickbooks-php) for giving the concept of
creating quickbooks toolkit. Thanks for [Django_to_QuickBooks_API](https://github.com/treviza153/Django_to_QuickBooks_API) 
and [pyqwc](https://github.com/BillBarry/pyqwc) for giving core realization of soap server which made this library possible.
