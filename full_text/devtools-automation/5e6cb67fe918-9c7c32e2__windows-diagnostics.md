---
name: windows-diagnostics
description: Operate Sysinternals and NirSoft CLI tools for Windows diagnostics and operations. Use when asked to investigate processes, memory, network connections, disk usage, registry, system info, remote admin, or Active Directory on a live Windows system using these specific toolsets. Example triggers: "what process is locking this file", "triage unknown network connection", "find memory leak", "check autoruns for suspicious entries". Do not use for general code debugging, application development, or non-Windows systems.
---

# Windows Diagnostics & Operations

This skill gives the agent a complete reference for invoking Sysinternals and NirSoft tools
present in the working directory. Tools live under two subfolders:

- `./systeminternals/` — Sysinternals Suite
- `./nirsoft/` — NirSoft utilities

Always prefer the 64-bit variant (e.g. `procexp64.exe`) where available; fall back to the
32-bit variant silently when no 64-bit binary exists. Never rely on PATH — always use
explicit relative paths from the working directory.


## Agent Workflow

For every request, follow this decision sequence in order.

1. **Validate tool availability**: Before constructing any command, verify the tool exists:

```powershell
# Check 64-bit tool first, fall back to 32-bit
$tool64 = "./systeminternals/procexp64.exe"
$tool32 = "./systeminternals/procexp.exe"

if (Test-Path $tool64) {
    $tool = $tool64
} elseif (Test-Path $tool32) {
    $tool = $tool32
    Write-Warning "Using 32-bit variant: procexp.exe"
} else {
    Write-Error "Tool not found: procexp64.exe. Alternative: ProcessActivityView.exe (NirSoft)"
    exit 1
}
```

If missing, report to user and suggest alternatives from the same capability domain.

2. **Classify the request** into one of the capability domains: Process & Memory, Network & Traffic,
   Disk & File System, Registry, System Info & Security, Monitoring & Logging,
   Remote & Admin Operations, or Active Directory.

3. **Select the minimum viable tool(s)** for the task. Do not load more tools than needed.

4. **Prefer read-only and non-destructive tools first**. Escalate to mutating tools only when
   the user explicitly instructs it.

5. **Construct the exact command** with full argument list using the rules in
   "Command Construction Rules" below.

6. **Execute and handle errors**: If the tool fails (access denied, missing dependencies, crash),
   consult the "Error Handling" section below for fallback strategies.

7. **Parse and summarise output**. Flag anomalies. Do not dump raw output.

8. **If the task requires chaining tools**, specify the order and what data passes between steps.
   Use the recipes in "Chaining Recipes" as templates.

Hard rule: never run `notmyfault64.exe`, `Testlimit64.exe` with extreme resource limits,
or `CPUSTRES64.exe` without explicit user confirmation in the same conversation turn.
State the risk before asking.


## Tool Selection

For detailed tool specifications (flags, output formats, prerequisites, chaining notes, and examples),
see individual tool files in `tools/` or browse the organized index at `references/tool-catalog.md`.

The catalog organizes 80+ tools into 8 capability domains:

### A. Process & Memory
- [procexp64.exe](tools/procexp64-exe.md) — Interactive process explorer with full process tree, DLL, and handle detail
- [Procmon64.exe](tools/Procmon64-exe.md) — Real-time file system, registry, and process/thread activity monitor
- [procdump64.exe](tools/procdump64-exe.md) — Capture process memory dumps on trigger conditions (CPU spike, crash, hang)
- [pslist64.exe](tools/pslist64-exe.md) — List running processes with CPU and memory stats
- [pskill64.exe](tools/pskill64-exe.md) — Terminate a process by name or PID
- [pssuspend64.exe](tools/pssuspend64-exe.md) — Suspend or resume a process without terminating it
- [handle64.exe](tools/handle64-exe.md) — Show open file, registry, and object handles for all or specific processes
- [vmmap64.exe](tools/vmmap64-exe.md) — Visualise virtual memory layout of a process
- [RAMMap64.exe](tools/RAMMap64-exe.md) — Physical memory usage breakdown by type (file, heap, standby, etc.)
- [Listdlls.exe](tools/Listdlls-exe.md) — List DLLs loaded by processes, including unsigned or unsigned-path DLLs
- [ProcessActivityView.exe](tools/ProcessActivityView-exe.md) — Show file and registry activity of a running process
- [ProcessThreadsView.exe](tools/ProcessThreadsView-exe.md) — Display threads of a process with start address and module info
- [HeapMemView.exe](tools/HeapMemView-exe.md) — Display heap memory blocks allocated by a process
- [GDIView.exe](tools/GDIView-exe.md) — Monitor GDI object usage per process to detect GDI handle leaks
- [Cacheset64.exe](tools/Cacheset64-exe.md) — View and adjust the system file cache working set size
- [CPUSTRES64.exe](tools/CPUSTRES64-EXE.md) — Stress CPU threads to test thermal and stability limits
- [shmnview.exe](tools/shmnview-exe.md) — Display shared memory sections and the processes accessing them

### B. Network & Traffic
- [tcpvcon64.exe](tools/tcpvcon64-exe.md) — List active TCP and UDP connections with owning process
- [tcpview64.exe](tools/tcpview64-exe.md) — Interactive GUI network connection viewer with real-time updates
- [psping64.exe](tools/psping64-exe.md) — Measure TCP/UDP latency and bandwidth; ICMP ping with statistics
- [whois64.exe](tools/whois64-exe.md) — WHOIS lookup for IP addresses and domain names
- [cports.exe](tools/cports-exe.md) — Display open TCP/UDP ports with process and module info
- [NetworkTrafficView.exe](tools/NetworkTrafficView-exe.md) — Capture and display network traffic statistics per connection
- [smsniff.exe](tools/smsniff-exe.md) — Packet sniffer that captures raw network packets
- [WebSiteSniffer.exe](tools/WebSiteSniffer-exe.md) — Capture HTTP/HTTPS web traffic and save page content
- [WebCookiesSniffer.exe](tools/WebCookiesSniffer-exe.md) — Capture cookies transmitted over HTTP/HTTPS
- [WirelessKeyView.exe](tools/WirelessKeyView-exe.md) — Recover WEP/WPA keys stored on the local machine

### C. Disk & File System
- [du64.exe](tools/du64-exe.md) — Report disk usage for a directory tree
- [diskext64.exe](tools/diskext64-exe.md) — Show disk extents (physical location) for volumes
- [Diskmon64.exe](tools/Diskmon64-exe.md) — Monitor real-time disk I/O activity
- [DiskView64.exe](tools/DiskView64-exe.md) — Graphical cluster map of disk usage
- [ntfsinfo64.exe](tools/ntfsinfo64-exe.md) — Display NTFS volume metadata (cluster size, MFT location, etc.)
- [Contig64.exe](tools/Contig64-exe.md) — Defragment individual files or analyse fragmentation
- [streams64.exe](tools/streams64-exe.md) — List or delete NTFS alternate data streams on files or directories
- [FindLinks64.exe](tools/FindLinks64-exe.md) — Find all hard links pointing to a file
- [junction64.exe](tools/junction64-exe.md) — Create, list, or delete NTFS junction points (directory symlinks)
- [sdelete64.exe](tools/sdelete64-exe.md) — Securely delete files or wipe free space
- [sync64.exe](tools/sync64-exe.md) — Flush file system buffers to disk
- [movefile64.exe](tools/movefile64-exe.md) — Schedule a file move or delete to occur at next reboot
- [pendmoves64.exe](tools/pendmoves64-exe.md) — List pending file rename/delete operations scheduled for next boot
- [OpenedFilesView.exe](tools/OpenedFilesView-exe.md) — Show all files currently opened by processes on the system
- [disk2vhd64.exe](tools/disk2vhd64-exe.md) — Create a VHD/VHDX snapshot of a live volume
- [pagedfrg.exe](tools/pagedfrg-exe.md) — Defragment paged pool, non-paged pool, and registry hives
- [Volumeid64.exe](tools/Volumeid64-exe.md) — Change the volume ID (serial number) of FAT and NTFS volumes

### D. Registry
- [Autoruns64.exe](tools/Autoruns64-exe.md) — GUI view of all autostart locations across the system
- [autorunsc64.exe](tools/autorunsc64-exe.md) — CLI version of Autoruns. Enumerate all autostart entries
- [RegScanner.exe](tools/RegScanner-exe.md) — Search the registry for values, keys, or data matching a pattern
- [RegFromApp.exe](tools/RegFromApp-exe.md) — Monitor and log registry changes made by a specific process
- [RegDelNull64.exe](tools/RegDelNull64-exe.md) — Scan and optionally delete registry keys containing embedded null characters
- [regjump.exe](tools/regjump-exe.md) — Open Regedit and jump directly to a specified registry path
- [ru64.exe](tools/ru64-exe.md) — Show registry disk usage by key, useful for inventorying large hives
- [RegDllView.exe](tools/RegDllView-exe.md) — Display registered DLL/OCX/ActiveX files in the Windows registry

### E. System Info & Security
- [PsInfo64.exe](tools/PsInfo64-exe.md) — Display system information (OS version, uptime, CPU, RAM, hotfixes)
- [Coreinfo64.exe](tools/Coreinfo64-exe.md) — Display CPU topology, cache, NUMA, and virtualisation features
- [Clockres64.exe](tools/Clockres64-exe.md) — Report the current system timer resolution
- [accesschk64.exe](tools/accesschk64-exe.md) — Show effective permissions for users or groups on files, registry keys, services, and objects
- [AccessEnum.exe](tools/AccessEnum-exe.md) — Scan a directory or registry tree and show where permissions differ from parent
- [sigcheck64.exe](tools/sigcheck64-exe.md) — Verify file signatures, check VirusTotal, and display version info
- [strings64.exe](tools/strings64-exe.md) — Extract printable strings from binary files
- [efsdump.exe](tools/efsdump-exe.md) — Display EFS encryption information for files
- [DriverView.exe](tools/DriverView-exe.md) — List all loaded kernel drivers with version and path info
- [LoadOrd64.exe](tools/LoadOrd64-exe.md) — Show the order in which drivers and services are loaded at boot
- [LoadOrdC64.exe](tools/LoadOrdC64-exe.md) — Console version of LoadOrd for scripting and automation
- [logonsessions64.exe](tools/logonsessions64-exe.md) — List active logon sessions and the processes running in each
- [PsLoggedon64.exe](tools/PsLoggedon64-exe.md) — Show users logged on locally and via resource shares
- [pipelist64.exe](tools/pipelist64-exe.md) — List named pipes on the system
- [ShareEnum64.exe](tools/ShareEnum64-exe.md) — Enumerate network shares and their permissions
- [Winobj64.exe](tools/Winobj64-exe.md) — Browse the Windows Object Manager namespace
- [shexview.exe](tools/shexview-exe.md) — View and disable Shell Extension handlers
- [dllexp.exe](tools/dllexp-exe.md) — Display exported functions from DLL files
- [FileTypesMan.exe](tools/FileTypesMan-exe.md) — View and edit file type associations in the registry
- [URLProtocolView.exe](tools/URLProtocolView-exe.md) — Display registered URL protocol handlers
- [SpecialFoldersView.exe](tools/SpecialFoldersView-exe.md) — Display paths of all Windows special folders
- [Testlimit64.exe](tools/Testlimit64-exe.md) — Test Windows limits by consuming handles, threads, memory, or other resources
- [notmyfault64.exe](tools/notmyfault64-exe.md) — Deliberately crash the system or leak memory for testing crash dump configuration
- [notmyfaultc64.exe](tools/notmyfaultc64-exe.md) — Console version of notmyfault for scripted crash testing
- [ldmdump.exe](tools/ldmdump-exe.md) — Dump Logical Disk Manager (LDM) database information for dynamic disks
- [exiftool.exe](tools/exiftool-exe.md) — Read and write metadata from image, audio, video, and document files
- [RootkitRevealer.exe](tools/RootkitRevealer-exe.md) — Advanced rootkit detection using API comparison techniques
- [sysexp.exe](tools/sysexp-exe.md) — System Explorer for viewing processes, modules, windows, and system information

### F. Monitoring & Logging
- [Sysmon64.exe](tools/Sysmon64-exe.md) — Log detailed process creation, network, file, and registry events to the Windows Event Log
- [dbgview64.exe](tools/dbgview64-exe.md) — Capture OutputDebugString and kernel debug messages in real time
- [livekd64.exe](tools/livekd64-exe.md) — Run kernel debugger commands against a live system without a remote debugger
- [psloglist64.exe](tools/psloglist64-exe.md) — Dump Windows event log entries from local or remote systems

### G. Remote & Admin Operations
- [PsExec64.exe](tools/PsExec64-exe.md) — Execute processes on remote systems with optional interactive session
- [PsService64.exe](tools/PsService64-exe.md) — View and control services on local or remote systems
- [psfile64.exe](tools/psfile64-exe.md) — List files opened remotely on the local system via network shares
- [PsGetsid64.exe](tools/PsGetsid64-exe.md) — Translate between account names and SIDs
- [psshutdown64.exe](tools/psshutdown64-exe.md) — Shut down, restart, or log off local or remote systems
- [ShellRunas.exe](tools/ShellRunas-exe.md) — Launch a program as a different user from the shell context menu
- [RDCMan.exe](tools/RDCMan-exe.md) — Manage multiple Remote Desktop connections in a tabbed GUI
- [pspasswd64.exe](tools/pspasswd64-exe.md) — Change account passwords on local or remote Windows systems

### H. Active Directory
- [ADExplorer64.exe](tools/ADExplorer64-exe.md) — Browse and snapshot Active Directory as an LDAP client
- [ADInsight64.exe](tools/ADInsight64-exe.md) — Real-time LDAP traffic analyser — captures all LDAP calls from client applications
- [adrestore64.exe](tools/adrestore64-exe.md) — List and restore deleted Active Directory objects from the tombstone


## Command Construction Rules

- Resolve the correct subfolder before building any path:
  - Sysinternals tools: `./systeminternals/<tool>.exe`
  - NirSoft tools: `./nirsoft/<tool>.exe`
- Prepend `-accepteula` (or `/accepteula`) to every Sysinternals invocation to suppress the EULA dialog on first run.
- Include `-nobanner` or `/quiet` for any CLI tool that supports it to suppress decorative output.
- When output is tabular, pipe through `| findstr /V "^$"` to strip blank lines before returning to agent context.
- For tools that write to files (Procmon64, Sysmon64, disk2vhd64, procdump64), always specify an explicit output path in the working directory. Never use a bare filename without a path.
- Never rely on PATH. Always use explicit relative paths from the working directory.
- For NirSoft tools, prefer `/stext ./<output>.txt` for tab-delimited export or `/scsv ./<output>.csv` for CSV export over GUI interaction.

## Error Handling

When a tool invocation fails, follow these fallback strategies:

**Tool not found** (file does not exist):
- Check if the 32-bit variant exists (e.g., `procexp.exe` instead of `procexp64.exe`).
- If neither variant exists, report to user and suggest an alternative tool from the same capability domain.
- Example: If `handle64.exe` is missing, suggest `OpenedFilesView.exe` (NirSoft) as an alternative for file lock investigation.

**Access denied** (elevation required):
- Confirm the tool requires [ADMIN] privileges (check the tool entry in `tools/<tool-name>.md`).
- Instruct the user to relaunch the shell as administrator.
- Do not retry without confirmation that the shell is now elevated.

**Driver load failure** (tools marked [DRIVER]):
- Confirm the user has administrator privileges.
- Check if another instance of the tool is already running (e.g., Procmon64 can only run one instance).
- If the driver is stuck from a previous crash, instruct the user to reboot or manually unload the driver.
- For Procmon64 specifically: `./systeminternals/Procmon64.exe /terminate` unloads the driver.

**Tool crashes or hangs**:
- Check if the tool is GUI-only and was invoked with CLI flags it doesn't support.
- For GUI-only tools, instruct the user to launch manually and describe what to look for.
- If a CLI tool crashes, check the command syntax against the tool entry example in `tools/<tool-name>.md`.

**Output parsing failure** (unexpected format):
- Verify the tool version matches expectations (some tools change output format across versions).
- Fall back to instructing the user to review the raw output file manually.
- Report the issue and suggest an alternative tool if available.

**Remote operation failure** (PsExec64, PsService64, PsInfo64):
- Verify network connectivity to the remote system.
- Confirm the user has admin credentials for the remote system.
- Check if Windows Firewall is blocking remote admin ports (135, 139, 445).
- Suggest using `psping64` to test connectivity first.


## Chaining Recipes

### a. What process is holding a file locked?

```powershell
# Step 1 — find which process has the file open
./nirsoft/OpenedFilesView.exe /stext ./ofv_out.txt

# Validation: Check if output file was created
if (!(Test-Path ./ofv_out.txt)) {
    Write-Error "OpenedFilesView failed. Check if tool exists and shell is elevated."
    exit 1
}

# Validation: Check if output contains data
if ((Get-Item ./ofv_out.txt).Length -eq 0) {
    Write-Warning "No open files found. File may not be locked or path incorrect."
    # Fallback to handle64
    Write-Host "Falling back to handle64..."
    ./systeminternals/handle64.exe -accepteula "C:\path\to\locked\file.txt" | findstr /V "^$"
    exit 0
}

# Parse ofv_out.txt: split on \t, find rows where Filename matches target path.
# Extract Process Name and PID columns.
$lockingProcess = Select-String -Path ./ofv_out.txt -Pattern "C:\\path\\to\\locked\\file.txt"
if (!$lockingProcess) {
    Write-Warning "File not found in OpenedFilesView output. Verify file path is correct."
    exit 1
}

# Step 2 — confirm with handle64 and get handle value
./systeminternals/handle64.exe -accepteula "C:\path\to\locked\file.txt" | findstr /V "^$"
# Output format: <process> pid: <PID>  type: File  <handle>: <path>
# Extract PID for next step.

# Validation: Verify handle64 found the file
if ($LASTEXITCODE -ne 0) {
    Write-Warning "handle64 did not find the file. Possible causes: file not locked, incorrect path, or insufficient privileges."
    Write-Host "Recommendation: Relaunch shell as administrator or reboot to release locks."
    exit 1
}

# Step 3 — inspect process in procexp64 (visual confirmation)
./systeminternals/procexp64.exe /accepteula
# In Process Explorer: Ctrl+F, search for the file path to highlight the owning process.
```

### b. Network connection to unknown IP — triage

```powershell
# Step 1 — list all connections with owning process
./systeminternals/tcpvcon64.exe -accepteula -a -c > ./tcpvcon_out.csv

# Validation: Check if output file was created
if (!(Test-Path ./tcpvcon_out.csv)) {
    Write-Error "tcpvcon64 failed. Check if tool exists and shell is elevated."
    exit 1
}

# Validation: Check if target IP is in output
if (!(Select-String -Path ./tcpvcon_out.csv -Pattern "203.0.113.42")) {
    Write-Warning "Target IP not found in connections. Verify IP address or check if connection closed."
    exit 1
}

# CSV columns: Protocol, Local Addr, Local Port, Remote Addr, Remote Port, State, PID, Process
# Identify the unknown remote IP and owning PID/process binary path.

# Step 2 — WHOIS the remote IP
./systeminternals/whois64.exe -accepteula 203.0.113.42

# Step 3 — verify the owning process binary signature
./systeminternals/sigcheck64.exe -accepteula -v "C:\path\to\owning\process.exe"
# Flag if unsigned or low VT detection count.

# Validation: Verify sigcheck64 completed successfully
if ($LASTEXITCODE -ne 0) {
    Write-Error "sigcheck64 failed. Possible causes: file not found, access denied, or network issue."
    exit 1
}

# Step 4 — capture traffic window [CAPTURE — may contain credentials]
Write-Warning "NetworkTrafficView will capture network traffic. Captured data may contain credentials or sensitive information."
./nirsoft/NetworkTrafficView.exe /stext ./ntv_out.txt
# Parse ntv_out.txt: split on \t, filter rows by remote IP.
```

### c. High memory — find the culprit

```powershell
# Validation: Check if shell is elevated (required for memory tools)
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (!$isAdmin) {
    Write-Error "Administrator privileges required for RAMMap64 and vmmap64. Relaunch shell as administrator."
    exit 1
}

# Step 1 — review physical memory breakdown
./systeminternals/RAMMap64.exe /accepteula
# GUI-only. Instruct user to check "Process Private" tab for largest consumers.
# Note the PID of the top consumer.

# Step 2 — inspect virtual memory layout of suspect process
$pid = Read-Host "Enter PID of suspect process from RAMMap64"
if (!$pid -or $pid -notmatch '^\d+$') {
    Write-Error "Invalid PID. Must be a numeric process ID."
    exit 1
}

./systeminternals/vmmap64.exe -accepteula $pid
# GUI-only for interactive use. Look for large Private Data or Heap regions.

# Step 3 — capture dump if leak is confirmed
$dumpPath = "./memleak_$pid.dmp"
./systeminternals/procdump64.exe -accepteula -ma $pid $dumpPath

# Validation: Verify dump was created
if (!(Test-Path $dumpPath)) {
    Write-Error "procdump64 failed to create dump. Check if process still exists and shell is elevated."
    exit 1
}

# Report dump path to user for analysis with WinDbg or Visual Studio.
Write-Host "Memory dump created: $dumpPath (Size: $((Get-Item $dumpPath).Length / 1MB) MB)"
```

### d. Suspicious autostart entry

```powershell
# Step 1 — enumerate all autoruns as CSV
./systeminternals/autorunsc64.exe -accepteula -nobanner -a * -c -s > ./autoruns.csv

# Validation: Check if output file was created
if (!(Test-Path ./autoruns.csv)) {
    Write-Error "autorunsc64 failed. Check if tool exists and shell is elevated."
    exit 1
}

# Validation: Check if output contains data
if ((Get-Item ./autoruns.csv).Length -eq 0) {
    Write-Warning "No autoruns found. This is unusual and may indicate a problem."
    exit 1
}

# Parse CSV: split on comma (watch for quoted fields). Check Signer and VT detection columns.
# Flag entries where Signer is empty or VT detection > 0.
$suspiciousEntries = Import-Csv ./autoruns.csv | Where-Object { 
    $_.Signer -eq "" -or ([int]$_.VTdetection -gt 0)
}

if ($suspiciousEntries.Count -eq 0) {
    Write-Host "No suspicious autoruns found. All entries are signed or have zero VT detections."
    exit 0
}

Write-Host "Found $($suspiciousEntries.Count) suspicious entries:"
$suspiciousEntries | Format-Table Entry, ImagePath, Signer, VTdetection

# Step 2 — verify binary signature for first suspicious entry
$targetBinary = $suspiciousEntries[0].ImagePath
if (!(Test-Path $targetBinary)) {
    Write-Warning "Binary not found: $targetBinary. May have been deleted or path is incorrect."
} else {
    ./systeminternals/sigcheck64.exe -accepteula -v $targetBinary
}

# Step 3 — extract strings from binary
if (Test-Path $targetBinary) {
    ./systeminternals/strings64.exe -accepteula -n 8 $targetBinary | findstr /V "^$" > ./strings_out.txt
    # Look for embedded URLs, IP addresses, registry paths, or encoded payloads.
    Write-Host "Strings extracted to: ./strings_out.txt"
    
    # Quick analysis: Look for suspicious patterns
    $suspiciousPatterns = Select-String -Path ./strings_out.txt -Pattern "http://|https://|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|HKEY_"
    if ($suspiciousPatterns) {
        Write-Warning "Found suspicious patterns in strings:"
        $suspiciousPatterns | Select-Object -First 10
    }
}

# Step 4 — report VT permalink from sigcheck64 output for manual review
# sigcheck64 -v outputs a VirusTotal permalink; present it to the user.
```

### e. Validate system before a change (snapshot)

```powershell
# Step 1 — export autoruns baseline
./systeminternals/autorunsc64.exe -accepteula -nobanner -a * -c -s > ./baseline_autoruns.csv

# Validation: Check if autoruns baseline was created
if (!(Test-Path ./baseline_autoruns.csv)) {
    Write-Error "autorunsc64 failed to create baseline. Check if tool exists and shell is elevated."
    exit 1
}

# Validation: Check if baseline contains data
if ((Get-Item ./baseline_autoruns.csv).Length -eq 0) {
    Write-Warning "Autoruns baseline is empty. This is unusual."
    exit 1
}

Write-Host "Autoruns baseline created: ./baseline_autoruns.csv ($(((Get-Item ./baseline_autoruns.csv).Length / 1KB).ToString('F2')) KB)"

# Step 2 — create volume snapshot
Write-Warning "Creating VHD snapshot. This may take several minutes and requires significant disk space."
$vhdPath = "./snapshot_C.vhdx"
./systeminternals/disk2vhd64.exe -accepteula C: $vhdPath

# Validation: Check if VHD was created
if (!(Test-Path $vhdPath)) {
    Write-Error "disk2vhd64 failed to create snapshot. Check if tool exists, shell is elevated, and sufficient disk space is available."
    exit 1
}

# Report VHDX path and size to user
Write-Host "Volume snapshot created: $vhdPath (Size: $((Get-Item $vhdPath).Length / 1GB) GB)"

# Step 3 — inventory registry size
./systeminternals/ru64.exe -accepteula -c HKLM > ./baseline_registry.csv

# Validation: Check if registry baseline was created
if (!(Test-Path ./baseline_registry.csv)) {
    Write-Error "ru64 failed to create registry baseline. Check if tool exists."
    exit 1
}

Write-Host "Registry baseline created: ./baseline_registry.csv"
Write-Host "System snapshot complete. Baseline files ready for comparison after changes."
```

### f. AD authentication failing

```powershell
# Step 1 — capture live LDAP trace [GUI — instruct user]
Write-Host "Launching ADInsight64 to capture LDAP trace..."
Write-Host "Instructions: Reproduce the auth failure while ADInsight is running, then File > Save trace to ./adinsight_trace.xml"

# Validation: Check if ADInsight64 exists
if (!(Test-Path ./systeminternals/ADInsight64.exe)) {
    Write-Error "ADInsight64.exe not found. Check if tool exists in ./systeminternals/"
    exit 1
}

./systeminternals/ADInsight64.exe /accepteula
# GUI-only. Wait for user to save trace file.

# Validation: Check if trace file was saved
$timeout = 300  # 5 minutes
$elapsed = 0
while (!(Test-Path ./adinsight_trace.xml) -and $elapsed -lt $timeout) {
    Start-Sleep -Seconds 5
    $elapsed += 5
}

if (!(Test-Path ./adinsight_trace.xml)) {
    Write-Warning "ADInsight trace not saved. User may need to manually save trace to ./adinsight_trace.xml"
}

# Step 2 — pull Security event log
./systeminternals/psloglist64.exe -accepteula -s | findstr /V "^$" > ./security_log.txt

# Validation: Check if security log was captured
if (!(Test-Path ./security_log.txt)) {
    Write-Error "psloglist64 failed to capture security log. Check if tool exists and shell is elevated."
    exit 1
}

# Look for Event ID 4625 (logon failure), 4771 (Kerberos pre-auth failed)
$authFailures = Select-String -Path ./security_log.txt -Pattern "4625|4771"
if ($authFailures) {
    Write-Warning "Found authentication failures in security log:"
    $authFailures | Select-Object -First 5
} else {
    Write-Host "No authentication failures found in security log."
}

# Step 3 — list active logon sessions
./systeminternals/logonsessions64.exe -accepteula -p | findstr /V "^$" > ./logon_sessions.txt

# Validation: Check if logon sessions were captured
if (!(Test-Path ./logon_sessions.txt)) {
    Write-Error "logonsessions64 failed. Check if tool exists and shell is elevated."
    exit 1
}

# Confirm whether a valid session exists for the affected user
Write-Host "Active logon sessions captured: ./logon_sessions.txt"
Write-Host "Review logon sessions to confirm if affected user has a valid session."
```

### g. Remote system unresponsive to RDP

```powershell
# Validation: Check if remote system is reachable
$remotePC = "REMOTEPC"
Write-Host "Testing connectivity to $remotePC..."

if (!(Test-Connection -ComputerName $remotePC -Count 2 -Quiet)) {
    Write-Error "Cannot reach $remotePC. Check network connectivity and hostname."
    exit 1
}

# Step 1 — gather remote system info
./systeminternals/PsInfo64.exe -accepteula \\$remotePC | findstr /V "^$" > ./psinfo_remote.txt

# Validation: Check if PsInfo64 succeeded
if ($LASTEXITCODE -ne 0 -or !(Test-Path ./psinfo_remote.txt)) {
    Write-Error "PsInfo64 failed to connect to $remotePC. Check if admin credentials are valid and firewall allows remote admin (ports 135, 139, 445)."
    Write-Host "Recommendation: Use 'psping64 -accepteula \\$remotePC' to test connectivity."
    exit 1
}

Write-Host "Remote system info captured: ./psinfo_remote.txt"

# Step 2 — check RDP-related services
Write-Host "Checking RDP services on $remotePC..."
./systeminternals/PsService64.exe -accepteula \\$remotePC query TermService > ./termservice_status.txt
./systeminternals/PsService64.exe -accepteula \\$remotePC query UmRdpService > ./umrdp_status.txt

# Validation: Check if services were queried successfully
if (!(Test-Path ./termservice_status.txt) -or !(Test-Path ./umrdp_status.txt)) {
    Write-Error "PsService64 failed to query services. Check if shell is elevated and remote admin is enabled."
    exit 1
}

# Check if TermService is running
$termServiceRunning = Select-String -Path ./termservice_status.txt -Pattern "RUNNING"
if (!$termServiceRunning) {
    Write-Warning "TermService is not running on $remotePC. Attempting to start..."
    
    # Step 3 — restart service if stopped (confirm with user first)
    Write-Warning "About to start TermService on $remotePC. This will enable RDP access."
    $confirm = Read-Host "Proceed? (y/n)"
    
    if ($confirm -eq 'y') {
        ./systeminternals/PsService64.exe -accepteula \\$remotePC start TermService
        
        # Validation: Check if service started
        Start-Sleep -Seconds 3
        ./systeminternals/PsService64.exe -accepteula \\$remotePC query TermService > ./termservice_status_after.txt
        $serviceStarted = Select-String -Path ./termservice_status_after.txt -Pattern "RUNNING"
        
        if ($serviceStarted) {
            Write-Host "TermService started successfully on $remotePC."
        } else {
            Write-Warning "PsService64 failed to start TermService. Attempting fallback with PsExec64..."
            
            # Step 4 — if service restart fails, execute remediation remotely
            ./systeminternals/PsExec64.exe -accepteula \\$remotePC -s cmd /c "net start TermService"
            
            # Validation: Check if PsExec succeeded
            if ($LASTEXITCODE -eq 0) {
                Write-Host "TermService started via PsExec64."
            } else {
                Write-Error "Failed to start TermService. Manual intervention required on $remotePC."
                exit 1
            }
        }
    } else {
        Write-Host "Service start cancelled by user."
    }
} else {
    Write-Host "TermService is already running on $remotePC."
}
```

### h. CPU thermal/stability check

```powershell
# Validation: Check if shell is elevated (required for some CPU tools)
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (!$isAdmin) {
    Write-Warning "Administrator privileges recommended for CPU stress testing. Some features may not work."
}

# Step 1 — display CPU topology and features
./systeminternals/Coreinfo64.exe -accepteula | findstr /V "^$" > ./coreinfo_out.txt

# Validation: Check if Coreinfo64 succeeded
if (!(Test-Path ./coreinfo_out.txt)) {
    Write-Error "Coreinfo64 failed. Check if tool exists."
    exit 1
}

Write-Host "CPU topology captured: ./coreinfo_out.txt"
Get-Content ./coreinfo_out.txt | Select-Object -First 20

# Step 2 — apply CPU stress load [DESTRUCTIVE — confirm with user first]
Write-Warning "CPUSTRES64 will stress CPU cores. This may cause system instability, thermal throttling, or crashes."
Write-Warning "Ensure adequate cooling and monitor temperatures during test."
$confirm = Read-Host "Proceed with CPU stress test? (y/n)"

if ($confirm -ne 'y') {
    Write-Host "CPU stress test cancelled by user."
    exit 0
}

# Validation: Check if CPUSTRES64 exists
if (!(Test-Path ./systeminternals/CPUSTRES64.exe)) {
    Write-Error "CPUSTRES64.exe not found. Check if tool exists in ./systeminternals/"
    exit 1
}

Write-Host "Launching CPUSTRES64. Instructions: Set thread count and activity level, then click 'Start'."
Write-Host "Monitor system temperature and stability. Press Ctrl+C in this window to stop monitoring."
./systeminternals/CPUSTRES64.exe
# GUI-only. Instruct user to set thread count and activity level, then start.

# Step 3 — measure timer resolution under load
Write-Host "Measuring timer resolution under load..."
./systeminternals/Clockres64.exe -accepteula > ./clockres_out.txt

# Validation: Check if Clockres64 succeeded
if (!(Test-Path ./clockres_out.txt)) {
    Write-Error "Clockres64 failed. Check if tool exists."
    exit 1
}

# Parse clockres output and flag if resolution drifts above 15.6 ms
$clockresOutput = Get-Content ./clockres_out.txt
$currentResolution = $clockresOutput | Select-String -Pattern "Current timer interval:"
Write-Host $currentResolution

if ($currentResolution -match "(\d+\.\d+)") {
    $resolutionMs = [double]$matches[1]
    if ($resolutionMs -gt 15.6) {
        Write-Warning "Timer resolution ($resolutionMs ms) is above default (15.6 ms). System may be under stress."
    } else {
        Write-Host "Timer resolution is normal: $resolutionMs ms"
    }
}

# Step 4 — watch for kernel debug messages
Write-Host "Capturing kernel debug messages. Look for thermal, throttling, or error messages..."
./systeminternals/dbgview64.exe /accepteula /k /l ./dbgview_stress.log

# Validation: Check if dbgview log was created
Start-Sleep -Seconds 5
if (!(Test-Path ./dbgview_stress.log)) {
    Write-Warning "dbgview64 did not create log file. Tool may require elevation or kernel debug messages may be disabled."
} else {
    # Parse log: look for lines containing "thermal", "throttl", "WHEA", or "error"
    $suspiciousMessages = Select-String -Path ./dbgview_stress.log -Pattern "thermal|throttl|WHEA|error" -CaseSensitive:$false
    
    if ($suspiciousMessages) {
        Write-Warning "Found suspicious kernel messages during stress test:"
        $suspiciousMessages | Select-Object -First 10
    } else {
        Write-Host "No thermal or error messages detected in kernel debug log."
    }
}

Write-Host "CPU stress test monitoring complete. Review ./dbgview_stress.log for detailed kernel messages."
```


## Output Parsing Guidance

**CSV output** (autorunsc64 `-c`, tcpvcon64 `-c`, cports `/scsv`, procdump64):
- Split each line on `,`.
- Watch for quoted fields that contain commas — treat content inside `"..."` as a single field.
- Skip the header row (first non-blank line).
- Map columns by index from the header row; do not assume fixed positions across tool versions.

**Tab-delimited output** (most NirSoft `/stext` exports):
- Split each line on `\t`.
- First non-blank line is the header row; use it to build a column index map.
- Empty fields appear as consecutive `\t` characters.

**Plain text — pslist, handle, strings, psloglist**:
- Use line-by-line regex matching.
- `pslist64`: skip lines until the header line matching `^Name\s+Pid`. Each data line: `(\S+)\s+(\d+)\s+...`
- `handle64`: each result line matches `(\S+)\s+pid:\s+(\d+)\s+type:\s+(\S+)\s+\w+:\s+(.+)`
- `strings64`: each line is a candidate string; filter with regex for URLs (`https?://`), IPs (`\d{1,3}(\.\d{1,3}){3}`), or paths (`[A-Za-z]:\\`).
- `psloglist64`: events are multi-line blocks separated by blank lines. Split on `\n\n`, then parse each block for `Event ID:`, `Date:`, `Time:`, `Source:`, and `Description:` fields.

**GUI-only tools** (see `references/tool-catalog.md` for full list):
- Do not attempt to parse interactive windows.
- Drive via `/stext`, `/scsv`, or `/export` flags where available.
- For tools with no export flag, instruct the user what to look for in the GUI and what to report back.

**Binary/structured output** (Procmon64 PML, vmmap64 XML, disk2vhd64 VHDX, procdump64 DMP):
- These formats require the GUI or a dedicated post-processing tool (WinDbg, Procmon GUI).
- Always save to an explicit path in the working directory and report that path to the user.
- Do not attempt to parse binary content inline.


## Safety & Privilege Rules

### Elevation requirements [ADMIN]

The following tools require administrator privileges. Always verify the shell is elevated before running them.

See `references/tool-catalog.md` for the complete list of tools marked [ADMIN], or check individual tool files in `tools/`. Key examples:
procexp64, Procmon64, procdump64, handle64, vmmap64, RAMMap64, disk2vhd64, tcpvcon64,
PsInfo64, accesschk64, Sysmon64, dbgview64, livekd64, psloglist64, PsExec64, PsService64,
ADExplorer64, ADInsight64, adrestore64.

### Kernel driver tools [DRIVER]

These tools load a kernel driver on first run. The driver must be unloaded on exit to avoid resource leaks or conflicts.

| Tool | Driver notes |
|---|---|
| Procmon64 | Driver loaded automatically; unload via File > Unload Driver or `/terminate` |
| handle64 | Driver loaded on first invocation |
| Diskmon64 | Uses `DMON.SYS`; unload via GUI |
| livekd64 | Loads debugger driver; unload on exit |
| Sysmon64 | Persistent driver; uninstall with `Sysmon64.exe -u` |
| notmyfault64 | Loads crash driver; system will crash or become unstable |
| pagedfrg | Loads defrag driver; unload on exit |

### Destructive tools [DESTRUCTIVE]

Always state the risk and wait for explicit user confirmation in the same conversation turn before running any of these.

| Tool | Risk |
|---|---|
| sdelete64 | Permanent file deletion, unrecoverable |
| psshutdown64 | Shuts down or restarts the system |
| pskill64 | Terminates processes, may cause data loss |
| RegDelNull64 `-c` | Deletes registry keys permanently |
| movefile64 | Schedules file deletion/move at reboot |
| pendmoves64 | Lists pending destructive operations |
| adrestore64 `-r` | Restores tombstoned AD objects, may cause conflicts |
| notmyfault64 | Deliberately crashes the system |
| Testlimit64 | Can exhaust system resources and cause instability |
| CPUSTRES64 | Can cause thermal damage or system instability |

### Network capture tools [CAPTURE]

Warn the user before running any of these that captured traffic may contain credentials, session tokens, or other sensitive data.

| Tool | Notes |
|---|---|
| smsniff | Raw packet capture |
| WebSiteSniffer | HTTP/HTTPS content capture |
| WebCookiesSniffer | Cookie capture — high credential risk |
| NetworkTrafficView | Traffic statistics; may log payload data |


## Agent Persona & Response Style

When using this skill, the agent must follow these rules.

- State which tool is being run and why before running it. Example: "Running `handle64` to identify which process holds a lock on the target file."
- Report findings as a structured summary. Do not paste raw output. Extract the relevant rows, flag anomalies, and present conclusions.
- Before any [ADMIN] action, confirm the shell is elevated. If not, instruct the user to relaunch as administrator.
- Before any [DRIVER] action, note that a kernel driver will be loaded and must be unloaded on exit.
- Before any [DESTRUCTIVE] action, state the exact risk and wait for explicit confirmation in the same turn. Do not proceed on implied consent.
- Before any [CAPTURE] action, warn the user that captured traffic may contain credentials or sensitive data.
- For GUI-only tools with no export flag, describe what the user should look for in the interface and what information to report back. Do not attempt to automate GUI interaction.
- Prefer the minimum invasive tool chain. Escalate only when results are inconclusive.
- When chaining tools, explain what data is being passed from one step to the next and why.


## Configuration Files

Many NirSoft tools support persistent configuration via `.cfg` files stored in the same directory as the executable. These files control default settings, column visibility, sorting, and filters.

**Configuration files in nirsoft/ directory**:
- cports.cfg, dllexp.cfg, DriverView.cfg, FileTypesMan.cfg
- GDIView.cfg, NetworkTrafficView.cfg, OpenedFilesView.cfg
- ProcessActivityView.cfg, RegFromApp.cfg, regscanner.cfg
- shexview.cfg, shmnview.cfg, SpecialFoldersView.cfg
- sysexp.cfg, URLProtocolView.cfg, WebSiteSniffer.cfg
- WirelessKeyView.cfg

**How configuration files work**:
- Created automatically when you save settings in the GUI
- Persist column layout, sort order, and filters between sessions
- Can be edited manually (INI format) or via GUI
- Deleted to reset tool to defaults

**Using configuration files**:
```powershell
# Reset a tool to defaults by deleting its config
Remove-Item ./nirsoft/cports.cfg

# Backup current configuration
Copy-Item ./nirsoft/cports.cfg ./nirsoft/cports.cfg.backup

# Restore previous configuration
Copy-Item ./nirsoft/cports.cfg.backup ./nirsoft/cports.cfg
```

**Note**: Sysinternals tools generally do not use configuration files. Settings are stored in the registry under `HKCU\Software\Sysinternals\`.


## Help Files

Detailed documentation for most tools is available in CHM (Compiled HTML Help) files.

**Opening help files**:
```powershell
# Open Sysinternals help file
hh.exe ./systeminternals/procexp.chm

# Open NirSoft help file
hh.exe ./nirsoft/cports.chm
```

**Available help files**:

**Sysinternals CHM files**:
- AdExplorer.chm, ADInsight.chm, autoruns.chm, Dbgview.chm
- Disk2vhd.chm, procexp.chm, procmon.chm, Pstools.chm
- RootkitRevealer.chm, tcpview.chm, Vmmap.chm

**NirSoft CHM files**:
- cports.chm, dllexp.chm, driverview.chm, FileTypesMan.chm
- GDIView.chm, heapmemview.chm, NetworkTrafficView.chm
- OpenedFilesView.chm, ProcessActivityView.chm, ProcessThreadsView.chm
- RegDllView.chm, RegFromApp.chm, regscanner.chm
- shexview.chm, shmnview.chm, smsniff.chm, SpecialFoldersView.chm
- sysexp.chm, URLProtocolView.chm, WebCookiesSniffer.chm
- WebSiteSniffer.chm, WirelessKeyView.chm, netpass.chm

**Legacy HLP files** (Windows XP/2000 format):
- DISKMON.HLP, pagedfrg.hlp, TCPVIEW.HLP, WINOBJ.HLP
- Open with: `winhlp32.exe <file>.hlp` (may require Windows XP compatibility mode)

**When to reference help files**:
- User needs detailed flag documentation beyond what's in `tools/*.md`
- Tool has complex GUI features not covered in skill documentation
- User wants official vendor documentation for compliance or audit purposes

**Note**: All tool documentation in `tools/*.md` is derived from official CHM/HLP files and vendor websites. For the most current information, consult the CHM files or visit sysinternals.com / nirsoft.net.


## 32-bit Tool Variants

Most Sysinternals tools have both 64-bit and 32-bit variants. Always prefer the 64-bit variant on 64-bit Windows systems.

**Available 32-bit variants** (in `./systeminternals/`):
- accesschk.exe, ADExplorer.exe, ADInsight.exe, adrestore.exe
- Autoruns.exe, autorunsc.exe, Cacheset.exe, Clockres.exe
- Contig.exe, Coreinfo.exe, CPUSTRES.EXE, Dbgview.exe
- disk2vhd.exe, diskext.exe, Diskmon.exe, DiskView.exe
- du.exe, FindLinks.exe, handle.exe, junction.exe
- Listdlls.exe, livekd.exe, LoadOrd.exe, LoadOrdC.exe
- logonsessions.exe, movefile.exe, notmyfault.exe, notmyfaultc.exe
- ntfsinfo.exe, pendmoves.exe, pipelist.exe, procdump.exe
- procexp.exe, Procmon.exe, PsExec.exe, psfile.exe
- PsGetsid.exe, PsInfo.exe, pskill.exe, pslist.exe
- PsLoggedon.exe, psloglist.exe, pspasswd.exe, psping.exe
- PsService.exe, psshutdown.exe, pssuspend.exe, RAMMap.exe
- RegDelNull.exe, ru.exe, sdelete.exe, ShareEnum.exe
- sigcheck.exe, streams.exe, strings.exe, sync.exe
- Sysmon.exe, tcpvcon.exe, tcpview.exe, Testlimit.exe
- vmmap.exe, Volumeid.exe, whois.exe, Winobj.exe

**When to use 32-bit variants**:
- Running on 32-bit Windows (rare)
- 64-bit variant is missing or corrupted
- Debugging 32-bit processes (some tools work better with matching architecture)

**Fallback logic** (already implemented in Agent Workflow step 1):
```powershell
# Check 64-bit tool first, fall back to 32-bit
$tool64 = "./systeminternals/procexp64.exe"
$tool32 = "./systeminternals/procexp.exe"

if (Test-Path $tool64) {
    $tool = $tool64
} elseif (Test-Path $tool32) {
    $tool = $tool32
    Write-Warning "Using 32-bit variant: procexp.exe"
} else {
    Write-Error "Tool not found: procexp64.exe"
    exit 1
}
```


## Support Files

**Sysinternals support files**:
- `Eula.txt` - End User License Agreement for Sysinternals Suite
- `psversion.txt` - Version information for PsTools
- `readme.txt` - General readme for Sysinternals Suite
- `setp.bat` - Setup batch file for PsTools
- `DMON.SYS` - Kernel driver for Diskmon64.exe

**NirSoft support files**:
- `vlmshlp.dll` - Helper DLL for NirSoft tools (required for some tools to function)

**Usage notes**:
- `Eula.txt`: Reference for license terms. All Sysinternals tools require EULA acceptance via `-accepteula` flag.
- `DMON.SYS`: Loaded automatically by Diskmon64.exe. Do not delete or move.
- `vlmshlp.dll`: Required by some NirSoft tools. Keep in same directory as executables.
- `setp.bat`: Legacy setup script. Not needed for modern usage.
- `psversion.txt`, `readme.txt`: Documentation files. Reference for version information.

**Do not delete support files** - they are required for proper tool operation or provide important documentation.
