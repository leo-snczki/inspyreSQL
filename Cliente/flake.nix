# https://www.youtube.com/watch?v=6fftiTJ2vuQ
{
  description = "python project";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      packageOverrides = pkgs.callPackage ./python-packages.nix { };
      python = pkgs.python3.override { inherit packageOverrides; };
    in
    {
      devShells.x86_64-linux.default = pkgs.mkShell {
        packages = [
          (python.withPackages (p: [ p.readkeys p.sockets p.mysql-connector-python ]))
        ];
      };
    };
}
