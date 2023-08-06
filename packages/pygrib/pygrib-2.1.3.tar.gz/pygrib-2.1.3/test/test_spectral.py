import matplotlib
import pytest
import matplotlib.pyplot as plt
import pygrib
import numpy as np
from cartopy.util import add_cyclic_point
import cartopy.crs as ccrs
try:
    import spharm
except:
    print("skipping test that requires pyspharm (python spherical harmonic module) from http://code.google.com/p/pyspharm")
    raise SystemExit(0)

grbs = pygrib.open('../sampledata/spherical_pressure_level.grib1')
g = grbs[1]
fld = g.values

# ECMWF normalizes the spherical harmonic coeffs differently than NCEP.
# (m=0,n=0 is global mean, instead of sqrt(2)/2 times global mean)
fld = 2.*fld/np.sqrt(2.)
fldr = fld[0::2]
fldi = fld[1::2]
fld = np.zeros(fldr.shape,'F')
fld.real = fldr
fld.imag = fldi
nlons = 360;  nlats = 181
s = spharm.Spharmt(nlons,nlats)
data = s.spectogrd(fld)
lons = (360./nlons)*np.arange(nlons)
lats = 90.-(180./(nlats-1))*np.arange(nlats)
# add cyclic (wrap-around) point to global grid
data,lons = add_cyclic_point(data, coord=lons)
lons,lats = np.meshgrid(lons, lats)

@pytest.mark.mpl_image_compare(tolerance=20,remove_text=True)
def test_spectral():
    # setup mercator map projection.
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.Mercator(central_longitude=0))
    cs = ax.contourf(lons,lats,data,15,cmap=plt.cm.jet,transform=ccrs.PlateCarree())
    ax.coastlines()
    gl = ax.gridlines(draw_labels=True)
    gl.ylabels_top = False; gl.xlabels_top = False
    gl.ylabels_right = False; gl.xlabels_right = False
    plt.colorbar(cs,shrink=0.9)
    plt.title(repr(g.level)+' '+g.typeOfLevel+' '+g.name+' from Spherical Harmonic Coeffs',fontsize=9)
    return fig

# if running with GUI backend, show plot.
if matplotlib.get_backend().lower() != 'agg':
    test_spectral()
    plt.show()
