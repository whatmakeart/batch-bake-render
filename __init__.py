# File: eevee_batch_bake_lighting/__init__.py

bl_info = {
    "name": "Eevee Batch Bake Lighting",
    "blender": (2, 80, 0),
    "category": "Render",
    "version": (1, 0, 0),
    "author": "Jimmy Kuehnle",
    "description": "Batch bakes indirect lighting for each frame in Eevee and batch renders. Adds a panel to show render status and stop rendering.",
    "warning": "Ensure to backup Blender projects before using.",
    "wiki_url": "https://github.com/whatmakeart/eevee-batch-bake-lighting",
    "category": "Render"
}

import bpy

# Property group to store rendering status
class BatchBakeRenderProps(bpy.types.PropertyGroup):
    is_rendering: bpy.props.BoolProperty(name="Is Rendering", default=False)
    render_progress: bpy.props.IntProperty(name="Render Progress", default=0)
    total_frames: bpy.props.IntProperty(name="Total Frames", default=0)
    original_file_path: bpy.props.StringProperty(name="Original File Path", default="")
    current_frame: bpy.props.IntProperty(name="Current Frame", default=0)

# Function to get 3D view context for operator overrides
def get_3d_view_context(context):
    for area in context.window.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    return {
                        'window': context.window,
                        'screen': context.screen,
                        'area': area,
                        'region': region,
                        'scene': context.scene,
                        'blend_data': context.blend_data,
                    }
    # If no 3D view is found, return the current context
    return context

# Main class for batch rendering
class BatchBakeRender(bpy.types.Operator):
    bl_idname = "render.batch_bake_render"
    bl_label = "Batch Bake Lighting Render"
    bl_description = "Starts a batch rendering process in the background"
    bl_options = {'REGISTER', 'UNDO'}

    # User confirmation property
    confirm_render: bpy.props.BoolProperty(
        name="Confirm Render",
        description="Confirm that you want to start rendering",
        default=False
    )

    _timer = None

    # Draw UI elements
    def draw(self, context):
        layout = self.layout
        layout.separator()
        layout.label(text="This will render in the background and")
        layout.label(text="will only stop if complete or")
        layout.label(text="the 'Stop Rendering' button is clicked")
        layout.label(text="in the Batch Bake Lighting Render Status panel")
        layout.separator()
        layout.label(text="You can monitor the rendering status and stop the render")
        layout.label(text="in the 'Batch Bake Lighting Render Status' panel")
        layout.label(text="located in the Render Properties tab.")
        layout.separator()
        layout.label(text="Please confirm to start rendering.")
        layout.prop(self, "confirm_render")
        layout.separator()

    # Execute method to start rendering process
    def execute(self, context):
        if not self.confirm_render:
            self.report({'WARNING'}, "Render canceled: You must confirm render.")
            return {'CANCELLED'}

        props = context.scene.batch_bake_render_props

        # Check for ongoing render
        if props.is_rendering:
            self.report({'WARNING'}, "Render already in progress.")
            return {'CANCELLED'}

        # Check for light probes
        if not any(obj.type == 'LIGHT_PROBE' for obj in bpy.context.scene.objects):
            self.report({'WARNING'}, "No light probes found in the scene. Please add a light probe to use this addon.")
            return {'CANCELLED'}

        # Store original file path
        props.original_file_path = context.scene.render.filepath

        # Initialize rendering variables
        props.is_rendering = True
        props.render_progress = 0
        props.total_frames = context.scene.frame_end - context.scene.frame_start + 1
        props.current_frame = context.scene.frame_start

        # Add a timer
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)

        # Force redraw of the UI to show the panel
        for window in wm.windows:
            for area in window.screen.areas:
                area.tag_redraw()

        return {'RUNNING_MODAL'}

    # Modal method to keep track of the rendering process
    def modal(self, context, event):
        props = context.scene.batch_bake_render_props

        if event.type == 'TIMER':
            if not props.is_rendering:
                # Rendering is complete
                self.finish_rendering(context)
                return {'FINISHED'}

            # Render the current frame
            scn = context.scene
            scn.frame_set(props.current_frame)

            # Bake the light cache using context manager
            override_context = get_3d_view_context(context)
            try:
                with bpy.context.temp_override(**override_context):
                    bpy.ops.object.lightprobe_cache_bake(subset='ACTIVE')
            except Exception as e:
                self.report({'ERROR'}, f"Error during light cache bake: {e}")
                self.cancel(context)
                return {'CANCELLED'}

            # Set the file path for this frame
            frame_number = str(props.current_frame).zfill(len(str(scn.frame_end)))
            frame_file_name = f"{props.original_file_path}{frame_number}"
            scn.render.filepath = frame_file_name

            # Render the frame
            bpy.ops.render.render(write_still=True)

            # Update progress
            props.render_progress = props.current_frame - scn.frame_start + 1
            props.current_frame += 1

            # Force redraw of the UI to update the panel
            for window in bpy.context.window_manager.windows:
                for area in window.screen.areas:
                    area.tag_redraw()

            # Check if rendering is complete
            if props.current_frame > scn.frame_end:
                props.is_rendering = False
                self.finish_rendering(context)
                return {'FINISHED'}

            return {'PASS_THROUGH'}

        elif event.type in {'ESC'}:
            # User pressed ESC, cancel the operation
            self.cancel(context)
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def finish_rendering(self, context):
        props = context.scene.batch_bake_render_props
        # Restore original file path
        context.scene.render.filepath = props.original_file_path

        # Remove the timer
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

        props.is_rendering = False

        # Force redraw of the UI to hide the panel
        for window in wm.windows:
            for area in window.screen.areas:
                area.tag_redraw()

        self.report({'INFO'}, "Render completed.")

    # Cancel method to stop rendering
    def cancel(self, context):
        props = context.scene.batch_bake_render_props
        props.is_rendering = False
        wm = context.window_manager
        if self._timer:
            wm.event_timer_remove(self._timer)
        context.scene.render.filepath = props.original_file_path

        # Force redraw of the UI to hide the panel
        for window in wm.windows:
            for area in window.screen.areas:
                area.tag_redraw()

        self.report({'INFO'}, "Render canceled.")

    # Invoke method to display dialog
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# Panel to display render status and stop button
class BatchBakeRenderPanel(bpy.types.Panel):
    bl_label = "Batch Bake Lighting Render Status"
    bl_idname = "RENDER_PT_batch_bake_render_status"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    @classmethod
    def poll(cls, context):
        # Show the panel only when rendering is in progress
        return context.scene.batch_bake_render_props.is_rendering

    def draw(self, context):
        props = context.scene.batch_bake_render_props
        layout = self.layout

        layout.label(text="Rendering update (slower than realtime):")
        layout.label(text="Check output folder for rendered frames")
        layout.label(text=f"Rendering: Frame {props.render_progress} of {props.total_frames}", icon='RENDER_STILL')
        layout.operator("render.stop_batch_bake_render", text="Stop Rendering", icon='CANCEL')

# Operator to stop rendering
class StopBatchBakeRender(bpy.types.Operator):
    bl_idname = "render.stop_batch_bake_render"
    bl_label = "Stop Batch Baked Render"
    bl_description = "Stops the ongoing batch rendering process"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        props = context.scene.batch_bake_render_props
        if not props.is_rendering:
            self.report({'INFO'}, "No active render to stop.")
            return {'FINISHED'}

        props.is_rendering = False

        # Force redraw of the UI to hide the panel
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                area.tag_redraw()

        self.report({'INFO'}, "Render stopping...")
        return {'FINISHED'}

# Function to add menu items
def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(BatchBakeRender.bl_idname)

# Registration
classes = (
    BatchBakeRenderProps,
    BatchBakeRender,
    BatchBakeRenderPanel,
    StopBatchBakeRender,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.batch_bake_render_props = bpy.props.PointerProperty(type=BatchBakeRenderProps)
    bpy.types.TOPBAR_MT_render.append(menu_func)

def unregister():
    bpy.types.TOPBAR_MT_render.remove(menu_func)
    del bpy.types.Scene.batch_bake_render_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
