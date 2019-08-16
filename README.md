# CC0 Assets Loader

![GitHub](https://img.shields.io/github/license/yuki-koyama/cc0assetsloader)
![Blender](https://img.shields.io/badge/blender-2.80-brightgreen)

A Blender add-on for loading CC0 assets (PBR textures, HDR images, etc.)

## Goals

- Provide an easy way to define PBR textured materials
- Provide an easy way to load HDR images that can be used as background

## Policies

- Manage assets (`jpg`, `hdr`, etc.) using Git LFS
- Follow the PEP80 style and 120-column limit
- Include PBR textures obtained from <https://cc0textures.com/>

## Supported Blender Versions

- 2.80

## Creating a ZIP File for Distribution/Installation

Prerequisites: `git` and `git-lfs`

```
git clone https://github.com/yuki-koyama/cc0assetsloader.git --recursive
zip -r cc0assetsloader.zip cc0assetsloader -x *.git*
rm -fr cc0assetsloader
```

## Download

ZIP file created using the latest release (v0.1): <https://github.com/yuki-koyama/cc0assetsloader/releases/download/0-1/cc0assetsloader.zip>

## Known Issues

This repository is hosted on GitHub and uses its Git LFS functionality. The bandwidth is limited to 1.0 GB/month in its free plan, so cloning this repository probably fails due to the bandwidth limit. I am looking for easy and sustainable solutions.

## Dependencies

- [nodelayout](https://github.com/yuki-koyama/nodelayout) (included as a git submodule)

## License

All the Python codes (`*.py`) are distributed under GPLv3. The third-party asset files (`assets/*`) are distributed under CC0.

## TODOs

- Support HDR images
- Provide material previews
- Allow users to add PBR textures and HDR images
- Create documentation
