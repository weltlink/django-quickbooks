from abc import ABC

from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.exceptions import ValidationError
from django_quickbooks.utils import xml_setter
from django_quickbooks.validators import SchemeValidator, is_primitive, is_list


class BaseObject(ABC):
    fields = dict()
    validator = SchemeValidator()

    def __setattr__(self, key, value):
        if key in self.fields:
            if self.validator.validate(value, **self.fields[key]):
                pass
            else:
                raise ValidationError
        super().__setattr__(key, value)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def as_xml(self, class_name=None, indent=0, opp_type=QUICKBOOKS_ENUMS.OPP_ADD,
               version=QUICKBOOKS_ENUMS.VERSION_13, **kwargs):
        xml = ''
        for field_key, options in self.fields.items():
            if hasattr(self, field_key):
                obj = getattr(self, field_key)
                if is_primitive(obj):
                    if self.fields[field_key]['validator']['type'] == self.validator.BOOLTYPE:
                        xml += xml_setter(field_key, str(obj).lower(), encode=True)
                    else:
                        xml += xml_setter(field_key, str(obj), encode=True)

                elif is_list(obj):
                    for element in obj:
                        if is_primitive(element):
                            if self.fields[field_key]['validator']['type'] == self.validator.BOOLTYPE:
                                xml += xml_setter(field_key, str(element).lower(), encode=True)
                            else:
                                xml += xml_setter(field_key, str(element), encode=True)
                        else:
                            if field_key in kwargs.get('ref_fields', []):
                                xml += element.as_xml(class_name=field_key, indent=indent,
                                                      opp_type=QUICKBOOKS_ENUMS.OBJ_REF, version=version, **kwargs)
                            elif field_key in kwargs.get('change_fields', []):
                                xml += element.as_xml(class_name=field_key, indent=indent, opp_type=opp_type,
                                                      version=version, **kwargs)
                            elif field_key in kwargs.get('complex_fields', []):
                                xml += element.as_xml(class_name=field_key, indent=indent, opp_type='', version=version,
                                                      **kwargs)
                else:
                    if field_key in kwargs.get('ref_fields', []):
                        xml += obj.as_xml(class_name=field_key, indent=indent, opp_type=QUICKBOOKS_ENUMS.OBJ_REF,
                                          version=version, **kwargs)
                    elif field_key in kwargs.get('change_fields', []):
                        xml += obj.as_xml(class_name=field_key, indent=indent, opp_type=opp_type, version=version,
                                          **kwargs)
                    elif field_key in kwargs.get('complex_fields', []):
                        xml += obj.as_xml(class_name=field_key, indent=indent, opp_type='', version=version, **kwargs)

        class_name = self.__class__.__name__ if not class_name else class_name
        xml = xml_setter(class_name + opp_type, xml)
        return xml

    @classmethod
    def from_lxml(cls, lxml_obj):

        def to_internal_value(field, type):
            converters = dict(
                STRTYPE=lambda x: x.text,
                IDTYPE=lambda x: x.text,
                BOOLTYPE=lambda x: bool(x.text),
                # OBJTYPE=lambda x: x,
                # LISTTYPE=lambda x: x,
            )
            return converters[type](field) if type in converters else None

        obj = cls()
        for field in list(lxml_obj):
            if field.tag in cls.fields:
                setattr(obj, field.tag, to_internal_value(field, cls.fields[field.tag]['validator']['type']))
            elif field.tag == 'ParentRef':
                setattr(obj, 'Parent', cls.from_lxml(field))

        return obj

    @staticmethod
    def get_service():
        raise NotImplemented
