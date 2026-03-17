from playwright.sync_api import sync_playwright
import csv
import os
import sys

app_folder = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(app_folder, "data")
print(data_folder)



downloaded_zilla_ids = [9, 49, 17, 35, 24, 10, 42, 25, 52, 56, 8, 13, 28, 36, 45, 26, 4, 37, 44, 19,55,20,29,53,31,54,21,48,15,40,18,5,33,6,60,14,27,1,2,41,7,12,3]
not_downloaded_zilla_ids = [19]


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://103.183.38.66:81/")
     # Wait for page fully loaded
    #page.wait_for_load_state("networkidle")
    #html = page.content()
    #text = page.inner_text("body")
    #with open("output.html", "w", encoding="utf-8") as f:
        #f.write(html)
    page.wait_for_selector("#result_type")
     # Select value
    page.select_option("#result_type", value="1")
    page.select_option("#election_type_id", value="1")

     # Wait for state dropdown to update
    page.wait_for_timeout(2000)
    page.select_option("#election_id", value="178")
    page.wait_for_timeout(2000)
    page.select_option("#candidate_type_id", value="1")
    page.wait_for_timeout(2000)
    
    zilla_list = page.query_selector_all("#zilla_id option")
    seat_id = 94
    for zilla in zilla_list:

        zilla_value = zilla.get_attribute("value")
        if not zilla_value:   # যদি value না থাকে
            continue 
        if  int(zilla_value) not in not_downloaded_zilla_ids:
            continue 
        
        page.select_option("#zilla_id", value=zilla_value)
        page.wait_for_timeout(2000)
    
    
        seats = page.query_selector_all("#constituency_id option")

        

        print ('seal Values:',seats)
        for opt in seats:
            seat_value = opt.get_attribute("value")
            if not seat_value:   # যদি value না থাকে
                continue 
            # header
            data_list = []  # সব data এখানে store হবে
            seat_Name = opt.inner_text().strip()
            seat_id +=1 
            page.select_option("#constituency_id", value=seat_value)
            # Click the button
            page.click(".btn.btn-outline-info")
            page.wait_for_timeout(2000)
            pagination = page.locator("#data-table_paginate ul.pagination li a")
            pagination_count = pagination.count()
            for i in range(pagination_count):
                btn = pagination.nth(i)
                pagination_text = btn.inner_text().strip()
                # skip Previous and Next
                if pagination_text in ["Previous", "Next"]:
                    continue
                    print("Clicking pageination:", pagination_text)
                btn.click()


                page.wait_for_selector("#data-table tbody tr")
                page.wait_for_timeout(2000)
                rows = page.locator("#data-table tbody tr")
                row_count = rows.count()

                for i in range(row_count):
                    #cols = rows.nth(i).locator("td")
                    #data = cols.all_inner_texts()
                    zilla_td = rows.nth(i).locator("td:nth-child(1)").inner_text()
                    seat_td = rows.nth(i).locator("td:nth-child(2)").inner_text()
                    center_no_td = rows.nth(i).locator("td:nth-child(3)").inner_text()
                    center_name_td = rows.nth(i).locator("td:nth-child(4)").inner_text()
                    legal_vote_td = rows.nth(i).locator("td:nth-child(5)").inner_text()
                    cancel_vote_td = rows.nth(i).locator("td:nth-child(6)").inner_text()
                    absent_vote_td = rows.nth(i).locator("td:nth-child(7)").inner_text()
                    total_vote_td = rows.nth(i).locator("td:nth-child(8)").inner_text()

                    link = rows.nth(i).locator("td:nth-child(3) a")
                    link.click()
                    print("Clicking row:", i + 1)
                    # Wait for modal to appear
                
                    page.wait_for_selector("#centerResultModal.modal.show")
                    #page.wait_for_timeout(2000)
                    modal_rows = page.locator("#centerResultModal table tbody tr")
                    #tbody = page.locator("#centerResultModal")

                    
                    for j in range(modal_rows.count()):
                        cols = modal_rows.nth(j).locator("td")
                        data = cols.all_inner_texts()
                        data_list.append([zilla_td,seat_id,seat_td,center_no_td,center_name_td,legal_vote_td,cancel_vote_td,absent_vote_td,total_vote_td] + data)
                        print(zilla_td,seat_td,center_no_td)

                    # Close modal (if close button exists)
                    # Click close button inside modal footer
                    page.locator(".modal-footer .btn.btn-secondary").click()    

                    # Wait for modal to disappear
                    
                    page.wait_for_selector("#centerResultModal", state="hidden")
            file_path = os.path.join(data_folder,   f"{seat_Name}.csv")
            with open(file_path, mode="w", newline="",  encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                # header
                writer.writerow(["zilla_name", "seat_id","seat_name", "center_no", "center_name", "legal_vote","cancel_vote","Absent_vote","total_vote","candidate_name","symbol","candidate_vote"])
                writer.writerows(data_list)
            print(f"CSV saved at: {file_path}")
         
    browser.close()
   

