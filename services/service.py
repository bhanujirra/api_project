import time
from playwright.sync_api import sync_playwright
import asyncio
import sys
from fastapi import HTTPException

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def is_table_empty(table_selector) -> bool:
   
    if not table_selector.count():
        return True
    
    # Check for any visible rows in tbody (more efficient than counting all rows)
    has_rows = table_selector.locator("tbody tr").count()
    return not has_rows 

def login_to_mri(page, username, password):
    page.goto("https://ts.meeseva.telangana.gov.in/meeseva/login.htm")
    user_name = page.locator("#j_username")
    user_name.click()
    user_name.press_sequentially(username) #Enter the username
    pass_word = page.locator("#password")
    pass_word.click()
    pass_word.press_sequentially(password) #Enter the password
    button = page.get_by_role("button", name="Login")
    button.click()
    
    
    if page.locator("#msgError").is_visible():
        print("Invalid Credentials")
        raise HTTPException(status_code=401, detail=page.locator("#msgError").inner_text())
    else:
        print("Login successful!")
    return page

def auto_mri(usernam_e, passwor_d):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            permissions=["geolocation"]  # Denying geolocation permissions
        )
        page = context.new_page() #create new page
        try:
            page = login_to_mri(page, usernam_e, passwor_d) #login to mri

            page.wait_for_load_state("load", timeout=5000)
        
            page.locator("#repaeaterdata_A1_0").click() #application processing
            page.wait_for_load_state("load", timeout=5000)
            page.locator("#Repeater1_a1_1").click() #community
            page.wait_for_load_state("load", timeout=5000)
            page.locator("#cmbProblemStatus").select_option(value="14") #selecting the authority
            print("Authority selected!")
            page.locator("#btnSearch").click() #search
            print("Search button clicked!")

            page.wait_for_load_state("load", timeout=5000)
            table = page.locator("#gvCustomers")

            rows = table.locator("tbody tr").count()
            print("Number of rows in the table: " + str(rows))
            
            while not is_table_empty(table) :
                
                link_locator = table.locator("tbody tr:nth-child(1) td:nth-child(2) a")
                link_locator.click()

                page.wait_for_load_state("load", timeout=5000)
                page.wait_for_selector("#txtDateOfBirth")

                # Remove readonly attribute and clear the field
                page.evaluate("document.getElementById('txtDateOfBirth').removeAttribute('readonly')")
                page.evaluate("document.querySelector('#txtDateOfBirth').setAttribute('value', '')")
                # page.fill("#txtDateOfBirth", "")
                page.wait_for_load_state("load", timeout=5000)

                with page.expect_popup() as new_page_info:
                    page.locator("#lnlCheckList").click() #checklist 

                new_page = new_page_info.value  # Get the new page reference
                new_page.wait_for_load_state("load", timeout=5000)  # Wait for the new page to fully load

                
                new_page.locator("#ddlconduct").select_option(value = "Yes") 
                new_page.locator("#txtSanction").fill("Yes") 
                new_page.locator("#txtRecordSt").fill("Yes")
                new_page.locator("#txtMediator").fill("Yes") 
                new_page.locator("#ddlRecommVRO").select_option(value = "Recommonded") 
                new_page.locator("#txtVerificationVRO").fill("Yes") 
                new_page.locator("#txtVeriRPA").fill("Yes") 
                new_page.locator("#ddlRecommRI").select_option(value = "Recommonded")

                new_page.click("#btnSubmit")  # Submit the form
                new_page.wait_for_load_state("load", timeout=5000)  # Wait for the response
                new_page.close()  # Close the current tab
                
                page.locator("#txtMRIRemarks").fill("recommended                                                              ")
                page.click("#btnFwdDYMRO")  # Click the button using its ID
                page.wait_for_load_state("load", timeout=5000)  # Wait for submission to complete
                page.locator("#btnBack").click()  # Go back to the previous page
                page.wait_for_load_state("load", timeout= 5000)  # Wait for the page to load
            page.wait_for_timeout(50)
        except TimeoutError:
            raise HTTPException(status_code=408, detail="Request timed out")
        finally:
           browser.close()
