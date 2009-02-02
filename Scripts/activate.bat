@echo off
set VIRTUAL_ENV=C:\openalea_test2

if not defined PROMPT (
    set PROMPT=$P$G
)

if defined _OLD_VIRTUAL_PROMPT (
    set PROMPT=%_OLD_VIRTUAL_PROMPT%
)

set _OLD_VIRTUAL_PROMPT=%PROMPT%
set PROMPT=(openalea_test2) %PROMPT%

if defined _OLD_VIRTUAL_PATH (
    set PATH=%_OLD_VIRTUAL_PATH%
    goto SKIPPATH
)
set _OLD_VIRTUAL_PATH=%PATH%

:SKIPPATH
set PATH=%VIRTUAL_ENV%\\Scripts;%PATH%

:END
