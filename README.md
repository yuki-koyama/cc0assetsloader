# CC0 Assets Loader

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

```
git clone https://github.com/yuki-koyama/cc0-assets-loader.git --recursive
zip -r cc0-assets-loader.zip cc0-assets-loader -x *.git*
rm -fr cc0-assets-loader
```

## Dependencies

- [nodelayout](https://github.com/yuki-koyama/nodelayout) (included as a git submodule)

## License

All the Python codes (`*.py`) are distributed under GPLv3. The third-party asset files (`assets/*`) are distributed under CC0.

## TODOs

- Support HDR images
- Provide material previews
- Allow users to add PBR textures and HDR images
- Create documentation
