{ pkgs ? import <nixpkgs> {} }:

let
  python = pkgs.python313;

  chess-bot = python.pkgs.buildPythonApplication {
    pname = "chess-bot";
    version = "0.1.0";
    src = ./.;
    pyproject = true;

    propagatedBuildInputs = with python.pkgs; [
      discordpy
      python-chess
      python-dotenv 
    ];

    nativeBuildInputs = with pkgs; [
      uv
      mypy
    ];

    buildInputs = with pkgs; [
      stdenv.cc.cc.lib
      zlib
      stockfish
    ];
 
    postFixup = ''
      wrapProgram $out/bin/chess-bot \
        --prefix LD_LIBRARY_PATH : "${pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc.lib pkgs.zlib ]}"
    '';

    preBuild = ''
      ${pkgs.uv}/bin/uv sync
    '';

    meta = with pkgs.lib; {
      description = "A chess bot using discord.py and python-chess";
      license = licenses.mit;
      maintainers = [ maintainers.Joulex ];
    };
  };

in
chess-bot