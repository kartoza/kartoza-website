---
title: "Reading and Writing XLSX File with Openpyxl"
description: "The piece introduces Openpyxl as a Python library used for manipulating Excel files."
tags:
  - Python
  - Excel
date: 2022-03-30
author: "Zulfikar Akbar Muzakki"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Reading and Writing XLSX File with Openpyxl"
    subtitle="Python"
    class="is-primary"
    sub-block-side="bottom"
>}}
The piece introduces Openpyxl as a Python library used for manipulating Excel files.
{{< /block >}}

## Introduction

The piece introduces Openpyxl as "a Python library used for manipulating Excel files." The author describes encountering a project requiring data export to XLSX format and selected this library for its straightforward implementation.

## Reading XLSX Files

To load an Excel file, developers instantiate a Workbook object:

```python
from openpyxl import load_workbook
wb = load_workbook(filename = 'empty_book.xlsx')
sheet = book.active
```

Cell values retrieve via coordinate reference: `sheet['D18'].value`

For batch processing, iteration works effectively:

```python
for row in sheet.iter_rows(min_row=2, min_col=1):
    print(row[2].value, row[3].value, row[4].value)
```

## Writing to XLSX Files

File creation requires instantiating a Workbook object before saving:

```python
from openpyxl import Workbook
wb = Workbook()
ws1 = wb.active
ws1.title = "Range"
```

The `append()` function assigns iterables to sequential cells. Additional sheets use `create_sheet()`. Files save via `wb.save(filename=dest_filename)`.

## Django Integration

For web applications, save workbooks to response objects rather than disk. Set the content type to `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` and configure content disposition as attachment:

```python
response = HttpResponse(
    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
)
response['Content-Disposition'] = 'attachment; filename=export.xlsx'
workbook.save(response)
return response
```

## Conclusion

The tutorial emphasizes that Openpyxl covers most standard requirements. Users should progress from basic read/write operations toward advanced formatting techniques via official documentation.
