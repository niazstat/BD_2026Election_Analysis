from playwright.sync_api import sync_playwright
import csv
import os
import sys

app_folder = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(app_folder, "data")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("http://103.183.38.66:81/election-result/")
    page.wait_for_load_state("networkidle")
    html = page.content()
    text = page.inner_text("body")
    #with open("output.html", "w", encoding="utf-8") as f:
        #f.write(html)
    first_item = page.locator('[role="combobox"]').first
    
    first_item.click()
    page.get_by_role("option", name="কেন্দ্র ভিত্তিক ফলাফল").click()
    # Step 2: Wait for options
    text = first_item.inner_text()
    print("First item text:", text)

    # Step 1: Select second combobox
    second_item = page.locator('[role="combobox"]').nth(1)

# Step 2: Open dropdown
    second_item.click()

# Step 3: Wait for options
    page.wait_for_selector('[role="option"]')

# Step 4: Select desired option
    page.get_by_role("option", name="জাতীয় সংসদ নির্বাচন").click()
    print("Selected:", second_item.inner_text())
    
    #3rd Item
      # Step 1: Select second combobox
    third_item = page.locator('[role="combobox"]').nth(2)

# Step 2: Open dropdown
    third_item.click()

# Step 3: Wait for options
    page.wait_for_selector('[role="option"]')

# Step 4: Select desired option
    page.get_by_role("option", name="ত্রয়োদশ জাতীয় সংসদ নির্বাচন ও গণভোট ২০২৬").click()
    print("Selected:", third_item.inner_text())


     #4th Item
      # Step 1: Select second combobox
    fourth_item = page.locator('[role="combobox"]').nth(3)
    page.wait_for_load_state("networkidle")

# Step 2: Open dropdown
    fourth_item.click()

# Step 3: Wait for options
    page.wait_for_selector('[role="option"]')

# Step 4: Select desired option
    page.get_by_role("option", name="সংসদ সদস্য").click()
    print("Selected:", fourth_item.inner_text())



    #5thth Item
      # Step 1: Select second combobox
    fifth_item = page.locator('[role="combobox"]').nth(4)
    page.wait_for_load_state("networkidle")

# Step 2: Open dropdown
    fifth_item.click()
    options = page.locator('[role="option"]')
    count = options.count()

    print("Total items:", count)
    # Click again to close
    page.keyboard.press("Escape")
    seat_id = 1

    for i in range(1,count):
        data_list = []  # সব data এখানে store হবে
        print("loop started:")
        fifth_item.click()
        #print("fift Item Clicked:")
        page.wait_for_selector('[role="option"]')
        #print("role option:")
        option = options.nth(i)
        #print("ntyh i")
        option_text = option.inner_text()
        
        seat_id +=1 
        print("--", option_text)
        option.click()
        page.wait_for_load_state("networkidle")
        sixth_item = page.locator('[role="combobox"]').nth(5)
        sixth_item.click()
        page.wait_for_load_state("networkidle")
        options2 = page.locator('[role="option"]')
        count2 = options2.count()
        print("Total items2:", count2)
        page.keyboard.press("Escape")
        for j in range(1,count2):
            data_list=[]
            sixth_item.click()
            
            #print("role2 option:")
            option2 = options2.nth(j)
            #print("ntyh j")
            option_text2 = option2.inner_text()
            seat_Name=option_text2
            print("-------", option_text2)
            option2.click()
            page.get_by_role("button", name="অনুসন্ধান").click()
            page.wait_for_timeout(2000)
 
            page.wait_for_load_state("networkidle")
            pagination_links = page.locator('ul[data-slot="pagination-content"] a[data-slot="pagination-link"]')
            pagination_count = pagination_links.count()
            for k in range(pagination_count):
                btn = pagination_links.nth(k)
                pagination_text = btn.inner_text().strip()

                if pagination_text in ["Previous", "Next"]:
                    continue
                    print("Clicking pageination:", pagination_text)
                btn.click()
                print("Pagnation", pagination_text)
                page.wait_for_selector('table[data-slot="table"] tbody tr')
                page.wait_for_timeout(2000)
                rows = page.locator('table[data-slot="table"] tbody tr')
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
                    print(zilla_td,seat_td,center_no_td,center_name_td,legal_vote_td,cancel_vote_td,absent_vote_td,total_vote_td)
                    link = rows.nth(i).locator("td:nth-child(3)")
                    link.click()
                    print("Clicking row:", i + 1)
                    page.wait_for_selector('table.w-full.text-sm.text-left tbody tr')
                    modal_rows = page.locator('table.w-full.text-sm.text-left tbody tr')
                    for j in range(modal_rows.count()):
                        cols = modal_rows.nth(j).locator("td")
                        data = cols.all_inner_texts()
                        data_list.append([zilla_td,seat_id,seat_td,center_no_td,center_name_td,legal_vote_td,cancel_vote_td,absent_vote_td,total_vote_td] + data)
                        print(zilla_td,seat_td,center_no_td)
                    page.get_by_role("button", name="বন্ধ করুন").click()
                    
        

        


            page.wait_for_timeout(5000)
            file_path = os.path.join(data_folder,   f"{seat_Name}.csv")
            with open(file_path, mode="w", newline="",  encoding="utf-8-sig") as file:
                        writer = csv.writer(file)
                        # header
                        writer.writerow(["zilla_name", "seat_id","seat_name", "center_no", "center_name", "legal_vote","cancel_vote","Absent_vote","total_vote","candidate_name","symbol","candidate_vote"])
                        writer.writerows(data_list)
            print(f"CSV saved at: {file_path}")
    browser.close()