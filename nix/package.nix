{
  lib,
  stdenv,
  hugo,
}:

stdenv.mkDerivation {
  name = "kartoza-website";

  src = lib.cleanSourceWith {
    src = ../.;
    filter = (
      path: type:
      (builtins.all (x: x != baseNameOf path) [
        ".git"
        ".github"
        "flake.nix"
        "flake.lock"
        "package.nix"
        "result"
      ])
    );
  };

  buildInputs = [ hugo ];

  buildPhase = ''
    hugo --config config.toml --enableGitInfo=false
  '';

  installPhase = ''
    mkdir -p $out
    cp -r public $out/
  '';

  meta = with lib; {
    description = "Kartoza website";
    license = licenses.mit;
  };
}
