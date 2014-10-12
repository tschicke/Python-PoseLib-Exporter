import bpy
import math
from mathutils import Quaternion
from mathutils import Vector

def getQuatBetweenVectors(v1, v2):
    v1.normalize()
    v2.normalize()
    dot = v1.dot(v2)
    if dot == -1:
        #180 degree rotation
        dot2 = v1.dot(Vector([1, 0, 0]))
        if dot2 < 1.0:
            return Quaternion(v1.cross(Vector([1, 0, 0])), math.radians(180))
        else:
            return Quaternion(v1.cross(Vector([0, 1, 0])), math.radians(180))
    cross = v1.cross(v2)
    return Quaternion((dot + 1, cross.x, cross.y, cross.z)).normalized()

def save(operator, context, filepath=""):
    bpy.ops.object.mode_set(mode='OBJECT')

    poseLib = None
    armature = None
    for object in bpy.data.objects:
        if object.type == 'ARMATURE':
            poseLib = object.pose_library
            armature = object.data
            break
    if poseLib == None or armature == None:
        raise NameError("Cannot export Pose Library %s, there is no armatures" % filepath)
    
    
    numPoses = len(poseLib.groups[0].channels[4].keyframe_points)
    numBones = len(poseLib.groups)
    poseArray = []
    nameArray = []
    
    print("Exporting")
    
    oglBoneArray = []
    oglBoneDirectionArray = []
    
    startNodes = []
    for i in range(0, len(armature.bones)):
        bone = armature.bones[i]
        if bone.parent == None:
            dupIndex = -1
            for j in range(0, len(startNodes)):
                if bone.head[:] == startNodes[j][:]:
                    dupIndex = j
                    break
            if dupIndex == -1:
                baseNode = bone.head_local
                startNodes.append((baseNode.x, baseNode.y, baseNode.z))
                oglBoneArray.append(-1)
        oglBoneArray.append(i)
        boneDirection = bone.tail_local - bone.head_local
        oglBoneDirectionArray.append(boneDirection)
    
    for i in range(0, numPoses):
        nameArray.append(poseLib.pose_markers[i].name)
        boneArray = []
        for j in range(0, len(oglBoneArray)):
            index = oglBoneArray[j]
            q = Quaternion()
            if index == -1:
                q = Quaternion([1, 0, 0, 0])
            else:
                quat = Quaternion([1, 0, 0, 0])
                for k in range(0, 4):
                    quat[k] = poseLib.groups[index].channels[k + 3].keyframe_points[i].co.y
                axisVector = Vector([0, 1, 0])
                boneVector = oglBoneDirectionArray[index]
                quatBetween = getQuatBetweenVectors(boneVector, axisVector)
                q = quatBetween.inverted() * quat * quatBetween
                q.normalize()
            boneArray.append(tuple([q.w, q.x, q.z, -q.y]))
        poseArray.append(boneArray)
    
    print(filepath)
    file = open(filepath, 'w')
    fw = file.write
    
    fw("poslib\n")
    fw("%d %d\n" % (numPoses, len(oglBoneArray)))
    for i in range(0, numPoses):
        fw("n " + nameArray[i] + '\n')
        for j in range(0, len(oglBoneArray)):
            q = poseArray[i][j]
            fw("q %f %f %f %f\n" % (q[0], q[1], q[2], q[3]))
        fw('f\n')
        
    file.close()
    
    print("Finished Exporting")
    
    return {'FINISHED'}