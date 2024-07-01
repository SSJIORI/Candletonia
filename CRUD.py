import mysql.connector
import streamlit as st
import pandas as pd
import os

# Establish a connection to MySQL server
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Princessfranz02",
    database="dbCandletonia"
)

mycursor = mydb.cursor()
print("Connection established!")

# Create Streamlit App

def main():
    port = os.getenv('PORT', 8501)
    st.title("Candletonia Database")
    
    menu = ["Inventory", "Supplier", "Shipping Details", "Payment Mode", "Customer Details", "Order Details"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Inventory":
        product_menu()
    elif choice == "Supplier":
        supplier_menu()
    elif choice == "Shipping Details":
        shipping_menu()
    elif choice == "Payment Mode":
        payment_mode_menu()
    elif choice == "Customer Details":
        customer_menu()
    elif choice == "Order Details":
        order_menu()
        
def product_menu(): # Create, Read, Update, Delete Product and Item Operations
    
    product_menu = ["Product", "Item", "Product-Item Relationship"]
    product_choice = st.selectbox("Product Menu", product_menu)
    
    # Add a horizontal line
    st.markdown("---")
    
    # Product Operations
    if product_choice == "Product":
        
        # Create a new product
        st.subheader("Create a new product")
        strName = st.text_input("Product Name *")
        txtDescription = st.text_area("Product Description *")
        intQtyPerUnit = st.number_input("Quantity Per Unit *", min_value=1)
        unitPrice = st.number_input("Unit Price *", min_value=0.0)
        boolIsDiscontinued = st.checkbox("Is Discontinued? *")
        
        # Check if the user has entered all the required fields
        if st.button("Add Product"):
            # check if there are any empty fields
            if strName == "" or txtDescription == "" or intQtyPerUnit == 0 or unitPrice == 0.00:
                st.warning("Please fill in all fields.")
            # check if the product already exists
            else:
                mycursor.execute("SELECT * FROM tblProduct WHERE strName = %s AND txtDescription = %s", (strName, txtDescription,))
                resultP = mycursor.fetchone()
            
                if resultP:
                    st.warning("Product already exists.")
                else:
                    mycursor.execute("INSERT INTO tblProduct (strName, txtDescription, intQtyPerUnit, unitPrice, boolIsDiscontinued) VALUES (%s, %s, %s, %s, %s)", (strName, txtDescription, intQtyPerUnit, unitPrice, boolIsDiscontinued,))
                    mydb.commit()
                    st.success("Product added successfully!")
        
        # Add a horizontal line
        st.markdown("---")
        
        # Read all products
        st.subheader("Read all products")
        mycursor.execute("SELECT * FROM tblProduct")
        resultP = mycursor.fetchall()
            
        if not resultP:
            st.warning("No products found.")
        else:
            productDF = pd.DataFrame(resultP, columns=["Product ID", "Product Name", "Description", "Quantity Per Unit", "Unit Price", "Is Discontinued?"])
                
            # Add filters
            filter_options = st.multiselect("Select Product columns to display", productDF.columns)
            if filter_options:
                productDF = productDF[filter_options]
            # Allow users to query the data using a search bar
            search = st.text_input("Search Product")
            if search:
                productDF = productDF[productDF.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
                    
            st.write(productDF)
        
        # Add a horizontal line
        st.markdown("---")
        
        # Update a product
        st.subheader("Update a product")
        intProductID = st.number_input("Enter Product ID to update", min_value=1)

        # Ensure the user selects which columns to update
        update_name = st.checkbox("Update Product Name")
        update_description = st.checkbox("Update Product Description")
        update_qty_per_unit = st.checkbox("Update Quantity Per Unit")
        update_unit_price = st.checkbox("Update Unit Price")
        update_is_discontinued = st.checkbox("Update Discontinued Status")

        # Fields for the updates
        strName = st.text_input("New Product Name") if update_name else None
        txtDescription = st.text_area("New Product Description") if update_description else None
        intQtyPerUnit = st.number_input("New Quantity Per Unit", min_value=1) if update_qty_per_unit else None
        unitPrice = st.number_input("New Unit Price", min_value=0.0) if update_unit_price else None
        boolIsDiscontinued = st.checkbox("Is Discontinued?") if update_is_discontinued else None

        if st.button("Update Product"):
            if intProductID == 0:
                st.warning("Please enter a valid Product ID.")
            else:
                mycursor.execute("SELECT * FROM tblProduct WHERE intProductID = %s", (intProductID,))
                resultP = mycursor.fetchone()
                    
                if not resultP:
                    st.warning("Product does not exist.")
                else:
                    changes = []
                    if update_name and strName and strName != resultP[1]:
                        # Check for unique constraint on product name
                        mycursor.execute("SELECT * FROM tblProduct WHERE strName = %s", (strName,))
                        if mycursor.fetchone():
                            st.warning("Product name already exists.")
                        else:
                            changes.append(f"strName = '{strName}'")
                        
                    if update_description and txtDescription and txtDescription != resultP[2]:
                        # Check for unique constraint on product description
                        mycursor.execute("SELECT * FROM tblProduct WHERE txtDescription = %s", (txtDescription,))
                        if mycursor.fetchone():
                            st.warning("Product description already exists.")
                        else:
                            changes.append(f"txtDescription = '{txtDescription}'")
                        
                    if update_qty_per_unit and intQtyPerUnit is not None and intQtyPerUnit != resultP[3]:
                        changes.append(f"intQtyPerUnit = {intQtyPerUnit}")
                        
                    if update_unit_price and unitPrice is not None and unitPrice != resultP[4]:
                        changes.append(f"unitPrice = {unitPrice}")
                        
                    if update_is_discontinued and boolIsDiscontinued is not None and boolIsDiscontinued != resultP[5]:
                        changes.append(f"boolIsDiscontinued = {boolIsDiscontinued}")
                        
                    if changes:
                        update_query = "UPDATE tblProduct SET " + ", ".join(changes) + " WHERE intProductID = %s"
                        mycursor.execute(update_query, (intProductID,))
                        mydb.commit()
                        st.success("Product updated successfully!")
                    else:
                        st.warning("No changes made or duplicate value exists.")
        
        # Add a horizontal line
        st.markdown("---")
        
        # Delete a product
        st.subheader("Delete a product")
        intProductID = st.number_input("Enter Product ID", min_value=1)
        
        if st.button("Delete Product"):
            if intProductID == 0:
                st.warning("Please enter a valid Product ID.")
            else:
                mycursor.execute("SELECT * FROM tblProduct WHERE intProductID = %s", (intProductID,))
                resultP = mycursor.fetchone()
                
                if not resultP:
                    st.warning("Product does not exist.")
                else:
                    mycursor.execute("DELETE FROM tblProduct WHERE intProductID = %s", (intProductID,))
                    mydb.commit()
                    st.success("Product deleted successfully!")
        else:
            st.warning("You cannot undo this action.")
    
    # Item Operations
    elif product_choice == "Item":
        
        # Create a new item
        st.subheader("Create a new item")
        txtDescriptionItem = st.text_area("Item Description *")
        unitPriceItem = st.number_input("Item Unit Price *", min_value=0.0)
        quantity = st.number_input("Quantity *", min_value=0.0)
        strUnitMeasurement = st.text_input("Unit Measurement")
        intSupplierID = st.number_input("Supplier ID *", min_value=0)
        
        # Check if the user has entered all the required fields
        if st.button("Add Item"):
            # check if there are any empty fields
            if txtDescriptionItem == "" or unitPriceItem == 0.00 or quantity == 0.00 or intSupplierID == 0:
                st.warning("Please fill in all fields.")
            else:
                # check if supplier ID exists
                mycursor.execute("SELECT * FROM tblSupplier WHERE intSupplierID = %s", (intSupplierID,))
                supplier_exists = mycursor.fetchone()
                
                if not supplier_exists:
                    st.warning("Supplier ID does not exist.")
                else:
                    # check if the item already exists
                    mycursor.execute("SELECT * FROM tblItem WHERE txtDescription = %s", (txtDescriptionItem,))
                    resultI = mycursor.fetchone()
                
                    if resultI:
                        st.warning("Item already exists.")
                    else:
                        mycursor.execute("INSERT INTO tblItem (txtDescription, unitPrice, quantity, strUnitMeasurement, intSupplierID) VALUES (%s, %s, %s, %s, %s)", (txtDescriptionItem, unitPriceItem, quantity, strUnitMeasurement, intSupplierID,))
                        mydb.commit()
                        st.success("Item added successfully!")
        
        # Add a horizontal line
        st.markdown("---")
        
        # Read all items
        st.subheader("Read all items")
        mycursor.execute("SELECT * FROM tblItem")
        resultI = mycursor.fetchall()
            
        if not resultI:
            st.warning("No items found.")
        else:
            itemDF = pd.DataFrame(resultI, columns=["Item ID", "Description", "Unit Price", "Quantity", "Unit Measurement", "Supplier ID"])
                
            # Add filters
            filter_options = st.multiselect("Select Item columns to display", itemDF.columns)
            if filter_options:
                itemDF = itemDF[filter_options]
            # Allow users to query the data using a search bar
            search = st.text_input("Search Item")
            if search:
                itemDF = itemDF[itemDF.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
                    
            st.write(itemDF)
            
        # Add a horizontal line
        st.markdown("---")
        
        # Update an item
        st.subheader("Update an item")
        intItemID = st.number_input("Enter Item ID to update", min_value=1)
            
        # Ensure the user selects which columns to update   
        update_description_item = st.checkbox("Update Item Description")
        update_unit_price_item = st.checkbox("Update Item Unit Price")
        update_quantity = st.checkbox("Update Quantity")
        update_unit_measurement = st.checkbox("Update Unit Measurement")
        update_supplier_id = st.checkbox("Update Supplier ID")
            
        # Fields for the updates
        txtDescriptionItem = st.text_area("New Item Description") if update_description_item else None
        unitPriceItem = st.number_input("New Item Unit Price", min_value=0.0) if update_unit_price_item else None
        quantity = st.number_input("New Quantity", min_value=0.0) if update_quantity else None
        strUnitMeasurement = st.text_input("New Unit Measurement") if update_unit_measurement else None
        intSupplierID = st.number_input("New Supplier ID", min_value=0) if update_supplier_id else None
            
        if st.button("Update Item"):
            if intItemID == 0:
                st.warning("Please enter a valid Item ID.")
            else:
                mycursor.execute("SELECT * FROM tblItem WHERE intItemID = %s", (intItemID,))
                resultI = mycursor.fetchone()
                    
                if not resultI:
                    st.warning("Item does not exist.")
                else:
                    changes = []
                    if update_description_item and txtDescriptionItem and txtDescriptionItem != resultI[1]:
                        # Check for unique constraint on item description
                        mycursor.execute("SELECT * FROM tblItem WHERE txtDescription = %s", (txtDescriptionItem,))
                        if mycursor.fetchone():
                            st.warning("Item description already exists.")
                        else:
                            changes.append(f"txtDescription = '{txtDescriptionItem}'")
                        
                    if update_unit_price_item and unitPriceItem is not None and unitPriceItem != resultI[2]:
                        changes.append(f"unitPrice = {unitPriceItem}")
                        
                    if update_quantity and quantity is not None and quantity != resultI[3]:
                        changes.append(f"quantity = {quantity}")
                        
                    if update_unit_measurement and strUnitMeasurement and strUnitMeasurement != resultI[4]:
                        changes.append(f"strUnitMeasurement = '{strUnitMeasurement}'")
                        
                    if update_supplier_id and intSupplierID is not None and intSupplierID != resultI[5]:
                        changes.append(f"intSupplierID = {intSupplierID}")
                        
                    if changes:
                        update_query = "UPDATE tblItem SET " + ", ".join(changes) + " WHERE intItemID = %s"
                        mycursor.execute(update_query, (intItemID,))
                        mydb.commit()
                        st.success("Item updated successfully!")
                    else:
                        st.warning("No changes made or duplicate value exists.")
            
        # Add a horizontal line
        st.markdown("---")
        
        # Delete an item
        st.subheader("Delete an item")
        intItemID = st.number_input("Item ID", min_value=1)
        
        if st.button("Delete Item"):
            if intItemID == 0:
                st.warning("Please enter a valid Item ID.")
            else:
                mycursor.execute("SELECT * FROM tblItem WHERE intItemID = %s", (intItemID,))
                resultI = mycursor.fetchone()
                
                if not resultI:
                    st.warning("Item does not exist.")
                else:
                    mycursor.execute("DELETE FROM tblItem WHERE intItemID = %s", (intItemID,))
                    mydb.commit()
                    st.success("Item deleted successfully!")
        else:
            st.warning("You cannot undo this action.")

    # Product-Item Relationship Operations
    
    elif product_choice == "Product-Item Relationship":
        
        # Create a new product-item relationship
        st.subheader("Create a new product-item relationship")
        intProductID = st.number_input("Product ID *", min_value=1)
        intItemID = st.number_input("Item ID *", min_value=1)
        quantityPI = st.number_input("Item Quantity Used *", min_value=0.0)
        strUnitMeasurementPI = st.text_input("Item Unit Measurement Used")
        
        # Check if the user has entered all the required fields
        if st.button("Add Product-Item Relationship"):
            # check if there are any empty fields
            if intProductID == 0 or intItemID == 0 or quantityPI == 0.00:
                st.warning("Please fill in all fields.")
            else:
                # check if product ID exists and item ID exists
                mycursor.execute("SELECT * FROM tblProduct WHERE intProductID = %s", (intProductID,))
                product_exists = mycursor.fetchone()
                
                mycursor.execute("SELECT * FROM tblItem WHERE intItemID = %s", (intItemID,))
                item_exists = mycursor.fetchone()
                
                if not product_exists:
                    st.warning("Product ID does not exist.")
                elif not item_exists:
                    st.warning("Item ID does not exist.")
                else:
                    # check if the product-item relationship already exists
                    mycursor.execute("SELECT * FROM tblProductItem WHERE intProductID = %s AND intItemID = %s", (intProductID, intItemID,))
                    resultPI = mycursor.fetchone()
                
                    if resultPI:
                        st.warning("Product-Item relationship already exists.")
                    else:
                        if strUnitMeasurementPI == "":
                            strUnitMeasurementPI = None
                        
                        mycursor.execute("INSERT INTO tblProductItem (intProductID, intItemID, quantity, strUnitMeasurement) VALUES (%s, %s, %s, %s)", (intProductID, intItemID, quantityPI, strUnitMeasurementPI,))
                        mydb.commit()
                        st.success("Product-Item relationship added successfully!")
        
        # Add a horizontal line
        st.markdown("---")
        
        # Read all product-item relationships
        st.subheader("Read all product-item relationships")
        mycursor.execute("SELECT tblProduct.intProductID, tblProduct.strName, tblItem.intItemID, tblItem.txtDescription, tblProductItem.quantity, tblProductItem.strUnitMeasurement FROM tblProductItem JOIN tblProduct ON tblProductItem.intProductID = tblProduct.intProductID JOIN tblItem ON tblProductItem.intItemID = tblItem.intItemID")
        resultPI = mycursor.fetchall()
            
        if not resultPI:
            st.warning("No product-item relationships found.")
        else:
            productItemDF = pd.DataFrame(resultPI, columns=["Product ID","Product Name", "Item ID","Item Description", "Quantity Used", "Unit Measurement Used"])
                
            # Add filters
            filter_options = st.multiselect("Select Product-Item columns to display", productItemDF.columns)
            if filter_options:
                productItemDF = productItemDF[filter_options]
            # Allow users to query the data using a search bar
            search = st.text_input("Search Product-Item")
            if search:
                productItemDF = productItemDF[productItemDF.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
                    
            st.write(productItemDF)
    
        # Add a horizontal line
        st.markdown("---")
        
        # Update a product-item relationship
        st.subheader("Update a product-item relationship")
        intProductIDPI = st.number_input("Enter Product ID to update", min_value=1)
        intItemIDPI = st.number_input("Enter Item ID to update", min_value=1)

        # Ensure the user selects which columns to update
        update_quantity_pi = st.checkbox("Update Quantity Used")
        update_unit_measurement_pi = st.checkbox("Update Unit Measurement Used")

        # Fields for the updates
        quantityPI = st.number_input("New Quantity Used", min_value=0.0) if update_quantity_pi else None
        strUnitMeasurementPI = st.text_input("New Unit Measurement Used") if update_unit_measurement_pi else None

        if st.button("Update Product-Item Relationship"):
            if intProductIDPI == 0 or intItemIDPI == 0:
                st.warning("Please enter a valid Product ID.")
            else:
                # Check if the Product-Item relationship exists
                mycursor.execute("SELECT * FROM tblProductItem WHERE intProductID = %s AND intItemID = %s", (intProductIDPI, intItemIDPI,))
                resultPI = mycursor.fetchone()
                
                if not resultPI:
                    st.warning("Product-Item relationship does not exist.")
                else:
                    changes = []
                    if update_quantity_pi and quantityPI is not None and quantityPI != resultPI[2]:
                        changes.append(f"quantity = {quantityPI}")
                        
                    if update_unit_measurement_pi and strUnitMeasurementPI and strUnitMeasurementPI != resultPI[3]:
                        changes.append(f"strUnitMeasurement = '{strUnitMeasurementPI}'")
                        
                    if changes:
                        update_query = "UPDATE tblProductItem SET " + ", ".join(changes) + " WHERE intProductID = %s AND intItemID = %s"
                        mycursor.execute(update_query, (intProductIDPI, intItemIDPI,))
                        mydb.commit()
                        st.success("Product-Item relationship updated successfully!")
                    else:
                        st.warning("No changes made.")
                
        # Add a horizontal line
        st.markdown("---")
        
        # Delete a product-item relationship
        st.subheader("Delete a product-item relationship")
        intProductIDPI = st.number_input("Enter Product ID", min_value=1)
        intItemIDPI = st.number_input("Enter Item ID", min_value=1)

        if st.button("Delete Product-Item Relationship"):
            if intProductIDPI == 0 or intItemIDPI == 0:
                st.warning("Please enter valid Product and Item IDs.")
            else:
                mycursor.execute("SELECT * FROM tblProductItem WHERE intProductID = %s AND intItemID = %s", (intProductIDPI, intItemIDPI,))
                resultPI = mycursor.fetchone()
                
                if not resultPI:
                    st.warning("Product-Item relationship does not exist.")
                else:
                    mycursor.execute("DELETE FROM tblProductItem WHERE intProductID = %s AND intItemID = %s", (intProductIDPI, intItemIDPI,))
                    mydb.commit()
                    st.success("Product-Item relationship deleted successfully!")
        else:
            st.warning("You cannot undo this action.")
                        
    
def supplier_menu(): # Create, Read, Update, Delete Supplier Operations
    
    # Create a new supplier
    st.subheader("Create a new supplier")
    strNameSP = st.text_input("Supplier Name *")
    strEmailSP = st.text_input("Supplier Email *")
    strContactNumberSP = st.text_input("Supplier Contact Number *", max_chars=11)
    strBlockUnitSP = st.text_input("Supplier Block/Unit *")
    strStreetSP = st.text_input("Supplier Street *")        
    strCitySP = st.text_input("Supplier City *")
    strProvinceSP = st.text_input("Supplier Province *")
    strCountrySP = st.text_input("Supplier Country *")
        
    # Check if the user has entered all the required fields
    if st.button("Add Supplier"):
        # check if there are any empty fields
        if strNameSP == "" or strEmailSP == "" or strContactNumberSP == "" or strBlockUnitSP == "" or strStreetSP == "" or strCitySP == "" or strProvinceSP == "" or strCountrySP == "":
            st.warning("Please fill in all fields.")
        # check if the supplier already exists
        else:
            mycursor.execute("SELECT * FROM tblSupplier WHERE strName = %s AND strEmail = %s AND strContactNumber = %s", (strNameSP, strEmailSP, strContactNumberSP,))
            resultSP = mycursor.fetchone()
                
            if resultSP:
                st.warning("Supplier already exists.")
            else:
                mycursor.execute("INSERT INTO tblSupplier (strName, strEmail, strContactNumber, strBlockUnit, strStreet, strCity, strProvince, strCountry) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (strNameSP, strEmailSP, strContactNumberSP, strBlockUnitSP, strStreetSP, strCitySP, strProvinceSP, strCountrySP,))
                mydb.commit()
                st.success("Supplier added successfully!")
    
    # Add a horizontal line
    st.markdown("---")
    
    # Read all suppliers
    st.subheader("Read all suppliers")
    mycursor.execute("SELECT * FROM tblSupplier")
    resultSP = mycursor.fetchall()
            
    if not resultSP:
        st.warning("No suppliers found.")
    else:
        supplierDF = pd.DataFrame(resultSP, columns=["Supplier ID", "Supplier Name", "Supplier Email", "Supplier Contact Number", "Block/Unit", "Street", "City", "Province", "Country"])
                
        # Add filters
        filter_options = st.multiselect("Select Supplier columns to display", supplierDF.columns)
        if filter_options:
            supplierDF = supplierDF[filter_options]
        # Allow users to query the data using a search bar
        search = st.text_input("Search Supplier")
        if search:
            supplierDF = supplierDF[supplierDF.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
                    
        st.write(supplierDF)

    # Add a horizontal line
    st.markdown("---")
    
    # Update a supplier
    st.subheader("Update a supplier")
    intSupplierID = st.number_input("Enter Supplier ID to update", min_value=1)
            
    # Ensure the user selects which columns to update
    update_name_sp = st.checkbox("Update Supplier Name")
    update_email_sp = st.checkbox("Update Supplier Email")
    update_contact_number_sp = st.checkbox("Update Supplier Contact Number")
    update_address_sp = st.checkbox("Update Supplier Address")
            
    # Fields for the updates
    strNameSP = st.text_input("New Supplier Name") if update_name_sp else None
    strEmailSP = st.text_input("New Supplier Email") if update_email_sp else None
    strContactNumberSP = st.text_input("New Supplier Contact Number") if update_contact_number_sp else None
    strAddressSP = st.text_input("New Supplier Address") if update_address_sp else None
            
    if st.button("Update Supplier"):
        if intSupplierID == 0:
            st.warning("Please enter a valid Supplier ID.")
        else:
            mycursor.execute("SELECT * FROM tblSupplier WHERE intSupplierID = %s", (intSupplierID,))
            resultSP = mycursor.fetchone()
                    
            if not resultSP:
                st.warning("Supplier does not exist.")
            else:
                changes = []
                if update_name_sp and strNameSP and strNameSP != resultSP[1]:
                    changes.append(f"strName = '{strNameSP}'")
                        
                if update_email_sp and strEmailSP and strEmailSP != resultSP[2]:
                    changes.append(f"strEmail = '{strEmailSP}'")
                        
                if update_contact_number_sp and strContactNumberSP and strContactNumberSP != resultSP[3]:
                    changes.append(f"strContactNumber = '{strContactNumberSP}'")
                        
                if update_address_sp and strAddressSP and strAddressSP != resultSP[4]:
                    changes.append(f"strAddress = '{strAddressSP}'")
                        
                if changes:
                    update_query = "UPDATE tblSupplier SET " + ", ".join(changes) + " WHERE intSupplierID = %s"
                    mycursor.execute(update_query, (intSupplierID,))
                    mydb.commit()
                    st.success("Supplier updated successfully!")
                else:
                    st.warning("No changes made.")
    
    # Add a horizontal line
    st.markdown("---")
    
    # Delete a supplier
    st.subheader("Delete a supplier")
    intSupplierID = st.number_input("Supplier ID", min_value=1)
        
    if st.button("Delete Supplier"):
        if intSupplierID == 0:
            st.warning("Please enter a valid Supplier ID.")
        else:
            mycursor.execute("SELECT * FROM tblSupplier WHERE intSupplierID = %s", (intSupplierID,))
            resultSP = mycursor.fetchone()
                
            if not resultSP:
                st.warning("Supplier does not exist.")
            else:
                mycursor.execute("DELETE FROM tblSupplier WHERE intSupplierID = %s", (intSupplierID,))
                mydb.commit()
                st.success("Supplier deleted successfully!")
    else:
        st.warning("You cannot undo this action.")

def shipping_menu(): # Create, Read, Update, Delete Drop-Off, Shipping Company, and Shipping Cost Operations
    
    shipping_menu = ["Drop-Off", "Shipping Company", "Shipping Cost"]
    shipping_choice = st.selectbox("Shipping Menu", shipping_menu)
    
    # Add a horizontal line
    st.markdown("---")
    
    # Drop-Off Operations
    if shipping_choice == "Drop-Off":
        
        # Create a new drop-off location
        st.subheader("Create a new drop-off location")
        strBlockUnitDO = st.text_input("Drop-Off Block/Unit *")
        strStreetDO = st.text_input("Drop-Off Street *")        
        strCityDO = st.text_input("Drop-Off City *")
        strProvinceDO = st.text_input("Drop-Off Province *")
        
        # Check if the user has entered all the required fields
        if st.button("Add Drop-Off Location"):
            # check if there are any empty fields
            if strBlockUnitDO == "" or strStreetDO == "" or strCityDO == "" or strProvinceDO == "":
                st.warning("Please fill in all fields.")
            # check if the drop-off location already exists
            else:
                mycursor.execute("SELECT * FROM tblDropOff WHERE strBlockUnit = %s AND strStreet = %s AND strCity = %s AND strProvince = %s", (strBlockUnitDO, strStreetDO, strCityDO, strProvinceDO,))
                resultDO = mycursor.fetchone()
                
                if resultDO:
                    st.warning("Drop-Off Location already exists.")
                else:
                    mycursor.execute("INSERT INTO tblDropOff (strBlockUnit, strStreet, strCity, strProvince) VALUES (%s, %s, %s, %s)", (strBlockUnitDO, strStreetDO, strCityDO, strProvinceDO,))
                    mydb.commit()
                    st.success("Drop-Off Location added successfully!")
        
        # Add a horizontal line
        st.markdown("---")
        
        # Read all drop-off locations
        st.subheader("Read all drop-off locations")
        mycursor.execute("SELECT * FROM tblDropOff")
        resultDO = mycursor.fetchall()
            
        if not resultDO:
            st.warning("No drop-off locations found.")
        else:
            dropOffDF = pd.DataFrame(resultDO, columns=["Drop-Off ID", "Block/Unit", "Street", "City", "Province"])
                
            # Add filters
            filter_options = st.multiselect("Select Drop-Off columns to display", dropOffDF.columns)
            if filter_options:
                dropOffDF = dropOffDF[filter_options]
            # Allow users to query the data using a search bar
            search = st.text_input("Search Drop-Off")
            if search:
                dropOffDF = dropOffDF[dropOffDF.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
                    
            st.write(dropOffDF)
        
        # Add a horizontal line
        st.markdown("---")
        
        # Update a drop-off location
        st.subheader("Update a drop-off location")
        intDropOffID = st.number_input("Enter Drop-Off ID to update", min_value=1)
            
        # Ensure the user selects which columns to update
        update_block_unit_do = st.checkbox("Update Block/Unit")
        update_street_do = st.checkbox("Update Street")
        update_city_do = st.checkbox("Update City")
        update_province_do = st.checkbox("Update Province")
            
        # Fields for the updates
        strBlockUnitDO = st.text_input("New Drop-Off Block/Unit") if update_block_unit_do else None
        strStreetDO = st.text_input("New Drop-Off Street") if update_street_do else None
        strCityDO = st.text_input("New Drop-Off City") if update_city_do else None
        strProvinceDO = st.text_input("New Drop-Off Province") if update_province_do else None
            
        if st.button("Update Drop-Off Location"):
            if intDropOffID == 0:
                st.warning("Please enter a valid Drop-Off ID.")
            else:
                mycursor.execute("SELECT * FROM tblDropOff WHERE intDropOffID = %s", (intDropOffID,))
                resultDO = mycursor.fetchone()
                    
                if not resultDO:
                    st.warning("Drop-Off Location does not exist.")
                else:
                    changes = []
                    if update_block_unit_do and strBlockUnitDO and strBlockUnitDO != resultDO[1]:
                        changes.append(f"strBlockUnit = '{strBlockUnitDO}'")
                        
                    if update_street_do and strStreetDO and strStreetDO != resultDO[2]:
                        changes.append(f"strStreet = '{strStreetDO}'")
                        
                    if update_city_do and strCityDO and strCityDO != resultDO[3]:
                        changes.append(f"strCity = '{strCityDO}'")
                        
                    if update_province_do and strProvinceDO and strProvinceDO != resultDO[4]:
                        changes.append(f"strProvince = '{strProvinceDO}'")
                        
                    if changes:
                        update_query = "UPDATE tblDropOff SET " + ", ".join(changes) + " WHERE intDropOffID = %s"
                        mycursor.execute(update_query, (intDropOffID,))
                        mydb.commit()
                        st.success("Drop-Off Location updated successfully!")
                    else:
                        st.warning("No changes made.")
            
        # Add a horizontal line
        st.markdown("---")
        
        # Delete a drop-off location
        st.subheader("Delete a drop-off location")
        intDropOffID = st.number_input("Drop-Off ID", min_value=1)
            
        if st.button("Delete Drop-Off Location"):
            if intDropOffID == 0:
                st.warning("Please enter a valid Drop-Off ID.")
            else:
                mycursor.execute("SELECT * FROM tblDropOff WHERE intDropOffID = %s", (intDropOffID,))
                resultDO = mycursor.fetchone()
                    
                if not resultDO:
                    st.warning("Drop-Off Location does not exist.")
                else:
                    mycursor.execute("DELETE FROM tblDropOff WHERE intDropOffID = %s", (intDropOffID,))
                    mydb.commit()
                    st.success("Drop-Off Location deleted successfully!")
        else:
            st.warning("You cannot undo this action.")
        
    # Shipping Company Operations
    elif shipping_choice == "Shipping Company":
        
        # Create a new shipping company
        st.subheader("Add a new shipping company")
        strCompanyNameSC = st.text_input("Shipping Company Name *")
        intDropOffIDSC = st.number_input("Drop-Off ID *", min_value=0)
        
        # Check if the user has entered all the required fields
        if st.button("Add Shipping Company"):
            # check if there are any empty fields
            if strCompanyNameSC == "" or intDropOffIDSC == 0:
                st.warning("Please fill in all fields.")
            else:
                # check if drop-off ID exists
                mycursor.execute("SELECT * FROM tblDropOff WHERE intDropOffID = %s", (intDropOffIDSC,))
                drop_off_exists = mycursor.fetchone()
                
                if not drop_off_exists:
                    st.warning("Drop-Off ID does not exist.")
                else:
                    # check if the shipping company already exists
                    mycursor.execute("SELECT * FROM tblShipping WHERE strCompanyName = %s", (strCompanyNameSC,))
                    resultSH = mycursor.fetchone()
                    
                    if resultSH:
                        st.warning("Shipping Company already exists.")
                    else:
                        mycursor.execute("INSERT INTO tblShipping (strCompanyName, intDropOffID) VALUES (%s, %s)", (strCompanyNameSC, intDropOffIDSC,))
                        mydb.commit()
                        st.success("Shipping Company added successfully!")
        
        # Add a horizontal line
        st.markdown("---")
        
        # Read all shipping companies
        st.subheader("Read all shipping companies")
        mycursor.execute("SELECT * FROM tblShipping")
        resultSH = mycursor.fetchall()
            
        if not resultSH:
            st.warning("No shipping companies found.")
        else:
            shippingDF = pd.DataFrame(resultSH, columns=["Shipping ID", "Company Name", "Drop-Off ID"])
                
            # Add filters
            filter_options = st.multiselect("Select Shipping columns to display", shippingDF.columns)
            if filter_options:
                shippingDF = shippingDF[filter_options]
            # Allow users to query the data using a search bar
            search = st.text_input("Search Shipping")
            if search:
                shippingDF = shippingDF[shippingDF.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
                    
            st.write(shippingDF)
    
        # Add a horizontal line
        st.markdown("---")
        
        # Update a shipping company
        st.subheader("Update a shipping company")
        intShippingID = st.number_input("Enter Shipping ID to update", min_value=1)

        # Ensure the user selects which columns to update
        update_company_name_sc = st.checkbox("Update Company Name")
        update_drop_off_id_sc = st.checkbox("Update Drop-Off ID")

        # Fields for the updates
        strCompanyNameSC = st.text_input("New Company Name") if update_company_name_sc else None
        intDropOffIDSC = st.number_input("New Drop-Off ID", min_value=1) if update_drop_off_id_sc else None

        if st.button("Update Shipping Company"):
            if intShippingID == 0:
                st.warning("Please enter a valid Shipping ID.")
            else:
                mycursor.execute("SELECT * FROM tblShipping WHERE intShippingID = %s", (intShippingID,))
                resultSH = mycursor.fetchone()
                    
                if not resultSH:
                    st.warning("Shipping Company does not exist.")
                else:
                    changes = []
                    if update_company_name_sc:
                        if strCompanyNameSC is None or strCompanyNameSC.strip() == "":
                            st.warning("Company Name cannot be empty.")
                        elif strCompanyNameSC != resultSH[1]:
                            changes.append(f"strCompanyName = '{strCompanyNameSC}'")
                            
                    if update_drop_off_id_sc and intDropOffIDSC is not None and intDropOffIDSC != resultSH[2]:
                        changes.append(f"intDropOffID = {intDropOffIDSC}")
                        
                    if changes:
                        update_query = "UPDATE tblShipping SET " + ", ".join(changes) + " WHERE intShippingID = %s"
                        mycursor.execute(update_query, (intShippingID,))
                        mydb.commit()
                        st.success("Shipping Company updated successfully!")
                    else:
                        st.warning("No changes made.")
                        
        # Add a horizontal line
        st.markdown("---")
        
        # Delete a shipping company
        st.subheader("Delete a shipping company")
        intShippingID = st.number_input("Shipping ID", min_value=1)
            
        if st.button("Delete Shipping Company"):
            if intShippingID == 0:
                st.warning("Please enter a valid Shipping ID.")
            else:
                mycursor.execute("SELECT * FROM tblShipping WHERE intShippingID = %s", (intShippingID,))
                resultSH = mycursor.fetchone()
                    
                if not resultSH:
                    st.warning("Shipping Company does not exist.")
                else:
                    mycursor.execute("DELETE FROM tblShipping WHERE intShippingID = %s", (intShippingID,))
                    mydb.commit()
                    st.success("Shipping Company deleted successfully!")
        else:
            st.warning("You cannot undo this action.")
        
    # Shipping Cost Operations
    elif shipping_choice == "Shipping Cost":
        
        # Create a new shipping cost
        st.subheader("Add a new shipping cost")
        strCitySC = st.text_input("Shipping City *")
        strProvinceSC = st.text_input("Shipping Province *")
        shippingCostSC = st.number_input("Shipping Cost *", min_value=0.0)
        intShippingIDSC = st.number_input("Shipping Company ID *", min_value=1)

        # Check if the user has entered all the required fields
        if st.button("Add Shipping Cost"):
            # check if there are any empty fields
            if strCitySC == "" or strProvinceSC == "" or shippingCostSC == 0.00 or intShippingIDSC == 0:
                st.warning("Please fill in all fields.")
            else:
                # check if the Shipping Company ID exists
                mycursor.execute("SELECT * FROM tblShipping WHERE intShippingID = %s", (intShippingIDSC,))
                shipping_company_exists = mycursor.fetchone()

                if not shipping_company_exists:
                    st.warning("Shipping Company ID does not exist.")
                else:
                    # check if the shipping cost already exists
                    mycursor.execute("SELECT * FROM tblShippingCost WHERE strCity = %s AND strProvince = %s AND shippingCost = %s AND intShippingID = %s", (strCitySC, strProvinceSC, shippingCostSC, intShippingIDSC,))
                    resultSC = mycursor.fetchone()

                    if resultSC:
                        st.warning("Shipping Cost already exists.")
                    else:
                        mycursor.execute("INSERT INTO tblShippingCost (strCity, strProvince, shippingCost, intShippingID) VALUES (%s, %s, %s, %s)", (strCitySC, strProvinceSC, shippingCostSC, intShippingIDSC,))
                        mydb.commit()
                        st.success("Shipping Cost added successfully!")

        
        # Add a horizontal line
        st.markdown("---")
        
        # Read all shipping costs
        st.subheader("Read all shipping costs")
        mycursor.execute("SELECT * FROM tblShippingCost")
        resultSC = mycursor.fetchall()
            
        if not resultSC:
            st.warning("No shipping costs found.")
        else:
            shippingCostDF = pd.DataFrame(resultSC, columns=["Shipping Cost ID", "City", "Province", "Shipping Cost", "Shipping ID"])
                
            # Add filters
            filter_options = st.multiselect("Select Shipping Cost columns to display", shippingCostDF.columns)
            if filter_options:
                shippingCostDF = shippingCostDF[filter_options]
            # Allow users to query the data using a search bar
            search = st.text_input("Search Shipping Cost")
            if search:
                shippingCostDF = shippingCostDF[shippingCostDF.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
                    
            st.write(shippingCostDF)
        
        # Add a horizontal line
        st.markdown("---")
        
        # Update a shipping cost
        st.subheader("Update a shipping cost")
        intShippingCostID = st.number_input("Enter Shipping Cost ID to update", min_value=1)
        
        # Ensure the user selects which columns to update
        update_city_sc = st.checkbox("Update Shipping City")
        update_province_sc = st.checkbox("Update Shipping Province")
        update_shipping_cost = st.checkbox("Update Shipping Cost")
        
        # Fields for the updates
        strCitySC = st.text_input("New City") if update_city_sc else None
        strProvinceSC = st.text_input("New Province") if update_province_sc else None
        shippingCost = st.number_input("New Shipping Cost", min_value=0.0) if update_shipping_cost else None
        
        if st.button("Update Shipping Cost"):
            if intShippingCostID == 0:
                st.warning("Please enter a valid Shipping Cost ID.")
            else:
                mycursor.execute("SELECT * FROM tblShippingCost WHERE intShippingCostID = %s", (intShippingCostID,))
                resultSC = mycursor.fetchone()
                    
                if not resultSC:
                    st.warning("Shipping Cost does not exist.")
                else:
                    changes = []
                    if update_city_sc and strCitySC and strCitySC != resultSC[1]:
                        changes.append(f"strCity = '{strCitySC}'")
                        
                    if update_province_sc and strProvinceSC and strProvinceSC != resultSC[2]:
                        changes.append(f"strProvince = '{strProvinceSC}'")
                        
                    if update_shipping_cost and shippingCost is not None and shippingCost != resultSC[3]:
                        changes.append(f"shippingCost = {shippingCost}")
                        
                    if changes:
                        update_query = "UPDATE tblShippingCost SET " + ", ".join(changes) + " WHERE intShippingCostID = %s"
                        mycursor.execute(update_query, (intShippingCostID,))
                        mydb.commit()
                        st.success("Shipping Cost updated successfully!")
                    else:
                        st.warning("No changes made.")
            
        # Add a horizontal line
        st.markdown("---")
        
        # Delete a shipping cost
        st.subheader("Delete a shipping cost")
        intShippingCostID = st.number_input("Shipping Cost ID", min_value=1)
            
        if st.button("Delete Shipping Cost"):
            if intShippingCostID == 0:
                st.warning("Please enter a valid Shipping Cost ID.")
            else:
                mycursor.execute("SELECT * FROM tblShippingCost WHERE intShippingCostID = %s", (intShippingCostID,))
                resultSC = mycursor.fetchone()
                
                if not resultSC:
                    st.warning("Shipping Cost does not exist.")
                else:
                    mycursor.execute("DELETE FROM tblShippingCost WHERE intShippingCostID = %s", (intShippingCostID,))
                    mydb.commit()
                    st.success("Shipping Cost deleted successfully!")
        else:
            st.warning("You cannot undo this action.")

def payment_mode_menu(): # Create, Read, Update, Delete Payment Mode Operation
        
    # Create a new payment mode
    st.subheader("Create a new payment mode")
    txtDescriptionPM = st.text_area("Payment Mode Description *")
        
    # Check if the user has entered all the required fields
    if st.button("Add Payment Mode"):
        # check if there are any empty fields
        if txtDescriptionPM == "":
            st.warning("Please fill in all fields.")
        # check if the payment mode already exists
        else:
            mycursor.execute("SELECT * FROM tblPaymentMode WHERE txtDescription = %s", (txtDescriptionPM,))
            resultPM = mycursor.fetchone()
                
            if resultPM:
                st.warning("Payment Mode already exists.")
            else:
                mycursor.execute("INSERT INTO tblPaymentMode (txtDescription) VALUES (%s)", (txtDescriptionPM,))
                mydb.commit()
                st.success("Payment Mode added successfully!")
                
    # Add a horizontal line
    st.markdown("---")
        
    # Read all payment modes
    st.subheader("Read all payment modes")
    mycursor.execute("SELECT * FROM tblPaymentMode")
    resultPM = mycursor.fetchall()
            
    if not resultPM:
        st.warning("No payment modes found.")
    else:
        paymentModeDF = pd.DataFrame(resultPM, columns=["Payment Mode ID", "Description"])
                
        # Add filters
        filter_options = st.multiselect("Select Payment Mode columns to display", paymentModeDF.columns)
        if filter_options:
            paymentModeDF = paymentModeDF[filter_options]
        # Allow users to query the data using a search bar
        search = st.text_input("Search Payment Mode")
        if search:
            paymentModeDF = paymentModeDF[paymentModeDF.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
                    
        st.write(paymentModeDF)
    
    # Add a horizontal line
    st.markdown("---")
        
    # Update a payment mode
    st.subheader("Update a payment mode")
    intPaymentModeID = st.number_input("Enter Payment Mode ID to update", min_value=1)
        
    # Ensure the user selects which columns to update
    update_description_pm = st.checkbox("Update Payment Mode Description")
        
    # Fields for the updates
    txtDescriptionPM = st.text_area("New Payment Mode Description") if update_description_pm else None
        
    if st.button("Update Payment Mode"):
        if intPaymentModeID == 0:
            st.warning("Please enter a valid Payment Mode ID.")
        else:
            mycursor.execute("SELECT * FROM tblPaymentMode WHERE intPaymentModeID = %s", (intPaymentModeID,))
            resultPM = mycursor.fetchone()
                    
            if not resultPM:
                st.warning("Payment Mode does not exist.")
            else:
                changes = []
                if update_description_pm and txtDescriptionPM and txtDescriptionPM != resultPM[1]:
                    changes.append(f"txtDescription = '{txtDescriptionPM}'")
                        
                if changes:
                    update_query = "UPDATE tblPaymentMode SET " + ", ".join(changes) + " WHERE intPaymentModeID = %s"
                    mycursor.execute(update_query, (intPaymentModeID,))
                    mydb.commit()
                    st.success("Payment Mode updated successfully!")
                else:
                    st.warning("No changes made.")
    
    # Add a horizontal line
    st.markdown("---")
    
    # Delete a payment mode
    st.subheader("Delete a payment mode")
    intPaymentModeID = st.number_input("Payment Mode ID", min_value=1)
    
    if st.button("Delete Payment Mode"):
        if intPaymentModeID == 0:
            st.warning("Please enter a valid Payment Mode ID.")
        else:
            mycursor.execute("SELECT * FROM tblPaymentMode WHERE intPaymentModeID = %s", (intPaymentModeID,))
            resultPM = mycursor.fetchone()
            
            if not resultPM:
                st.warning("Payment Mode does not exist.")
            else:
                mycursor.execute("DELETE FROM tblPaymentMode WHERE intPaymentModeID = %s", (intPaymentModeID,))
                mydb.commit()
                st.success("Payment Mode deleted successfully!")
    else:
        st.warning("You cannot undo this action.")

def customer_menu(): # Create, Read, Update, Delete Customer Operations
    
    customer_menu = ["Customer Address", "Customer"]
    customer_choice = st.selectbox("Customer Menu", customer_menu)
    
    # Add a horizontal line
    st.markdown("---")
    
    # Customer Operations
    if customer_choice == "Customer Address":
        
        # Create a new customer address
        st.subheader("Create a new customer address")
        intCustomerIDCA = st.number_input("Customer ID *", min_value=1)
        strBlockUnitCA = st.text_input("Customer Block/Unit *")
        strStreetCA = st.text_input("Customer Street *")        
        strCityCA = st.text_input("Customer City *")
        strProvinceCA = st.text_input("Customer Province *")
        
        # Check if the user has entered all the required fields
        if st.button("Add Customer Address"):
            # check if there are any empty fields
            if intCustomerIDCA == 0 or strBlockUnitCA == "" or strStreetCA == "" or strCityCA == "" or strProvinceCA == "":
                st.warning("Please fill in all fields.")
            else:
                # check if customer ID exists
                mycursor.execute("SELECT * FROM tblCustomer WHERE intCustomerID = %s", (intCustomerIDCA,))
                customer_exists = mycursor.fetchone()
                
                if not customer_exists:
                    st.warning("Customer ID does not exist.")
                else:
                    # check if the customer address already exists
                    mycursor.execute("SELECT * FROM tblCustomerAddress WHERE intCustomerID = %s AND strBlockUnit = %s AND strStreet = %s AND strCity = %s AND strProvince = %s", (intCustomerIDCA, strBlockUnitCA, strStreetCA, strCityCA, strProvinceCA,))
                    resultCA = mycursor.fetchone()
                    
                    if resultCA:
                        st.warning("Customer Address already exists.")
                    else:
                        mycursor.execute("INSERT INTO tblCustomerAddress (intCustomerID, strBlockUnit, strStreet, strCity, strProvince) VALUES (%s, %s, %s, %s, %s)", (intCustomerIDCA, strBlockUnitCA, strStreetCA, strCityCA, strProvinceCA,))
                        mydb.commit()
                        st.success("Customer Address added successfully!")
        
        # Add a horizontal line
        st.markdown("---")
        
        # Read all customer addresses
        st.subheader("Read all customer addresses")
        mycursor.execute("SELECT * FROM tblCustomerAddress")
        resultCA = mycursor.fetchall()
        
        if not resultCA:
            st.warning("No customer addresses found.")
        else:
            customerAddressDF = pd.DataFrame(resultCA, columns=["Customer Address ID", "Customer ID", "Block/Unit", "Street", "City", "Province"])
            
            # Add filters
            filter_options = st.multiselect("Select Customer Address columns to display", customerAddressDF.columns)
            if filter_options:
                customerAddressDF = customerAddressDF[filter_options]
            # Allow users to query the data using a search bar
            search = st.text_input("Search Customer Address")
            if search:
                customerAddressDF = customerAddressDF[customerAddressDF.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
                
            st.write(customerAddressDF)
        
        # Add a horizontal line
        st.markdown("---")
        
        # Update a customer address
        st.subheader("Update a customer address")
        intCustomerAddressID = st.number_input("Enter Customer Address ID to update", min_value=1)
        
        # Ensure the user selects which columns to update
        update_block_unit_ca = st.checkbox("Update Customer Block/Unit")
        update_street_ca = st.checkbox("Update Customer Street")
        update_city_ca = st.checkbox("Update Customer City")
        update_province_ca = st.checkbox("Update Customer Province")
        
        # Fields for the updates
        strBlockUnitCA = st.text_input("New Block/Unit") if update_block_unit_ca else None
        strStreetCA = st.text_input("New Street") if update_street_ca else None
        strCityCA = st.text_input("New City") if update_city_ca else None
        strProvinceCA = st.text_input("New Province") if update_province_ca else None
        
        if st.button("Update Customer Address"):
            if intCustomerAddressID == 0:
                st.warning("Please enter a valid Customer Address ID.")
            else:
                mycursor.execute("SELECT * FROM tblCustomerAddress WHERE intCustomerAddressID = %s", (intCustomerAddressID,))
                resultCA = mycursor.fetchone()
                    
                if not resultCA:
                    st.warning("Customer Address does not exist.")
                else:
                    changes = []
                    if update_block_unit_ca and strBlockUnitCA and strBlockUnitCA != resultCA[2]:
                        changes.append(f"strBlockUnit = '{strBlockUnitCA}'")
                        
                    if update_street_ca and strStreetCA and strStreetCA != resultCA[3]:
                        changes.append(f"strStreet = '{strStreetCA}'")
                        
                    if update_city_ca and strCityCA and strCityCA != resultCA[4]:
                        changes.append(f"strCity = '{strCityCA}'")
                        
                    if update_province_ca and strProvinceCA and strProvinceCA != resultCA[5]:
                        changes.append(f"strProvince = '{strProvinceCA}'")
                        
                    if changes:
                        update_query = "UPDATE tblCustomerAddress SET " + ", ".join(changes) + " WHERE intCustomerAddressID = %s"
                        mycursor.execute(update_query, (intCustomerAddressID,))
                        mydb.commit()
                        st.success("Customer Address updated successfully!")
                    else:
                        st.warning("No changes made.")
            
        # Add a horizontal line
        st.markdown("---")
        
        # Delete a customer address
        st.subheader("Delete a customer address")
        intCustomerAddressID = st.number_input("Customer Address ID", min_value=1)
        
        if st.button("Delete Customer Address"):
            if intCustomerAddressID == 0:
                st.warning("Please enter a valid Customer Address ID.")
            else:
                mycursor.execute("SELECT * FROM tblCustomerAddress WHERE intCustomerAddressID = %s", (intCustomerAddressID,))
                resultCA = mycursor.fetchone()
                
                if not resultCA:
                    st.warning("Customer Address does not exist.")
                else:
                    mycursor.execute("DELETE FROM tblCustomerAddress WHERE intCustomerAddressID = %s", (intCustomerAddressID,))
                    mydb.commit()
                    st.success("Customer Address deleted successfully!")
        else:
            st.warning("You cannot undo this action.")
    
    # Customer Operations
    elif customer_choice == "Customer":
        
        # Create a new customer
        st.subheader("Create a new customer")
        strFirstNameC = st.text_input("Customer First Name *")
        strMiddleNameC = st.text_input("Customer Middle Name")
        strLastNameC = st.text_input("Customer Last Name *")
        strEmailC = st.text_input("Customer Email *")
        strContactNumberC = st.text_input("Customer Contact Number *", max_chars=11)
        
        # Check if the user has entered all the required fields
        if st.button("Add Customer"):
            # check if there are any empty fields
            if strFirstNameC == "" or strLastNameC == "" or strEmailC == "" or strContactNumberC == "":
                st.warning("Please fill in all fields.")
            # check if the customer already exists
            else:
                mycursor.execute("SELECT * FROM tblCustomer WHERE strFirstName = %s AND strMiddleName = %s AND strLastName = %s", (strFirstNameC, strMiddleNameC, strLastNameC,))
                resultC = mycursor.fetchone()
            
                if resultC:
                    st.warning("Customer already exists.")
                else:
                    if strMiddleNameC == "":
                        strMiddleNameC = None
                    
                    mycursor.execute("INSERT INTO tblCustomer (strFirstName, strMiddleName, strLastName, strEmail, strContactNumber) VALUES (%s, %s, %s, %s, %s)", (strFirstNameC, strMiddleNameC, strLastNameC, strEmailC, strContactNumberC,))
                    mydb.commit()
                    st.success("Customer added successfully!")
        
        # Add a horizontal line
        st.markdown("---")
        
        # Read all customers
        st.subheader("Read all customers")
        mycursor.execute("SELECT * FROM tblCustomer")
        resultC = mycursor.fetchall()
        
        if not resultC:
            st.warning("No customers found.")
        else:
            customerDF = pd.DataFrame(resultC, columns=["Customer ID", "First Name", "Middle Name", "Last Name", "Email", "Contact Number"])
            
            # Add filters
            filter_options = st.multiselect("Select Customer columns to display", customerDF.columns)
            if filter_options:
                customerDF = customerDF[filter_options]
            # Allow users to query the data using a search bar
            search = st.text_input("Search Customer")
            if search:
                customerDF = customerDF[customerDF.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
                
            st.write(customerDF)
    
        # Add a horizontal line
        st.markdown("---")
        
        # Update a customer
        st.subheader("Update a customer")
        intCustomerID = st.number_input("Enter Customer ID to update", min_value=1)
        
        # Ensure the user selects which columns to update
        update_first_name_c = st.checkbox("Update First Name")
        update_middle_name_c = st.checkbox("Update Middle Name (Can be NULL)")
        update_last_name_c = st.checkbox("Update Last Name")
        update_email_c = st.checkbox("Update Email")
        update_contact_number_c = st.checkbox("Update Contact Number")
        
        # Fields for the updates
        strFirstNameC = st.text_input("New First Name") if update_first_name_c else None
        strMiddleNameC = st.text_input("New Middle Name") if update_middle_name_c else None
        strLastNameC = st.text_input("New Last Name") if update_last_name_c else None
        strEmailC = st.text_input("New Email") if update_email_c else None
        strContactNumberC = st.text_input("New Contact Number") if update_contact_number_c else None
        
        if st.button("Update Customer"):
            if intCustomerID == 0:
                st.warning("Please enter a valid Customer ID.")
            else:
                mycursor.execute("SELECT * FROM tblCustomer WHERE intCustomerID = %s", (intCustomerID,))
                resultC = mycursor.fetchone()
                    
                if not resultC:
                    st.warning("Customer does not exist.")
                else:
                    changes = []
                    if update_first_name_c and strFirstNameC and strFirstNameC != resultC[1]:
                        changes.append(f"strFirstName = '{strFirstNameC}'")
                        
                    if update_middle_name_c:
                        if strMiddleNameC is None:
                            changes.append("strMiddleName = NULL")
                        elif strMiddleNameC != resultC[2]:
                            changes.append(f"strMiddleName = '{strMiddleNameC}'")
                        
                    if update_last_name_c and strLastNameC and strLastNameC != resultC[3]:
                        changes.append(f"strLastName = '{strLastNameC}'")
                        
                    if update_email_c and strEmailC and strEmailC != resultC[4]:
                        changes.append(f"strEmail = '{strEmailC}'")
                        
                    if update_contact_number_c and strContactNumberC and strContactNumberC != resultC[5]:
                        changes.append(f"strContactNumber = '{strContactNumberC}'")
                        
                    if changes:
                        update_query = "UPDATE tblCustomer SET " + ", ".join(changes) + " WHERE intCustomerID = %s"
                        mycursor.execute(update_query, (intCustomerID,))
                        mydb.commit()
                        st.success("Customer updated successfully!")
                    else:
                        st.warning("No changes made.")
        
        # Add a horizontal line
        st.markdown("---")
        
        # Delete a customer
        st.subheader("Delete a customer")
        intCustomerID = st.number_input("Customer ID", min_value=1)
        
        if st.button("Delete Customer"):
            if intCustomerID == 0:
                st.warning("Please enter a valid Customer ID.")
            else:
                mycursor.execute("SELECT * FROM tblCustomer WHERE intCustomerID = %s", (intCustomerID,))
                resultC = mycursor.fetchone()
                
                if not resultC:
                    st.warning("Customer does not exist.")
                else:
                    mycursor.execute("DELETE FROM tblCustomer WHERE intCustomerID = %s", (intCustomerID,))
                    mydb.commit()
                    st.success("Customer deleted successfully!")
        else:
            st.warning("You cannot undo this action.")

def order_menu(): # Create, Read, Update, Delete Order Operations
    
    order_menu = ["Order", "Order-Product"]
    order_choice = st.selectbox("Order Menu", order_menu)
    
    # Add a horizontal line
    st.markdown("---")
    
    # Order Operations
    if order_choice == "Order":
        
        # Create a new order
        st.subheader("Create a new order")
        intCustomerIDO = st.number_input("Customer ID *", min_value=0)
        intShippingIDO = st.number_input("Shipping Company ID *", min_value=0)
        datOrderDateO = st.date_input("Order Date *")
        datDateDeliveredO = st.date_input("Delivery Date *")
        intPaymentModeIDO = st.number_input("Payment Mode ID *", min_value=0)
        
        # Check if the user has entered all the required fields
        if st.button("Add Order"):
            # check if there are any empty fields
            if intCustomerIDO == 0 or intShippingIDO == 0 or datOrderDateO == "" or datDateDeliveredO == "" or intPaymentModeIDO == 0:
                st.warning("Please fill in all fields.")
            else:
                # check if customer ID exists, shipping ID exists, and payment mode ID exists
                mycursor.execute("SELECT * FROM tblCustomer WHERE intCustomerID = %s", (intCustomerIDO,))
                customer_exists = mycursor.fetchone()
                
                mycursor.execute("SELECT * FROM tblShipping WHERE intShippingID = %s", (intShippingIDO,))
                shipping_exists = mycursor.fetchone()
                
                mycursor.execute("SELECT * FROM tblPaymentMode WHERE intPaymentModeID = %s", (intPaymentModeIDO,))
                payment_mode_exists = mycursor.fetchone()
                
                if not customer_exists:
                    st.warning("Customer ID does not exist.")
                elif not shipping_exists:
                    st.warning("Shipping ID does not exist.")
                elif not payment_mode_exists:
                    st.warning("Payment Mode ID does not exist.")
                else:
                    mycursor.execute("INSERT INTO tblOrder (intCustomerID, intShippingID, datOrderDate, datDateDelivered, intPaymentModeID) VALUES (%s, %s, %s, %s, %s)", (intCustomerIDO, intShippingIDO, datOrderDateO, datDateDeliveredO, intPaymentModeIDO,))
                    mydb.commit()
                    st.success("Order added successfully!")
        
        # Add a horizontal line
        st.markdown("---")
        
        # Read all orders
        st.subheader("Read all orders")
        mycursor.execute("SELECT tblOrder.intOrderID, tblOrder.intCustomerID, tblCustomer.strFirstName, tblCustomer.strLastName, tblShipping.intShippingID, tblShipping.strCompanyName, tblOrder.datOrderDate, tblOrder.datDateDelivered, tblPaymentMode.intPaymentModeID, tblPaymentMode.txtDescription FROM tblOrder JOIN tblCustomer ON tblOrder.intCustomerID = tblCustomer.intCustomerID JOIN tblShipping ON tblOrder.intShippingID = tblShipping.intShippingID JOIN tblPaymentMode ON tblOrder.intPaymentModeID = tblPaymentMode.intPaymentModeID")
        resultO = mycursor.fetchall()
        
        if not resultO:
            st.warning("No orders found.")
        else:
            orderDF = pd.DataFrame(resultO, columns=["Order ID", "Customer ID", "First Name", "Last Name", "Shipping ID", "Shipping Company Name", "Order Date", "Date Delivered", "Payment Mode ID", "Payment Mode"])
            
            # Add filters
            filter_options = st.multiselect("Select Order columns to display", orderDF.columns)
            if filter_options:
                orderDF = orderDF[filter_options]
            # Allow users to query the data using a search bar
            search = st.text_input("Search Order")
            if search:
                orderDF = orderDF[orderDF.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
                
            st.write(orderDF)
        
        # Add a horizontal line
        st.markdown("---")
        
        # Show sum to pay for each order ID, show customer name, payment mode
        st.subheader("Total Payment per Order")
        mycursor.execute("SELECT tblOrder.intOrderID, tblCustomer.strFirstName, tblCustomer.strLastName, tblPaymentMode.txtDescription, SUM(tblProduct.unitPrice * tblOrderProduct.intQuantity) AS 'Sum to Pay' FROM tblOrder JOIN tblOrderProduct ON tblOrder.intOrderID = tblOrderProduct.intOrderID JOIN tblProduct ON tblOrderProduct.intProductID = tblProduct.intProductID JOIN tblCustomer ON tblOrder.intCustomerID = tblCustomer.intCustomerID JOIN tblPaymentMode ON tblOrder.intPaymentModeID = tblPaymentMode.intPaymentModeID GROUP BY tblOrder.intOrderID")
        resultSP = mycursor.fetchall()
        
        if not resultSP:
            st.warning("No orders found.")
        else:
            sumPayDF = pd.DataFrame(resultSP, columns=["Order ID", "First Name", "Last Name", "Payment Mode", "Sum to Pay"])
            
            # Add filters
            filter_options = st.multiselect("Select Sum to Pay columns to display", sumPayDF.columns)
            if filter_options:
                sumPayDF = sumPayDF[filter_options]
            # Allow users to query the data using a search bar
            search = st.text_input("Search Sum to Pay")
            if search:
                sumPayDF = sumPayDF[sumPayDF.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
                
            st.write(sumPayDF)
        
        # Add a horizontal line
        st.markdown("---")
        
        # Update an order
        st.subheader("Update an order")
        intOrderID = st.number_input("Enter Order ID to update", min_value=1)

        # Ensure the user selects which columns to update
        update_customer_id_o = st.checkbox("Update Customer ID")
        update_shipping_id_o = st.checkbox("Update Shipping ID")
        update_order_date_o = st.checkbox("Update Order Date")
        update_delivery_date_o = st.checkbox("Update Delivery Date")
        update_payment_mode_id_o = st.checkbox("Update Payment Mode ID")

        # Fields for the updates
        intCustomerIDO = st.number_input("New Customer ID", min_value=0) if update_customer_id_o else None
        intShippingIDO = st.number_input("New Shipping ID", min_value=0) if update_shipping_id_o else None
        datOrderDateO = st.date_input("New Order Date") if update_order_date_o else None
        datDateDeliveredO = st.date_input("New Delivery Date") if update_delivery_date_o else None
        intPaymentModeIDO = st.number_input("New Payment Mode ID", min_value=0) if update_payment_mode_id_o else None

        if st.button("Update Order"):
            if intOrderID == 0:
                st.warning("Please enter a valid Order ID.")
            else:
                mycursor.execute("SELECT * FROM tblOrder WHERE intOrderID = %s", (intOrderID,))
                resultO = mycursor.fetchone()
                    
                if not resultO:
                    st.warning("Order does not exist.")
                else:
                    changes = []

                    # Check if the new customer ID exists
                    if update_customer_id_o and intCustomerIDO is not None and intCustomerIDO != resultO[1]:
                        mycursor.execute("SELECT * FROM tblCustomer WHERE intCustomerID = %s", (intCustomerIDO,))
                        customer_exists = mycursor.fetchone()
                        if customer_exists:
                            changes.append(f"intCustomerID = {intCustomerIDO}")
                        else:
                            st.warning("Customer ID does not exist.")

                    # Check if the new shipping ID exists
                    if update_shipping_id_o and intShippingIDO is not None and intShippingIDO != resultO[2]:
                        mycursor.execute("SELECT * FROM tblShipping WHERE intShippingID = %s", (intShippingIDO,))
                        shipping_exists = mycursor.fetchone()
                        if shipping_exists:
                            changes.append(f"intShippingID = {intShippingIDO}")
                        else:
                            st.warning("Shipping ID does not exist.")

                    if update_order_date_o and datOrderDateO is not None and datOrderDateO != resultO[3]:
                        changes.append(f"datOrderDate = '{datOrderDateO}'")
                        
                    if update_delivery_date_o and datDateDeliveredO is not None and datDateDeliveredO != resultO[4]:
                        changes.append(f"datDateDelivered = '{datDateDeliveredO}'")
                        
                    if update_payment_mode_id_o and intPaymentModeIDO is not None and intPaymentModeIDO != resultO[5]:
                        mycursor.execute("SELECT * FROM tblPaymentMode WHERE intPaymentModeID = %s", (intPaymentModeIDO,))
                        payment_mode_exists = mycursor.fetchone()
                        if payment_mode_exists:
                            changes.append(f"intPaymentModeID = {intPaymentModeIDO}")
                        else:
                            st.warning("Payment Mode ID does not exist.")

                    if changes:
                        update_query = "UPDATE tblOrder SET " + ", ".join(changes) + " WHERE intOrderID = %s"
                        mycursor.execute(update_query, (intOrderID,))
                        mydb.commit()
                        st.success("Order updated successfully!")
                    else:
                        st.warning("No changes made.")
        
        # Add a horizontal line
        st.markdown("---")
        
        # Delete an order
        st.subheader("Delete an order")
        intOrderID = st.number_input("Order ID", min_value=1)
        
        if st.button("Delete Order"):
            if intOrderID == 0:
                st.warning("Please enter a valid Order ID.")
            else:
                mycursor.execute("SELECT * FROM tblOrder WHERE intOrderID = %s", (intOrderID,))
                resultO = mycursor.fetchone()
                
                if not resultO:
                    st.warning("Order does not exist.")
                else:
                    mycursor.execute("DELETE FROM tblOrder WHERE intOrderID = %s", (intOrderID,))
                    mydb.commit()
                    st.success("Order deleted successfully!")
        else:
            st.warning("You cannot undo this action.")
    
    # Order Product Operations
    elif order_choice == "Order-Product":
        
        # Create a new order product relationship
        st.subheader("Create a new order-product relationship")
        intOrderIDO = st.number_input("Order ID *", min_value=0)
        intProductIDO = st.number_input("Product ID *", min_value=0)
        intQuantityOP = st.number_input("Product Quantity *", min_value=0)
        
        # Check if the user has entered all the required fields
        if st.button("Add Order-Product Relationship"):
            # check if there are any empty fields
            if intOrderIDO == 0 or intProductIDO == 0 or intQuantityOP == 0:
                st.warning("Please fill in all fields.")
            else:
                # check if order ID exists and product ID exists
                mycursor.execute("SELECT * FROM tblOrder WHERE intOrderID = %s", (intOrderIDO,))
                order_exists = mycursor.fetchone()
                
                mycursor.execute("SELECT * FROM tblProduct WHERE intProductID = %s", (intProductIDO,))
                product_exists = mycursor.fetchone()
                
                if not order_exists:
                    st.warning("Order ID does not exist.")
                elif not product_exists:
                    st.warning("Product ID does not exist.")
                else:
                    # check if the order-product relationship already exists
                    mycursor.execute("SELECT * FROM tblOrderProduct WHERE intOrderID = %s AND intProductID = %s", (intOrderIDO, intProductIDO,))
                    resultOP = mycursor.fetchone()
                
                    if resultOP:
                        st.warning("Order-Product relationship already exists.")
                    else:
                        mycursor.execute("INSERT INTO tblOrderProduct (intOrderID, intProductID, intQuantity) VALUES (%s, %s, %s)", (intOrderIDO, intProductIDO, intQuantityOP,))
                        mydb.commit()
                        st.success("Order-Product relationship added successfully!")

        # Add a horizontal line
        st.markdown("---")
        
        # Read all order product relationships
        st.subheader("Read all order-product relationships")
        mycursor.execute("SELECT tblOrderProduct.intOrderID, tblOrderProduct.intProductID, tblProduct.strName, tblOrderProduct.intQuantity, tblCustomer.strFirstName, tblCustomer.strLastName FROM tblOrderProduct JOIN tblProduct ON tblOrderProduct.intProductID = tblProduct.intProductID JOIN tblOrder ON tblOrderProduct.intOrderID = tblOrder.intOrderID JOIN tblCustomer ON tblOrder.intCustomerID = tblCustomer.intCustomerID")
        resultOP = mycursor.fetchall()
        
        if not resultOP:
            st.warning("No order-product relationships found.")
        else:
            orderProductDF = pd.DataFrame(resultOP, columns=["Order ID", "Product ID", "Product Name", "Quantity", "First Name", "Last Name"])
            
            # Add filters
            filter_options = st.multiselect("Select Order-Product columns to display", orderProductDF.columns)
            if filter_options:
                orderProductDF = orderProductDF[filter_options]
            # Allow users to query the data using a search bar
            search = st.text_input("Search Order-Product")
            if search:
                orderProductDF = orderProductDF[orderProductDF.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
                
            st.write(orderProductDF)

        # Add a horizontal line
        st.markdown("---")
        
        # Update an order product relationship
        st.subheader("Update an order-product relationship")
        intOrderIDOP = st.number_input("Enter Order ID to update", min_value=1)
        intProductIDOP = st.number_input("Enter Product ID to update", min_value=1)
            
        # Ensure the user selects which columns to update
        update_quantity_op = st.checkbox("Update Quantity")
            
        # Fields for the updates
        intQuantityOP = st.number_input("New Quantity", min_value=0) if update_quantity_op else None
            
        if st.button("Update Order-Product Relationship"):
            if intOrderIDOP == 0:
                st.warning("Please enter a valid Order ID.")
            else:
                # Check if the Order-Product relationship exists
                mycursor.execute("SELECT * FROM tblOrderProduct WHERE intOrderID = %s AND intProductID = %s", (intOrderIDOP, intProductIDOP,))
                resultOP = mycursor.fetchone()
                        
                if not resultOP:
                    st.warning("Order-Product relationship does not exist.")
                else:
                    changes = []
                            
                    if update_quantity_op and intQuantityOP is not None and intQuantityOP != resultOP[2]:
                        changes.append(f"intQuantity = {intQuantityOP}")
                            
                    if changes:
                        update_query = "UPDATE tblOrderProduct SET " + ", ".join(changes) + " WHERE intOrderID = %s AND intProductID = %s"
                        mycursor.execute(update_query, (intOrderIDOP, intProductIDOP,))
                        mydb.commit()
                        st.success("Order-Product relationship updated successfully!")
                    else:
                        st.warning("No changes made.")
        
        # Add a horizontal line
        st.markdown("---")
        
        # Delete an order product relationship
        st.subheader("Delete an order-product relationship")
        intOrderIDOP = st.number_input("Enter Order ID", min_value=1)
        intProductIDOP = st.number_input("Enter Product ID", min_value=1)
        
        if st.button("Delete Order-Product Relationship"):
            if intOrderIDOP == 0 or intProductIDOP == 0:
                st.warning("Please enter valid Order and Product IDs.")
            else:
                mycursor.execute("SELECT * FROM tblOrderProduct WHERE intOrderID = %s AND intProductID = %s", (intOrderIDOP, intProductIDOP,))
                resultOP = mycursor.fetchone()
                
                if not resultOP:
                    st.warning("Order-Product relationship does not exist.")
                else:
                    mycursor.execute("DELETE FROM tblOrderProduct WHERE intOrderID = %s AND intProductID = %s", (intOrderIDOP, intProductIDOP,))
                    mydb.commit()
                    st.success("Order-Product relationship deleted successfully!")
        else:
            st.warning("You cannot undo this action.")
        
if __name__ == '__main__':
    main()