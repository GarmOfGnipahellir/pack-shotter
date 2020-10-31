import sys

try:
    import blender_addon_tester as BAT
except Exception as e:
    print(e)
    sys.exit(1)

try:
    exit_val = BAT.test_blender_addon(
        addon_path="pack-shotter", blender_revision="2.90")
except Exception as e:
    print(e)
    exit_val = 1

sys.exit(exit_val)
