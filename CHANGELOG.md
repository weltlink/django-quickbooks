# Changelog

All notable changes to this project will be documented in this file.

## [0.6.0] - 2020-02-12

### Added

- Add ValidationError handling
- Add basic decorators for realm connection
- Add realm_connection decorator to ResponseProcessor and SessionManager
- Add initial documentation structure

### CHANGED

- All Signal `schema_name` arguments were changed to `realm_id` (after removing *django-tenant-schemas*)

### Removed

- Remove *django-tenant-schemas* dependency from project (make it as optional)


[0.6.0]: https://github.com/weltlink/django-quickbooks/compare/0.5...0.6
