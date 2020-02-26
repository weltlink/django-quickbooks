### Installation
`pip install django-quickbooks`

You can run `pip install django-quickbooks pika spyne celery` to install all of the dependencies.

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
You need also to install RabbitMQ, which is a widely known message broker, 
you can find instructions on how to install RabbitMQ Here [https://www.rabbitmq.com/download.html]

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
    
    def to_qbd_obj(self, **fields):
        from django_quickbooks.objects import Customer as QBCustomer
        # map your fields to the qbd_obj fields
        return QBCustomer(Name=self.__str__(),
                          IsActive=True,
                          FirstName=self.first_name,
                          LastName=self.last_name,
                          Phone=self.phone,
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




