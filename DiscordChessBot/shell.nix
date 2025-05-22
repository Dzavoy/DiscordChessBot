{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {

  packages = [
    pkgs.git
    pkgs.python313
    pkgs.uv
    pkgs.stdenv.cc.cc
    pkgs.mypy
  ];

  env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
    pkgs.stdenv.cc.cc.lib
    pkgs.zlib
  ];

  shellHook = ''
    echo "🐍 Python environment activated."
  '';
}