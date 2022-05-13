from django.test import TestCase

# Create your tests here.
import matplotlib.path as mplPath
import numpy as np

a = [[0,832],[516,35],[904,37],[1486,710], [1482,830]]
bbPath = mplPath.Path(np.array([[a[0], a[1]],
[a[1], a[2]],
[a[2], a[3]],
[a[3], a[0]]]))

bbPath.contains_point((200, 100))