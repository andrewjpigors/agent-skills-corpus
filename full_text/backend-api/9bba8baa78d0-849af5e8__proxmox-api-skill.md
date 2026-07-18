---
name: proxmox-api-skill
description: "Proxmox VE complete API coverage — VMs, LXC, Ceph, HA, SDN, storage, backup, firewall, networking, ACME, user management, metrics, and more via proxmoxer"
version: 2.0.0
category: devops
---

# PVE Cluster Management (v2 — Full API)

Complete Proxmox VE management via the REST API using `proxmoxer`.

## Prerequisites

1. **Install proxmoxer**: Dependencies auto-install on first import (`pip install proxmoxer python-dotenv` if you prefer manual)
2. **Set environment variables** in `.env`:
   - `PVE_HOST` — Proxmox host IP or FQDN (no https://). For Tailscale, use hostname (e.g. `pve-01`)
   - `PVE_USER` — User@realm (e.g. `root@pam`)
   - `PVE_TOKEN_NAME` — API token name
   - `PVE_TOKEN_VALUE` — API token UUID
   - `PVE_VERIFY_SSL` — `true`/`false` (default: `false` for self-signed certs)
   - `PVE_TIMEOUT` — request timeout in seconds (default: `30`)

3. **Token setup on PVE side**:
   - Datacenter → Permissions → API Tokens
   - Create token under desired user, set privileges (Admin for full access)
   - Copy the UUID value — shown only once

## Connection (always start here)

```python
import sys, os, json
from dotenv import load_dotenv
load_dotenv()
sys.path.insert(0, "./scripts")
from pve_helper import get_proxmox, fmt_vm, fmt_node, fmt_task, fmt_storage, fmt_backup, fmt_ceph_osd, fmt_replication, wait_for_task
prox = get_proxmox()
```

---

## 1. Cluster Overview

```python
prox.version.get()                        # PVE version
prox.cluster.status.get()                 # Cluster status (list — check 'type' field)
prox.cluster.nextid.get()                 # Next available VMID
prox.cluster.resources.get(type="vm")     # All VMs/CTs cluster-wide
prox.cluster.resources.get(type="node")   # All nodes
prox.cluster.resources.get(type="storage")# All storage
```

---

## 2. Nodes

```python
# List all nodes
for n in prox.nodes.get():
    print(fmt_node(n))

# Detailed node status
prox.nodes("nodename").status.get()       # CPU, mem, uptime, etc.

# Node power control
prox.nodes("nodename").status.shutdown.post()  # Shutdown
prox.nodes("nodename").status.reboot.post()    # Reboot

# Node info
prox.nodes("nodename").hostname.get()     # Hostname
prox.nodes("nodename").time.get()         # Timezone
prox.nodes("nodename").time.put(timezone="Asia/Seoul")  # Set timezone
prox.nodes("nodename").version.get()      # PVE version on this node
prox.nodes("nodename").capabilities.get() # QEMU machine types, etc.
prox.nodes("nodename").netstat.get()      # Network stats

# RRD metrics
prox.nodes("nodename").rrddata.get(timeframe="hour", cf="AVERAGE")
# Returns: cpu, iowait, loadavg, meminfo, netin/netout, swap, time

# System logs
prox.nodes("nodename").syslog.get(limit=50)
prox.nodes("nodename").journal.get(limit=50)

# Disks & SMART
prox.nodes("nodename").disks.get()
prox.nodes("nodename").disks("smart").get()    # S.M.A.R.T. data
prox.nodes("nodename").disks("zfs").get()      # ZFS pool status
```

### Services

```python
prox.nodes("nodename").services.get()                          # List services
prox.nodes("nodename").services("pveproxy").state.get()       # Service state
prox.nodes("nodename").services("pveproxy").start.post()      # Start
prox.nodes("nodename").services("pveproxy").stop.post()       # Stop
prox.nodes("nodename").services("pveproxy").restart.post()    # Restart
prox.nodes("nodename").services("pveproxy").reload.post()     # Reload
# Key services: pveproxy, pvedaemon, pvestatd, pve-firewall, pve-ha-crm,
#   pve-ha-lrm, pve-cluster, corosync, chrony, postfix, pve-guests
```

### Network

```python
prox.nodes("nodename").network.get()           # List all interfaces
prox.nodes("nodename").network.post(type="bridge", iface="vmbr1", bridge_ports="eno1", autostart=1)
prox.nodes("nodename").network("vmbr1").put(bridge_vids="100-200", bridge_vlan_aware=1)
prox.nodes("nodename").network("vmbr1").delete()
prox.nodes("nodename").network("apply_config").post()   # Apply pending changes
# Types: bridge, bond, vlan, eth, OVSBridge, OVSBond, OVSPort, OVSIntPort
# Bond modes: balance-rr, active-backup, balance-xor, broadcast, 802.3ad, balance-tlb, balance-alb
```

### DNS & Hosts

```python
prox.nodes("nodename").dns.get()               # DNS config (search, dns1-3)
prox.nodes("nodename").dns.put(search="local", dns1="8.8.8.8")
prox.nodes("nodename").hosts.get()             # /etc/hosts content
prox.nodes("nodename").hosts.put(data="127.0.0.1 localhost\n...")
```

---

## 3. QEMU VMs

### Basic CRUD

```python
# List & Status
prox.nodes("node").qemu.get()
prox.nodes("node").qemu(vmid).status.current.get()

# Power control
prox.nodes("node").qemu(vmid).status.start.post()
prox.nodes("node").qemu(vmid).status.stop.post()
prox.nodes("node").qemu(vmid).status.reboot.post()
prox.nodes("node").qemu(vmid).status.reset.post()
prox.nodes("node").qemu(vmid).status.suspend.post()
prox.nodes("node").qemu(vmid).status.resume.post()

# Create VM (returns UPID)
prox.nodes("node").qemu.post(
    vmid=100, name="my-vm",
    cores=2, sockets=1, memory=4096,
    net0="virtio,bridge=vmbr0",
    scsi0="local-lvm:vm-100-disk-0,size=32G",
    ostype="l26", onboot=1
)

# Clone
prox.nodes("node").qemu(vmid).clone.post(newid=200, name="cloned-vm", full=1)

# Migrate
prox.nodes("node").qemu(vmid).migrate.post(target="other-node", online=1)

# Convert to template (must be stopped)
prox.nodes("node").qemu(vmid).template.post()
```

### Config (detailed)

```python
# Read config
prox.nodes("node").qemu(vmid).config.get()

# Update sync (requires reboot for some changes)
prox.nodes("node").qemu(vmid).config.put(cores=4, memory=8192)

# Update async (hotplug-capable changes applied immediately)
prox.nodes("node").qemu(vmid).config.post(cores=4)
```

**CPU parameters:** `cores`, `sockets`, `cpu` (cputype=host,flags=+aes), `cpulimit` (0-128), `cpuunits` (1-262144), `affinity` ("0,5,8-11"), `vcpus`, `numa` (bool)

**Memory parameters:** `memory` (MiB, min 16), `balloon` (min target, 0=off), `shares` (0-50000), `hugepages` (2|1024|any), `numa[n]` ("cpus=X,memory=Y,hostnodes=Z,policy=bind")

**Disks (4 controllers):**
- `ide[n]` (0-3), `sata[n]` (0-5), `scsi[n]` (0-30), `virtio[n]` (0-15)
- Format: `"file=STORAGE:SIZE,format=raw|qcow2,aio=native|threads|io_uring,cache=none,discard=on,iothread=1,ssd=1"`
- Sub-options: backup, bps/iops throttling, cache, discard, format, iothread, replicate, ssd

**Network:** `net[n]` (0-31) — `"model=virtio,bridge=vmbr0,firewall=1,macaddr=XX:XX,queues=N,rate=MBs,tag=VLAN,mtu=SIZE,trunks=VLANs"`

**Machine:** `machine` (pc|q35|virt), `bios` (seabios|ovmf), `viommu` (intel|virtio)

**Other:** `hotplug` ("disk,network,cpu,memory,usb"), `agent` (bool), `boot` ("order=scsi0;ide2;net0"), `efidisk0`, `tpmstate0`, `scsihw`, `vga`, `serial[n]`, `usb[n]`, `hostpci[n]`, `args`, `onboot`, `protection`, `tags`, `description`, `hookscript`

### Disk Operations

```python
# Resize disk
prox.nodes("node").qemu(vmid).resize.put(disk="scsi0", size="+10G")

# Move disk to different storage
upid = prox.nodes("node").qemu(vmid).move_disk.post(
    disk="scsi0", storage="local-lvm", delete=1, format="raw"
)
```

### Snapshots

```python
prox.nodes("node").qemu(vmid).snapshot.get()
upid = prox.nodes("node").qemu(vmid).snapshot.post(name="before-upgrade", description="pre-patch", vmstate=1)
result = wait_for_task(prox, "node", upid)
prox.nodes("node").qemu(vmid).snapshot("snapname").config.get()
prox.nodes("node").qemu(vmid).snapshot("snapname").config.put(description="updated")
prox.nodes("node").qemu(vmid).snapshot("snapname").rollback.post()
prox.nodes("node").qemu(vmid).snapshot("snapname").delete()
```

### QEMU Guest Agent

```python
# All via POST with "command" param
prox.nodes("node").qemu(vmid).agent.post(command="ping")
prox.nodes("node").qemu(vmid).agent.post(command="info")
prox.nodes("node").qemu(vmid).agent.post(command="network-get-interfaces")
prox.nodes("node").qemu(vmid).agent.post(command="get-osinfo")
prox.nodes("node").qemu(vmid).agent.post(command="get-host-name")
prox.nodes("node").qemu(vmid).agent.post(command="get-time")
prox.nodes("node").qemu(vmid).agent.post(command="exec", command_data="/bin/ls -la /tmp")
prox.nodes("node").qemu(vmid).agent.get(command="exec-status", pid=1234)
prox.nodes("node").qemu(vmid).agent.post(command="file-read", file="/etc/hostname")
prox.nodes("node").qemu(vmid).agent.post(command="file-write", file="/tmp/test.txt", content="base64content")
prox.nodes("node").qemu(vmid).agent.post(command="fsfreeze", freeze=True)
prox.nodes("node").qemu(vmid).agent.post(command="fstrim")
prox.nodes("node").qemu(vmid).agent.post(command="user-password", username="root", password="newpass")
prox.nodes("node").qemu(vmid).agent.post(command="shutdown")
```

### Cloud-Init

```python
# Cloud-init is configured via VM config PUT params
prox.nodes("node").qemu(vmid).config.put(
    ciuser="admin",
    cipassword="secret",
    sshkeys="ssh-ed25519 AAAA... user@host",
    citype="nocloud",  # or configdrive2
    nameserver="8.8.8.8",
    searchdomain="local",
    ipconfig0="ip=192.168.1.100/24,gw=192.168.1.1,ip6=dhcp",
    ipconfig1="ip=dhcp"
)
# Read cloud-init dump
prox.nodes("node").qemu(vmid).cloudinit.get()
prox.nodes("node").qemu(vmid).cloudinit("dump").get()
# Custom snippets: cicustom="user=local:snippets/user-data.yaml,network=local:snippets/network-config.yaml"
```

### Console Access

```python
# VNC
vnc = prox.nodes("node").qemu(vmid).vncproxy.post(websocket=1)
# Returns: port, ticket, cert, upid

# SPICE
spice = prox.nodes("node").qemu(vmid).spiceproxy.post()

# Send key
prox.nodes("node").qemu(vmid).sendkey.put(key="ctrl-alt-delete")
```

### Misc

```python
# Feature check
prox.nodes("node").qemu(vmid).feature.get(feature="snapshot")  # snapshot|clone|copy|spice

# Pending config (changes that apply after reboot)
prox.nodes("node").qemu(vmid).pending.get()

# Monitor command (raw QEMU monitor)
prox.nodes("node").qemu(vmid).monitor.post(command="info kvm")

# Unlink disks
prox.nodes("node").qemu(vmid).unlink.put(idlist="scsi1,scsi2", force=1)

# RRD metrics
prox.nodes("node").qemu(vmid).rrddata.get(timeframe="day", cf="AVERAGE")
```

---

## 4. LXC Containers

### Basic CRUD

```python
prox.nodes("node").lxc.get()
prox.nodes("node").lxc(vmid).status.current.get()

# Power
prox.nodes("node").lxc(vmid).status.start.post()
prox.nodes("node").lxc(vmid).status.stop.post()
prox.nodes("node").lxc(vmid).status.shutdown.post()
prox.nodes("node").lxc(vmid).status.suspend.post()
prox.nodes("node").lxc(vmid).status.resume.post()

# Create
prox.nodes("node").lxc.post(
    vmid=101, hostname="my-ct", password="secret",
    ostemplate="local:vztmpl/ubuntu-24.04-standard.tar.zst",
    storage="local-lvm", rootfs="local-lvm:10",
    cores=2, memory=2048, swap=512,
    net0="name=eth0,bridge=vmbr0,ip=dhcp",
    unprivileged=1, onboot=1
)

# Migrate
prox.nodes("node").lxc(vmid).migrate.post(target="other-node")

# Convert to template
prox.nodes("node").lxc(vmid).template.post()
```

### Config (detailed)

```python
prox.nodes("node").lxc(vmid).config.get()
prox.nodes("node").lxc(vmid).config.put(
    cores=4, memory=4096, swap=1024,
    features="nesting=1,fuse=1,mount=nfs",
    mp0="volume=local-lvm:20,mp=/mnt/data,backup=1",
    net1="name=eth1,bridge=vmbr1,ip=dhcp",
    startup="order=3,up=30,down=60",
    tags="web;production",
    timezone="Asia/Seoul"
)
```

**Key LXC config params:** `arch` (amd64|arm64), `cmode` (shell|console|tty), `console`, `cores`, `cpulimit`, `cpuunits`, `description`, `features` (nesting, fuse, mount, keyctl), `hookscript`, `hostname`, `lock`, `memory`, `swap`, `nameserver`, `searchdomain`, `net[n]`, `onboot`, `ostype`, `protection`, `rootfs`, `mp[n]`, `startup`, `tags`, `template`, `timezone`, `tty`, `unprivileged`, `lxc` (raw LXC options)

### Disk Operations

```python
# Resize rootfs or mount point
prox.nodes("node").lxc(vmid).resize.put(disk="rootfs", size="+5G")
prox.nodes("node").lxc(vmid).resize.put(disk="mp0", size="50G")

# Move volume to different storage
upid = prox.nodes("node").lxc(vmid).move_volume.post(
    volume="rootfs", storage="nfs-storage", delete=1
)
```

### Snapshots, Firewall, Console

```python
# Snapshots (same pattern as QEMU)
prox.nodes("node").lxc(vmid).snapshot.get()
upid = prox.nodes("node").lxc(vmid).snapshot.post(name="pre-update")
prox.nodes("node").lxc(vmid).snapshot("snap").rollback.post()
prox.nodes("node").lxc(vmid).snapshot("snap").delete()

# Firewall
prox.nodes("node").lxc(vmid).firewall.options.get()
prox.nodes("node").lxc(vmid).firewall.options.put(enable=1, policy_in="DROP", policy_out="ACCEPT")
prox.nodes("node").lxc(vmid).firewall.rules.get()
prox.nodes("node").lxc(vmid).firewall.rules.post(
    type="in", action="ACCEPT", source="192.168.1.0/24", dport="443", proto="tcp", comment="HTTPS"
)
prox.nodes("node").lxc(vmid).firewall.aliases.get()
prox.nodes("node").lxc(vmid).firewall.ipset.get()
prox.nodes("node").lxc(vmid).firewall.log.get()

# Console
vnc = prox.nodes("node").lxc(vmid).vncproxy.post()
term = prox.nodes("node").lxc(vmid).termproxy.post()

# Network interfaces (running CT only)
prox.nodes("node").lxc(vmid).interfaces.get()

# RRD metrics
prox.nodes("node").lxc(vmid).rrddata.get(timeframe="day", cf="AVERAGE")
```

---

## 5. Storage

### Storage CRUD

```python
prox.storage.get()                          # List all storage
prox.storage("local").get()                 # Get specific storage config

# Create storage (type-specific params vary)
prox.storage.post(
    storage="nfs-backup", type="nfs",
    server="192.168.1.100", export="/mnt/backups",
    content="backup,iso,vztmpl", nodes="pve-01,pve-02"
)
```

**15 Storage Types:** dir, nfs, cifs, glusterfs, cephfs, btrfs, zfspool, lvm, lvmthin, iscsi, iscsidirect, rbd, zfs (over iSCSI), pbs (Proxmox Backup), esxi

**Content Types:** images (VM disks), rootdir (CT rootfs), vztmpl (templates), backup (archives), iso, snippets

**Common params:** `storage`, `type`, `content`, `nodes`, `disable`, `shared`, `format` (raw|qcow2|vmdk), `preallocation`, `bwlimit`, `prune-backups`

### Node-level Storage

```python
prox.nodes("node").storage.get()            # List storage on node
prox.nodes("node").storage("local-lvm").status.get()   # Total/used/avail
prox.nodes("node").storage("local").content.get()       # List volumes
prox.nodes("node").storage("local").content.get(content="backup")  # Filter by type
prox.nodes("node").storage("local").content("local:iso/ubuntu.iso").get()  # Volume info
prox.nodes("node").storage("local").content.post(...)   # Allocate volume
prox.nodes("node").storage("local").content("vol").delete()  # Delete volume
```

### Upload & Download

```python
# Upload (multipart — requires Privilege Separation OFF on token)
prox.nodes("node").storage("local").upload.post(content="iso", filename=fileobj)

# Download from URL
prox.nodes("node").storage("local").download_url.post(
    url="https://releases.ubuntu.com/24.04/ubuntu-24.04-server-amd64.iso",
    content="iso", filename="ubuntu-24.04.iso"
)

# Prune backups
prox.nodes("node").storage("local").prunebackups.post(
    prune_backups="keep-last=7,keep-weekly=4,keep-monthly=3"
)
```

### File Restore

```python
prox.nodes("node").storage("local").content("local:backup/vzdump-qemu-100.vma.zst").file_restore.post(...)
prox.nodes("node").storage("local").content("local:backup/vzdump-qemu-100.vma.zst").file_restore("list").get()
```

---

## 6. Backup (VZDump)

### Backup Jobs (scheduled)

```python
prox.cluster.backup.get()                   # List all backup jobs
prox.cluster.backup.post(                   # Create scheduled job
    vmid="100,101,102",                     # or "all"
    schedule="02:30",                       # systemd calendar format
    storage="nfs-backup",
    mode="snapshot",                        # snapshot|suspend|stop
    compress="zstd",
    enabled=1,
    prune_backups="keep-last=7,keep-weekly=4,keep-monthly=3",
    mailto="admin@example.com",
    comment="Nightly backup"
)
prox.cluster.backup("job-id").put(enabled=0)   # Disable
prox.cluster.backup("job-id").delete()         # Remove

# Check unbacked guests
prox.cluster("backup-info").get()
```

**Retention params:** `keep-all`, `keep-last`, `keep-hourly`, `keep-daily`, `keep-weekly`, `keep-monthly`, `keep-yearly`

### One-time Backup

```python
upid = prox.nodes("node").vzdump.post(
    vmid="100", storage="local",
    mode="snapshot", compress="zstd",
    bwlimit=50000,                          # KiB/s limit
    prune_backups="keep-last=3",
    fleecing="enabled=1,storage=local-lvm",  # PVE 8.1+
    performance="pbs-change-detection-mode=data"
)
result = wait_for_task(prox, "node", upid, timeout=1800)
```

### Restore

```python
# Restore VM from backup
upid = prox.nodes("node").qemu.post(
    vmid=200, archive="local:backup/vzdump-qemu-100.vma.zst",
    storage="local-lvm", force=1, unique=1
)

# Restore CT from backup
upid = prox.nodes("node").lxc.post(
    vmid=201, ostemplate="local:backup/vzdump-lxc-101.tar.zst",
    storage="local-lvm", restore=1, force=1
)
```

---

## 7. Firewall

### Cluster-level

```python
prox.cluster.firewall.options.get()
prox.cluster.firewall.options.put(enable=1, policy_in="DROP", policy_out="ACCEPT")
prox.cluster.firewall.rules.get()
prox.cluster.firewall.rules.post(type="in", action="ACCEPT", source="10.0.0.0/8", dport="8006", proto="tcp")
prox.cluster.firewall.aliases.get()
prox.cluster.firewall.ipset.get()
prox.cluster.firewall.log.get(limit=100)
```

### Node-level

```python
prox.nodes("node").firewall.options.get()
prox.nodes("node").firewall.rules.get()
prox.nodes("node").firewall.log.get()
```

### VM/CT-level

```python
prox.nodes("node").qemu(vmid).firewall.options.get()
prox.nodes("node").qemu(vmid).firewall.options.put(enable=1, policy_in="DROP")
prox.nodes("node").qemu(vmid).firewall.rules.get()
prox.nodes("node").qemu(vmid).firewall.rules.post(
    type="in", action="ACCEPT", dport="22", proto="tcp", comment="SSH"
)
prox.nodes("node").qemu(vmid).firewall.aliases.get()
prox.nodes("node").qemu(vmid).firewall.ipset.get()
prox.nodes("node").lxc(vmid).firewall.options.get()   # Same for LXC
```

**Firewall options:** `enable`, `policy_in` (ACCEPT|DROP|REJECT), `policy_out`, `loglevel_in/out`, `dhcp`, `ndp`, `radv`

---

## 8. Ceph

### Init & Status

```python
prox.nodes("node").ceph.status.get()        # Cluster health, fsid, quorum
prox.nodes("node").ceph.config.get()        # Global Ceph config
prox.nodes("node").ceph.config.put(key="mon_max_pg_per_osd", value="512")
prox.nodes("node").ceph.init.post(network="10.0.0.0/24")
prox.nodes("node").ceph.install.post(version="reef")
prox.nodes("node").ceph.flags.get()
prox.nodes("node").ceph.log.get(limit=50)
```

### OSD Management

```python
prox.nodes("node").ceph.osd.get()           # List OSDs
prox.nodes("node").ceph.osd.post(dev="/dev/sdb", crush_device_class="ssd")
prox.nodes("node").ceph.osd(osdid).get()    # OSD details
prox.nodes("node").ceph.osd(osdid).delete(cleanup=1)
prox.nodes("node").ceph.osd(osdid).scrub.post(deep=1)
prox.nodes("node").ceph.osd(osdid)("in").post()   # Mark in
prox.nodes("node").ceph.osd(osdid)("out").post()  # Mark out
prox.nodes("node").ceph.osd(osdid).metadata.get()
```

### Pool Management

```python
prox.nodes("node").ceph.pool.get()
prox.nodes("node").ceph.pool.post(name="rbd-ssd", size=3, min_size=2, pg_num=128, crush_rule="ssd-rule")
prox.nodes("node").ceph.pool("rbd-ssd").get()
prox.nodes("node").ceph.pool("rbd-ssd").put(size=2, pg_num=256)
prox.nodes("node").ceph.pool("rbd-ssd").delete()
```

### CephFS, MON, MGR, MDS

```python
prox.nodes("node").ceph.fs.get()
prox.nodes("node").ceph.fs.post(name="cephfs", pg_num=32, add_storpool=1)
prox.nodes("node").ceph.fs("cephfs").delete()

prox.nodes("node").ceph.mon.get()
prox.nodes("node").ceph.mon.post()
prox.nodes("node").ceph.mon(monid).delete()

prox.nodes("node").ceph.mgr.get()
prox.nodes("node").ceph.mgr.post()
prox.nodes("node").ceph.mgr(mgrid).delete()

prox.nodes("node").ceph.mds.get()
prox.nodes("node").ceph.mds.post(name="mds-1", hotstandby=1)
prox.nodes("node").ceph.mds("mds-1").delete()
```

### CRUSH

```python
prox.nodes("node").ceph.crush.get()         # CRUSH map
prox.nodes("node").ceph.rules.get()         # CRUSH rules
```

---

## 9. High Availability (HA)

```python
# HA Resources
prox.cluster.ha.resources.get()
prox.cluster.ha.resources.post(
    sid="vm:100",                           # or "ct:101"
    state="started",                        # started|stopped|disabled|ignored
    group="my-group",
    max_relocate=1, max_restart=1, comment="Critical VM"
)
prox.cluster.ha.resources("vm:100").get()
prox.cluster.ha.resources("vm:100").put(state="stopped")
prox.cluster.ha.resources("vm:100").delete()

# Online migrate
prox.cluster.ha.resources("vm:100").migrate.post(node="pve-02")

# Hard relocate (stop then start)
prox.cluster.ha.resources("vm:100").relocate.post(node="pve-03")

# HA Rules (PVE 9+ — replaces groups)
prox.cluster.ha.rules.get()
prox.cluster.ha.rules.post(
    name="web-tier", type="node-affinity",
    groups="vm:100,vm:101", comment="Web servers on SSD nodes"
)
prox.cluster.ha.rules("web-tier").put(groups="vm:100,vm:101,vm:102")
prox.cluster.ha.rules("web-tier").delete()

# HA Groups (deprecated in PVE 9, use rules)
prox.cluster.ha.groups.get()
prox.cluster.ha.groups.post(group="ssd-nodes", nodes="pve-01:1,pve-02:2", restricted=1, nofailback=0)

# HA Status
prox.cluster.ha.status.get()
prox.cluster.ha.manager_status.get()
```

---

## 10. SDN (Software Defined Network)

```python
prox.cluster.sdn.get()                     # SDN index
prox.cluster.sdn.applied.get()             # Currently applied config
prox.cluster.sdn.status.get()              # Status

# VNets
prox.cluster.sdn.vnets.get()
prox.cluster.sdn.vnets.post(vnet="myvnet", zone="zone1", alias="My Network")
prox.cluster.sdn.vnets("myvnet").put(alias="Updated")
prox.cluster.sdn.vnets("myvnet").delete()

# Subnets in VNet
prox.cluster.sdn.vnets("myvnet").subnets.get()
prox.cluster.sdn.vnets("myvnet").subnets.post(subnet="10.10.0.0/24", gateway="10.10.0.1", snat=1)
prox.cluster.sdn.vnets("myvnet").subnets("10.10.0.0/24").delete()

# Zones (simple, vlan, qinq, vxlan, evpn, faucet)
prox.cluster.sdn.zones.get()
prox.cluster.sdn.zones.post(zone="z-vxlan", type="vxlan", peers="10.0.0.1,10.0.0.2", mtu=1450)
prox.cluster.sdn.zones.post(zone="z-evpn", type="evpn", controller="ctrl1", vrf_vxlan=10000)
prox.cluster.sdn.zones("z-vxlan").delete()

# Controllers (evpn, bgp, isis, faucet)
prox.cluster.sdn.controllers.get()
prox.cluster.sdn.controllers.post(controller="ctrl1", type="evpn", asn=65000, peers="10.0.0.1")
prox.cluster.sdn.controllers("ctrl1").delete()

# IPAM (pve, netbox, phpipam)
prox.cluster.sdn.ipam.get()
prox.cluster.sdn.ipam.post(ipamid="netbox", type="netbox", url="http://netbox:8000", token="xxx")
prox.cluster.sdn.ipam("netbox").status.get()

# DNS (powerdns)
prox.cluster.sdn.dns.get()
prox.cluster.sdn.dns.post(dnsid="pdns", type="powerdns", url="http://pdns:8081", key="xxx")

# Apply & Rollback
prox.cluster.sdn.pending.get()              # View pending changes
prox.cluster.sdn.apply.post()               # Apply (acquires global SDN lock)
prox.cluster.sdn.rollback.post()            # Rollback pending
```

---

## 11. Replication (ZFS)

```python
# Cluster-level
prox.cluster.replication.get()
prox.cluster.replication.post(
    id="100-0", source="pve-01", target="pve-02",
    schedule="*/15", rate=50                  # MB/s limit
)
prox.cluster.replication("100-0").put(schedule="*/30")
prox.cluster.replication("100-0").delete()

# Node-level
prox.nodes("node").replication.get()        # Jobs on this node
prox.nodes("node").replication("100-0").status.get()
prox.nodes("node").replication("100-0").log.get()
prox.nodes("node").replication("100-0").schedule_now.post()  # Immediate sync
```

---

## 12. ACME / Certificates

### ACME Accounts

```python
prox.cluster.acme.tos.get()                 # Terms of Service
prox.cluster.acme.directory.get()           # ACME directory URL
prox.cluster.acme.challenge_schemas.get()   # Available challenge types

prox.cluster.acme.account.get()
prox.cluster.acme.account.post(name="letsencrypt", contact="admin@example.com")
prox.cluster.acme.account("letsencrypt").delete()
```

### ACME Plugins (150+ DNS providers)

```python
prox.cluster.acme.plugins.get()
prox.cluster.acme.plugins.post(
    plugin="cloudflare", type="dns",
    data="CF_API_EMAIL=admin@example.com\nCF_API_KEY=xxx",
    validation_delay=30
)
prox.cluster.acme.plugins("cloudflare").put(data="CF_API_TOKEN=newtoken")
prox.cluster.acme.plugins("cloudflare").delete()
```

### Node Certificates

```python
prox.nodes("node").certificates.info.get()  # List certs
prox.nodes("node").certificates.custom.post(
    certificates="-----BEGIN CERTIFICATE-----\n...",
    key="-----BEGIN PRIVATE KEY-----\n...",
    force=1, restart=1
)

# Order ACME cert
prox.nodes("node").certificates.acme.post(force=1)
prox.nodes("node").certificates.acme_challenge.post(type="dns", plugin="cloudflare")
```

---

## 13. Mapping (PCI / USB / Directory)

```python
# PCI (GPU passthrough etc.)
prox.cluster.mapping.pci.get()
prox.cluster.mapping.pci.post(
    id="gpu-rtx4090",
    map=["node=pve-01,pciid=0000:01:00.0,iommu_group=1", "node=pve-02,pciid=0000:01:00.0,iommu_group=1"],
    mdev="nvidia-460", description="RTX 4090"
)
prox.cluster.mapping.pci("gpu-rtx4090").delete()
prox.cluster.mapping.pci.get(check_node="pve-01")  # Validate on node

# USB
prox.cluster.mapping.usb.get()
prox.cluster.mapping.usb.post(
    id="yubikey",
    map=["node=pve-01,path=/dev/bus/usb/001/002", "node=pve-02,usbid=1050:0407"],
    description="YubiKey 5"
)

# Directory
prox.cluster.mapping.directory.get()
prox.cluster.mapping.directory.post(
    id="shared-data", map=["node=pve-01,path=/mnt/shared", "node=pve-02,path=/mnt/shared"]
)
```

---

## 14. Metrics / Monitoring

### Export

```python
prox.cluster.metrics("export").get(start_time=1700000000, end_time=1700086400)
```

### Metric Servers

```python
prox.cluster.metrics.server.get()

# Graphite
prox.cluster.metrics.server.graphite.post(id="graphite1", server="10.0.0.50", port=2003, proto="udp")

# InfluxDB
prox.cluster.metrics.server.influxdb.post(
    id="influx1", server="10.0.0.51", port=8086,
    proto="http", bucket="pve", organization="home", token="xxx", version=2
)

# OpenTelemetry
prox.cluster.metrics.server.opentelemetry.post(
    id="otel1", server="10.0.0.52", port=4318, proto="http", gzip=1
)

# Update / Delete
prox.cluster.metrics.server.graphite("graphite1").put(port=2004)
prox.cluster.metrics.server.influxdb("influx1").delete()
```

---

## 15. APT / Package Management

```python
prox.nodes("node").apt.update.get()         # List available updates
prox.nodes("node").apt.update.post()        # Run apt-get update
prox.nodes("node").apt.upgrade.post()       # Run apt-get upgrade
prox.nodes("node").apt.changelog.get(name="proxmox-ve", version="8.2-1")
prox.nodes("node").apt.repositories.get()   # List repos
prox.nodes("node").apt.versions.get()       # Installed versions
```

---

## 16. User / Access Management

### Users & Groups

```python
prox.access.users.get()
prox.access.users.post(userid="admin@pve", password="secret", email="admin@local",
                        groups=["admins"], enable=1, expire=0)
prox.access.users("admin@pve").put(groups=["admins","operators"])
prox.access.users("admin@pve").delete()

prox.access.groups.get()
prox.access.groups.post(groupid="devops", comment="DevOps team")
prox.access.groups("devops").delete()
```

### Roles & ACL

```python
prox.access.roles.get()
prox.access.roles.post(roleid="custom-admin", privileges=["Sys.Modify","VM.Allocate","Datastore.Allocate"])

prox.access.acl.get()
prox.access.acl.put(path="/vms/100", roles="custom-admin", users=["admin@pve"], propagate=1)
prox.access.acl.put(path="/vms/100", roles="custom-admin", users=["admin@pve"], delete=1)  # Remove
```

### Authentication Domains

```python
prox.access.domains.get()
# Types: pam, pve, ad, ldap, openid
prox.access.domains.post(realm="corp-ad", type="ad", server1="ad.corp.local", ssl=1)
prox.access.domains.post(realm="github", type="openid",
    issuer_url="https://github.com", client_id="xxx", client_key="xxx")
prox.access.domains("corp-ad").delete()
```

### TFA (Two-Factor Auth)

```python
prox.access.tfa.get()
prox.access.tfa("admin@pve").get()
prox.access.tfa("admin@pve").post(type="totp", secret="JBSWY3DPEHPK3PXP", digits=6, step=30)
prox.access.tfa("admin@pve").post(type="recovery")  # Generate recovery codes
prox.access.tfa("admin@pve")(tfa_id).delete()
```

### Password & Permissions

```python
prox.access.password.put(userid="admin@pve", password="newpass", confirmation="newpass")
prox.access.permissions.get()               # Current user's permissions
prox.access.permissions.get(userid="admin@pve")  # Specific user (needs Sys.Access)
```

---

## 17. Tasks

```python
prox.cluster.tasks.get()                               # Recent cluster tasks
prox.nodes("node").tasks.get()                         # Tasks on node
prox.nodes("node").tasks(upid).status.get()            # Task status
prox.nodes("node").tasks(upid).log.get()               # Task log
result = wait_for_task(prox, "node", upid, timeout=600)
```

---

## API Conventions

### Method Mappings
`get()` → GET | `post()`/`create()` → POST | `put()`/`set()` → PUT | `delete()` → DELETE

### Path Notation
```python
# Dotted (pythonic) — preferred
prox.nodes("pve1").qemu(100).status.current.get()

# String path — for hyphens in endpoint names
prox("nodes/pve1/qemu/100/agent/exec-status").get(pid=1234)
```

### Task-based Operations
VM create, clone, snapshot, backup, migrate, Ceph OSD create, etc. return UPID strings.
Always poll with `wait_for_task()` or check `.tasks(upid).status.get()`.

---

## Pitfalls

1. **Self-signed certs**: Use `verify_ssl=False` until proper certs configured
2. **Task-based operations**: VM create, clone, snapshot, backup, migrate return UPID — must poll
3. **Cluster-wide vs node-scoped**: `/cluster/resources` shows all VMs; `/nodes/{node}/qemu` shows only that node's
4. **API token permissions**: Token inherits user's permissions unless separated. Verify with `pveum token permissions` on PVE host
5. **LXC rootfs format**: `rootfs="local-lvm:10"` means 10GB on that storage
6. **Network config difference**: VMs use `net0="virtio,bridge=vmbr0"`; LXC uses `net0="name=eth0,bridge=vmbr0,ip=dhcp"`
7. **cluster.status.get()** returns a **list** — iterate checking `type` field
8. **Upload endpoint** requires multipart/form-data; token must have Privilege Separation OFF
9. **NUMA required for memory hotplug**: Set `numa=1` before enabling memory hotplug
10. **SDN changes require apply**: After creating zones/vnets/controllers, call `sdn.apply.post()`
11. **HA Groups deprecated in PVE 9**: Use `ha.rules` instead of `ha.groups`
12. **/nodes/{node}/execute** is batch API calls only — NOT shell execution
13. **Restore uses create endpoints**: POST to `/qemu` or `/lxc` with `archive`/`ostemplate` param
14. **Backup retention**: Use `prune-backups` string, NOT deprecated `maxfiles`

## Full Endpoint Catalog

See `references/api-endpoints.md` for a searchable catalog of all endpoints with paths, methods, and key params.