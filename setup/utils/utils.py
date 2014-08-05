import os.path

# returns true if the data for the given package has been downloaded
def data_downloaded(package):
  return os.path.isdir(data_dir(package))

# Given a path, returns a list of its components.
# Joining with os.sep should give a valid path
def path_components(path):
  comps = os.path.normpath(path.strip()).split(os.sep)
  if comps[0] == '':
    del comps[0]
    comps[0] = "/" + comps[0]
  return comps

# Given a package name, returns the data directory containing that
# package's data files
def data_dir(package):
  (path, _) = os.path.split(os.path.realpath(__file__))
  return os.sep.join(path_components(path) + [package])

# loads a file into a 2d array
def load_file(package, filename, cols, delim="\t", comment=""):
  lines = []
  f = os.sep.join([data_dir(package),filename])
  with open(f,'rU') as f:
    for l in f:
      if l[0] == comment: continue
      data = l.split(delim)
      line = []
      for col in cols: line.append(data[col])
      lines.append(line)
  return lines 
