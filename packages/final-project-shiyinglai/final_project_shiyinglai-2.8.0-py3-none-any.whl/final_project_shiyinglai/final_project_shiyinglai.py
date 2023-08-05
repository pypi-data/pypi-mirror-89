import pandas as pd
import urllib3
import json
import requests
from PIL import Image
from io import BytesIO
import matplotlib. pyplot as plt
from datetime import date


def search_artwork_by_culture(apikey,culture,page):
    """
    Search Artwork by culture from the The Harvard Museum API based on query parameters.
    
    Parameters
    ----------
    apikey : String
           your API key for The Harvard Museum API
    culture : String
            The culture you want to look up.ex."Chinese"
    page : String
         This API could only return 100 records per request ar maxium. One request is counted as 1 page.
         if you want to see more records. Enter the number of Page. ex. "2" or "3"  
         Note: only integer in string format.Please enter "1" at the first time.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        A dataframe that contains the 'id',"title",'objectnumber','century','worktypes','culture','technique','medium','description',
        'classificationid','colorcount' based on thee query_parameter you entered.
           
    Examples
    --------
    >>>import pandas as pd 
    >>>import json
    >>>import urllib3
    >>>search_artwork_by_culture(apikey="your api key",culture="Chinese",page="1")
    >>> A dataframe
    """
    try:
        try:
 # request data
            http = urllib3.PoolManager()
            r = http.request('GET', 'https://api.harvardartmuseums.org/object',
            fields = {
                'apikey':apikey ,
                "size":"100",
                "culture":culture,
                "page":page
                })
        except HTTPError as error:
            print(f'HTTP error occurred: {error}')
        except Exception as other_error:
            print(f'Other error occurred: {other_error}')
        else:
             print('The request successes!')
        record = json.loads(r.data)
#generate dataframe
        df = pd.DataFrame(record["records"])
        final_df=df[['id',"title",'objectnumber','century','worktypes','culture','technique','medium','description','classificationid','colorcount']]
        return final_df
    except:
        print("Sorry! No result! Please enter strings for all parameters. Or Enter another culture.")

def function_search_for_artworks(title,vague_search,apikey):
    """
    Search Artwork by title from the The Harvard Museum API based on query parameters.
    
    Parameters
    ----------
    apikey : String
           your API key for The Harvard Museum API
    title : String
          The title of the artwork you want to look up.ex."Pouring Vessel"
    vague_search : Boolean
                 True: return all the artwork contains the title 
                 False:return one artwork has that exactly title
                 Note: When you enter False, and your title is not exactly the same as the havard museum provide.
                 You will receive nothing.           
    Returns
    -------
    pandas.core.frame.DataFrame
         A dataframe that contains some information about the artwork based on the title you entered.
           
    Examples
    --------
    >>>import pandas as pd 
    >>>import json
    >>>import urllib3
    >>>function_search_for_artworks(title="Pouring Vessel", vague_search=True,apikey="your api key")
    >>> A dataframe contains many records
    >>>function_search_for_artworks(title="Pouring Vessel", vague_search=False,apikey="your api key")
    >>> A dataframe contains one record  
    """
    try:
        final_result=[]
        all_df=[]
    # I can only get 100 records per requests at maxium, a request is counted as a page.
    #Thus, the first request serves to check how many requests I need to get full records. 
        try:
            http = urllib3.PoolManager()
            r = http.request('GET', 'https://api.harvardartmuseums.org/object',
            fields = {
                'apikey':apikey,
                "title":title,
                "size":"100",
                })
        except HTTPError as error:
            print(f'HTTP error occurred: {error}')
        except Exception as other_error:
            print(f'Other error occurred: {other_error}')
        else:
             print('The request successes!')
        object = json.loads(r.data) 
        info = pd.DataFrame(object["info"],index=[0])
# pages indicates the number of requests I need to get full record. Thus, I need to get total pages first.
        total_pages=int(info['pages'])
    #Use for loop to get all records
        for i in range(1,total_pages+1):
            r2 = http.request('GET', 'https://api.harvardartmuseums.org/object',
            fields = {
                'apikey':apikey,
                "size":"100",
                "page":str(i),
                "title":title,
                })
            print(str(i),end='')
            record = json.loads(r2.data)
            final_result.append(record)
            df = pd.DataFrame(final_result)
            #extract the actual content of full records
        for p in range(0,total_pages):
            df_1=pd.DataFrame(df["records"].iloc[p])
# Choose the columns I needed
            all_df.append(df_1[['id',"title",'objectnumber','century','worktypes','culture','technique','medium','description','classificationid','colorcount']])
# Combine all the dfs I get
        finalqueryresult = pd.concat(all_df, ignore_index=True)
        if vague_search==True:
            all_items=finalqueryresult[finalqueryresult.apply(lambda row: row.astype(str).str.contains(title).any(), axis=1)]
            return all_items
        if vague_search==False:   
            exact_searching_result=finalqueryresult[finalqueryresult['title']==title]
            exact_searching_result_df=exact_searching_result.drop_duplicates(subset=['id', 'title'], keep=False)
            return exact_searching_result_df
    except:
        print("Please enter strings for all parameters! Or try another title. :D")


def search_for_images_by_width(width,apikey, page):
    """
    Search images by width from the The Harvard Museum API based on query parameters.
    
    Parameters
    ----------
    apikey : String
           your API key for The Harvard Museum API
    width : String
          The width of the image. ex.">1000"
    page : String 
         This funtion could only return 10 records per request. One request is counted as 1 page.
         if you want to see more records. Enter the number of Page. ex. "2" or "3"  
         Note: only integer in string format.Please enter "1" at the first time.
     
    Returns
    -------
    matplotlib.image.AxesImage
        10 images 
           
    Examples
    --------
    >>>import pandas as pd 
    >>>import json
    >>>import urllib3
    >>>import requests
    >>>from PIL import Image
    >>>from io import BytesIO
    >>>import matplotlib. pyplot as plt 
    >>>search_for_images_by_size(width=">1000",apikey="your api key")
    >>> An matplotlib.image.AxesImage
    """
    try:
        try:
# request images by width
            http = urllib3.PoolManager()
            r = http.request('GET', 'https://api.harvardartmuseums.org/image',
                fields = {
                    'apikey':apikey ,
                    "size":"10",
                    "width":width,
                    "page":page
            })
        except HTTPError as error:
            print(f'HTTP error occurred: {error}')
        except Exception as other_error:
            print(f'Other error occurred: {other_error}')
        else:
             print('The request successes!')
        data = json.loads(r.data)
        pd.set_option('display.max_colwidth', None)
        df = pd.DataFrame(data["records"])
        urls=df['baseimageurl']
        all=[]
#collect all images' urls from the response
        for u in urls:
#read the images' urls into real image
                response = requests.get(str(u))
                img=Image.open(BytesIO(response.content))
                all.append(img)
  
        plt.figure(figsize=(20,10))
        columns = 5
        for i, image in enumerate(all):
            try:
                plt.subplot(len(all) / columns + 1, columns, i + 1)
                plt.imshow(image)
            except:
                continue
    except:
        print("No result. Please enter string for all parameters. Or try other size. :D")
        
def search_for_images_by_height(height,apikey, page):
    """
    Search images by size from the The Harvard Museum API based on query parameters.
    
    Parameters
    ----------
    apikey : String
           your API key for The Harvard Museum API
    height : String
           The height of the image. ex. ">400"
    page : String 
         This funtion could only return 10 records per request. One request is counted as 1 page.
         if you want to see more records. Enter the number of Page. ex. "2" or "3"  
         Note: only integer in string format.Please enter "1" at the first time.
     
    Returns
    -------
    matplotlib.image.AxesImage
        10 images 
           
    Examples
    --------
    >>>import pandas as pd 
    >>>import json
    >>>import urllib3
    >>>import requests
    >>>from PIL import Image
    >>>from io import BytesIO
    >>>import matplotlib. pyplot as plt 
    >>>search_for_images_by_size(height=">400",apikey="your api key")
    >>> An matplotlib.image.AxesImage
    """
    try:
        try:
# request images by width and height
            http = urllib3.PoolManager()
            r = http.request('GET', 'https://api.harvardartmuseums.org/image',
                fields = {
                    'apikey':apikey ,
                    "size":"10",
                    "Height":height,
                    "page":page
            })
        except HTTPError as error:
            print(f'HTTP error occurred: {error}')
        except Exception as other_error:
            print(f'Other error occurred: {other_error}')
        else:
             print('The request successes!')
        data = json.loads(r.data)
        pd.set_option('display.max_colwidth', None)
        df = pd.DataFrame(data["records"])
        urls=df['baseimageurl']
        all=[]
#collect all images' urls from the response
        for u in urls:
#read the images' urls into real image
                response = requests.get(str(u))
                img=Image.open(BytesIO(response.content))
                all.append(img)
  
        plt.figure(figsize=(20,10))
        columns = 5
        for i, image in enumerate(all):
            try:
                plt.subplot(len(all) / columns + 1, columns, i + 1)
                plt.imshow(image)
            except:
                continue
    except:
        print("No result. Please enter string for all parameters. Or try other size. :D")
        
def exhibition_explorer(apikey,exhibition):
    """
    Get the information of artwork for a particualr exhibition in the Harvard Museum from the The Harvard Museum API based on query parameters.
    
    Parameters
    ----------
    apikey : String
           your API key for The Harvard Museum API
    exhibition : String
               The exact name of exhibition that showed in the Harvard Museum website.
    Returns
    -------
    pandas.core.frame.DataFrame
         A dataframe that contains the information about artworks appearing in that exhibition.
           
    Examples
    --------
    >>>import pandas as pd 
    >>>import json
    >>>import urllib3
    >>>exhibition_explorer(apikey="your api key",exhibition="Botticelli's Witness:  Changing Style in a Changing Florence")
    >>> A dataframe
    """
# Send the first request to get the exhibition id for the exhibitions
    http = urllib3.PoolManager()
    try:
        try:
            r = http.request('GET', 'https://api.harvardartmuseums.org/exhibition',
                fields = {
                'apikey': apikey,
                'exact_title':exhibition
                 })
        except HTTPError as error:
            print(f'HTTP error occurred: {error}')
        except Exception as other_error:
            print(f'Other error occurred: {other_error}')
        else:
             print('The request successes!')            
        data = json.loads(r.data)
        pd.set_option('display.max_colwidth', None)
        df = pd.DataFrame(data["records"])
        exhibitionid=int(df['exhibitionid'])
#Use the exhibition id  to send the second request to get all the artwork in that exhibition. 
        r1 = http.request('GET', 'https://api.harvardartmuseums.org/object',
            fields = {
            'apikey': '544ea1bf-7cd9-4c94-96a7-9a4d4057c91a',
            "size":"10",
            "exhibition":str(exhibitionid)
             })
        data1 = json.loads(r1.data)
        df_for_pieces = pd.DataFrame(data1["records"])
        final_df=df_for_pieces[['id',"title",'objectnumber','century','worktypes','culture','technique','medium','description','classificationid','colorcount','colors','primaryimageurl']]
        return final_df
    except:
        print("Please check your input, they have to be strings, and exhibition has to be exactly the same with the Harvard Museum Website.")

def artwork_for_today(apikey):
    """
    Request an image of artwork that enter the Harvard Museum at today in history.
    
    Parameters
    ----------
    apikey : String
           your API key for The Harvard Museum API
    Returns
    -------
    PIL.JpegImagePlugin.JpegImageFile
         an image
              
    Examples
    --------
    >>>from io import BytesIO
    >>>from datetime import date
    >>>import urllib3
    >>>import json
    >>>import pandas as pd
    >>>import matplotlib. pyplot as plt
    >>>artwork_for_today(apikey="your api key")
    >>> An Image
    """
#Read today's time
    today = date.today()
    print(f'Hi~ Today is {today}')
    print("Start to prepare artwork for you! Good Luck")
    today_month_day=str(today)[5:]
    final_result=[]
    all_df=[]
    try:
        http = urllib3.PoolManager()
        for i in range(1,30):
#Get 3000 images for further selection
            r1 = http.request('GET', 'https://api.harvardartmuseums.org/image',
                fields = {
                    'apikey': apikey,
                    "size":"100",
                    "page":str(i)
                })
            print(str(i),end='')
            data1 = json.loads(r1.data)
            final_result.append(data1)
            df1 = pd.DataFrame(final_result)
        for p in range(0,29):
            df_1=pd.DataFrame(df1["records"][p])
#Selection information on imageurl and dates
            all_df.append(df_1[['id',"date","baseimageurl","description"]])
            finalqueryresult = pd.concat(all_df, ignore_index=True)
        finalqueryresult['date'] = pd.to_datetime(finalqueryresult.date)
        finalqueryresult['new_date'] = finalqueryresult['date'].dt.strftime('%m-%d')
#Match the computer's time and artwork's date
        new_date=finalqueryresult[finalqueryresult['new_date']==today_month_day]
        #I just need it to display one photo for a particular date
        urls=new_date['baseimageurl'].iloc[0]
        response = requests.get(urls)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        print("Sorry! No artwork enter Harvard Museum at today in the history~ Try Tomrrow Please~ : D")

def trendplot_for_particular_artwork_type(artwork_type, apikey):
    """
    Gnerate a trend plot for the number of certain artwoork type during 10th -20th century's .
    
    Parameters
    ----------
    apikey : String
           your API key for The Harvard Museum API
    artwork_type : String
                 The artwork type you want to generate trend plot. ex."sculpture"
      
    Returns
    -------
    A bar plot
          A trend plot for 10th -20th century.
              
    Examples
    --------
    >>>import urllib3
    >>>import json
    >>>import pandas as pd
    >>>import matplotlib. pyplot as plt
    >>>trendplot_for_particular_artwork_type(artwork_type="sculpture", apikey="your api key")
    >>> An trend plot
    """
#Send the first request to check how many pages I need to get all results
    try:
        http = urllib3.PoolManager()
        final_result=[]
        all_df=[]
        try:
            r = http.request('GET', 'https://api.harvardartmuseums.org/object',
                fields = {
                    'apikey': apikey,
                    "size":"100",
                    "worktype":str(artwork_type)
                })
        except HTTPError as error:
            print(f'HTTP error occurred: {error}')
        except Exception as other_error:
            print(f'Other error occurred: {other_error}')
        else:
             print('The request successes!')
        data = json.loads(r.data)
        info = pd.DataFrame(data["info"],index=[0])
        total_pages=int(info['pages'])
# Use the number of total pages to get all the results
        for i in range(1,total_pages+1):
            r1 = http.request('GET', 'https://api.harvardartmuseums.org/object',
                fields = {
                    'apikey': apikey,
                    "size":"100",
                    "worktype":str(artwork_type),
                    "page":str(i)
                })
            print(str(i),end='')
            data1 = json.loads(r1.data)
            final_result.append(data1)
            df1 = pd.DataFrame(final_result)
        for p in range(0,total_pages):
            df_1=pd.DataFrame(df1["records"][p])
            all_df.append(df_1[['id',"title",'objectnumber',"century"]])
            finalqueryresult = pd.concat(all_df, ignore_index=True)
#Find all BCE first:Before the century, since there are confusing.
        finalqueryresult['patterns'] = finalqueryresult['century'].str.findall(r'BCE')
        finalqueryresult['patterns_string']=finalqueryresult['patterns'].astype(str)
#Create another dataframe exclude BCE
        df_without_bce=finalqueryresult[finalqueryresult['patterns_string']!="['BCE']"]
#Count the number of artwork for each century
        tenth=len(df_without_bce[df_without_bce.apply(lambda row: row.astype(str).str.contains("10th").any(), axis=1)])
        eleventh=len(df_without_bce[df_without_bce.apply(lambda row: row.astype(str).str.contains("11th").any(), axis=1)])
        twelfth=len(df_without_bce[df_without_bce.apply(lambda row: row.astype(str).str.contains("12th").any(), axis=1)])
        thirteenth=len(df_without_bce[df_without_bce.apply(lambda row: row.astype(str).str.contains("13th").any(), axis=1)])
        fourteenth=len(df_without_bce[df_without_bce.apply(lambda row: row.astype(str).str.contains("14th").any(), axis=1)])
        fifteenth=len(df_without_bce[df_without_bce.apply(lambda row: row.astype(str).str.contains("15th").any(), axis=1)])
        sixteenth=len(df_without_bce[df_without_bce.apply(lambda row: row.astype(str).str.contains("16th").any(), axis=1)])
        seventeenth=len(df_without_bce[df_without_bce.apply(lambda row: row.astype(str).str.contains("17th").any(), axis=1)])
        eighteenth=len(df_without_bce[df_without_bce.apply(lambda row: row.astype(str).str.contains("18th").any(), axis=1)])
        nineteenth=len(df_without_bce[df_without_bce.apply(lambda row: row.astype(str).str.contains("19th").any(), axis=1)])
        twentieth=len(df_without_bce[df_without_bce.apply(lambda row: row.astype(str).str.contains("20th").any(), axis=1)])
#Generating trend plot
        x=["10th","11th","12th","13th","14th","15th","16th","17th","18th","19th","20th"]
        height = [tenth,eleventh,twelfth,thirteenth,fourteenth,fifteenth,sixteenth,seventeenth,eighteenth,nineteenth,twentieth]
        plt.bar(x, height, color="orange", width=0.4)
        plt.xlabel("Century")
        plt.ylabel("Number of Artworks")
    # add the number of cases on the top of each bars
        x_position=[1,2,3,4,5,6,7,8,9,10,11]
        for i in range(11):
            plt.text(x = x_position[i]-1.2, y = height[i]+1, s = height[i])
        plt.show()
    except:
        print("Sorry! No result! Please enter strings for all Parameters! Or please try another artwork type. :D")


    


        

    
