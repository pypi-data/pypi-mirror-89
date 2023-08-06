
from .file import SRTM1_DIR_CNAME, SAMPLES, ElevationSupport, elevation_from_constant


def bilinear_elevation_from_constant(s, dir_name=SRTM1_DIR_CNAME):
    return elevation_from_constant(s, BilinearElevation, dir_name=dir_name)


class BilinearElevation(ElevationSupport):
    '''
    Provide elevation data from the files in `dir` which should be hgt files with standard naming,
    either zipped or unzipped, downloaded from http://dwtkns.com/srtm30m/.

    You can download *all* data by going to https://search.earthdata.nasa.gov/search?q=srtm%20v3 and
    selecting 'NASA Shuttle Radar Topography Mission Global 1 arc second V003'.  That will lead to
    a download page that provides a further links to a list of links and a download script.  Running
    the download script downloads the links.  You need to register.

    All coords are "GPS coords" afaict.

    If dir is None then None will be return as elevation for all queries.

    If dir is not None and a file is missing for a particular lat/lon then an exception is raised.

    Elevations are bilinear interpolated from the surrounding arcsec grid.
    '''

    def elevation(self, lat, lon):
        if self._dir:
            flat, flon, h = self._lookup(lat, lon)
            x = (lon - flon) * (SAMPLES - 1)
            y = (lat - flat) * (SAMPLES - 1)  # -1 because weird inclusive-at-each-side tiling
            i, j = int(x), int(y)
            # bilinear
            # it's ok to use +1 blindly here because we're never on the top/right cells or we'd be in
            # a different tile.
            k = y - j
            h0 = h[j, i] * (1-k) + h[j+1, i] * k
            h1 = h[j, i+1] * (1-k) + h[j+1, i+1] * k
            k = x - i
            return h0 * (1-k) + h1 * k
        else:
            return None
