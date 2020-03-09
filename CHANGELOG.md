# Changelog

All notable changes to this project will be documented in this file.

## [0.6.4.2] - 2020-03-09

### FIXED

- Fix logger handling to django default
- Fix is_list method of validators
- Fix validate method of SchemeValidator when many option is enabled

## [0.6.4.1] - 2020-03-06

### FIXED

- Fix local_customer filtering by name
- Fix setting tenant to conection instead of schema_name
- Fix default REALM_CONNECTION_DECORATOR
- Fix installation requirements of extra tenant package


## [0.6.4] - 2020-02-26

### ADDED

- Add converter from qbd_mixin_model to qbd_task
- Add signal to handle post_process after realm is authenticated successfully

## [0.6.3] - 2020-02-14

### ADDED

- Add Exception coverage for QBTask request conversion
- Add several exceptions

## FIXED

- Fix argument parameter of method CustomerAddResponseProcessor.process()  

## [0.6.0] - 2020-02-12

### ADDED

- Add ValidationError handling
- Add basic decorators for realm connection
- Add realm_connection decorator to ResponseProcessor and SessionManager
- Add initial documentation structure

### CHANGED

- All Signal `schema_name` arguments were changed to `realm_id` (after removing *django-tenant-schemas*)

### REMOVED

- Remove *django-tenant-schemas* dependency from project (make it as optional)


[0.6.0]: https://github.com/weltlink/django-quickbooks/compare/0.5...0.6
[0.6.3]: https://github.com/weltlink/django-quickbooks/compare/0.6...0.6.3
[0.6.4]: https://github.com/weltlink/django-quickbooks/compare/0.6.3...0.6.4
[0.6.4.1]: https://github.com/weltlink/django-quickbooks/compare/0.6.4...0.6.4.1
[0.6.4.2]: https://github.com/weltlink/django-quickbooks/compare/0.6.4.1...0.6.4.2
