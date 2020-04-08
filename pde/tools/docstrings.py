'''
Created on Mar 21, 2020

.. codeauthor:: David Zwicker <david.zwicker@ds.mpg.de>
'''

import textwrap
import re
from typing import TypeVar



DOCSTRING_REPLACEMENTS = {
    # description of function arguments
    '{ARG_BOUNDARIES_INSTANCE}': """
        Specifies the boundary conditions applied to the field. This must be an
        instance of :class:`~pde.grids.boundaries.axes.Boundaries`, which can be
        created from various data formats using the class method
       :func:`~pde.grids.boundaries.axes.Boundaries.from_data`."""[1:],
       
    '{ARG_BOUNDARIES}': """
        Boundary conditions are generally given as a list with one condition for
        each axis. For periodic axis, only periodic boundary conditions are
        allowed (indicated by 'periodic'). For non-periodic axes, different 
        boundary conditions can be specified for the lower and upper end (by a
        tuple of two conditions). For instance, Dirichlet conditions enforcing a
        value NUM (specified by `{'value': NUM}`) and Neumann conditions 
        enforcing the value DERIV for the derivative in the normal direction
        (specified by `{'derivative': DERIV}`) are supported.Note that the
        special value 'natural' imposes periodic boundary conditions for
        periodic axis and a vanishing derivative otherwise. More information can
        be found in the
        :ref:`boundaries documentation <documentation-boundaries>`."""[1:],

    '{ARG_TRACKER_INTERVAL}': """
        Determines how often the tracker interrupts the simulation. Simple
        numbers are interpreted as durations measured in the simulation time
        variable. Alternatively, a string using the format 'hh:mm:ss' can be
        used to give durations in real time. Finally, instances of the classes
        defined in :mod:`~pde.trackers.intervals` can be given for more control.
        """[1:-1],
        
    '{ARG_PLOT_QUANTITIES}': """
        A 2d list of quantities that are shown in a rectangular arrangement.
        If `quantities` is a simple list, the panels will be rendered as a
        single row.
        Each panel is defined by a dictionary, where the mandatory item 'source'
        defines what is being shown. Here, an integer specifies the component
        that is extracted from the field while a function is evaluate with the
        full state as an input and the result is shown.
        Additional items in the dictionary can be 'title' (setting the title of
        the panel), 'scale' (defining the color range shown; these are typically
        two numbers defining the lower and upper bound, but if only one is given
        the range [0, scale] is assumed), and 'cmap' (defining the colormap
        being used)."""[1:],
        
    '{ARG_PLOT_SCALE}': """
        Flag determining how the range of the color scale is determined. In the
        simplest case a tuple of numbers marks the lower and upper end of the 
        scalar values that will be shown. If only a single number is supplied,
        the range starts at zero and ends at the given number. Additionally, the
        special value 'automatic' determines the range from the range of scalar
        values."""[1:-1],
    
    # descriptions of the discretization and the symmetries         
    '{DESCR_CYLINDRICAL_GRID}': r"""
        The cylindrical grid assumes polar symmetry, so that fields only depend
        on the radial coordinate `r` and the axial coordinate `z`. Here, the
        first axis is along the radius, while the second axis is along the axis
        of the cylinder. The radial discretization is defined as
        :math:`r_i = (i + \frac12) \Delta r` for :math:`i=0, \ldots, N_r-1`.
        """[1:-1],
        
    '{DESCR_POLAR_GRID}': r"""
        The polar grid assumes polar symmetry, so that fields only depend on the
        radial coordinate `r`. The radial discretization is defined as
        :math:`r_i = r_\mathrm{min} + (i + \frac12) \Delta r` for
        :math:`i=0, \ldots, N_r-1`,  where :math:`r_\mathrm{min}` is the radius
        of the inner boundary, which is zero by default. Note that the radius of
        the outer boundary is given by
        :math:`r_\mathrm{max} = r_\mathrm{min} + N_r \Delta r`."""[1:],
        
    '{DESCR_SPHERICAL_GRID}': r"""
        The spherical grid assumes spherical symmetry, so that fields only
        depend on the radial coordinate `r`. The radial discretization is
        defined as :math:`r_i = r_\mathrm{min} + (i + \frac12) \Delta r` for
        :math:`i=0, \ldots, N_r-1`,  where :math:`r_\mathrm{min}` is the radius
        of the inner boundary, which is zero by default. Note that the radius of
        the outer boundary is given by
        :math:`r_\mathrm{max} = r_\mathrm{min} + N_r \Delta r`."""[1:],
        
    # notes in the docstring
    '{WARNING_EXEC}': r"""
        This implementation uses :func:`exec` and should therefore not be used 
        in a context where malicious input could occur."""[1:]
}



TFunc = TypeVar('TFunc')


def fill_in_docstring(f: TFunc) -> TFunc:
    """ decorator that replaces text in the docstring of a function """
    # initialize textwrapper for formatting docstring
    tw = textwrap.TextWrapper(width=80, expand_tabs=True,
                              replace_whitespace=True, drop_whitespace=True)
            
    docstring = f.__doc__
    for token, value in DOCSTRING_REPLACEMENTS.items():
        
        def repl(matchobj) -> str:
            """ helper function replacing token in docstring """
            tw.initial_indent = tw.subsequent_indent = matchobj.group(1)
            return tw.fill(textwrap.dedent(value))

        # replace the token with the correct indentation
        docstring = re.sub(f"^([ \t]*){token}", repl, docstring,  # type: ignore
                           flags=re.MULTILINE)

    f.__doc__ = docstring
    return f
