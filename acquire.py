import requests
import pandas as pd

def get_items():
    # Creating base_url
    base_url = 'https://python.zgulde.net'
    # response is holding json returned from calling /api/v1/items
    response = requests.get(base_url + '/api/v1/items')
    # Saving the returned json information to variable data
    data = response.json()# ALL of items including the payload
    # Saving our data into dataframe
    df = pd.DataFrame(data['payload']['items'])
    
    # to add the 2nd page 
    response = requests.get(base_url + data['payload']['next_page'])
    # 2nd page and in a json format
    data = response.json()
    # here I am make a df out of the 2nd page column payload items list
    df_item_page2 = pd.DataFrame(data['payload']['items'])
    # index so it is continuous
    df = pd.concat([df, df_item_page2]).reset_index()
    
    # Here new response is getting third page
    response = requests.get(base_url + data['payload']['next_page'])
    # save the response in json format as the variable data
    data = response.json()
    # here I set the df to concatenate the existing df(page 1 and 2) with the new       variable
    # equal to the 3rd page and list the from payload the items, and then reset the     index
    # so it is continuous
    df = pd.concat([df, pd.DataFrame(data['payload']['items'])]).reset_index()
    return df

def get_stores():
    # Creating base_url
    base_url = 'https://python.zgulde.net'
    # response is holding json returned from calling /api/v1/stores
    response = requests.get(base_url + '/api/v1/stores')
    response.json()['payload']
    # Saving the returned json information to variable data
    data = response.json()# ALL of stores including the payload
    # Saving our data into dataframe
    df = pd.DataFrame(data['payload']['stores'])
    return df

def get_sales():
    base_url = 'https://python.zgulde.net'
    # response is holding json returned from calling /api/v1/items
    response = requests.get(base_url + '/api/v1/sales')
    # Saving the returned json information to variable data
    data = response.json()# ALL of items including the payload
    # Saving total pages to maxpage
    maxpage = data['payload']['max_page']
    # Saving our data into dataframe and creating the first page
    df_sales = pd.DataFrame(data['payload']['sales'])
    # Creating a loop from page 2 to maxpage + 1.  I did +1 because range's last         value is not included
    for page_num in range(2, data['payload']['max_page'] + 1):
        url = "https://python.zgulde.net/api/v1/sales?page=" + str(page_num)
        sales_data = requests.get(url).json()['payload']['sales']
        df_sales = pd.concat([df_sales, pd.DataFrame(sales_data)])
    return df_sales

def get_everything():
    df_items = get_items()
    df_stores = get_stores()
    df_sales = get_sales()
    #merge all three on foreign keys
    sales_plus_stores = pd.merge(
    df_sales,
    df_stores,
    how='left',
    left_on='store',
    right_on='store_id')
    everything = pd.merge(
    sales_plus_stores,
    df_items,
    how='left',
    left_on='item',
    right_on='item_id')
    return everything

