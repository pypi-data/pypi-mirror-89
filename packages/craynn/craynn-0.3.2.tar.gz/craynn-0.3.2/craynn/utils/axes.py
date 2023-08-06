__all__ = [
  'normalize_split_axes',
  'normalize_split_shape',
  'normalize_axis',
  'gsum'
]

def normalize_axis(tensor_or_dim, axis):
  if isinstance(tensor_or_dim, int):
    dim = tensor_or_dim
  elif isinstance(tensor_or_dim, tuple):
    dim = len(tensor_or_dim)
  else:
    dim = len(tensor_or_dim.shape)

  if isinstance(axis, int):
    return axis % dim
  else:
    return tuple(a % dim for a in axis)

def normalize_split_axes(shape_or_dim, axes):
  if isinstance(shape_or_dim, int):
    dim = shape_or_dim
  else:
    dim = len(shape_or_dim)

  if isinstance(axes, int):
    axes = (axes, )

  normalized = tuple(axis % dim for axis in axes)

  rest = tuple(
    axis
    for axis in range(dim)
    if axis not in normalized
  )

  return normalized, rest

def normalize_split_shape(shape, axes):
  selected, rest = normalize_split_axes(shape, axes)
  return tuple(
    shape[axis]
    for axis in selected
  ), tuple(
    shape[axis]
    for axis in rest
  )

def gsum(xs):
  acc = 0
  for x in xs:
    if x is None:
      return None
    else:
      acc += x

  return acc