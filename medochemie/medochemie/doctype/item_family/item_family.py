# Copyright (c) 2023, Medochemie and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import erpnext
import socket
from frappe.model.document import Document

class ItemFamily(Document):
	def after_insert(self):
		return