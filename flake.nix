{
  description = "Kartoza Website";

  # nixConfig = {
  #   extra-substituters = [ "https://example.cachix.org" ];
  #   extra-trusted-public-keys = [ "example.cachix.org-1:xxxx=" ];
  # };

  inputs = {
    nixpkgs-version.url = "github:QGIS/qgis-nixpkgs-version";
    nixpkgs.follows = "nixpkgs-version/nixpkgs-25-05";
    nixpkgs-unstable.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs =
    { self, nixpkgs, nixpkgs-unstable, ... }:

    let
      # Flake system
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;

      nixpkgsFor = forAllSystems (
        system:
        import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        }
      );

      # nixpkgs-unstable for packages with security fixes
      nixpkgsUnstableFor = forAllSystems (
        system:
        import nixpkgs-unstable {
          inherit system;
          config.allowUnfree = true;
        }
      );

    in
    {
      #
      ### PACKAGES
      #

      packages = forAllSystems (
        system:
        let
          pkgs = nixpkgsFor.${system};
        in
        rec {
          website = pkgs.callPackage ./nix/package.nix { };
          default = website;
        }
      );

      #
      ### APPS
      #

      apps = forAllSystems (
        system:
        let
          pkgs = nixpkgsFor.${system};
          pkgsUnstable = nixpkgsUnstableFor.${system};
          inherit (nixpkgs) lib;

          # Python environment for scripts
          pythonEnv = pkgsUnstable.python3.withPackages (ps: with ps; [
            requests pyyaml beautifulsoup4 python-dateutil tabulate
          ]);

          wwwLauncher = pkgs.writeShellApplication {
            name = "website";
            runtimeInputs = [ pkgs.python3 ];
            text = ''
              exec ${lib.getExe pkgs.python3} \
                -m http.server 8000 \
                -d ${self.packages.${system}.website}/public_www/
            '';
          };

          syncBlogs = pkgs.writeShellApplication {
            name = "sync-blogs";
            runtimeInputs = [ pythonEnv ];
            text = ''
              exec ${pythonEnv}/bin/python3 \
                ${self}/scripts/fetch-erpnext-blogs.py "$@"
            '';
          };

          syncBlogsDryRun = pkgs.writeShellApplication {
            name = "sync-blogs-dry-run";
            runtimeInputs = [ pythonEnv ];
            text = ''
              exec ${pythonEnv}/bin/python3 \
                ${self}/scripts/fetch-erpnext-blogs.py --dry-run "$@"
            '';
          };

          listBlogs = pkgs.writeShellApplication {
            name = "list-blogs";
            runtimeInputs = [ pythonEnv ];
            text = ''
              exec ${pythonEnv}/bin/python3 \
                ${self}/scripts/fetch-erpnext-blogs.py --list "$@"
            '';
          };
        in
        rec {
          website = {
            type = "app";
            program = "${wwwLauncher}/bin/website";
          };
          sync-blogs = {
            type = "app";
            program = "${syncBlogs}/bin/sync-blogs";
          };
          sync-blogs-dry-run = {
            type = "app";
            program = "${syncBlogsDryRun}/bin/sync-blogs-dry-run";
          };
          list-blogs = {
            type = "app";
            program = "${listBlogs}/bin/list-blogs";
          };
          default = website;
        }
      );

      #
      ### SHELLS
      #

      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgsFor.${system};
          pkgsUnstable = nixpkgsUnstableFor.${system};
          # Use unstable Python packages for security fixes (Pillow CVE-2026-25990)
          pythonEnv = pkgsUnstable.python3.withPackages (ps: with ps; [
            icalendar # Calendar handling
            requests # HTTP requests - for ERPNext API
            pyyaml # YAML generation
            pillow # Image processing (12.1.0 - patched for CVE-2026-25990)
            stripe # Donor management
            beautifulsoup4 # HTML parsing - for content comparison
            html2text # HTML to markdown conversion
            python-dateutil # Date parsing
            tabulate # Nice table output
            pytest # Testing framework
          ]);
        in
        {
          # Development environment
          default = pkgs.mkShell {
            packages = [
              pkgs.hugo # Hugo for building the website
              pkgs.vscode # VSCode for development
              pythonEnv # Python with all packages from unstable
              pkgs.gnumake # GNU Make for build automation
              # Linting and formatting tools
              pkgs.nodePackages.markdownlint-cli # Markdown linting
              pkgs.nodePackages.prettier # Code formatting
              pkgs.nodePackages.cspell # Spell checking
              # Testing tools
              pkgs.nodejs_22 # Node.js for Playwright
              pkgs.playwright-driver.browsers # Playwright browsers
            ];
            shellHook = ''
              export DIRENV_LOG_FORMAT=
              export PLAYWRIGHT_BROWSERS_PATH=${pkgs.playwright-driver.browsers}
              export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true
              echo "-----------------------"
              echo "🌈 Your Hugo Dev Environment is ready."
              echo "It provides hugo and vscode for use with the Kartoza Website Project"
              echo ""
              echo "🪛 VSCode:"
              echo "--------------------------------"
              echo "Start vscode like this:"
              echo ""
              echo "./vscode.sh"
              echo ""
              echo "🪛 Hugo:"
              echo "--------------------------------"
              echo "Start Hugo like this:"
              echo ""
              echo "hugo server"
              echo ""
              echo "🎭 Playwright:"
              echo "--------------------------------"
              echo "Run e2e tests like this:"
              echo ""
              echo "cd playwright/ci-test && npm test"
              echo "-----------------------"
            '';
          };
        }
      );
    };
}
