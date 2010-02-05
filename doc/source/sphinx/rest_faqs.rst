The link do not appear correctly when using :class: directive
=============================================================


For simplcity, let us consider the case of the function `openalea.stat_too.output.Display`.

The first reason may be that you are using :class: whereas you should use :func:  or another directive.

The second reason is that within all your reST files, you have not defined the module openalea.stat_tool.output: Another reason is that you defined it with the wrong namespace. For instance vplants.stat_tool.output and later on you try to refer to openalea.stat_tool.output.


