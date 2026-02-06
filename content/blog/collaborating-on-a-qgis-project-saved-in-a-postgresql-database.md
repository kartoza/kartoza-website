---
title: "Collaborating on a QGIS Project Saved in a PostgreSQL Database"
description: "QGIS provides a couple of options when it comes to working with QGIS projects. All these formats have their strengths and weakness."
tags:
  - Database
  - QGIS
  - PostgreSQL
date: 2021-06-25
author: "Admire Nyakudya"
thumbnail: "/img/blog/placeholder.png"
---

{{< block
    title="Collaborating on a QGIS Project Saved in a PostgreSQL Database"
    subtitle="Database"
    class="is-primary"
    sub-block-side="bottom"
>}}
QGIS provides a couple of options when it comes to working with QGIS projects. All these formats have their strengths and weakness.
{{< /block >}}

## QGIS Project Collaboration

QGIS provides a couple of options when it comes to working with QGIS projects. All these formats have their strengths and weakness. When doing some work in QGIS we used to pass around the QGIS project files but ever since storing the QGIS projects in a PostgreSQL database became an option we have been investigating using this as our primary method of collaboration.

## Best Practices for Enterprise Environments

**When working with QGIS projects in an enterprise environment we encourage following these rules:**

1. When connecting to the database either use PostgreSQL Service files or the QGIS authentification framework. Do not use basic authentification as the passwords are stored as plain text in QGIS projects
2. When using images for SVG icons always embed them into the project
3. Choose an appropriate CRS that relates to your area of interest. Local CRS would be preferred over global CRS
4. Store rasters in the DB or serve them as COGs that can be accessed as remote layers, or store them relative to a specific location where users will be able to access them.
5. Ensure that intended users have adequate permissions on the QGIS project table as well as all the layers or tables the project loads.

Once all these options are satisfied then you can proceed to save your QGIS project in the database and be assured that any user will be able to open the project with out a hitch. The following procedure outlines how to connect to a database and store the project in the same database.

## Setup Procedure

**Step 1: Prepare your PostgreSQL Service file**

`~/.pg_service.conf`

```ini
[gis_service]
host=localhost
port=25432
user=xxx
dbname=gis
password=xxx
```

2. Set up your PostgreSQL connection within QGIS using the service name you defined above.
3. Load all your layers into the QGIS Project.
4. From the Project menu select Save to PostgreSQL and populate the dialog as needed.
5. In the PostGIS connection properties enable 'allow loading/saving QGIS projects in the database'
6. Ensure your database role has permission to create or use the _qgis_projects_ table

## Version Control for Database Projects

Now the QGIS Project is saved into the database. But we now have a different kind of problem. How do we track which project is the most recent and how do we prevent users from overwriting each other's changes? To handle this, we can write a custom function and trigger in the database.

**SQL Implementation:**

1. Open the DBManager and connect to your database.

Run the SQL below:

```sql
-- Function to copy old project into a the new row in the same project table
CREATE OR REPLACE FUNCTION update_project()
RETURNS trigger LANGUAGE plpgsql
AS
$$
BEGIN
  IF NEW.content <> OLD.content THEN
        INSERT INTO qgis_projects (name,metadata, content)
        VALUES(OLD.name ||'_'|| now(),OLD.metadata,old.content);
  END IF;
  RETURN NEW;
END ;
$$;

-- Create a trigger to populate the backup project with old copies of the QGIS project
CREATE TRIGGER last_project_changes
  BEFORE UPDATE
  ON qgis_projects
  FOR EACH ROW
  EXECUTE PROCEDURE update_project()
```

2. Now all users can start working on the project and save them as they go. You can always revert to an older project if you feel someone has overwritten some important changes.
