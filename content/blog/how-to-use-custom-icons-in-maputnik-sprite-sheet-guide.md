---
author: Jeremy Prior
date: '2026-07-17'
description: Learn how to compile custom SVG icons into a Maputnik-friendly sprite
  sheet using spritezero-cli. We cover generation, GitHub hosting, and s
erpnext_id: /blog/fossgis/how-to-use-custom-icons-in-maputnik-sprite-sheet-guide
erpnext_modified: '2026-07-17'
reviewedBy: Automated Check
reviewedDate: '2026-07-22'
tags:
- Fossgis
thumbnail: /img/blog/erpnext/UcXLuvc.png
title: How to Use Custom Icons in Maputnik (Sprite Sheet Guide)
---

### The Missing SVG Button

If you have ever tried styling a vector map in Maputnik, you have probably hit this wall: you have a folder full of perfectly designed SVG icons, but there is no simple "Upload SVG" button for your symbol layers.

![](/img/blog/erpnext/UcXLuvc.png)

  


Unlike desktop GIS software, web mapping specifications (like MapLibre and Mapbox GL) are optimised for rendering speed. Loading hundreds of individual SVG files requires too many HTTP requests and bogs down performance. Instead, the style specification requires a **sprite sheet** : a single raster image (PNG) containing all your icons, paired with an index file (JSON) that tells the map exactly where each icon sits on that image.

  


Here is a step-by-step technical guide to creating your SVGs, generating a sprite sheet using `@beyondtracks/spritezero-cli`, and hosting it via GitHub to link directly into Maputnik.

###   


### Step 1: Install Spritezero

We will use a command-line tool called `spritezero-cli` to compile the SVGs. Specifically, we will use the `@beyondtracks` fork, which is actively maintained. Ensure you have Node.js and npm installed on your machine before beginning.

  


**For Mac/Linux:** Open your terminal and install it globally via npm using `sudo`:
    
    
    sudo npm install --force -g @beyondtracks/spritezero-cli

You can verify the installation by running `/usr/bin/spritezero` or simply `spritezero`.

  


**For Windows:** Open Command Prompt or PowerShell (preferably as Administrator) and install it globally without `sudo`:
    
    
    npm install --force -g @beyondtracks/spritezero-cli

  


Verify the installation by running `spritezero`.

  


On any operating system, running the verification command will return the tool's usage instructions (`<outputfile> <inputdir>`) if installed correctly.

###   


### Step 2: Prepare Your Workspace and SVGs

Next, we need to set up a working directory. Create a main project folder and a subfolder specifically for your SVGs (these commands work across Mac, Linux, and Windows):
    
    
    mkdir maputnik-sprites
    
    cd maputnik-sprites
    
    mkdir sprites

  


Now, create your custom SVG icons (e.g., using Inkscape) and save them directly into the `sprites/` directory. Keep your filenames simple and lowercase (e.g., `hospital.svg`, `school.svg`), as these will become the IDs you use inside Maputnik.

### ![](/img/blog/erpnext/WpsOHNM.png)

  


### Step 3: Generate the Sprite Sheets

With your SVGs in the `sprites` folder, it is time to compile them. The command structure takes the output file prefix first, followed by the input directory.

  1. **Generate standard resolution sprites:**


    
    
     # Syntax: spritezero <output_file_path> <input_directory_path>
    
    spritezero sprites sprites

  1. **Generate high-definition (Retina) sprites:** It is best practice to generate a high-DPI version for modern screens:


    
    
    # Syntax: spritezero --retina <output_file_path>@2x <input_directory_path>
    
    spritezero --retina sprites@2x sprites

  


If you run `ls` (on Mac/Linux) or `dir` (on Windows) in your root directory, you should now see your compiled files alongside your input folder: `sprites/` `sprites.json` `sprites.png` `[sprites@2x.json](<mailto:sprites@2x.json>)` `[sprites@2x.png](<mailto:sprites@2x.png>)`

![](/img/blog/erpnext/gOZjDht.png)

  


The actual spritesheet.png will look something like the following image if you open it:

![](/img/blog/erpnext/jIaJzQd.png)

###   


### Step 4: Host on GitHub and Link to Maputnik

Maputnik needs a live URL to fetch your sprite sheet. A free and highly reliable way to host these files is using a public GitHub repository.

  1. Create a public repository on GitHub (e.g., named `sprites`).
  2. Push your four generated files (`sprites.png`, `sprites.json`, `[sprites@2x.png](<mailto:sprites@2x.png>)`, `[sprites@2x.json](<mailto:sprites@2x.json>)`) to the main branch.![](/img/blog/erpnext/wRjkomk.png)
  3. Get the correct URL. You cannot use the standard GitHub repository link. Instead, navigate to the `sprites.json` file in your repo and click the **Raw** button on the right side of the file view.
  4. Copy the URL from your browser's address bar, but **strictly remove the**`**.json**`**extension**.
  5. _Example:_ If your raw URL is `<https://raw.githubusercontent.com/User-Name/sprites/refs/heads/main/sprites.json>`, you will copy and use: `<https://raw.githubusercontent.com/User-Name/sprites/refs/heads/main/sprites>`



  


> **Crucial Note:** The URL you provide to Maputnik must _exclude_ the file extensions. The rendering engine automatically appends `.png` and `.json` when making the network requests in the background.

  


Open Maputnik (if you are not hosting your own instance, you can use the public editor at `[https://maplibre.org/maputnik/](<https://maplibre.org/maputnik>)`), click **Style Settings** in the top navigation bar, paste your modified raw GitHub URL into the **Sprite URL** field, and close the modal.

### ![](/img/blog/erpnext/SL9M9ZB.png)  


###   


### Step 5: Configure Your Symbol Layer

Now that Maputnik has your sprite sheet, you can apply your custom icons to your map data.

  1. Create a new **Symbol Layer** in Maputnik.
  2. Under the **Text Layout Properties** group, clear the **Text field** and **Font** fields (unless you are adding text back in, as explained below).
  3. Scroll down to the **Icon Layout Properties** group.
  4. Click into the **Image** property field. It should automatically autocomplete based on the names of the SVGs compiled into your hosted `sprites.json` file!



### ![](/img/blog/erpnext/POgtHl1.png)  


###   


### Important Note: Handling Text in SVGs

If the original SVG you created has text in it (like a label or a number inside a marker), **the text will not be stored in the compiled sprite sheet.** The compilation tool strips out standard font elements.

  


To solve this, you can apply text directly within Maputnik using the same **Symbol Layer**. Keep your custom icon in the **Image** field (under _Icon Layout Properties_), and simply fill in your desired text in the **Text field** (under _Text Layout Properties_).

  


This approach works perfectly if all instances of that symbol will display the exact same text, or if you are dynamically pulling the text from your data attributes (e.g., `{name}`). If you have a scenario where you need completely separate styling, filtering, or positioning rules for your text versus your icon, you can always create a second, separate Symbol Layer just for the text.

![](/img/blog/erpnext/pIBfykg.png)

###   


### The Kartoza Challenge

Now it is your turn to put this workflow into practice.

  1. Create a simple SVG icon (like a coffee cup or a warning sign) using Inkscape.
  2. Use the `spritezero` commands outlined above to generate both standard and retina sprite sheets.
  3. Push the files to a public GitHub repository, grab the raw URL minus the extension _(e.g.,_`_<https://raw.githubusercontent.com/User-Name/sprites/refs/heads/main/sprites>_`_)_ , link it to a fresh Maputnik style, and successfully render your custom icon on a blank map canvas.



  


Once you master this workflow, you will never be restricted by default map icons again. Happy styling!
