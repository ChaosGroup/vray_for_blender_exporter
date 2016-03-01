import sys
import json
import os
import shutil
import glob

from importlib.machinery import SourceFileLoader

shutil.move('texture', 'textures')

sys.path.insert(0, './brdf')
dirs = glob.glob('*/')

fake_dirs = ['vb30', 'vb30/lib', 'vb30/debug', 'vb30/vray_tools', 'vb30/nodes']
fake_files = [
	'vb30/lib/ExportUtils.py',
	'vb30/lib/PluginUtils.py',
	'vb30/debug/Debug.py',
	'bpy.py',
	'vb30/vray_tools/VRaySceneParser.py',
	'vb30/vray_tools/VrmatParser.py'
]

def ordered(obj):
	if isinstance(obj, dict):
		return sorted((k, ordered(v)) for k, v in obj.items())
	if isinstance(obj, list):
		return sorted(ordered(x) for x in obj)
	else:
		return obj

def subset(A, B):
	"""
	Checks if the json A is subset of the json B
	"""
	if isinstance(A, dict) != isinstance(B, dict) and isinstance(A, list) != isinstance(B, list):
		# print('Type missmatch')
		return False

	if isinstance(A, dict):
		for key, val in A:
			if not key in A or not subset(A[key], B[key]):
				# print('Dict missmatch')
				return False
	elif isinstance(A, list):
		for item in A:
			if not any([subset(item, ix) for ix in B]):
				# print('List missmatch', item)
				return False
				break
	else:
		if A != B:
			# print('Values missmatch %s != %s' % (A, B))
			return False

	return True


manual_check = []
missmatch_json = []
missing_json = []

for f in fake_dirs:
	try:
		os.mkdir(f)
	except:
		pass
for f in fake_files:
	try:
		open(f, 'w+').write(' ')
	except:
		pass

for pl_dir in dirs:
	for root, _, files in os.walk(pl_dir):
		if root.find('__') != -1:
				continue
		for f in files:
			if f.find('__') != -1:
				continue

			pyFile = os.path.join(root, f)
			modName = os.path.basename(pyFile).replace('.py', '')
			jsonFile = os.path.join('..', 'plugins_desc', pl_dir, '%s.json' % modName)
			if not os.path.exists(jsonFile):
				missing_json.append(pyFile)
				# print('Missing json %s \t->\t %s' % (pyFile, jsonFile))
				continue

			pyJson = None
			jsJson = ordered(json.loads(open(jsonFile, 'r').read())['Widget'])
			# print('Checking %s' % pyFile)

			lastE = None
			while True:
				try:
					mod = SourceFileLoader(modName, pyFile).load_module()
					if not hasattr(mod, 'PluginWidget'):
						break
					pyJson = ordered(json.loads(mod.PluginWidget))
				except ImportError as e:
					if e.name:
						fakePy = '%s.py' % e.name
						open(fakePy, 'w+').write(' ')
						fake_files.append(fakePy)
						# print('Making fake %s' % fakePy)
					# else:
					# 	print(e.args, '!', e.name, '!', e.path, pyFile)
					if str(e) == str(lastE):
						manual_check.append(pyFile)
						break
					lastE = e
					continue
				except AttributeError as e:
					break
				break

			if not pyJson or subset(pyJson, jsJson):
				pass
			else:
				missmatch_json.append(pyFile)
				# print('Missmatch for for %s' % pyFile)
				# print(json.dumps(jsJson, indent=2), json.dumps(pyJson, indent=2))


print('Manual check these:')
for m in manual_check:
	print('\t', m)

print('\nMissing json for these:')
for m in missing_json:
	print('\t', m)

print('\nNon matching json for these:')
for m in missmatch_json:
	print('\t', m)


shutil.move('textures', 'texture')
fake_dirs.reverse()
for f in fake_files:
	try:
		os.remove(f)
	except:
		pass

for f in fake_dirs:
	try:
		shutil.rmtree(f)
	except:
		pass
