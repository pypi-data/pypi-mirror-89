Project Description
===============

**gsheet_access** is a small wrapper around the [Google Sheet (V4)](https://developers.google.com/sheets/) to provide more convenient access to Google Sheets from Python scripts and plot the chart between two numerical columns . It contains **gsheet** method and it will take four arguments as **oauth client ID as JSON file**  .Anyone can download the credentials file from **Google Cloud Platform** , sheet id ,x-axis and y-axis in their method.

----------


Installation
-------------
This package runs under 3.5+, use *pip* to install:
> $ pip install gsheet_access

This will also install **pandas** , **matplotlib** ,***oauth2client**,**gsheet** , **numpy** as required dependencies

#### **QuickStart**

Log into the [Google Developers Console](https://console.developers.google.com/?pli=1) with the Google account whose spreadsheets you want to access. Create  a project and enable the  Sheets API (under Google Apps APIs).[Learn How to create oauth credentials](https://medium.com/better-programming/how-to-enable-pythons-access-to-google-sheets-e4264cdb545b) . Take sheet id from google sheet and required columns for plotting.

> import gsheet_access
>  gsheet_access.gsheet('1SrZfvr2ee54r7HR1jGtAE9zHIj_YUzK9ok8bdwkpqc','creds.json','average_sales','timestamp')

#### <i class="icon-pencil"></i> **SEE ALSO**

1. gspread – Google Spreadsheets Python API (more mature and featureful Python wrapper, currently using the XML-based legacy v3 API)

**LICENSE**

This package is distributed under the [MIT license](https://opensource.org/licenses/MIT)
