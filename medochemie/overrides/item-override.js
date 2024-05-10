frappe.ui.form.on('Item', {
    onload_post_render: function(frm) {
            console.log('Load Form');

        console.log(frm);
            if (frm.doc.item_group != "Products") {
                document.querySelector('div[data-doctype="BOM"]').remove()
            }

    }
});

// Filter items based on product groups
frappe.ui.form.on('BOM', {
    onload_post_render: function(frm) {
        // Filter items with product group "Materials" or "API"
        
        frm.set_query("item_code", "items", function() {
            return {
                filters: [
                    ['item_group', 'in', ['Raw Material', 'API', 'BOM Materials']]
                ]
            };
        });

    }
});