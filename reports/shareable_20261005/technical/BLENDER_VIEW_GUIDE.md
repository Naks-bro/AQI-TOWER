# Blender presentation guide

Open AQI_R03M_REVIEW.blend. Use the active/latest scene named AQI R03M Review Presentation (currently .001); other pre-existing scenes were preserved, not overwritten.

Frame 1: assembled. Frames 30-36: exploded. Frame 48: assembled again. Camera zoom is animated to keep exploded parts inside the view. Space/play controls animate the assembly; render the camera for final lighting.

493 source parts are actual CAD tessellations, in metres for display. Five studio objects and 32 illustrative air markers bring the latest scene to 530 objects. The source CAD remains authoritative; Blender mesh dimensions do not establish fabrication tolerances. Guards remain solid envelopes.

Air markers are hidden from render by default. The supplied air GIF was rendered from a temporary cutaway with CAD animations cleared, cabinet/guard panels hidden and air markers enabled. These paths are hand-authored, NOT CFD. The source file remains the assembly animation. Use the provided GIF or offline viewer for the ready-to-share airflow explanation.

Sources: scripts/visualization/build_blender_review.py and render_blender_review.py. The latter renders a temporary background copy and does not save over the source scene. No paid assets or copied product model are used.
