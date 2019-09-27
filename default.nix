with import <nixpkgs> {};
stdenv.mkDerivation rec {
    name = "oil";

    buildInputs = [
        (python3.withPackages ( p:
            with p; [ pip ]
        ))
        postgresql
    ];

    env = buildEnv {
        inherit name;
        paths = buildInputs;
    };

    shellHook = ''
        # fix terminal behavior when running shell with --pure
        export TERM=xterm-256color
        # set up python stuff
        alias pip="PIP_PREFIX='$(pwd)/_build/pip_packages' \pip"
        export PYTHONPATH="$(pwd)/_build/pip_packages/lib/python3.7/site-packages:$(pwd)/_build/pip_packages/bin:$PYTHONPATH"
        unset SOURCE_DATE_EPOCH
        # postgresql
        export PGDATA='pgdata'
        initdb
        pg_ctl start
        createdb oil
    '';
}