# Steering Wheel Track Button Swap (HMG-API mod)

Swaps the steering wheel's track up and track down buttons, so each one does what the other did.
This applies to every audio source, including CarPlay and the radio.

**[Download the latest release](https://github.com/dibble9012/steering-wheel-track-button-swap/releases/latest)**

Tested on a 2023 Kia EV6 GT-Line (USA), firmware 260507, with HMG-API 1.0.0. The mod only installs
on that model, region and firmware.

## Install

You need HMG-API 1.0.0 or later on the car first. Both methods use a USB flash drive. Download
the file for your method from the
[latest release](https://github.com/dibble9012/steering-wheel-track-button-swap/releases/latest),
listed under **Assets**.

ADB over USB has to be off, or the port can't read the drive.

### With the HMG-API app

1. Download `steering-wheel-track-button-swap-v1.0.0-hmgapi-usb.zip`.
2. Unzip it onto the top level of a FAT32 flash drive, so the drive has
   `HMGAPI/updates/steering-wheel-track-button-swap-v1.0.0.zip`.
3. Plug the drive into the car and install the mod from the updates page in the HMG-API app.
4. Tap **Apply changes** in the app.
5. Restart the head unit.

To remove the mod, use the HMG-API app, then restart the head unit.

### With NEMESIS

1. Download `steering-wheel-track-button-swap-v1.0.0-nemesis-usb.zip`.
2. Unzip it onto the top level of a FAT32 or exFAT flash drive, so the drive has `NEMESIS.data`
   and the `packages` folder at its top level. Keep only one NEMESIS package on the drive.
3. Once Android is up, plug the drive into the car and confirm the install of
   "Steering Wheel Track Button Swap".
4. Take the drive out and restart the head unit.

HMG-API installs and applies the mod for you. To remove it, uninstall the package in NEMESIS
Manager, then restart the head unit.

If you have an older track swap NEMESIS package (`hkmc.track-button-swap` or
`local.hkmc.swrc-swap`), uninstall it first. They change the same lines, so NEMESIS won't install
them together.

## How it works

The wheel's two buttons reach Android as scan codes 34 and 35. The mod swaps what they mean in the
EV6's key layout file, `/system/usr/keylayout/daudio_wp_daudioplus_cvev_base.kl`:

| Scan code | Stock | With the mod |
|---|---|---|
| 34 | `CHANNEL_UP` | `CHANNEL_DOWN` |
| 35 | `CHANNEL_DOWN` | `CHANNEL_UP` |

Android applies the layout before any app sees the key, so short presses and holds work as before,
with no delay. There's no service, hook or polling, and no settings. Other buttons, including the
seek buttons on the head unit and the rear-seat remote's keys, are unchanged.

HMG-API makes the edit and puts the stock file back when the mod is turned off or removed. Android
reads the layout at startup, so changes take effect after a restart.

## Build

You need a checkout of [HMG-API](https://github.com/VysseCodes/HMG-API), whose
`tools/mknemesismod.sh` makes the NEMESIS package.

```bash
./build.py ~/.hmgapi/author.key ../HMG-API
```

This writes the two release files to `dist/`, along with
`steering-wheel-track-button-swap-v1.0.0.hmgapi.zip`, the signed mod inside them, and
`steering-wheel-track-button-swap-v1.0.0-nemesis-package.zip`, the file to upload to the NEMESIS
Package Store. Updates must be signed with the same key as the first install.

## Test

```bash
test/check.py
```

This applies the patch to a copy of the stock layout from firmware 260507 and checks that only
those two scan codes changed.

## License

AGPL-3.0. See [LICENSE](LICENSE).
