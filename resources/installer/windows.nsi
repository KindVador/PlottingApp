!include MUI2.nsh
!include FileFunc.nsh

;--------------------------------
;Perform Machine-level install, if possible

!define MULTIUSER_EXECUTIONLEVEL Highest
;Add support for command-line args that let uninstaller know whether to
;uninstall machine- or user installation:
!define MULTIUSER_INSTALLMODE_COMMANDLINE
!include MultiUser.nsh
!include LogicLib.nsh

!define APP_NAME "PlottingApp"

Function .onInit
  !insertmacro MULTIUSER_INIT
  ;Do not use InstallDir at all so we can detect empty $InstDir!
  ${If} $InstDir == "" ; /D not used
      ${If} $MultiUser.InstallMode == "AllUsers"
          StrCpy $InstDir "$PROGRAMFILES\${APP_NAME}"
      ${Else}
          StrCpy $InstDir "$LOCALAPPDATA\${APP_NAME}"
      ${EndIf}
  ${EndIf}
FunctionEnd

Function un.onInit
  !insertmacro MULTIUSER_UNINIT
FunctionEnd

;--------------------------------
;General

  Name "${APP_NAME}"
  OutFile "..\..\dist\${APP_NAME}Installer.exe"

;--------------------------------
;Interface Settings

  ; display a warning to user if installer window is closed using the red cross button (upper right of the window)
  !define MUI_ABORTWARNING

;--------------------------------
;Pages

  ; install pages
  !define MUI_WELCOMEPAGE_TEXT "This wizard will guide you through the installation of ${APP_NAME}.$\r$\n$\r$\n$\r$\nClick Next to continue."
  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_LICENSE "..\..\license.txt"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
    !define MUI_FINISHPAGE_NOAUTOCLOSE
    !define MUI_FINISHPAGE_RUN
    !define MUI_FINISHPAGE_RUN_CHECKED
    !define MUI_FINISHPAGE_RUN_TEXT "Run ${APP_NAME}"
    !define MUI_FINISHPAGE_RUN_FUNCTION "LaunchLink"
  !insertmacro MUI_PAGE_FINISH

  ; uninstall pages
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

!define UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"

Section "Main Tool Section" MainSection
  SetOutPath "$InstDir"
  File /r "..\..\dist\${APP_NAME}\*"
  WriteRegStr SHCTX "Software\${APP_NAME}" "" $InstDir
  WriteUninstaller "$InstDir\uninstall.exe"
  CreateShortCut "$SMPROGRAMS\${APP_NAME}.lnk" "$InstDir\${APP_NAME}.exe"
  WriteRegStr SHCTX "${UNINST_KEY}" "DisplayName" "${APP_NAME}"
  WriteRegStr SHCTX "${UNINST_KEY}" "UninstallString" "$\"$InstDir\uninstall.exe$\" /$MultiUser.InstallMode"
  WriteRegStr SHCTX "${UNINST_KEY}" "QuietUninstallString" "$\"$InstDir\uninstall.exe$\" /$MultiUser.InstallMode /S"
  WriteRegStr SHCTX "${UNINST_KEY}" "Publisher" "${author}"
  ${GetSize} "$InstDir" "/S=0K" $0 $1 $2
  IntFmt $0 "0x%08X" $0
  WriteRegDWORD SHCTX "${UNINST_KEY}" "EstimatedSize" "$0"

SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_MainSection $\{LANG_ENGLISH} "TODO put the right description for the Main App Section"

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${MainSection} $(DESC_MainSection) 
  !insertmacro MUI_FUNCTION_DESCRIPTION_END


;--------------------------------
;Uninstaller Section

Section "Uninstall"

  RMDir /r "$InstDir"
  Delete "$SMPROGRAMS\${APP_NAME}.lnk"
  DeleteRegKey /ifempty SHCTX "Software\${APP_NAME}"
  DeleteRegKey SHCTX "${UNINST_KEY}"

SectionEnd

Function LaunchLink
  !addplugindir "."
  ;ShellExecAsUser::ShellExecAsUser "open" "$SMPROGRAMS\${APP_NAME}.lnk"
  ExecShell "" "$SMPROGRAMS\${APP_NAME}.lnk"
FunctionEnd