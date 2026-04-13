---
author: Zulfikar Akbar Muzakki
date: '2022-03-30'
description: Openpyxl is a Python library used for manipulating Excel files. I came
  across a work that needs to export data to XLSX format, and I used Op
erpnext_id: /blog/python/reading-and-writing-xlsx-file-with-openpyxl
erpnext_modified: '2022-03-30'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Python
thumbnail: /img/blog/placeholder.png
title: Reading and Writing XLSX File with Openpyxl
---

Openpyxl is a Python library used for manipulating Excel files. I came across a ticket that needs to export data ti XLSX format, and I used Openpyxl for that as it’s pretty straightforward.

  


# Reading XLSX File

Reading XLSX file is simple. First, we load the file into a Workbook object and choose the sheets. If the file contains only one sheet, we can use .active to get the sheet. Active will return active sheet, and in the case when there’s only 1 sheet, that sheet will always be active.
    
    
    from openpyxl import load_workbook
    
      
    
    
    wb = load_workbook(filename = 'empty_book.xlsx')
    
    sheet = book.active

  


We can get cell value by entering cell coordinate, which will be useful when we need specific cell value.
    
    
    print(sheet['D18'].value)

or by looping the row, which can be used when we import a data.
    
    
    # min_row indicate the minimum row index that will be processed (1-based)
    
    # min_col indicate the minimum column index that will be processed (1-based)
    
    for row in sheet.iter_rows(min_row=2, min_col=1):
    
    	print(row[2].value, row[3].value, row[4].value)

  


On this example, I only print the cell value but in real case, we can literally do anything with those data. 

  


# Write to XLSX File

Writing to XLSX File is an easy feat with Openpyxl. We need to first create a workbook object before finally saving it to desired destination. This example creates workbook containing 2 worksheets.
    
    
    from openpyxl import Workbook
    
      
    
    
    def export_excel():
    
        wb = Workbook()
    
        dest_filename = 'empty_book.xlsx'
    
        
    
        # Get first sheet
    
        ws1 = wb.active
    
        ws1.title = "Range"
    
        
    
        # Write data to cell
    
        for row in range(1, 40):
    
            # append() will append iterables, which will assign each element to each cell.
    
        	ws1.append(range(10))
    
        
    
        # Create second sheet
    
        ws2 = wb.create_sheet(title="Phi")
    
        ws2['F5'] = 3.14
    
        
    
        
    
        ws3 = wb.create_sheet(title="Data")
    
        for row in range(10, 20):
    
            for col in range(27, 54):
    
                # Fill the cell with the column letter
    
                ws3.cell(column=col, row=row, value="{0}".format(get_column_letter(col)))
    
        
    
        # Save the workbook
    
        wb.save(filename=dest_filename)

  


We must call save() at the end to finally export the workbook, otherwise the workbook will exist only as an object.

Those are simple example to write XLSX to file. For more complex formatting such as style, you can read the detailed documentation here: [https://openpyxl.readthedocs.io/en/stable/index.html](<https://openpyxl.readthedocs.io/en/stable/index.html>)

  


# Returning XLSX File in Django

It's more than often that what we want to achieve in our Django app is not simply saving the XLSX file, but to return it the as a request’s reponse. The way of creating workbook object is basically the same, but now we save it to response object. We'll use the previous code to write XLSX file with some updates.

  


First, add this import.
    
    
    from django.http import HttpResponse

  


In previous code, we save the workbook to a file. Now, we will save it to a response object. We must explicitly set the content type of the response, which is application/vnd.openxmlformats-officedocument.spreadsheetml.sheet. Please note that the value is predefined, so for XLSX file the content type will always be the same and you cannot change it. Using different content type might make the browser to falsely think it as different media type. We also need to set the content disposition to attachment to make the response be downloaded instead of displayed on the browser, and provide the filename for the file.

  


Now, replace wb.save(filename=dest_filename) this code and remove dest_filename = 'empty_book.xlsx' as we won't need it anymore.
    
    
    # Set the content type of XLSX file 
    
    response = HttpResponse(
    
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    
    )
    
    # Set the content disposition as attachment and provide the filename
    
    response['Content-Disposition'] = 'attachment; filename=export.xlsx

  


And finally, save the workbook to the response object and return it with
    
    
    workbook.save(response)
    
    return response

  


So now, our code looks like this
    
    
    from django.http import HttpResponse
    
    from openpyxl import Workbook
    
      
    
    
      
    
    
    def export_excel():
    
        wb = Workbook()
    
        
    
        # Get first sheet
    
        ws1 = wb.active
    
        ws1.title = "Range"
    
        
    
        # Write data to cell
    
        for row in range(1, 40):
    
            # append() will append iterables, which will assign each element to each cell.
    
        	ws1.append(range(10))
    
        
    
        # Create second sheet
    
        ws2 = wb.create_sheet(title="Phi")
    
        ws2['F5'] = 3.14
    
        
    
        
    
        ws3 = wb.create_sheet(title="Data")
    
        for row in range(10, 20):
    
            for col in range(27, 54):
    
                # Fill the cell with the column letter
    
                ws3.cell(column=col, row=row, value="{0}".format(get_column_letter(col)))
    
        
    
        # Save the workbook
    
        response = HttpResponse(
    
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    
        )
    
        # Set the content disposition as attachment and provide the filename
    
        response['Content-Disposition'] = 'attachment; filename=export.xlsx
    
        workbook.save(response)
    
        return response

  


# Conclusion

Using Openpyxl to read and write XLSX file is pretty easy, and will basically cover most of our requirements. Now, you can try to read and write simple XLSX then move on to read and write XLSX with more complex formatting.
