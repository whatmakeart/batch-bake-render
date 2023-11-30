bl_info = {
    "name": "Eevee Batch Bake Lighting",
    "blender": (2, 80, 0),
    "category": "Render",
    "version": (0, 9, 0),
    "author": "Jimmy Kuehnle",
    "description": "Batch Batch Bake indirect lighting for each frame in Eevee and Batch Render. Adds menu item to Render to start and stop batch baked lighting rendering.",
    "warning": "Can be unstable, make sure to backup Blender projects before using.",
    "wiki_url": "https://github.com/whatmakeart/eevee-batch-bake-lighting",
    "category": "Render"
}

# Import necessary modules
import bpy

# Global variables to track rendering status
is_rendering = False
render_progress = 0
total_frames = 0
current_frame = 0  # Track the current frame being rendered
original_file_path = ""  # Store the original file path

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

    # Draw UI elements
    def draw(self, context):
        layout = self.layout
        layout.separator()
        layout.label(text="Renders in the background and")
        layout.label(text="will only stop if complete or")
        layout.label(text="the 'Stop Render' button is clicked")
        layout.label(text="under Batch Bake Lighting Render Status menu")
        layout.separator()
        layout.label(text="Please confirm to start rendering.")
        layout.prop(self, "confirm_render")
        layout.separator()
    # Modal method to keep track of the rendering process
    def modal(self, context, event):
        global is_rendering, render_progress, last_reported_progress

        if event.type == 'TIMER':
            if not is_rendering:
                self.report({'INFO'}, "Render completed.")
                return {'FINISHED'}

            # Update UI only when render progress changes significantly
            if self.last_reported_progress != render_progress:
                context.area.tag_redraw()
                self.last_reported_progress = render_progress
         
        return {'PASS_THROUGH'}
        
    # Execute method to start rendering process
    def execute(self, context):
        global is_rendering, render_progress, total_frames, current_frame, original_file_path
        # Check for ongoing render and confirm property
        if is_rendering:
            self.report({'WARNING'}, "Render already in progress.")
            return {'CANCELLED'}
        
        original_file_path = context.scene.render.filepath  # Store the original file path

        if not self.confirm_render:
            self.report({'WARNING'}, "Render canceled: You must confirm render.")
            return {'CANCELLED'}
        # Initialize rendering variables and start render
        is_rendering = True
        render_progress = 0
        total_frames = context.scene.frame_end - context.scene.frame_start + 1
        current_frame = context.scene.frame_start

        bpy.app.timers.register(self.batch_render)
        return {'RUNNING_MODAL'}

    # Render a single frame at a time
    def batch_render(self):
        global is_rendering, render_progress, current_frame, original_file_path
        scn = bpy.context.scene

        # Check if rendering should be stopped
        if not is_rendering:
            scn.render.filepath = original_file_path  # Reset file path
            return None

        # Render the current frame
        scn.frame_set(current_frame)
        bpy.ops.scene.light_cache_bake()
        frame_file_name = f"{original_file_path}{str(current_frame).zfill(len(str(scn.frame_end)))}"
        scn.render.filepath = frame_file_name
        bpy.ops.render.render(write_still=True)

        # Update progress
        render_progress = current_frame - scn.frame_start + 1
        current_frame += 1

        # Check if rendering is complete
        if current_frame > scn.frame_end:
            is_rendering = False
            scn.render.filepath = original_file_path  # Reset file path
            return None

        return 0.1  # Schedule next frame render
    
    # Cancel method to stop rendering
    def cancel(self, context):
        global is_rendering, original_file_path
        is_rendering = False
        bpy.app.timers.unregister(self.batch_render)
        context.scene.render.filepath = original_file_path  # Reset file path

    # Invoke method to display dialog
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class BatchBakeRenderStatus(bpy.types.Operator):
    bl_idname = "render.batch_bake_render_status"
    bl_label = "Batch Bake Lighting Render Status"
    bl_description = "Shows the current status of the batch rendering process"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        global is_rendering, render_progress, total_frames
        if not is_rendering:
            self.report({'INFO'}, "No active render.")
        else:
            self.report({'INFO'}, f"Rendering: Frame {render_progress} of {total_frames}")
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        global is_rendering, render_progress, total_frames
        layout = self.layout
        if is_rendering:
            layout.label(text=f"Rendering Update Slower than Realtime")
            layout.label(text=f"Check output folder for rendered frames")
            layout.label(text=f"Rendering: Frame {render_progress} of {total_frames}", icon='RENDER_STILL')
            layout.operator("render.stop_batch_bake_render", text="Stop Rendering", icon='CANCEL')
        else:
            layout.label(text="No active render.")

class StopBatchBakeRender(bpy.types.Operator):
    bl_idname = "render.stop_batch_bake_render"
    bl_label = "Stop Batch Baked Render"
    bl_description = "Stops the ongoing batch rendering process"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        global is_rendering
        if not is_rendering:
            self.report({'INFO'}, "No active render to stop.")
            return {'FINISHED'}

        is_rendering = False
        self.report({'INFO'}, "Render stopping...")
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(BatchBakeRender.bl_idname)
    self.layout.operator(BatchBakeRenderStatus.bl_idname)

def register():
    bpy.utils.register_class(BatchBakeRender)
    bpy.utils.register_class(BatchBakeRenderStatus)
    bpy.utils.register_class(StopBatchBakeRender)
    bpy.types.TOPBAR_MT_render.append(menu_func)

def unregister():
    bpy.utils.unregister_class(BatchBakeRender)
    bpy.utils.unregister_class(BatchBakeRenderStatus)
    bpy.utils.unregister_class(StopBatchBakeRender)
    bpy.types.TOPBAR_MT_render.remove(menu_func)

if __name__ == "__main__":
    register()
