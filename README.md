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
 * Celery (for handling asynchronous tasks)


## Notice
Soap server for Quickbooks Web Connector is built on top of Spyne and Lxml.


## Setup & Documentation


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
