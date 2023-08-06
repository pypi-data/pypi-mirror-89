Calendar heatmaps from Pandas time series data
==============================================

Calplot creates heatmaps from Pandas time series data.

Plot `Pandas <http://pandas.pydata.org/>`_ time series data sampled by day in
a heatmap per calendar year, similar to GitHub's contributions plot, using
`matplotlib <http://matplotlib.org/>`_.

.. image:: https://raw.githubusercontent.com/tomkwok/calplot/master/calplot_edgecolor_default.png
    :alt: Example calendar heatmap with default edgecolor

.. image:: https://raw.githubusercontent.com/tomkwok/calplot/master/calplot_edgecolor_None.png
    :alt: Example calendar heatmap with edgecolor set to None

Package `calplot <https://pypi.org/project/calplot/>`_ is a fork of `calmap <https://github.com/martijnvermaat/calmap>`_ with the following changes and additions.

- (Since version 0.1.5) Added argument :code:`edgecolor` for function :code:`calplot` and :code:`yearplot` to specify color of seperation lines between months. Defaults to :code:`gray`. Note that lines can be turned off by setting argument to :code:`None` without quotes.
- (Since version 0.1.4) :code:`pandas>=1.1` is now required to install the package. Legacy code for compatibility removed. Fixed a FutureWarning in :code:`yearplot`.
- (Since version 0.1.2) Added argument :code:`dropzero` for function :code:`calplot` and :code:`yearplot` to specify whether to not fill a cell with a color for days with a zero value. Defaults to :code:`True`.
- (Since version 0.1.1) Renamed function :code:`calendarplot` to :code:`calplot`.
- (Since version 0.1.1) Added argument :code:`colorbar` for function :code:`calplot` to display a colorbar to the right of the heatmap if more than one unique values in plot. Defaults to :code:`True`.
- (Since version 0.1.1) Added argument :code:`figsize` for function :code:`calplot`. Defaults to a tighter layout automatically adjusted to fit the number of years in plot.
- (Since version 0.1.1) Added argument :code:`suptitle` for function :code:`calplot`. Defaults to :code:`None`.
- (Since version 0.1.1) Added argument :code:`yearcolor` for function :code:`calplot`. Defaults to :code:`lightgray`. Note that the default color is in contrast to :code:`whitesmoke`, which is the default value for :code:`fillcolor`.
- (Since version 0.1.1) Added argument :code:`monthlabelha` for function :code:`calplot` and :code:`yearplot` to specify horizontal alignment for month labels. Defaults to :code:`center`.
- (Since version 0.1.1) Changed default colormap :code:`cmap` for function :code:`calplot` to :code:`viridis`.

Usage
-----

See the `documentation <https://calplot.readthedocs.io/en/latest/>`_.


Installation
------------

To install the latest release via PyPI using pip::

    pip install calplot

Todo
----

- Option to plot a rounded value for the day, or to plot the day of month for each mesh grid cell.
