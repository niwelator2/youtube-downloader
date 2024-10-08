#define MyAppName "Youtube-downloader"
#define MyAppVersion "2.3"
#define MyAppPublisher "niwelator2"
#define MyAppURL "https://gitlab.com/niwelator2/youtube-downloader"
#define MyAppExeName "Youtube-Downloader.exe"


[Setup]
AppId={{7203776C-FF1C-414E-86C4-A14E83C4873E}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=C:\Users\Pilif\Documents\youtube-downloader\license.txt
OutputDir=C:\Users\Pilif\Documents\youtube-downloader\windows
OutputBaseFilename=Youtube-Downloader.2.3_setup
SetupIconFile=src\gui\icon\logo.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\Pilif\Documents\youtube-downloader\windows\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Pilif\Documents\youtube-downloader\venv\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Pilif\Documents\youtube-downloader\src\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Pilif\Documents\youtube-downloader\src\gui\icon\*"; DestDir: "{app}\gui\src\icon"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
