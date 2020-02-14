# Changelog

All notable changes to this project will be documented in this file.

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
