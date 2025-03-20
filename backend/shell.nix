let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.flask
      python-pkgs.joblib
      python-pkgs.numpy
      python-pkgs.xgboost
      python-pkgs.opencv-python
      python-pkgs.flask-cors
      python-pkgs.scikit-learn
      python-pkgs.pip
    ]))
  ];
}
