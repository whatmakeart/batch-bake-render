# Eevee Batch Bake Lighting Addon

This Blender addon allows you to batch bake indirect lighting for each frame in Eevee and batch render them. It adds a panel to show render status and provides the ability to stop the rendering process at any time.

## Update and Bake Indirect Lighting in Every Frame in Eevee for Animation

This works for simple setup where the cost of baking every frame in Eevee is still faster than rendering in Cycles. This add-on enables users to batch rebake indirect lighting for each frame in Eevee and execute batch rendering.

## Installation

Follow these steps to install the Eevee Batch Bake Lighting addon:

### Step 1: Download the Addon

1. **Download the Addon Zip File:**

   - Go to the [Releases](https://github.com/whatmakeart/eevee-batch-bake-lighting/releases) section of this repository.
   - Download the latest release of the addon as a zip file (`eevee_batch_bake_lighting.zip`).

### Step 2: Install the Addon in Blender

1. **Open Blender Preferences:**

   - Open Blender.
   - Go to `Edit > Preferences` (on Windows/Linux) or `Blender > Preferences` (on macOS).

2. **Install the Addon:**

   - In the Preferences window, select the `Add-ons` tab on the left.
   - Click on the `Install...` button at the top.

3. **Select the Addon Zip File:**

   - Navigate to the location where you downloaded `eevee_batch_bake_lighting.zip`.
   - Select the zip file and click `Install Add-on`.

4. **Enable the Addon:**

   - After installation, the addon should appear in the list of addons with a checkbox.
   - Enable the addon by checking the box next to `Eevee Batch Bake Lighting`.

5. **Save Preferences (Optional):**

   - If you want Blender to remember that the addon is enabled, click on the `Save Preferences` button at the bottom left of the Preferences window.

## Usage

Follow these steps to use the Eevee Batch Bake Lighting addon in your Blender project:

### Step 1: Prepare Your Scene

1. **Set Render Engine to Eevee:**

   - In the **Render Properties** tab (the camera icon in the Properties Editor), ensure that the **Render Engine** is set to `Eevee`.

2. **Add Light Probes to Your Scene:**

   - The addon requires at least one light probe in the scene to bake indirect lighting.
   - To add a light probe:
     - Go to `Add > Light Probe` in the 3D Viewport.
     - Choose the appropriate light probe for your scene (e.g., `Irradiance Volume`, `Reflection Cubemap`, or `Reflection Plane`).

### Step 2: Configure Render Settings

1. **Set Output Path:**

   - In the **Output Properties** tab (the printer icon in the Properties Editor), set the `Output` path where you want the rendered frames to be saved.

2. **Set Frame Range:**

   - In the **Output Properties**, set the `Frame Start` and `Frame End` values to define the range of frames you want to render.

### Step 3: Start Batch Bake Lighting Render

1. **Access the Addon Operator:**

   - Go to the top menu bar and click on `Render`.

2. **Start the Batch Bake Lighting Render:**

   - Select `Batch Bake Lighting Render` from the dropdown menu.

3. **Confirm Rendering:**

   - A dialog will appear with information about the rendering process.
   - **Note:** The rendering will run in the background and can be monitored or stopped in the **Batch Bake Lighting Render Status** panel located in the **Render Properties** tab.
   - To proceed, check the `Confirm Render` box to confirm that you want to start rendering.
   - Click `OK` to start the rendering process.

### Step 4: Monitor Render Status and Stop Rendering (Optional)

1. **Open the Render Properties Tab:**

   - In the **Properties Editor** (usually on the right side of the Blender interface), click on the **Render Properties** tab (the camera icon).

2. **View the Render Status Panel:**

   - You will see a panel named **Batch Bake Lighting Render Status** at the top.
   - The panel displays:
     - A message indicating that rendering is in progress.
     - The current frame being rendered and the total number of frames.
     - A **Stop Rendering** button.

3. **Stop the Rendering Process:**

   - If you wish to stop the rendering process before it completes, click the **Stop Rendering** button in the panel.
   - The rendering process will stop, and the panel will disappear.

### Step 5: After Rendering Completes

1. **Check Rendered Frames:**

   - The rendered frames will be saved to the output directory you specified in the render settings.

2. **Verify Render Completion:**

   - Once rendering is complete, the **Batch Bake Lighting Render Status** panel will automatically disappear from the **Render Properties** tab.

## Important Notes

- **Light Probes Are Required:**

  - The addon requires at least one light probe in the scene to function properly.
  - Without a light probe, the addon will display a warning and cancel the operation.

- **Render Engine Must Be Eevee:**

  - This addon is designed specifically for the Eevee render engine.
  - Ensure that the **Render Engine** is set to `Eevee` in the **Render Properties** tab.

- **Backing Up Your Project:**

  - It is recommended to save and backup your Blender project before using the addon to prevent any potential data loss.

- **Render Output Path:**

  - The addon temporarily modifies the render output path to save each frame.
  - After rendering is complete or canceled, the original output path is restored.

- **Do Not Interrupt Blender:**

  - While the rendering process is running, avoid performing heavy operations in Blender to prevent interference with the rendering.

## Troubleshooting

- **Panel Not Showing Up:**

  - If the **Batch Bake Lighting Render Status** panel does not appear after starting the rendering process, try switching tabs in the Properties Editor or resizing the Blender interface to force a UI refresh.

- **Rendering Does Not Start:**

  - Ensure that you have checked the `Confirm Render` box in the dialog when starting the batch bake lighting render.
  - Make sure that your scene contains at least one light probe and that the render engine is set to Eevee.

- **Error Messages:**

  - If you encounter error messages during the rendering process, check the Blender console for more details.
  - Common issues include missing light probes or incorrect render settings.

## Support and Feedback

If you encounter any issues or have suggestions for improvements, please open an issue on the [GitHub repository](<[#](https://github.com/whatmakeart/eevee-batch-bake-lighting)>) or contribute by submitting a pull request.
