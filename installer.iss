; Amar Bangla Keyboard - Inno Setup script
; Build:  "C:\Users\<you>\AppData\Local\Programs\Inno Setup 6\ISCC.exe" installer.iss
; Output: installer\AmarBanglaKeyboard-Setup-<version>.exe

#define MyAppName "Amar Bangla Keyboard"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Amar Bangla"
#define MyAppURL "https://amarbangla.in"
#define MyAppExeName "Amar Bangla Keyboard.exe"
#define MyAppMutex "AmarBanglaKeyboard_SingleInstance"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
VersionInfoVersion={#MyAppVersion}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
AllowNoIcons=yes
; No admin needed by default; user can pick "install for all users" in the dialog.
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesInstallIn64BitMode=x64compatible
; Close a running copy before install/uninstall using the app's single-instance mutex.
AppMutex={#MyAppMutex}
CloseApplications=yes
RestartApplications=no
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
OutputDir=installer
OutputBaseFilename=AmarBanglaKeyboard-Setup-{#MyAppVersion}
SetupIconFile=assets\amar_bangla_keyboard_logo.ico
UninstallDisplayName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon";    Description: "{cm:CreateDesktopIcon}";  GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "autostart";      Description: "Start {#MyAppName} automatically when I log in"; GroupDescription: "Startup:"

[Files]
Source: "dist\{#MyAppExeName}";                     DestDir: "{app}"; Flags: ignoreversion
Source: "assets\amar_bangla_keyboard_logo.ico";     DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}";  Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
; Optional auto-start entry (per user).
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
    ValueType: string; ValueName: "AmarBanglaKeyboard"; \
    ValueData: """{app}\{#MyAppExeName}"""; \
    Tasks: autostart; Flags: uninsdeletevalue

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
Type: filesandordirs; Name: "{userappdata}\{#MyAppName}"
