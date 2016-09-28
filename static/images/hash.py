import hashlib
albumid = 30
filename = 'world_Washington.jpg'
m = hashlib.md5()
m.update(str(albumid))
m.update(filename)
print m.hexdigest()
