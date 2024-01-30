let
    nixpkgs = builtins.fetchTarball {
        name = "nixos-unstable-2023-11-24";
        url = "https://github.com/nixos/nixpkgs/archive/8b8c9407844599546393146bfac901290e0ab96b.tar.gz";
        # Hash obtained using `nix-prefetch-url --unpack <url>`
        sha256 = "15jq6701vzbmqchbj2cav022f63kqlcffk82g7nhv4ldp8iidzdw";
    };
in { pkgs ? import nixpkgs {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    gcc
    glibc
    git
    gnumake
    krb5.out
    krb5.dev
    poetry
    python312
    bison
  ];
}
