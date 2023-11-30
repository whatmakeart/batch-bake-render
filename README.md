# Eevee Batch Bake Lighting Add-on
Eevee Batch Bake Lighting indirect lighting for each frame in Eevee and Batch Render. Adds menu item to Render to start and stop batch baked lighting rendering.

## Update and Bake Indirect Lighting in Every Frame in Eevee for Animation

This works for simple setup where the cost of baking every frame in Eevee is still faster than rendering in Cycles.

# README for Eevee Batch Bake Lighting Add-on

This README provides detailed information about the Eevee Batch Bake Lighting Add-on for Blender. This add-on enables users to batch rebake indirect lighting for each frame in Eevee and execute batch rendering.

## Installation

To install the Eevee Batch Bake Lighting Add-on in Blender, follow these steps:

1. **Download the Add-on**:
   - Download the Python script file (`eevee_batch_lighting_rebake.py`) from the GitHub repository.

2. **Open Blender**:
   - Launch Blender and open your project.

3. **Install the Add-on**:
   - Navigate to `Edit > Preferences` in Blender.
   - In the Preferences window, go to the `Add-ons` section.
   - Click `Install...` and browse to the downloaded `eevee_batch_lighting_rebake.py` file.
   - Select the file and click `Install Add-on`.

4. **Activate the Add-on**:
   - In the Add-ons section, search for "Eevee Batch Bake Lighting".
   - Check the box next to the add-on's name to activate it.

5. **Save Preferences** (Optional):
   - Click `Save Preferences` if you want the add-on to be enabled by default in future Blender sessions.

## Usage

Once installed and activated, the Eevee Batch Bake Lighting Add-on can be used as follows:

1. **Accessing the Add-on**:
   - Go to the top menu bar and find the `Render` menu.
   - In the `Render` menu, you will find two new options: `Run Batch Baked Lighting Render` and `Batch Baked Lighting Render Status`.

2. **Running a Batch Render**:
   - Click `Run Batch Baked Lighting Render`. A dialog box will appear.
   - Confirm that you want to start rendering by checking the `Confirm Render` option.
   - Click `OK` to start the batch rendering process. The rendering will run in the background.

3. **Monitoring Render Progress**:
   - To check the status of the rendering process, select `Batch Bake Render Status` from the Render menu.
   - A dialog box will show the current frame being rendered.

4. **Stopping the Render**:
   - If you need to stop the rendering process, open the `Batch Bake Render Status` dialog.
   - Click the `Stop Rendering` button to halt the rendering process.

5. **Render Output**:
   - The rendered frames will be saved in the specified output directory as set in the render settings of your Blender project.

## Important Notes

- Before using this add-on, make sure to set up your render output settings in Blender.
- The add-on is designed to work with Blender version 2.80 and above.
- It's recommended to test the add-on in a non-production environment first to ensure it meets your needs.
- Always back up your Blender project before using the add-on, as it performs batch operations that can be resource-intensive.

## Support

For support, feature requests, or bug reports, please use the Issues section of the GitHub repository.

---

Thank you for using the Eevee Batch Bake Lighting Add-on!

