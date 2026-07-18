---
name: coreboot-firmware
description: >-
  Coreboot firmware development including board bring-up, QEMU testing, and flash programming.
  Use when developing coreboot ports or debugging firmware boot issues.
license: MIT
metadata:
  version: 1.0.0
  author: Original skill
allowed-tools: Read Write Edit Bash(make *) Bash(docker *) Bash(qemu-system-*) Bash(flashrom *)
---

# Coreboot Firmware Development

Build and test coreboot firmware. Port to new boards, debug boot failures, and flash to hardware. It's lower-level than most firmware work, but the tooling helps.

## Quick Start

**Essential steps:**
1. **Build crossgcc** — Compiler toolchain for target architecture
2. **Configure with Kconfig** — Select board and options
3. **Build ROM** — Compile to coreboot.rom
4. **Test in QEMU, then flash** — Always verify in VM before hardware

Always test in QEMU first. Hardware flashing can brick boards, and you don't want that.

## When to Use This Skill

- Bringing up a new coreboot board port from scratch
- Debugging firmware boot failures (romstage, ramstage, payload handoff)
- Building and testing coreboot ROMs in QEMU before flashing hardware
- Working with flashrom to program SPI flash chips

## Project Structure

```
coreboot/
├── src/
│   ├── mainboard/     # Board-specific code
│   │   ├── emulation/qemu-i440fx/
│   │   ├── google/    # Chromebook boards
│   │   └── pcengines/ # APU boards
│   ├── soc/           # System-on-chip support
│   ├── cpu/           # CPU init code
│   ├── northbridge/   # Memory controller
│   ├── southbridge/   # I/O controller
│   └── device/        # Device init
├── util/              # Build utilities
│   ├── crossgcc/      # Toolchain build scripts
│   ├── kconfig/       # Configuration tool
│   └── flashrom/      # Flash programming tool
└── 3rdparty/          # Third-party blobs
    └── blobs/         # Vendor binary blobs
```

## Build Toolchain

Before building coreboot, build crossgcc:

```bash
cd coreboot
make crossgcc-i386 CPUS=4
```

For 64-bit:
```bash
make crossgcc-x64 CPUS=4
```

For ARM:
```bash
make crossgcc-arm CPUS=4
```

This takes 30-60 minutes. It won't be faster even on beefy machines. Toolchain goes in `util/crossgcc/xgcc/`.

## Configuration (Kconfig)

```bash
make menuconfig
```

**Key settings:**

### Mainboard

```
Mainboard
  → Mainboard vendor (QEMU)
  → Mainboard model (QEMU x86 i440fx/piix4)
  → ROM chip size (4096 KB)
```

### Payload

```
Payload
  → Add a payload (SeaBIOS)
  → SeaBIOS version (master)
```

Payload options:
- **SeaBIOS** — Legacy BIOS, boots Linux/Windows
- **GRUB2** — Bootloader with menus
- **Tianocore** — UEFI implementation
- **Linux** — Linux kernel as payload
- **None** — For testing or custom payloads

### Debugging

```
Console
  → Send console output to: Serial port
  → Serial port base address (0x3f8)

Debugging
  → Check PIRQ table consistency
  → Check ACPI table consistency
  → Output verbose malloc debug messages
```

Save config to `.config`.

## Build ROM

```bash
make
```

Output: `build/coreboot.rom`

**Parallel build:**
```bash
make -j$(nproc)
```

**Clean rebuild:**
```bash
make clean
make
```

## Boot Stages

Coreboot boots in stages. Here's how they work:

### 1. Bootblock

Earliest code. Runs from reset vector. Sets up:
- Cache as RAM (CAR)
- Serial console
- Minimal init

**Source:** `src/mainboard/*/bootblock.c`

### 2. Romstage

Runs from ROM, using CAR. Initializes:
- DRAM controller
- Memory training
- Early devices (Super I/O)

**Source:** `src/mainboard/*/romstage.c`

### 3. Ramstage

Runs from RAM. Full C environment:
- PCI enumeration
- Device initialization
- ACPI table generation
- Payload loading

**Source:** `src/mainboard/*/devicetree.cb`, `mainboard.c`

### 4. Payload

OS bootloader (SeaBIOS, GRUB, Linux, etc.)

## QEMU Testing

Test ROM in QEMU before flashing hardware. You can't risk bricking a board without testing first.

```bash
qemu-system-x86_64 -bios build/coreboot.rom \
  -serial stdio \
  -m 1024
```

**With disk image:**
```bash
qemu-system-x86_64 -bios build/coreboot.rom \
  -serial stdio \
  -m 1024 \
  -drive file=disk.img,format=raw
```

**QEMU monitor:**
```bash
qemu-system-x86_64 -bios build/coreboot.rom \
  -serial stdio \
  -monitor telnet::45454,server,nowait \
  -m 1024
```

Then connect: `telnet localhost 45454`

**Expected output:**
```
coreboot-4.18 Sun Jan 15 2023 12:00:00 UTC bootblock starting (log level: 7)...
Enumerating buses...
CPU_CLUSTER: 0 enabled
...
Payload SeaBIOS (version rel-1.16.1)
```

## Serial Console Debugging

Connect to serial port:

```bash
# Linux
screen /dev/ttyUSB0 115200

# Or minicom
minicom -D /dev/ttyUSB0 -b 115200
```

**Add debug output:**
```c
#include <console/console.h>

printk(BIOS_DEBUG, "Value: %d\n", value);
printk(BIOS_ERR, "Error: %s\n", error_msg);
```

**Log levels:**
- `BIOS_EMERG` — System unusable
- `BIOS_ALERT` — Action required
- `BIOS_CRIT` — Critical condition
- `BIOS_ERR` — Error
- `BIOS_WARNING` — Warning
- `BIOS_NOTICE` — Normal but significant
- `BIOS_INFO` — Informational
- `BIOS_DEBUG` — Debug messages
- `BIOS_SPEW` — Verbose debug

Set log level in Kconfig:
```
Console
  → Default console log level (8: SPEW)
```

## Flash Programming

### Read Current BIOS

```bash
sudo flashrom -p internal -r backup.rom
```

**Always back up first!**

### Write New BIOS

```bash
sudo flashrom -p internal -w build/coreboot.rom
```

**Verify after write:**
```bash
sudo flashrom -p internal -v build/coreboot.rom
```

### External Programmer

For bricked boards, you'll need an external programmer:

```bash
# CH341A programmer
sudo flashrom -p ch341a_spi -w coreboot.rom

# Raspberry Pi
sudo flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=8000 -w coreboot.rom
```

### Flash Layout

Most systems have flash descriptor and ME region:

```bash
# Read descriptor
sudo flashrom -p internal --ifd -i fd -r fd.bin

# Write only BIOS region (safe)
sudo flashrom -p internal --ifd -i bios -w coreboot.rom
```

## Board Bring-Up

Porting to new board:

### 1. Copy Similar Board

```bash
cd src/mainboard
cp -r emulation/qemu-i440fx myvendor/myboard
```

### 2. Update Kconfig

```
config BOARD_MYVENDOR_MYBOARD
	bool "My Board"
	select SOC_INTEL_SKYLAKE  # Or appropriate SOC
```

### 3. Create devicetree.cb

```
chip soc/intel/skylake
	device cpu_cluster 0 on
		device lapic 0 on end
	end

	device domain 0 on
		device pci 00.0 on  end  # Host bridge
		device pci 02.0 on  end  # Graphics
		device pci 14.0 on  end  # USB controller
		device pci 1f.0 on       # LPC bridge
			chip superio/ite/it8772f
				device pnp 2e.1 on  # COM1
					io 0x60 = 0x3f8
					irq 0x70 = 4
				end
			end
		end
	end
end
```

### 4. GPIO Configuration

```c
// gpio.h
static const struct pad_config gpio_table[] = {
	PAD_CFG_NF(GPP_A0, NONE, DEEP, NF1),  // RCIN#
	PAD_CFG_NF(GPP_A1, NATIVE, DEEP, NF1), // LAD0
	PAD_CFG_GPO(GPP_B5, 1, DEEP),         // LED
};
```

### 5. Memory Configuration

```c
// romstage.c
void mainboard_memory_init_params(FSPM_UPD *mupd)
{
	FSP_M_CONFIG *mem_cfg = &mupd->FspmConfig;

	mem_cfg->DqPinsInterleaved = 0;
	mem_cfg->CaVrefConfig = 2;
	// ... SPD and timing settings
}
```

## POST Codes

Debug boot failures with POST code display:

**Add POST codes:**
```c
#include <console/post_codes.h>

post_code(0x10);  // At start of function
// ... code ...
post_code(0x11);  // After critical section
```

**Read via port 80h card:**
Hardware display shows last POST code before hang.

## Common Issues

These aren't rare -- most board ports hit at least one of them.

### Issue 1: No Serial Output

**Check:**
- Serial enabled in Kconfig
- Correct base address (0x3f8 for COM1)
- Baud rate matches (usually 115200)
- TX/RX not swapped on adapter

### Issue 2: Hang in Romstage

**Debug:**
- Add POST codes before/after memory init
- Check memory timings in devicetree
- Verify SPD data

### Issue 3: PCI Enumeration Fails

**Check:**
- devicetree.cb has correct PCI addresses
- Devices marked `on` not `off`
- No conflicting resources

## Writing Style

Firmware documentation and debug notes have a long shelf life. Apply `natural-writing-style`:

- Be precise about hardware: exact chip IDs, register addresses, timing constraints
- Don't claim a port "works" without specifying which stages boot and on which board revision
- State what was tested (serial output, QEMU, real hardware) and what wasn't
- Use contractions in documentation; firmware dev doesn't require formal prose

## Resources

- `references/coreboot-guide.md` — Complete coreboot documentation
- `references/kconfig-options.md` — All configuration options
- `references/flashrom-guide.md` — Flash programming details
- `assets/board-template/` — New board template files
