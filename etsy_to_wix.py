import pandas as pd



def etsy_to_wix(etsy_csv_path,wix_template_path,output_path = 'wix_csv_from_etsy.csv'):
    etsy_df = pd.read_csv(etsy_csv_path)
    wix_df = pd.read_csv(wix_template_path)
    
    wix_df.drop(wix_df.index, inplace=True)
    
    column_map = {x:x for x in etsy_df.columns if x in wix_df.columns }
    column_map['id'] = 'sku'
    column_map['title'] = 'name'
    main_images = etsy_df['image_link'].tolist()
    additional_images = etsy_df['additional_image_link'].tolist()
    wix_image_col = [(main_images[i]+';'+additional_images[i]).replace(',',';') if not isinstance(additional_images[i],float) else main_images[i]  for i in range(etsy_df.shape[0]) ]
    wix_df['productImageUrl'] = wix_image_col
    wix_df['fieldType'] = 'Product'
    wix_df ['handleId'] = range(etsy_df.shape[0])
    wix_df['visible'] = ['TRUE'] * len(etsy_df)
    

    for etsy_col_name,wix_col_name in column_map.items():
        wix_df[wix_col_name] = etsy_df[etsy_col_name]
    wix_df['price'] = wix_df['price'].apply(lambda x: x.split(' ')[0])
    
    too_long_names= [str(ind) for ind,x in enumerate(etsy_df.title) if len(x)>80]
    wix_df['name'] = wix_df['name'].apply(lambda x: x[:80])
    print( f"The followings titles must be shortened: {', '.join(too_long_names)}")
    
    wix_df.to_csv(output_path)
    return wix_df





if __name__ == '__main__':
    the_etsy_csv_path = r'ahueofGreekblue_facebook_catalogue.csv'
    etsy_to_wix(the_etsy_csv_path,r'Wix_Templates_Products_CSV.csv')