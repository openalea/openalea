



from setuptools import setup


setup( name = "Visualea Extension",
       version = "0.1",
       py_modules = ['visualeapg'],
       entry_points = {"openalea.app.layout":["visualea.df1 = visualeapg:df1",
                                              "visualea.df2 = visualeapg:df2"],
                       "openalea.app.singleton_view":["visualea.pm = visualeapg:pmanager_f",
                                                      "visualea.lo = visualeapg:logger_f"],
                       "openalea.app.data_editor":["Visualea.oa = visualeapg:dataflow_f"],
                       "openalea.ext":["Visualea = visualeapg.visualea"]
                       }
    )
