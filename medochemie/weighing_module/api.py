import frappe
from frappe import _
import json

from frappe.model.document import Document
from frappe.model.docstatus import DocStatus

#class Api(Document):
    
    # Define a function to update the state based on the is_active checkbox
def update_batch_state(doc, method):
    # Check if is_active checkbox is checked
    if doc.is_active:
        # Update state to 'Release'
        doc.docstatus = 'Released'
    else:
        # Update state to 'Blocked'
        doc.docstatus = 'Blocked'

# Hook the function to the after_save event of the Batch document
def register_batch_hooks():
    try:
        frappe.db.after_save('Batch', update_batch_state)
    except:
        frappe.log_error(frappe.get_traceback(), 'Error')

# Call the hook registration function
register_batch_hooks()


@frappe.whitelist()
def get(name):

    try:
        # select t1.item_code, t1.name, t1.parent, t2.custom_narcotic from `tabBOM Weighted Items` AS t1 JOIN `tabItem` as t2 ON t1.item_code = t2.item_code WHERE t1.parent = 'PO-JOB00130';
        # select count(*) from `tabBOM Weighted Items` WHERE parent = 'PO-JOB00130';

        # BOM-DEMO_BATCH_PRODUCT-001
        values = {'parent': name}
        data = frappe.db.sql("""
            SELECT t1.*, t2.custom_narcotic
            FROM `tabBOM Weighed Items` AS t1 
            JOIN `tabItem` as t2 ON t1.item_code = t2.item_code
            WHERE t1.parent = %(parent)s
        """, values=values, as_dict=1)
        return data

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Error')
        return None
    #tabBOM Weighted Items| _0d1b51abf4a18627  |     

@frappe.whitelist()
def get_batches_by_item(item_code=None) :
    """ Return all batches belong to a particulat item """
    return frappe.db.get_list('Batch', filters={
            'item': ['=', item_code]
        })
	# SELECT name, item  FROM tabBatch WHERE item = 'nl_2949';


# https://erpnext.medochemie.com/api/method/medochemie.weighting_module.api.get_batches_by_item?item_code=nl_2949

@frappe.whitelist()
def custom_get_item(item_code) :
    out = frappe._dict()
    out =frappe.db.get_list('Batch', filters={'item_code': ['=', item_code]}) or frappe._dict()

	#doc = frappe.get_cached_doc("Item", item_code)
    out.update(out.as_dict())

    return out



@frappe.whitelist()
def custom_get_bom(bom_name):

    values = {'parent': bom_name}
    # SELECT t1.name, t1.owner, t1.idx, t1.item_code, t1.item_name, t1.description, t1.qty, t1.uom, t2.custom_narcotic AS narcodic, t2.custom_flameable AS flameable 
    #   FROM `tabBOM Item` AS t1 
    #       JOIN `tabItem` AS t2 ON t1.item_code = t2.name  
    #           WHERE t1.parent = 'BOM-DEMO_BATCH_PRODUCT-001' AND t1.docstatus = 1;



    #data = frappe.db.sql("""
     #   SELECT t1.name, t1.owner, t1.idx, t1.item_code, t1.item_name, t1.description, t1.qty, t1.uom, t2.custom_narcotic AS narcodic, t2.custom_flameable AS flameable 
      #  FROM `tabBOM Item` AS t1  
       # JOIN `tabItem` as t2 ON t1.item_code = t2.item_code
       # WHERE t1.parent = %(parent)s AND t1.docstatus = 1;
    #""", values=values, as_dict=1)


    data = frappe.db.sql("""
        SELECT t1.name, t1.idx, t1.item_code, t1.item_name, t1.description, t1.qty, t1.uom, t2.custom_narcotic AS narcotic, t2.custom_flameable AS flameable 
        FROM `tabBOM Item` AS t1 
        JOIN `tabItem` AS t2 
                        ON t1.item_code = t2.item_code
        WHERE t1.parent = %(parent)s AND t1.docstatus = 1;
    """, values=values, as_dict=1)

    return data

@frappe.whitelist()
def execute_employee_peer_user(user_id):
    # Define your SQL query with a placeholder for the user ID
    sql_query = """
        SELECT t1.name, t1.first_name, t1.last_name, t1.user_id
        FROM `tabEmployee` AS t1
        JOIN `tabUser` AS t2 ON t1.user_id = t2.name
        WHERE user_id=%s
    """
    
    #sql_query = """SELECT t1.name, t1.first_name, t1.last_name FROM `tabEmployee` AS t1 WHERE t1.user_id=%s"""
    # Execute the SQL query with the provided user ID
    result = frappe.db.sql(sql_query, (user_id,), as_dict=True)
    return result

@frappe.whitelist()
def execute_sql_query(sql_query):
    result = frappe.db.sql(sql_query, as_dict=True)
    return result


@frappe.whitelist()
def test():
    return 'this is test ...'

@frappe.whitelist()
def save_weighted_items(job_card_name, weighted_items_data=None):
    response = {'success': False, 'message': '', 'job_card': None, 'error': None}
 
    try:
        job_card = frappe.get_doc("Job Card", job_card_name)
        # Fetch existing child table entries associated with the job card
        existing_items = {item.item_code: item for item in job_card.custom_bom_list}
        
        obj_weighted_items_data = json.loads(weighted_items_data)


        #response['job_card'] = obj_weighted_items_data
        #response['success'] = True
        #return response
    
        for data in obj_weighted_items_data:
            
            
            existing_item =  existing_items.get(data.get('item_code'))
            
            if existing_item:
                # Update existing record
                existing_item.weighted_qty = data.get('weighted_qty')
                response['job_card'] = existing_item.as_dict()
                response['success'] = True
            else:
                # Insert new record
                child_table = job_card.custom_bom_list.append("weighted_items", {})
                child_table.item_code = data.get('item_code')
                child_table.item_name = data.get('item_name')
                child_table.qty = data.get('qty')
                child_table.weighted_qty = data.get('weighted_qty')
                response['job_card'] = child_table.as_dict()
                response['success'] = True
                
            try:
                # Save the parent document after each child entry operation
                job_card.save()
            except Exception as e:
                response['job_card'] = None
                response['success'] = False
                response['error'] = str(e)
                return response

        return response
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Error')
        response['error'] = frappe.get_traceback()
        return response