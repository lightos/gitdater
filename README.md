# gitdater
Small Python script that recursively runs "git pull" on all folders containing a ".git" directory. To use, just place in the root folder containing the GIT projects you would like to update and run "python gitdater.py".


### Sample Output From "Pentesting Tools" Folder:

	".\credmap" has git dir: "['.git', 'lib', 'output', 'thirdparty', 'websites']"
	Checking for updates...
	Already at the latest revision 'f28e46e'.

	".\ntdsxtract" has git dir: "['.git', 'framework', 'ntds']"
	Checking for updates...
	Updated to the latest revision '7fa1c8c'.

	".\ntds_decode" has git dir: "['.git']"
	Checking for updates...
	Already at the latest revision '080edf2'.

	".\Panoptic" has git dir: "['.git', 'output', 'thirdparty']"
	Checking for updates...
	Already at the latest revision 'b5eae6b'.

	".\post-exploitation-wiki" has git dir: "['.git', 'images', 'linux', 'mdwiki-0.5.8', 'mobile', 'msf', 'osx', 'otheros', 'references', 'scripting', 'windows']"
	Checking for updates...
	Updated to the latest revision 'fa54cab'.

	".\PowerSploit" has git dir: "['.git', 'AntivirusBypass', 'CodeExecution', 'Exfiltration', 'Mayhem', 'Persistence', 'Privesc', 'Recon', 'ScriptModification', 'Tests']"
	Checking for updates...
	Updated to the latest revision '262a260'.

	".\quickjack" has git dir: "['.git']"
	Checking for updates...
	Updated to the latest revision 'eb3263f'.

	".\Responder-Windows" has git dir: "['.git', 'binaries', 'src']"
	Checking for updates...
	Already at the latest revision '4027c1a'.

	".\RFIDler" has git dir: "['.git', 'datasheets', 'firmware', 'Hardware', 'linux-support', 'python', 'windows driver', 'windows-src']"
	Checking for updates...
	Updated to the latest revision '66e8715'.

	".\smbexec" has git dir: "['.git', 'certs', 'lib', 'patches', 'powershell', 'progs', 'sources']"
	Checking for updates...
	Already at the latest revision '7827616'.

	".\smbmap" has git dir: "['.git']"
	Checking for updates...
	Already at the latest revision '57b0176'.

	".\sqlmap" has git dir: "['.git', 'doc', 'extra', 'lib', 'plugins', 'procs', 'shell', 'tamper', 'thirdparty', 'txt', 'udf', 'waf', 'xml']"
	Checking for updates...
	Updated to the latest revision '7cca56e'.

	".\UACME" has git dir: "['.git', 'Compiled', 'Source']"
	Checking for updates...
	Updated to the latest revision 'b908d03'.

	".\unicorn" has git dir: "['.git']"
	Checking for updates...
	Updated to the latest revision 'c44044f'.

	".\Vulndev" has git dir: "['.git', 'MS14-012', 'MS14-070']"
	Checking for updates...
	Updated to the latest revision 'e737104'.
