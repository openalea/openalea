// -*-c++-*- 
/*
#define EXPORT_DLL(NAME) 
#ifdef WIN32 \
#ifdef NAME##_DLL \
#define NAME##_EXPORT __declspec(dllexport) \
#else \
#define NAME##_EXPORT __declspec(dllimport) \
#endif \
#else \
#define  NAME##_EXPORT \
#endif \

EXPORT_DLL(SCENEOBJ)
EXPORT_DLL(SCENECONT)
*/

#ifdef WIN32
#ifdef SCENEOBJ_DLL 
#define SCENEOBJ_EXPORT __declspec(dllexport) 
#else 
#define SCENEOBJ_EXPORT __declspec(dllimport) 
#endif
#else 
#define  SCENEOBJ_EXPORT 
#endif 

#ifdef WIN32 
#ifdef SCENECONT_DLL
#define SCENECONT_EXPORT __declspec(dllexport)
#else 
#define SCENECONT_EXPORT __declspec(dllimport) 
#endif
#else 
#define  SCENECONT_EXPORT 
#endif 

