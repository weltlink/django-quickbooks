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

    def as_xml(self, root=None, indent=0, opp_type=QUICKBOOKS_ENUMS.OPP_ADD, version=QUICKBOOKS_ENUMS.VERSION_13):
        xml = ''
        for field_key, options in self.fields.items():
            if hasattr(self, field_key):

                if is_primitive(getattr(self, field_key)):
                    xml += xml_setter(field_key, str(getattr(self, field_key)), encode=True)

                elif is_list(getattr(self, field_key)):
                    for element in getattr(self, field_key):
                        if is_primitive(element):
                            xml += xml_setter(field_key, str(element), encode=True)
                        else:
                            xml += element.as_xml(root=xml, indent=indent, opp_type=opp_type, version=version)

                else:
                    xml += getattr(self, field_key).as_xml(root=xml, indent=indent, opp_type=opp_type, version=version)

        if opp_type == QUICKBOOKS_ENUMS.OPP_ADD and root:
            xml = xml_setter(self.__class__.__name__, xml)
        else:
            xml = xml_setter(self.__class__.__name__ + opp_type, xml)
        return xml
