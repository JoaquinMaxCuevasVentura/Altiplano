from pathlib import Path
p=Path('/tmp/fidelidad/chujlla.py');s=p.read_text()
# Allow the jamb reveal to open toward the interior, with its inner shoulder returning to the same far corner.
s=s.replace('p.z=z\n    if rough:', '''p.z=z
    if inner and z<cap(y).z-.01:
        station=max(0.,min(1.,(y-tf.y)/(.64-tf.y),(tb.y-y)/(tb.y-2.38)))
        weight=max(0.,min(1.,(2.80-z)/1.2))
        p.y+=inner*1.07*station*weight
    if rough:''')
s=s.replace('end=Vector((2.48,1.67,.075))','end=Vector((2.79,1.63,.075))')
s=s.replace('lt.energy=2950','lt.energy=1800').replace("lt.spot_blend=.68","lt.spot_blend=.92")
s=s.replace("vol=bpy.data.materials['Aire del estudio de luz'];vs=[];fs=[]","vol=bpy.data.materials['Aire del estudio de luz'];next(n for n in vol.node_tree.nodes if n.type=='VOLUME_SCATTER').inputs['Density'].default_value=.059;vs=[];fs=[]")
# Avoid an isolated tip in the shaft. Cloud the boundaries of the dust.
idx=s.index('# Sunlight reflects')
s=s[:idx]+'''nodes=vol.node_tree.nodes;links=vol.node_tree.links
tex=nodes.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=4.4;tex.inputs['Detail'].default_value=3
coord=nodes.new('ShaderNodeNewGeometry');links.new(coord.outputs['Position'],tex.inputs[0])
mul=nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=.106;links.new(tex.outputs['Fac'],mul.inputs[0])
links.new(mul.outputs[0],next(n for n in nodes if n.type=='VOLUME_SCATTER').inputs['Density'])
# A rectangular studio source is visible as a grazing reflection in the glass and the inside of the slot.
l=bpy.data.lights.new('Cielo de estudio sobre la banda de vidrio','AREA');l.shape='RECTANGLE';l.size=.22;l.size_y=3.2;l.energy=870;l.color=(1,.83,.64)
ob=bpy.data.objects.new(l.name,l);s.collection.objects.link(ob)
ob.location=(slit(1.55)-.29,1.6,top(slit(1.55),1.55)+1.65)
ob.rotation_euler=(Vector((slit(1.55),1.5,top(slit(1.55),1.55)))-ob.location).to_track_quat('-Z','Y').to_euler()
'''+s[idx:]
idx=s.index('# Low sunk timber')
s=s[:idx]+'''# Smaller wedges bed each continuous wall on the inner row of the dry stone plinth.
for side in (0,1):
    spans=[(tf.y,.64),(2.38,tb.y)] if side==0 else [(tf.y,tb.y)]
    for a,b in spans:
        count=max(2,round((b-a)/.41))
        for i in range(count):
            y=mix(a,b,(i+.5)/count)
            p=west(y,.19,.77) if side==0 else east(y,.19,.77)
            stone('Calce interior bajo el testero',p,(.49,(b-a)/count*1.14,.426),rng.uniform(-.1,.1))
'''+s[idx:]
# Native light and construction, earthen aggregate across the exposed gable.
idx=s.index('# Warmer grazing')
s=s[:idx]+'''for emat in [earth,dm]:
    nt=emat.node_tree;bs=nt.nodes.get('Principled BSDF');old=bs.inputs['Base Color'].links[0].from_socket
    c=nt.nodes.new('ShaderNodeNewGeometry');ns=nt.nodes.new('ShaderNodeTexNoise');ns.inputs['Scale'].default_value=118;ns.inputs['Detail'].default_value=2.7
    nt.links.new(c.outputs['Position'],ns.inputs['Vector']);r=nt.nodes.new('ShaderNodeValToRGB')
    r.color_ramp.elements[0].position=.28;r.color_ramp.elements[0].color=(.55,.49,.45,1)
    r.color_ramp.elements[-1].position=.70;r.color_ramp.elements[-1].color=(1,1,1,1)
    nt.links.new(ns.outputs['Fac'],r.inputs['Fac'])
    mx=nt.nodes.new('ShaderNodeMixRGB');mx.blend_type='MULTIPLY';mx.inputs[0].default_value=.54;nt.links.new(old,mx.inputs[1]);nt.links.new(r.outputs[0],mx.inputs[2]);nt.links.new(mx.outputs[0],bs.inputs['Base Color'])
'''+s[idx:]
p.write_text(s)
