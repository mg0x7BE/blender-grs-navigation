bl_info = {
    "name": "Blender GRS Navigation",
    "blender": (5, 0, 0),
    "category": "Interface",
    "version": (1, 0, 0),
    "description": "G/R/S switch the active tool to move/rotate/scale",
}

import bpy

addon_keymaps = []

KEY_TO_TOOL = {
    'G': 'builtin.move',
    'R': 'builtin.rotate',
    'S': 'builtin.scale',
}

KEYMAP_CONTEXTS = (
    'Object Mode', 'Mesh', 'Curve', 'Lattice',
    'Armature', 'Metaball', 'UV Editor', 'Pose',
)


class GRSNavigationSetTool(bpy.types.Operator):
    bl_idname = "wm.grs_navigation_set_tool"
    bl_label = "GRS Navigation Set Tool"
    bl_options = {'REGISTER', 'UNDO'}

    tool_name: bpy.props.StringProperty()

    def execute(self, context):
        try:
            bpy.ops.wm.tool_set_by_id(name=self.tool_name)
        except RuntimeError:
            pass
        return {'FINISHED'}


def register():
    bpy.utils.register_class(GRSNavigationSetTool)

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc is None:
        return

    for ctx_name in KEYMAP_CONTEXTS:
        km = kc.keymaps.new(name=ctx_name, space_type='EMPTY')
        for key, tool_id in KEY_TO_TOOL.items():
            kmi = km.keymap_items.new(
                GRSNavigationSetTool.bl_idname, key, 'PRESS',
                ctrl=False, shift=False,
            )
            kmi.properties.tool_name = tool_id
            addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(GRSNavigationSetTool)


if __name__ == "__main__":
    register()
