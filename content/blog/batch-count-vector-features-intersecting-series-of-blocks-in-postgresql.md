---
author: Admire Nyakudya
date: '2019-06-13'
description: The national mapping agency in South Africa (NGI ) caters for national
  mapping, digital topographic and other Geo-Spatial Information servic
erpnext_id: /blog/database/batch-count-vector-features-intersecting-series-of-blocks-in-postgresql
erpnext_modified: '2019-06-13'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Database
thumbnail: /img/blog/erpnext/index.png
title: Batch Count Vector Features Intersecting Series of Blocks in PostgreSQL
---

The national mapping agency in South Africa ([NGI](<http://www.ngi.gov.za> "NGI") ) caters for national mapping, digital topographic and other Geo-Spatial Information services. The department is mandated to provide spatial data for the whole country. In most cases, they have an in-house team that is responsible for digitizing aerial photography, field validation to produce vector data that is used to make 1:50 000 topographic maps.

The department has recently floated a tender in which they encourage service providers to participate in the mapping exercise for some other parts of the country. The department is mandated to update all the spatial data on a 5-year cycle. As an interested party, I set out to find how much work would be involved in mapping these areas based on data available for these areas.

The current coverage of areas that need to be mapped is:

![Image](/img/blog/erpnext/index.png)

I extracted all the sheets numbers from the supplied bid documents and created a text file which I then loaded into QGIS. I then imported this layer into a PostgreSQL database and called it **sample.**

I then proceeded to run the following SQL:

`CREATE TABLE ngi_work AS`

`SELECT b.id,b.sheet_number,b.sheet_name, b.geom FROM`

`"index1in50k" as b JOIN sample as a ON`

`b.sheet_number = a.name;`

The SQL above created a spatial layer indicating all blocks that needed to be captured.

In my database, I had already loaded the spatial layers I had acquired the previous year into a schema called ngi _**.**_ The schema contained about 40 odd layers. I set out to find the number of features from each layer in the schema ngi intersecting each block specified in the table ngi_work.

I wrote the resulting SQL to test how many features intersected a block.

            WITH clipping_test AS
                (SELECT
                ST_Multi(ST_Intersection(st_transform(v.wkb_geometry,4326),m.geom)) AS intersection_geom,
                v.*
                FROM
                  ngi.phys_landform_natural_exp_areal as v,
                 (select sheet_number,st_union(geom) as geom from ngi_work where sheet_number = '2328BD' group by sheet_number) 
                 as m
                WHERE
                  ST_Intersects(st_transform(v.wkb_geometry,4326), m.geom))
                (SELECT count(*) FROM clipping_test WHERE ST_Geometrytype(intersection_geom)='ST_MultiPolygon')

After running the SQL I figured out that it could run it successfully and now I had to script the whole procedure so that it could run for all the blocks and for all the layers that are in the schema **ngi.**

The full script to do this is attached below.

    import psycopg2  
    import sys  
    import csv  
      
      
    def main():  
        # Define our connection string  
        try:  
            connection = psycopg2.connect(host='localhost', database='foo', user='fool', password='foobar',  
                                          port=5432)  
        except psycopg2.OperationalError as e:  
            print(e)  
            sys.exit(1)  
      
        cursor = connection.cursor()  
      
        # SQL to query the ngi_work  table getting all sheets to be used  
        check_value = """ select sheet_number from ngi_work """  
        cursor.execute(check_value)  
        valid_sheets = cursor.fetchall()  
        for sheet in valid_sheets:  
            index_block = sheet[0]  
            cursor = connection.cursor()  
            # Retrieve all the spatial layers from the schema ngi  
            cursor.execute(  
                """ select f_table_name,f_geometry_column,f_table_schema from geometry_columns where f_table_schema = 'ngi';  
         """)  
            connection.commit()  
            # retrieve the records from the database  
            rows = cursor.fetchall()  
            for row in rows:  
                ngi_table = row[0]  
                print(ngi_table)  
                geom_field_name = row[1]  
                db_schema = row[2]  
                cursor = connection.cursor()  
                source_geom_type = """select ST_GeometryType(%s) from %s.%s""" % (geom_field_name, db_schema, ngi_table)  
                cursor.execute(source_geom_type)  
                connection.commit()  
                row = cursor.fetchone()  
                # Define geometry type ie ST_Multilinestring  
                geo_type = row[0]  
                # Create SQL to count records  
                layer_sql = ("""  
                WITH clipping_test AS  
                (SELECT  
                ST_Multi(ST_Intersection(st_transform(v.%s,4326),m.geom)) AS intersection_geom,  
                v.*  
                FROM  
                  %s.%s as v,  
                 (select sheet_number,st_union(geom) as geom from ngi_work where sheet_number = '%s' group by sheet_number)   
                 as m  
                WHERE  
                  ST_Intersects(st_transform(v.%s,4326), m.geom))  
                (SELECT count(*) FROM clipping_test WHERE ST_Geometrytype(intersection_geom)='%s')  
                  """) % (  
                    geom_field_name, db_schema, ngi_table, index_block, geom_field_name, geo_type  
                )  
                cursor = connection.cursor()  
                cursor.execute(layer_sql)  
                feature_count = cursor.fetchone()[0]  
                feature_row = [index_block, ngi_table, feature_count]  
                with open('/tmp/features.csv', 'a') as csvFile:  
                    writer = csv.writer(csvFile)  
                    writer.writerow(feature_row)  
                csvFile.close()  
                connection.commit()  
        connection.close()  
      
    if __name__ == "__main__":  
        main()
