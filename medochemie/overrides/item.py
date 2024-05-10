import frappe
from frappe.model.document import Document
import erpnext
from erpnext.stock.doctype.item.item import Item

class ItemCustom(Item):
    """ Inherit core item class """
    
    def on_update(self):
        # self.description = self.item_name
        if self.item_group == "API":
            #frappe.db.set_value("Item", self.item_code, "item_code", "000002")
            self.description = "Name: " + self.item_name + "<br>" + "Code: " + self.item_code + "<br>" + "Category: API"
            frappe.db.commit()
        elif self.item_group == "Raw Material":
             #self.item_code = "213_" + self.item_code 
             self.description = "Name: " + self.item_name + "<br>" + "Code: " + self.item_code
        """ print ("Get something") """