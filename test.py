import os


def clear():
    #os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(0, 30):
        print()


import bpy

mesh = bpy.data.objects['Cylinder'].data
skeleton = bpy.data.objects['Armature']
poslib = skeleton.pose_library

def printFunc():
    clear()
    for bone in skeleton.data.bones:
        print("Head ", bone.tail_local - bone.head_local)

printFunc()