from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class ItemInventory(BaseObject):
    fields = dict(
        ALU=dict(validator=dict(type=SchemeValidator.STRTYPE, max_length=20)),
        Cost=dict(validator=dict(type=SchemeValidator.FLOATTYPE)),
        DepartmentListID=dict(required=True, validator=dict(type=SchemeValidator.IDTYPE)),
        Desc1=dict(validator=dict(type=SchemeValidator.STRTYPE, max_length=30)),
        Desc2=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        IsEligibleForCommission=dict(validator=dict(type=SchemeValidator.BOOLTYPE)),
        IsPrintingTags=dict(validator=dict(type=SchemeValidator.BOOLTYPE)),
        IsUnorderable=dict(validator=dict(type=SchemeValidator.BOOLTYPE)),
        # ItemType may have one of the following values: Inventory, Non - Inventory, Service, Assembly, Group, SpecialOrder
        ItemType=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        MSRP=dict(validator=dict(type=SchemeValidator.FLOATTYPE)),
        OnHandStore01=dict(validator=dict(type=SchemeValidator.INTTYPE)),
        OrderCost=dict(validator=dict(type=SchemeValidator.FLOATTYPE)),
        Price1=dict(validator=dict(type=SchemeValidator.FLOATTYPE)),  # Original Price
        Price2=dict(validator=dict(type=SchemeValidator.FLOATTYPE)),  # Sale Price
        Price3=dict(validator=dict(type=SchemeValidator.FLOATTYPE)),  # Employee Price
        Price4=dict(validator=dict(type=SchemeValidator.FLOATTYPE)),  # Wholesale Price
        Price5=dict(validator=dict(type=SchemeValidator.FLOATTYPE)),  # Custom Price
        ReorderPoint=dict(validator=dict(type=SchemeValidator.INTTYPE)),
        #  SerialFlag may have one of the following values: Optional,Prompt
        SerialFlag=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        UPC=dict(validator=dict(type=SchemeValidator.STRTYPE, max_length=18)),

    )

    def __init__(self, Name=None, Price=None, Qty=None, Description=None, **kwargs):
        if Name:
            self.Desc1 = Name
        if Price:
            self.Price1 = Price
        if Qty:
            self.OnHandStore01 = Qty
        if Description:
            self.Desc2 = Description

        super().__init__(**kwargs)

    @staticmethod
    def get_service():
        from django_quickbooks.services.item_inventory import ItemInventoryService
        return ItemInventoryService
