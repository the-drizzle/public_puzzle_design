import numpy as np
import matplotlib.pyplot as plt


# static (affine) rotations about x0, x2 and x0 (resp.)
# could have skipped the affine part since the rotations
# are all about the origin, but this allows for quicker
# expansion into more elaborate schemes.
t0 = np.pi / 4
t1 = np.pi / 2

T0 = np.array([
    [1,          0,           0, 0],
    [0, np.cos(t0), -np.sin(t0), 0],
    [0, np.sin(t0),  np.cos(t0), 0],
    [0,          0,           0, 1]])

T1 = np.array([
    [np.cos(t1), -np.sin(t1), 0, 0],
    [np.sin(t1),  np.cos(t1), 0, 0],
    [         0,           0, 1, 0],
    [         0,           0, 0, 1]])

T2 = np.array([
    [1,          0,           0, 0],
    [0, np.cos(t1), -np.sin(t1), 0],
    [0, np.sin(t1),  np.cos(t1), 0],
    [0,          0,           0, 1]])

class RhomDoCuts(object):
    __doc__ = '''
        Parameters:
        -----------
            parabolic sheet defined by:

                f(x) = (x0, x1, a * (x0 ** 2 + x1 ** 2) + b), a >= 0

            R : float
                edge length of face (default=1)
        '''

    def __init__(self, a, b, R=1):
        if a < 0:
            raise ValueError('a must be positve for this to make sense')

        self.a = a
        self.b = b
        self.R = R

    def plot_cuts(self, **kwargs):
        '''
        vis convenience method
        '''
        sq_outline = np.array([
            [-self.R/2, -self.R/2],
            [ self.R/2, -self.R/2],
            [ self.R/2,  self.R/2],
            [-self.R/2,  self.R/2],
            [-self.R/2, -self.R/2]])

        cuts = self._get_cuts(**kwargs)

        fig, ax = plt.subplots(figsize=(4, 4))
        for i, value in enumerate(cuts.values()):
            for val in value.values():
                ax.plot(val[:, 1], val[:, 2], color='k', lw=1)#, color='gray', lw=2, alpha=0.4)

        ax.plot(sq_outline[:, 0], sq_outline[:, 1], color='k', lw=1)
        plt.title('a = {0:.3f}, b = {1:.3f}'.format(self.a, self.b))
        ax.axis('off')
        plt.show()

    def _get_cuts(self, **kwargs):
        '''
        un-necessarily large, method to get point arrays to plot.
        '''
        return {
            'intersecting_face_cut' : {
                0 : self._intersecting_face_cut(**kwargs),
                1 : np.vstack([T2 @ x for x in self._intersecting_face_cut(**kwargs)]),
                2 : np.vstack([T2 @ T2 @ x for x in self._intersecting_face_cut(**kwargs)]),
                3 : np.vstack([T2 @ T2 @ T2 @ x for x in self._intersecting_face_cut(**kwargs)])
            },
            'parallel_face_cut' : {
                0 : self._parallel_face_cut(**kwargs),
                1 : np.vstack([T2 @ x for x in self._parallel_face_cut(**kwargs)]),
                2 : np.vstack([T2 @ T2 @ x for x in self._parallel_face_cut(**kwargs)]),
                3 : np.vstack([T2 @ T2 @ T2 @ x for x in self._parallel_face_cut(**kwargs)])
            }
        }

    def _intersecting_face_cut(self, pts=1000):
        X = np.linspace(-self.R/2, self.R/2, pts)
        temp =  np.vstack([self._solve_intersection(x) for x in X])

        # rotate into view
        return np.vstack([T1 @ T0 @ x for x in temp])

    def _parallel_face_cut(self, pts=1000):
        p = np.abs(self._solve_intersection(self.R/2)[1])
        X = np.linspace(-p, p, pts)

        temp = np.vstack([(self.R/2, x, self.a * ((self.R/2) ** 2 + x ** 2) + self.b, 1) for x in X])

        # rotate into view
        return np.vstack([T0 @ x for x in temp])

    def _solve_intersection(self, x0):
        r = self.R * np.sqrt(2) / 2
        z = np.roots((self.a, -1, (self.a * x0 ** 2) + self.b - r))

        # only want the result in [-R/2 , 0]
        x1 = z.min()
        x2 = x1 + r

        return np.array((x0, x1, x2, 1))

# # examples:
# # helicopter cube
# RhomDoCuts(0, np.sqrt(2) / 4).plot_cuts()

# # cubic realisation of toru puzzle:
# RhomDoCuts(0, np.sqrt(2) / 8).plot_cuts()

# # cubic toru puzzle, more or less
# a = 1.5
# b = (4 * np.sqrt(2) - 6 * a) / 16
# RhomDoCuts(a, b).plot_cuts()

# # stable cubic realisation of a toru puzzle:
# a = 7 * np.sqrt(2) / 33
# b = (6 * np.sqrt(2) - 17 * a) / 36
# RhomDoCuts(a, b).plot_cuts()

# # something new, 3 equal edge divisions and deeper
# a = 3 * np.sqrt(2)  / 4
# b = (6 * np.sqrt(2) - 17 * a) / 36
# RhomDoCuts(a, b).plot_cuts()
