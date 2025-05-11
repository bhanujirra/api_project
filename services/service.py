from playwright.sync_api import sync_playwright



def auto_mri(usernam_e, passwor_d):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            permissions=["geolocation"]  # Denying geolocation permissions
        )

        page = context.new_page()

        page.goto("https://ts.meeseva.telangana.gov.in/meeseva/login.htm")
        page.wait_for_load_state("load")
        
        user_name = page.locator("#j_username")
        user_name.click()
        user_name.press_sequentially(usernam_e) #Enter the username
        pass_word = page.locator("#password")
        pass_word.click()
        pass_word.press_sequentially(passwor_d) #Enter the password
        button = page.get_by_role("button", name="Login")
        button.click()

        page.wait_for_load_state("load")
        page.locator("xpath= //*[@id='repaeaterdata_A1_0']").click() #application processing
        page.locator("xpath= //*[@id='Repeater1_a1_1']").click() #community
        page.locator("xpath=//*[@id='cmbProblemStatus']").select_option(value="14") #selecting the authority
        page.locator("xpath = //*[@id='btnSearch']").click() #search

        table = page.locator("//html/body/form/main/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/table") 
        rows = table.locator("tbody tr").count()
        i = 1
        while rows != 0:
            
            link_locator = table.locator("tbody tr:nth-child(1) td:nth-child(2) a")
            link_locator.click()
            page.wait_for_load_state("load")
            
            page.wait_for_selector("#txtDateOfBirth")

            # Remove readonly attribute and clear the field
            page.evaluate("document.getElementById('txtDateOfBirth').removeAttribute('readonly')")
            page.evaluate("document.querySelector('#txtDateOfBirth').setAttribute('value', '')")
            # page.fill("#txtDateOfBirth", "")
            page.wait_for_load_state("load")
            print("Date of Birth field cleared!" + str(i))
            i += 1
            with page.expect_popup() as new_page_info:
                page.locator("xpath = //*[@id='lnlCheckList']").click() #checklist 

            new_page = new_page_info.value  # Get the new page reference
            new_page.wait_for_load_state("load")  # Wait for the new page to fully load

            
            new_page.locator("xpath = //*[@id='ddlconduct']").select_option(value = "Yes") 
            new_page.locator("xpath = //*[@id='txtSanction']").fill("Yes") 
            new_page.locator("xpath = //*[@id='txtRecordSt']").fill("Yes")
            new_page.locator("xpath = //*[@id='txtMediator']").fill("Yes") 
            new_page.locator("xpath = //*[@id='ddlRecommVRO']").select_option(value = "Recommonded") 
            new_page.locator("xpath = //*[@id='txtVerificationVRO']").fill("Yes") 
            new_page.locator("xpath = //*[@id='txtVeriRPA']").fill("Yes") 
            new_page.locator("xpath = //*[@id='ddlRecommRI']").select_option(value = "Recommonded")

            new_page.click("#btnSubmit")  # Submit the form
            new_page.wait_for_load_state("load")  # Wait for the response
            new_page.close()  # Close the current tab
            
            page.locator("xpath = //*[@id='txtMRIRemarks']").fill("recommended                                                              ")
            page.click("#btnFwdDYMRO")  # Click the button using its ID
            page.wait_for_load_state("load")  # Wait for submission to complete
            page.locator("xpath = //*[@id='btnBack']").click()  # Go back to the previous page
            page.wait_for_load_state("load")  # Wait for the page to load
            rows = table.locator("tbody tr").count()
        page.wait_for_timeout(1000)
        browser.close()
